"""Recipe model for managing recipes and their ingredients."""

from decimal import Decimal
from sqlalchemy import text
from db import db
from models.food import Food


class RecipeIngredient:
    """Represents an ingredient in a recipe with its name, amount, and optional food_id."""

    def __init__(self, food_name, amount, food_id=None):
        self.food_name = food_name
        self.amount = amount
        self.food_id = food_id


class Recipe:
    """Represents a recipe with its name, author, and associated ingredients."""

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
        """Searches for recipes by name using a case-insensitive search."""
        recipe_search_query = """
            SELECT recipe_name, author FROM Recipe WHERE recipe_name ILIKE :query
            ORDER BY recipe_name
        """  # Using ILIKE for case-insensitive search
        results = db.session.execute(
            text(recipe_search_query), {"query": f"%{query_term}%"}
        ).fetchall()
        return [{"recipe_name": row[0], "author": row[1]} for row in results]

    @staticmethod
    def search_recipes(query_term="", selected_categories=None):
        """
        Searches for recipes by name and optionally filters by food categories.
        Returns a list of dicts with 'recipe_name' and 'author'.
        """
        params = {}

        # Base query to select distinct recipes
        sql_query_parts = ["SELECT DISTINCT r.recipe_name, r.author", "FROM Recipe r"]

        conditions = []

        if query_term:
            params["query_term"] = f"%{query_term}%"
            conditions.append("r.recipe_name ILIKE :query_term")

        if selected_categories and len(selected_categories) > 0:
            # Ensure selected_categories is a tuple for SQL IN clause
            params["selected_categories"] = tuple(selected_categories)

            # Subquery to check if the recipe contains any ingredient from the selected categories
            category_filter_subquery = """
                EXISTS (
                    SELECT 1
                    FROM Recipe_Content rc
                    JOIN Food f ON rc.food_id = f.food_id
                    WHERE rc.recipe_author = r.author AND rc.recipe_name = r.recipe_name
                    AND f.category IN :selected_categories
                )
            """
            conditions.append(category_filter_subquery)

        if conditions:
            sql_query_parts.append("WHERE " + " AND ".join(conditions))

        sql_query_parts.append("ORDER BY r.recipe_name")

        final_query = " ".join(sql_query_parts)

        results = db.session.execute(text(final_query), params).fetchall()
        return [{"recipe_name": row[0], "author": row[1]} for row in results]

    @staticmethod
    def get_recipe_details_with_emissions(author_username, recipe_name_str):
        """
        Fetches a recipe's ingredients, their amounts, and calculates CO2 emissions.
        Assumes Food.emission is kg CO2e / kg of food.
        Assumes Recipe_Content.amount is in grams.
        """
        # First, check if the recipe itself exists
        recipe_check_query = """
            SELECT recipe_name, author FROM Recipe
            WHERE author = :author AND recipe_name = :recipe_name
        """
        recipe_info = db.session.execute(
            text(recipe_check_query),
            {"author": author_username, "recipe_name": recipe_name_str},
        ).fetchone()

        if not recipe_info:
            return None  # Recipe not found

        query = """
            SELECT
                rc.recipe_name,
                rc.recipe_author,
                f.name AS food_name,
                rc.amount,
                f.emission AS food_emission_per_kg,
                f.category AS food_category
            FROM Recipe_Content rc
            JOIN Food f ON rc.food_id = f.food_id
            WHERE rc.recipe_author = :author AND rc.recipe_name = :recipe_name
        """
        results = db.session.execute(
            text(query), {"author": author_username, "recipe_name": recipe_name_str}
        ).fetchall()

        ingredients_details = []
        total_recipe_emission = Decimal("0.0")

        for row in results:
            amount_grams = Decimal(row[3])  # rc.amount
            emission_per_kg = Decimal(row[4])  # f.emission

            # Calculate CO2 emission for this ingredient
            ingredient_emission = (amount_grams / Decimal("1000.0")) * emission_per_kg
            total_recipe_emission += ingredient_emission

            ingredients_details.append(
                {
                    "name": row[2],  # food_name
                    "amount": amount_grams,
                    "unit": "g",  # Assuming amount is in grams
                    "co2_emission_per_ingredient": round(ingredient_emission, 4),
                }
            )

        return {
            "recipe_name": recipe_info[0],
            "author": recipe_info[1],
            "ingredients": ingredients_details,
            "total_co2_emission": round(total_recipe_emission, 4),
        }


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
