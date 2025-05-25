from flask import (
    Flask,
    render_template,
    abort,
)  # abort and render_template might be used by error handlers if defined here
from db import db

# Import Blueprints
from controllers.auth_controller import auth_bp
from controllers.recipe_controller import recipe_bp
from controllers.main_controller import main_bp

app = Flask(__name__, template_folder="views")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost/recipe_site"
db.init_app(app)

# Register Blueprints
# If you added url_prefix to your blueprints (e.g., url_prefix='/auth' for auth_bp),
# the routes would be like /auth/login.
# If no url_prefix, routes are as defined in the blueprint (e.g., /login).
app.register_blueprint(auth_bp)
app.register_blueprint(recipe_bp)
app.register_blueprint(main_bp)


# You might want a generic 404 error handler here
@app.errorhandler(404)
def page_not_found(e):
    # You can log the error e here if you want
    try:
        return render_template("404.html"), 404  # Assuming you have a 404.html template
    except:
        return "Page not found.", 404


if __name__ == "__main__":
    app.run(port=8000, debug=True)
