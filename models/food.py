from sqlalchemy import text
from client import db

# in ui when adding a food to a recipe, the user should speficy the amount in grams as well
class Food:
    def __init__(self, name, amount, emission):
        self.name = name
        self.db_id = name
        self._amount = amount
        self._emission = emission
    
    def get_exact_emission(self):
        amount_in_kg = self._amount / 1000
        return self._emission * amount_in_kg
            
            
