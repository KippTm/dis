from flask import Flask, render_template, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import re

app = Flask(__name__, template_folder="views")

db = SQLAlchemy()


def render_temp(temp):
    try:
        return render_template(f"{temp}.html")
    except:
        abort(404)


@app.route("/")
def main():
    return render_temp("index")

@app.route("/new_recipe")
def add_recipe():
    return render_temp("new_recipe")

@app.route("/check_ingredients", methods=["POST"])
def check_ingredients():
    ingredient_list = request.json
    result_list = []
    for ingredient in ingredient_list:
        match_word = re.compile(r"\w+"gm)
        match = match_word.findall(ingredient.name)
        if len(match) == 0:
            result_list.append({"name": ""})
            continue
        word_count = {}
        freq_words = set()
        fetch_food_query = """SELECT food_id, name, category, emission FROM food WHERE LOWER(name) LIKE '%:name%'"""
        for word in match:
            result = db.session.execute(text(fetch_food_query), {"name": word})
            for row in result:
                row 
       
