"""Recipe Controller Module."""

from flask import Blueprint, request, jsonify, render_template, abort
from jinja2 import TemplateNotFound
from models.recipe import Recipe
from models.food import Food

recipe_bp = Blueprint("recipe_bp", __name__)


@recipe_bp.route("/new_recipe", methods=["GET"])
def add_recipe_page():
    """Renders the new recipe page."""
    try:
        return render_template("new_recipe.html")
    except (FileNotFoundError, TemplateNotFound):
        abort(404)


@recipe_bp.route("/new_recipe", methods=["POST"])
def add_recipe_post():
    """Handles the submission of a new recipe."""
    user_cookie = request.cookies.get("user")
    if not user_cookie:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    recipe_name = data.get("recipe_name")
    ingredients_data = data.get("ingredients")

    if not recipe_name or not ingredients_data:
        return jsonify({"error": "Missing recipe name or ingredients"}), 400

    if Recipe.exists(user_cookie, recipe_name):
        return jsonify({"error": "Recipe with this name already exists"}), 409

    recipe = Recipe(
        recipe_name=recipe_name, author=user_cookie, ingredients=ingredients_data
    )
    try:
        recipe.save()
        saved_recipe_details = Recipe.get_recipe_details_with_emissions(
            user_cookie, recipe_name
        )

        if not saved_recipe_details:
            # This case should ideally not be hit if save() was successful
            return (
                jsonify({"error": "Recipe saved, but failed to retrieve its details"}),
                500,
            )

        return (
            jsonify(
                {
                    "message": "Recipe saved successfully!",
                    "recipe": saved_recipe_details,
                }
            ),
            200,
        )
    except (FileNotFoundError, TemplateNotFound) as e:

        print(f"Error in add_recipe_post: {e}")
        return jsonify({"error": "An error occurred while saving the recipe."}), 500


@recipe_bp.route("/check-ingredients", methods=["POST"])
def check_ingredients():
    """Checks the ingredients and returns suggestions for each ingredient."""
    data = request.json
    ingredient_list_data = data.get("ingredients", [])
    result_list = []

    for ingredient_item in ingredient_list_data:
        ingredient_name_raw = ingredient_item.get("name", "").strip()
        suggested_names = Food.search_by_name_pattern(ingredient_name_raw)
        result_list.append({"name": suggested_names})

    return jsonify(result_list)


@recipe_bp.route("/find_recipe", methods=["GET"])
def find_recipe_page():
    """Renders the find recipe page."""

    search_query = request.args.get("query", "").strip()
    selected_category_from_form = request.args.get("category", "").strip()
    sort_emission = request.args.get("sort_emission", "").strip()

    all_food_categories = Food.get_all_categories()
    found_recipes = []

    search_attempted = (
        "query" in request.args
        or "category" in request.args
        or "sort_emission" in request.args
    )

    if search_attempted:
        effective_query_term = search_query
        effective_selected_category = selected_category_from_form
        effective_sort_emission = (
            sort_emission if sort_emission in ["lowest", "highest"] else None
        )

        # if selected_category_from_form == "" and not sort_emission:
        #     effective_query_term = ""
        # elif selected_category_from_form == "" and sort_emission:
        #     pass

        found_recipes = Recipe.search_recipes(
            query_term=effective_query_term,
            selected_category=effective_selected_category,
            sort_by_emission=effective_sort_emission,
        )

    return render_template(
        "find.html",
        results=found_recipes,
        search_query=search_query,
        all_categories=all_food_categories,
        selected_category=selected_category_from_form,
        selected_sort_emission=sort_emission,
        search_attempted=search_attempted,
    )


@recipe_bp.route("/recipe/<string:author_username>/<string:recipe_name_str>")
def view_recipe(author_username, recipe_name_str):
    """Renders the recipe detail page for a specific recipe."""
    # Check if the logged-in user is the author or if recipes are public
    # For now, let's assume any user can view if they have the link.
    # You might want to add authentication/authorization checks here.
    # user_cookie = request.cookies.get("user")
    # if not user_cookie:
    #     return redirect(url_for('auth_bp.login'))
    # if user_cookie != author_username:
    #     # Handle cases where user is trying to view someone else's recipe
    #     # For now, allow, or you could restrict
    #     pass

    recipe_details = Recipe.get_recipe_details_with_emissions(
        author_username, recipe_name_str
    )

    if not recipe_details:
        abort(404)  # Recipe not found

    try:
        return render_template("recipe_detail.html", recipe=recipe_details)
    except (TemplateNotFound, FileNotFoundError) as e:
        print(f"Error rendering recipe_detail.html: {e}")  # For debugging
        abort(404)
    except (ValueError, TypeError) as e:
        print(f"Error rendering recipe_detail.html: {e}")  # For debugging
        abort(500)


@recipe_bp.route("/recipe_name_suggestions", methods=["POST"])
def recipe_name_suggestions():
    """Provides recipe name suggestions based on a partial query."""
    data = request.json
    query_term = data.get("query", "").strip()

    if not query_term:
        return jsonify([])

    suggestions = Recipe.search_by_name_pattern(query_term)
    return jsonify(suggestions)
