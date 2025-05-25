from db import db
from sqlalchemy import text
from .food import Food


class RecipeIngredient:
    def __init__(self, food_name, amount, food_id=None):
        self.food_name = food_name
        self.amount = amount
        self.food_id = food_id


class Recipe:
    def __init__(self, recipe_name, author, ingredients=None):
        self.recipe_name = recipe_name
        self.author = author
        self.ingredients_data = ingredients if ingredients is not None else []

    @staticmethod
    def exists(author, recipe_name):
        """Checks if a recipe with this name already exists for the user."""
        check_recipe_query = """
            SELECT recipe_name FROM Recipe
            WHERE author = :author AND recipe_name = :recipe_name
        """
        existing_recipe = db.session.execute(
            text(check_recipe_query), {"author": author, "recipe_name": recipe_name}
        ).fetchone()
        return True if existing_recipe else False

    def save(self):
        """Saves the recipe and its ingredients to the database."""
        try:
            # Insert the recipe
            insert_recipe_query = """
                INSERT INTO Recipe (author, recipe_name)
                VALUES (:author, :recipe_name)
            """
            db.session.execute(
                text(insert_recipe_query),
                {"author": self.author, "recipe_name": self.recipe_name},
            )

            # Insert ingredients
            for ing_data in self.ingredients_data:
                food_id = Food.find_id_by_name(ing_data["name"])
                if food_id:
                    insert_recipe_content_query = """
                        INSERT INTO Recipe_Content (recipe_name, recipe_author, food_id, amount)
                        VALUES (:recipe_name, :recipe_author, :food_id, :amount)
                    """
                    db.session.execute(
                        text(insert_recipe_content_query),
                        {
                            "recipe_name": self.recipe_name,
                            "recipe_author": self.author,
                            "food_id": food_id,
                            "amount": ing_data["amount"],
                        },
                    )
                else:

                    print(
                        f"Warning: Food item '{ing_data['name']}' not found. Skipping."
                    )
            db.session.commit()  # Commit the transaction after all operations
            return True
        except Exception as e:
            db.session.rollback()  # Rollback in case of any error
            print(f"Error saving recipe: {str(e)}")

            raise e

    @staticmethod
    def get_recipes_by_author(author_username):
        """Fetches all recipe names for a given author."""
        get_user_recipes_query = """
            SELECT recipe_name FROM Recipe WHERE author = :user
        """
        result = db.session.execute(
            text(get_user_recipes_query), {"user": author_username}
        )
        return [row[0] for row in result]

    @staticmethod
    def search_by_name(query_term):
        """Searches for recipes by name."""
        recipe_search_query = """
            SELECT recipe_name, author FROM Recipe WHERE recipe_name ILIKE :query
        """  # Using ILIKE for case-insensitive search
        results = db.session.execute(
            text(recipe_search_query), {"query": f"%{query_term}%"}
        )
        return [{"name": row[0], "author": row[1]} for row in results]


# from sqlalchemy import text
# from models.food import Food
# from db import db

# class Recipe:
#     def __init__(self, author, recipe_name):
#         self.foods = []
#         self.author = author
#         self.recipe_name = recipe_name

#     # save into both tables Recipe and Recipe_Content
#     def save_recipe(self):
#         try:
#             insert_recipe_query = """
#                 INSERT INTO Recipe (author, recipe_name) VALUES (:author, :recipe_name)
#             """
#             db.session.execute(text(insert_recipe_query), {"author": self.author, "recipe_name": self.recipe_name})

#             for food in self.foods:
#                 insert_ingredient_query = """
#                     INSERT INTO Recipe_Content (recipe_name, recipe_author, food_id, amount)
#                     VALUES (:recipe_name, :recipe_author, :food_id, :amount)
#                 """
#                 db.session.execute(text(insert_ingredient_query), {
#                     "recipe_name": self.recipe_name,
#                     "recipe_author": self.author,
#                     "food_id": food.db_id,
#                     "amount": food.amount
#                 })

#             db.session.commit()
#             return True
#         except:
#             db.session.rollback()
#             return False

#     def get_recipe_ingredients(self):
#         return self.foods

#     def add_ingredient(self, ingredient: Food):
#         self.foods.append(ingredient)

#     def calculate_recipe_emission(self) -> float:
#         return sum([food.get_food_emission() for food in self.foods])
