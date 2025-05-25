from flask import Blueprint, request, jsonify, render_template, abort
from models.recipe import Recipe
from models.food import Food

recipe_bp = Blueprint("recipe_bp", __name__)


@recipe_bp.route("/new_recipe", methods=["GET"])
def add_recipe_page():
    try:
        return render_template("new_recipe.html")
    except:
        abort(404)


@recipe_bp.route("/new_recipe", methods=["POST"])
def add_recipe_post():
    user = request.cookies.get("user")
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    recipe_name = data.get("recipe_name")
    ingredients_data = data.get("ingredients", [])

    if not recipe_name:
        return jsonify({"error": "Recipe name is required"}), 400

    if Recipe.exists(author=user, recipe_name=recipe_name):
        return (
            jsonify(
                {"error": "A recipe with this name already exists for your account."}
            ),
            409,
        )

    recipe = Recipe(recipe_name=recipe_name, author=user, ingredients=ingredients_data)
    try:
        recipe.save()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": f"Failed to save recipe: {str(e)}"}), 500


@recipe_bp.route("/check-ingredients", methods=["POST"])
def check_ingredients():
    data = request.json
    ingredient_list_data = data.get("ingredients", [])
    result_list = []

    for ingredient_item in ingredient_list_data:
        ingredient_name_raw = ingredient_item.get("name", "").strip()
        suggested_names = Food.search_by_name_pattern(ingredient_name_raw)
        result_list.append({"name": suggested_names})

    return jsonify(result_list)


@recipe_bp.route("/find_recipe")
def find_recipe_page():
    query_term = request.args.get("query")
    results = []
    if query_term:
        results = Recipe.search_by_name(query_term)
    try:
        return render_template("find.html", results=results, query=query_term)
    except:
        abort(404)
