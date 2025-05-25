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
    def find_id_by_name(name):
        """Finds the food_id for a given ingredient name."""
        find_food_query = """
            SELECT food_id FROM Food WHERE LOWER(name) = LOWER(:name) LIMIT 1
        """
        result = db.session.execute(text(find_food_query), {"name": name})
        food_row = result.fetchone()
        return food_row[0] if food_row else None

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
