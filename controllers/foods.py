# this controller could be responsible for searching in the foods list, matching the results by some regex
from models.recipe import Recipe
from models.food import Food
from models.user import User

def create_recipe(author, recipe_name, ingredients):
    recipe = Recipe(author, recipe_name)
    for ingredient in ingredients:
        food = Food(ingredient[0], ingredient[1], ingredient[2], ingredient[3], ingredient[4]) # matches food schema
        recipe.add_ingredient(food)
    return recipe.save()

def get_best_recipe(user: User) -> Recipe | None: # get recipe with lowest co2 pr mass unit
    recipes = user.get_recipes()
    best_recipe = None
    best_emission = float("inf")
    for recipe in recipes:
        recipe_emission = recipe.calculate_recipe_emission()
        if recipe_emission < best_emission:
            best_emission = recipe_emission
            best_recipe = recipe
    return best_recipe

def get_worst_recipe(user: User) -> Recipe | None: # get recipe with highest co2 pr mass unit
    recipes = user.get_recipes()
    worst_recipe = None
    worst_emission = float("-inf")
    for recipe in recipes:
        recipe_emission = recipe.calculate_recipe_emission()
        if recipe_emission > worst_emission:
            worst_emission = recipe_emission
            worst_recipe = recipe
    return worst_recipe