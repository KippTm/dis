from sqlalchemy import text
from client import db
from models.food import Food
from models.recipe import Recipe

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db_id = username

    def get_id(self):
        return self.db_id

    def get_recipes(self):
        query = """
            SELECT * FROM Recipe
            WHERE author = :author
        """
        result = db.session.execute(text(query), {"author": self.username}).fetchall()
        recipes = []
        for row in result:
            recipe = Recipe(row[0], row[1])
            recipes.append(recipe)
        return recipes

    def try_create_user(self) -> bool:
        try:
            insert_query = "INSERT INTO Users (u_name, password) VALUES (%s, %s)"
            db.session.execute(text(insert_query), (self.username, self.password))
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False # no need to throw a new exception, keeping it simple




    
