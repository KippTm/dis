from sqlalchemy import text
from app import db
from models.food import Food
from models.recipe import Recipe

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db_id = username
        self.recipes = []

    def get_id(self):
        return self.db_id

    def get_recipe(self, recipe_name):
        query = """
            SELECT * FROM Recipe
            WHERE author = :author AND recipe_name = :recipe_name
        """
        result = db.session.execute(text(query), {"author": self.username, "recipe_name": f"%{recipe_name}%"})
        return result.fetchone()

    def get_recipes(self, recipe_name):
        query = """
            SELECT * FROM Recipe
            WHERE author = :author
        """
        result = db.session.execute(text(query), {"author": self.username, "recipe_name": f"%{recipe_name}%"})
        return result.fetchall()

        # returns a bool to check for 
    def try_create_user(self) -> bool:
        try:
            insert_query = "INSERT INTO Users (u_name, password) VALUES (%s, %s)"
            db.session.execute(text(insert_query), (self.username, self.password))
            db.session.commit()
            return True
        except:
            return False # no need to throw a new exception, keeping it simple

    def add_recipe(self, recipe: list[Food]):
        self.recipes.append(recipe)

    def get_best_recipe(self) -> Recipe: # get recipe with lowest co2 pr mass unit
        return

    def get_worst_recipe(self) -> Recipe: # get recipe with highest co2 pr mass unit
        return


    
