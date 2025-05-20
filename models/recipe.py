from sqlalchemy import text
from models.food import Food
from client import db

class Recipe:
    def __init__(self, author, recipe_name):
        self.foods = []
        self.author = author
        self.recipe_name = recipe_name
        
    # save into both tables Recipe and Recipe_Content
    def save(self):
        try:
            insert_recipe_query = """
                INSERT INTO Recipe (author, recipe_name) VALUES (:author, :recipe_name)
            """
            db.session.execute(text(insert_recipe_query), {"author": self.author, "recipe_name": self.recipe_name})

            for food in self.foods:
                insert_ingredient_query = """
                    INSERT INTO Recipe_Content (recipe_name, recipe_author, food_id)
                    VALUES (:recipe_name, :recipe_author, :food_id)
                """
                db.session.execute(text(insert_ingredient_query), {
                    "recipe_name": self.recipe_name,
                    "recipe_author": self.author,
                    "food_id": food.db_id
                })

            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def get_recipe_ingredients(self):
        return self.foods

    def add_ingredient(self, ingredient: Food):
        self.foods.append(ingredient)
    
    def calculate_recipe_emission(self) -> float:
        return sum([food.get_food_emission() for food in self.foods])
