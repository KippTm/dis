from flask import Flask, render_template, abort, request, make_response, redirect, jsonify
from models.user import User
from sqlalchemy import text
from db import db
import re

app = Flask(__name__, template_folder="views")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/recipe_site'
db.init_app(app)

def render_temp(temp):
    try:
        return render_template(f"{temp}.html")
    except:
        abort(404)

@app.route("/",)
def main():
    user_cookie = request.cookies.get('user')
    if user_cookie:
        return render_temp("index")
    return redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        query = """
            SELECT * FROM Users
            WHERE username = :username AND password = :password
        """
        result = db.session.execute(text(query), {"username": username, "password": password})
        if (result.fetchone()):
            resp = make_response(redirect("/"))
            resp.set_cookie('user', username)
            return resp
        err = "User does not exist"
        render_template("login.html", error=err)

    return render_temp("login")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pass')
        confirm = request.form.get('conf')
        if (confirm != password):
            err = "Password and confirmation do not match"
            return render_template("signup.html", error=err)
            
        new_user = User(username, password)
        succ = new_user.try_create_user()
        if not succ:
            err = "User already exists"
            return render_template("signup.html", error=err)
        return redirect("/login")
             
            #return f"User creation unsuccesful"

    return render_temp("signup")

@app.route("/new_recipe", methods=['GET'])
def add_recipe():
    return render_temp("new_recipe")

@app.route("/new_recipe", methods=['POST'])
def add_recipe_post():
    return render_temp("new_recipe")

@app.route("/check-ingredients", methods=["POST"])
def check_ingredients():
    ingredient_list = request.json["ingredients"]
    result_list = []
    for ingredient in ingredient_list:
        match_word = re.compile(r"\w+", re.UNICODE)
        match = match_word.findall(ingredient["name"])

        if len(match) == 0:
            result_list.append({"name": ""})
            continue
        word_count = {}
        freq_words = set()
        max_count = 0
        fetch_food_query = """SELECT food_id, name, category, emission FROM food WHERE LOWER(name) LIKE :name"""
        for word in match:
            result = db.session.execute(text(fetch_food_query), {"name": f"%{word.lower()}%"})
            for row in result:
                word_count[row[0]] = word_count.get(row[0], 0) + 1
                if word_count[row[0]] > max_count:
                    max_count = word_count[row[0]]
                    freq_words = {row[0]}
                elif word_count[row[0]] == max_count:
                    freq_words.add(row[0])
        if max_count == 0:
            result_list.append({"name": ""})
            continue
        get_common_food = """SELECT food_id, name FROM food WHERE food_id=:food_id"""
        result_list.append({"name": db.session.execute(text(get_common_food), {"food_id": list(freq_words)[0]}).first()[1]})
    return jsonify(result_list)
       
if __name__ == '__main__':
    app.run(port=8000, debug=True)