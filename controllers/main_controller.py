from flask import Blueprint, request, redirect, render_template, abort
from models.recipe import Recipe

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def main_page():
    user_cookie = request.cookies.get("user")
    if user_cookie:
        try:
            return render_template("index.html")
        except:
            abort(404)
    return redirect("/login")


@main_bp.route("/profile")
def profile_page():
    user = request.cookies.get("user")
    if not user:
        return redirect("/login")

    recipe_names = Recipe.get_recipes_by_author(user)
    try:
        return render_template("profile.html", user=user, recipes=recipe_names)
    except:
        abort(404)
