# this controller could be responsible for searching in the foods list, matching the results by some regex
from models.recipe import Recipe
from models.food import Food

def create_recipe(author, recipe_name, ingredients):
    recipe = Recipe(author, recipe_name)
    for ingredient in ingredients:
        food = Food(ingredient["name"], ingredient["amount"], ingredient["emission"])
        recipe.add_ingredient(food)
    return recipe.save_recipe()