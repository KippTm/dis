from flask import Blueprint, request, make_response, redirect, render_template, abort
from models.user import User

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.authenticate(username, password)

        if user:
            resp = make_response(redirect("/"))  # Redirect to home page
            resp.set_cookie("user", username)
            return resp
        err = "User does not exist or password incorrect."
        try:
            return render_template("login.html", error=err)
        except:
            abort(404)

    try:
        return render_template("login.html")
    except:
        abort(404)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        confirm = request.form.get("conf")

        if confirm != password:
            err = "Password and confirmation do not match"
            try:
                return render_template("signup.html", error=err)
            except:
                abort(404)

        new_user = User(username=username)
        new_user.set_password(password)  # Set and hash the password

        if not new_user.try_create_user():
            err = "User already exists or error creating user."
            try:
                return render_template("signup.html", error=err)
            except:
                abort(404)

        # Log the user in by creating a response and setting the cookie
        resp = make_response(redirect("/"))  # Redirect to homepage
        resp.set_cookie("user", username)  # Set the user cookie
        return resp  # Return the response

    try:
        return render_template("signup.html")
    except:
        abort(404)


@auth_bp.route("/logout", methods=["POST"])  # Assuming POST for logout
def logout():
    response = make_response(redirect("/login"))
    response.set_cookie("user", "", expires=0)
    return response
