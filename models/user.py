class Food:
    def __init__(self, name, db_id):
        self.name = name
        self.db_id = db_id

# maybe make a this a builder?
class Recipe:
    def __init__(self):
        self.foods = []

    def get_recipe(self):
        return self.foods

    def add_ingredient(self, ingredient: Food):
        self.foods.append(ingredient)
        

class User:
    def __init__(self, id: int):
        self.id = id
        self.recipes = []

    def get_id(self):
        return self.id

    def get_recipe(self, recipe_name):
        # some regex to match recipes based on recipe_name
        return

    def add_recipe(self, recipe: list[Food]):
        self.recipes.append(recipe)

    def get_best_recipe(self) -> Recipe: # get recipe with lowest co2 pr mass unit
        return

    def get_worst_recipe(self) -> Recipe: # get recipe with highest co2 pr mass unit
        return

def calculate_recipe_emission(recipe: Recipe) -> float:
    # for each food in recipe, get the emissions from the database by Food.db_id, and sum the results
    # alternitavely, construct the query from the Recipe, and do the aggregation in the query
    return
