from datapreprocessing import *

recipes2 = getCleanedRecipes()

# Search for a recipe by ingredients only


def score_recipes(user_input, recipes2, best_num):

    recipes2 = recipes2.copy()

    def score(ingredient_list):
        score = 0
        for w in user_input:
            if w in ingredient_list:
                score += 1
        return score

    recipes2['score'] = recipes2['RecipeIngredientParts'].apply(
        lambda x: score(x))
    recipes2 = recipes2.sort_values(
        by='score', ascending=False).iloc[:best_num]
    return recipes2


'''
user_input = ['chicken', 'bread']
print('chicken bread')
r = score_recipes(user_input, recipes2, 10)
print(r.Name, r.RecipeIngredientParts)
'''


# Search with ingredints and keywords


def searchrecipe(ingredients, keywords, recipes2, best_num):
    recipes2 = recipes2.copy()

    def score(ingredient_list):
        score = 0
        for w in ingredients:
            if w in ingredient_list:
                score += 1
        return score

    def keyword_score(keyword_list):
        score = 0
        for w in keywords:
            if w in keyword_list:
                score += 1
        return score

    # Compute the score for each recipe based on ingredients and keywords
    recipes2['ingredient_score'] = recipes2['RecipeIngredientParts'].apply(
        lambda x: score(x))
    recipes2['keyword_score'] = recipes2['Keywords'].apply(
        lambda x: keyword_score(x))
    recipes2['total_score'] = recipes2['ingredient_score'] + \
        recipes2['keyword_score']

    # Sort the recipes by total score and return the top best_num recipes
    recipes2 = recipes2.sort_values(
        by='total_score', ascending=False).iloc[:best_num]

    return recipes2


"""
ingredients = ['chicken']
keywords = ['Healty', 'Indian']
print(ingredients, keywords)
print(searchrecipe(ingredients, keywords, recipes2, 10))"""
