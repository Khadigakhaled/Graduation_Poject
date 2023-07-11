from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd
from datapreprocessing import *

"""##Content based filtering algorithm uisng cosine similarity and TF-id
{by ingredients and keywords}
"""

r = getCleanedRecipes()


def recommendation(ingredients, keywords, recipes2, best_num):
    recipes2 = recipes2.copy()

    recipes2['RecipeIngredientParts'] = recipes2['RecipeIngredientParts'].apply(
        lambda x: ', '.join(x) if type(x) == list else x)
    recipes2['Keywords'] = recipes2['Keywords'].apply(
        lambda x: ', '.join(x) if type(x) == list else x)

    # Combine the ingredient and keyword lists into a single text column
    recipes2['text'] = recipes2['RecipeIngredientParts'] + \
        ' ' + recipes2['Keywords']

   # Vectorize the text column using a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(recipes2['text'])

    # Compute the cosine similarity between the user input and the recipe vectors
    user_input_text = ' '.join(ingredients + keywords)
    user_input_vector = vectorizer.transform([user_input_text])
    cosine_similarities = cosine_similarity(X, user_input_vector)

    # Sort the recipes by cosine similarity and return the top best_num recipes
    recipes2['cosine_similarity'] = cosine_similarities
    recipes2 = recipes2.sort_values(
        by='cosine_similarity', ascending=False).iloc[:best_num]

    return recipes2


"""
ingredients = ['bread', 'Cheese']
keywords = ['spicy']
toprecipes = recommendation(ingredients, keywords, recipes2, 5)
print(toprecipes.Name)
"""
