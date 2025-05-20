from sqlalchemy import text
from client import db

# in ui when adding a food to a recipe, the user should speficy the amount in grams as well
class Food:
    def __init__(self, food_id,
                name,
                category,
                emission,
                amount):
        self.db_id = food_id
        self.name = name
        self.category = category
        self._emission = emission
        self._amount = amount

    def get_exact_emission(self):
        amount_in_kg = self._amount / 1000
        return self._emission * amount_in_kg
            
            
