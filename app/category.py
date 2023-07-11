import pandas as pd
from datapreprocessing import *


def get_category(cat):
    recipes = getCleanedRecipes()

    category_recipes = recipes[recipes['RecipeCategory'] == cat]

    recipe_names = category_recipes.head(20)

    return recipe_names

