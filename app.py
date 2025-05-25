from flask import (
    Flask,
    render_template,
    abort,
    request,
    make_response,
    redirect,
    jsonify,
)
from models.user import User
from sqlalchemy import text
from db import db
import re

app = Flask(__name__, template_folder="views")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost/recipe_site"
db.init_app(app)


def render_temp(temp):
    try:
        return render_template(f"{temp}.html")
    except:
        abort(404)


@app.route(
    "/",
)
def main():
    user_cookie = request.cookies.get("user")
    if user_cookie:
        return render_temp("index")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        query = """
            SELECT * FROM Users
            WHERE username = :username AND password = :password
        """
        result = db.session.execute(
            text(query), {"username": username, "password": password}
        )
        if result.fetchone():
            resp = make_response(redirect("/"))
            resp.set_cookie("user", username)
            return resp
        err = "User does not exist"
        render_template("login.html", error=err)

    return render_temp("login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        confirm = request.form.get("conf")
        if confirm != password:
            err = "Password and confirmation do not match"
            return render_template("signup.html", error=err)

        new_user = User(username, password)
        succ = new_user.try_create_user()
        if not succ:
            err = "User already exists"
            return render_template("signup.html", error=err)
        return redirect("/login")

        # return f"User creation unsuccesful"

    return render_temp("signup")


@app.route("/new_recipe", methods=["GET"])
def add_recipe():
    return render_temp("new_recipe")


@app.route("/new_recipe", methods=["POST"])
def add_recipe_post():
    # Get user from cookie
    user = request.cookies.get("user")
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    # Get data from request
    data = request.json
    recipe_name = data.get("recipe_name")
    ingredients = data.get("ingredients", [])

    # Validate recipe name
    if not recipe_name:
        return jsonify({"error": "Recipe name is required"}), 400

    try:
        with db.session.begin():
            # Check for existing recipe name for this user
            check_recipe_query = """
                SELECT recipe_name FROM Recipe
                WHERE author = :author AND recipe_name = :recipe_name
            """
            existing_recipe = db.session.execute(
                text(check_recipe_query), {"author": user, "recipe_name": recipe_name}
            ).fetchone()

            if existing_recipe:
                return (
                    jsonify(
                        {
                            "error": "A recipe with this name already exists for your account."
                        }
                    ),
                    409,
                )

            insert_recipe_query = """
                INSERT INTO Recipe (author, recipe_name)
                VALUES (:author, :recipe_name)
            """
            db.session.execute(
                text(insert_recipe_query), {"author": user, "recipe_name": recipe_name}
            )

            # Insert ingredients
            for ingredient in ingredients:
                # Find the food_id for this ingredient
                find_food_query = """
                    SELECT food_id FROM Food WHERE LOWER(name) = LOWER(:name) LIMIT 1
                """
                result = db.session.execute(
                    text(find_food_query), {"name": ingredient["name"]}
                )
                food_row = result.fetchone()

                if food_row:
                    food_id = food_row[0]
                    # Insert into Recipe_Content table
                    insert_recipe_content_query = """
                        INSERT INTO Recipe_Content (recipe_name, recipe_author, food_id, amount)
                        VALUES (:recipe_name, :recipe_author, :food_id, :amount)
                    """
                    db.session.execute(
                        text(insert_recipe_content_query),
                        {
                            "recipe_name": recipe_name,
                            "recipe_author": user,
                            "food_id": food_id,
                            "amount": ingredient["amount"],
                        },
                    )
        return jsonify({"success": True})

    except Exception as e:
        db.session.rollback()
        print(f"Error saving recipe: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/check-ingredients", methods=["POST"])
def check_ingredients():
    data = request.json
    ingredient_list = data.get("ingredients", [])
    result_list = []

    for ingredient_item in ingredient_list:
        ingredient_name = ingredient_item.get("name", "").strip()

        if not ingredient_name:
            result_list.append({"name": []})
            continue

        search_term = f"{ingredient_name.lower()}%"

        fetch_food_query = """
            SELECT name 
            FROM food 
            WHERE LOWER(name) LIKE :search_term
            ORDER BY name 
            LIMIT 10
        """

        try:
            rows = db.session.execute(
                text(fetch_food_query), {"search_term": search_term}
            )
            names = [row[0] for row in rows]
            result_list.append(
                {"name": names if names else []}
            )  # Ensure an empty list if no matches
        except Exception as e:
            print(f"Error fetching ingredient suggestions: {e}")
            result_list.append({"name": []})  # Return empty list on error

    return jsonify(result_list)


@app.route("/profile")
def profile():
    user = request.cookies.get("user")
    get_user_recipes = """ SELECT recipe_name FROM Recipe WHERE author = :user """
    recipes = db.session.execute(text(get_user_recipes), {"user": user})
    return render_template("profile.html", user=user, recipes=recipes)


@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query")
    results = []
    if query:
        recipe_search = (
            """ SELECT recipe_name FROM Recipe WHERE recipe_name = :query """
        )
        results = db.session.execute(text(recipe_search), {"query": query})
    return render_template("find.html", results=results)


@app.route("/logout", methods=["POST"])  # Or GET if you used GET in the form
def logout():
    response = make_response(redirect("/login"))
    response.set_cookie("user", "", expires=0)  # Clear the cookie
    return response


if __name__ == "__main__":
    app.run(port=8000, debug=True)
