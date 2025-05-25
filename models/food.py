"""Food model for managing food items in the database."""

import re
from sqlalchemy import text
from db import db


class Food:
    """Represents a food item in the database."""

    def __init__(self, food_id, name, category, emission):
        self.food_id = food_id
        self.name = name
        self.category = category
        self.emission = emission

    @staticmethod
    def find_id_by_name(food_name):
        """Finds the food_id for a given ingredient name."""
        query = "SELECT food_id FROM Food WHERE name = :name"
        result = db.session.execute(text(query), {"name": food_name}).fetchone()
        return result[0] if result else None

    @staticmethod
    def search_by_name_pattern(ingredient_name_raw):
        """Searches for food items by a name pattern (case-insensitive regex)."""
        if not ingredient_name_raw:
            return []

        regex_pattern = re.escape(ingredient_name_raw)
        fetch_food_query = """
            SELECT name 
            FROM food 
            WHERE name ~* :pattern
            ORDER BY name 
            LIMIT 10
        """
        try:
            rows = db.session.execute(
                text(fetch_food_query), {"pattern": regex_pattern}
            )
            return [row[0] for row in rows]
        except (db.SQLAlchemyError, ValueError) as e:
            print(f"Error fetching ingredient suggestions: {e}")
            return []

    @staticmethod
    def get_all_categories():
        """Fetches all distinct, non-null food categories, ordered alphabetically."""
        query = """
            SELECT DISTINCT category
            FROM Food
            WHERE category IS NOT NULL AND category <> ''
            ORDER BY category
        """
        result = db.session.execute(text(query)).fetchall()
        return [row[0] for row in result]
