"""Main application file for the recipe site."""

from flask import (
    Flask,
    render_template,
)
import jinja2
from db import db

from controllers.auth_controller import auth_bp
from controllers.recipe_controller import recipe_bp
from controllers.main_controller import main_bp

app = Flask(__name__, template_folder="views")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost/recipe_site"
# Initialize the database
db.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(recipe_bp)
app.register_blueprint(main_bp)


@app.errorhandler(404)
def page_not_found(_):
    """Custom 404 error handler."""
    try:
        return render_template("404.html"), 404
    except (FileNotFoundError, jinja2.exceptions.TemplateNotFound):
        return "Page not found.", 404


if __name__ == "__main__":
    app.run(port=8000, debug=True)
