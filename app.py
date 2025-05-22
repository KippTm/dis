from flask import Flask, render_template, abort, request, make_response, redirect
from models.user import User
from sqlalchemy import text
from db import db

app = Flask(__name__, template_folder="views")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://recipe_user:recipe_pass@localhost/recipe_site'
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
            SELECT * FROM User
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
        new_user.try_create_user()
        return redirect("/login")
             
            #return f"User creation unsuccesful"

    return render_temp("signup")
