from flask import Flask, jsonify, request
from trending import *
from search import *
from datapreprocessing import *
from rec import *
from recipe_details import *
from related_recipes import *
from category import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/trending')
def get_trending():
    trending = get_popular()
    trending = trending[['RecipeId', 'Name', 'Images']]

    
    trending_arr = [{"ID": id, "Name": name, "Images": image} for id, name, image in zip(
        trending['RecipeId'], trending['Name'], trending['Images'])]

    ret = {}
    ret['recipes'] = trending_arr
    return jsonify(ret)


@app.route('/search/keywords', methods=['GET'])
def get_search_keywords():
    user_input_ingredients = request.args['ingredients']
    user_input_ingredients = user_input_ingredients.split(',')

    user_input_keywords = request.args['keywords']
    user_input_keywords = user_input_keywords.split(',')

    recipes_df = getCleanedRecipes()
    search_keywords = searchrecipe(user_input_ingredients,
                                   user_input_keywords, recipes_df, 10)
    search_keywords = search_keywords[[
        'RecipeId', 'Name', 'Images']]

    search_arr = [{"ID": id, "Name": name, "Images": image, } for id, name, image in zip(
        search_keywords['RecipeId'], search_keywords['Name'], search_keywords['Images'])]

    ret = {}
    ret['recipes'] = search_arr
    return ret


@app.route('/search', methods=['GET'])
def get_search():
    user_input = request.args['ingredients']
    user_input = user_input.split(',')

    recipes_df = getCleanedRecipes()
    search = score_recipes(user_input, recipes_df, 10)

    search = search[['RecipeId', 'Name', 'Images', 'RecipeCategory']]

    search_arr = [{"ID": id, "Name": name, "Images": image, "RecipeCategory": rCategory} for id, name, image, rCategory in zip(
        search['RecipeId'], search['Name'], search['Images'], search['RecipeCategory'])]

    ret = {}
    ret['recipes'] = search_arr
    return ret


@app.route('/rec', methods=['GET'])
def get_rec():
    user_input_ingredients = request.args['ingredients']
    user_input_ingredients = user_input_ingredients.split(',')

    user_input_keywords = request.args['keywords']
    user_input_keywords = user_input_keywords.split(',')

    recipes_df = getCleanedRecipes()
    rec_recipes = recommendation(
        user_input_ingredients, user_input_keywords, recipes_df, 10)

    rec_recipes = rec_recipes[['RecipeId', 'Name',
                               'Images', 'RecipeCategory']]

    rec_arr = [{"ID": id, "Name": name, "Images": image, "RecipeCategory": recCat} for id, name, image, recCat in zip(
        rec_recipes['RecipeId'], rec_recipes['Name'], rec_recipes['Images'], rec_recipes['RecipeCategory'])]

    ret = {}
    ret['recipes'] = rec_arr
    return jsonify(ret)


@app.route('/recipe', methods=['GET'])
def get_recipe():
    recipe_id = request.args['id']
    ret_recipe = get_recipe_details(int(recipe_id))

    ret_recipe['RecipeIngredientParts'] = ret_recipe['RecipeIngredientParts'].apply(
        lambda x: ", ".join(x))
    ret_recipe['RecipeIngredientQuantities'] = ret_recipe['RecipeIngredientQuantities'].apply(
        lambda x: ", ".join(x))
    ret_recipe['Keywords'] = ret_recipe['Keywords'].apply(
        lambda x: ", ".join(x))

    rec_arr = [{"ID": id, "Name": name, "Images": image, "CookTime": cook, "Keywords": keywords,
                "RecipeIngredientQuantities": quantity, "Ingredients": ingredient, "RecipeInstructions": instructions,
                "RecipeServings": servings, "Calories": calories,
                "FatContent": fat, "SaturatedFatContent": saturated, "CholesterolContent": cholesterol,
                "SodiumContent": sodium, "CarbohydrateContent": carb, "FiberContent": fiber,
                "SugarContent": sugar, "ProteinContent": protien}
               for id, name, image, cook, keywords, quantity, ingredient, instructions, servings, calories,
               fat, saturated, cholesterol, sodium, carb, fiber, sugar, protien in zip(
        ret_recipe['RecipeId'], ret_recipe['Name'], ret_recipe['Images'], ret_recipe['CookTime'], ret_recipe['Keywords'],
        ret_recipe['RecipeIngredientQuantities'], ret_recipe['RecipeIngredientParts'], ret_recipe['RecipeInstructions'], ret_recipe['RecipeServings'],
        ret_recipe['Calories'],
        ret_recipe['FatContent'], ret_recipe['SaturatedFatContent'], ret_recipe['CholesterolContent'], ret_recipe['SodiumContent'],
        ret_recipe['CarbohydrateContent'], ret_recipe['FiberContent'], ret_recipe['SugarContent'], ret_recipe['ProteinContent'])]

    ret = {}
    ret['recipe'] = rec_arr

    return jsonify(ret)


@app.route('/related', methods=['GET'])
def get_related():
    recipe_name = request.args['recipe']
    ret_recipe = get_recommendations(recipe_name)

    rec_arr = [{"ID": id, "Name": name, "Images": image} for id, name, image, in zip(
        ret_recipe['RecipeId'], ret_recipe['Name'], ret_recipe['Images'])]

    ret = {}
    ret['recipes'] = rec_arr
    return jsonify(ret)


@app.route('/category', methods=['GET'])
def get_cat():
    cat = request.args['category']
    ret_recipe = get_category(cat)
    cat_arr = [{"ID": id, "Name": name, "Images": image} for id, name, image, in zip(
        ret_recipe['RecipeId'], ret_recipe['Name'], ret['Images'])]

    ret = {}
    ret['recipes'] = cat_arr
    return jsonify(ret)


if __name__ == "__main__":
    app.run(debug=True)
