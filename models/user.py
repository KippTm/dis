from sqlalchemy import text
from db import db

# It's highly recommended to use a password hashing library like bcrypt or werkzeug.security
# from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, username, password, user_id=None):
        self.user_id = user_id
        self.username = username
        self.password = (
            password  # In a real application, this should be a hashed password
        )

    def try_create_user(self):
        """
        Attempts to create a new user in the database.
        Returns True if successful, False if the user already exists or an error occurs.
        """
        # Check if user already exists
        check_user_query = "SELECT username FROM Users WHERE username = :username"
        existing_user = db.session.execute(
            text(check_user_query), {"username": self.username}
        ).fetchone()
        if existing_user:
            return False  # User already exists

        # In a real application, hash the password before storing it:
        # self.password_hash = generate_password_hash(self.password)
        # Then store self.password_hash instead of self.password
        insert_user_query = (
            "INSERT INTO Users (username, password) VALUES (:username, :password)"
        )
        try:
            with db.session.begin():
                db.session.execute(
                    text(insert_user_query),
                    {
                        "username": self.username,
                        "password": self.password,
                    },  # Store self.password_hash
                )
            return True
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error creating user: {e}")
            return False

    @staticmethod
    def find_by_username(username):
        """Finds a user by their username."""
        # Assuming Users table only has username and password columns for now
        query = "SELECT username, password FROM Users WHERE username = :username"
        result = db.session.execute(text(query), {"username": username}).fetchone()
        if result:
            # user_id will be None as it's not fetched from the DB
            return User(username=result[0], password=result[1], user_id=None)
        return None

    def check_password(self, password_to_check):
        """
        Checks the provided password against the stored password (hash).
        Replace this with proper hash checking.
        """
        # return check_password_hash(self.password, password_to_check) # self.password would be the stored hash
        return (
            self.password == password_to_check
        )  # This is insecure for plain text passwords

    # Example of how login logic could be moved to the model:
    @staticmethod
    def authenticate(username, password):
        """Authenticates a user. Returns User object if valid, None otherwise."""
        user = User.find_by_username(username)
        if user and user.check_password(password):
            return user
        return None


# from sqlalchemy import text
# from db import db
# from models.food import Food
# from models.recipe import Recipe

# class User:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#         self.db_id = username
#         self.recipes = []

#     def get_id(self):
#         return self.db_id

#     def get_recipe(self, recipe_name):
#         query = """
#             SELECT * FROM Recipe
#             WHERE author = :author AND recipe_name = :recipe_name
#         """
#         result = db.session.execute(text(query), {"author": self.username, "recipe_name": f"%{recipe_name}%"})
#         return result.fetchone()

#     def get_recipes(self, recipe_name):
#         query = """
#             SELECT * FROM Recipe
#             WHERE author = :author
#         """
#         result = db.session.execute(text(query), {"author": self.username, "recipe_name": f"%{recipe_name}%"})
#         return result.fetchall()

#         # returns a bool to check for
#     def try_create_user(self) -> bool:
#         try:
#             insert_query = "INSERT INTO Users (username, password) VALUES (:username, :password)"
#             db.session.execute(text(insert_query), {"username": self.username, "password": self.password})
#             db.session.commit()
#             return True
#         except:
#             return False # no need to throw a new exception, keeping it simple

#     def add_recipe(self, recipe: list[Food]):
#         self.recipes.append(recipe)

#     def get_best_recipe(self) -> Recipe: # get recipe with lowest co2 pr mass unit
#         return

#     def get_worst_recipe(self) -> Recipe: # get recipe with highest co2 pr mass unit
#         return
