import pandas as pd
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from datapreprocessing import *
import re
import nltk
import numpy as np


path = "recipes.csv"
recipes = pd.read_csv(path, nrows=25000)

recipes.Images = reformatColumns(recipes.Images)

# Drop duplicates based on the 'Name' column
recipes = recipes.drop_duplicates(subset='Name', keep='first')


# Define additional stop words
additional_stop_words = ['margarine', 'oil', 'salt', 'butter', 'baking soda', 'black pepper', 'red pepper flakes', 'brown sugar', 'vanilla', 'garlic powder', 'firm butter', 'cumin', 'garlic cloves', 'dark brown sugar', 'chili powder', 'powdered sugar', 'pepper', 'green pepper', 'light brown sugar', 'boiling water', 'white pepper', 'fine salt', 'vanilla extract', 'green chili pepper', 'cider vinegar',
                         'real vanilla', 'unsalted butter', 'bell peppers', 'unsalted butte', 'vanilla essence', 'black salt', 'baking', 'bell', 'black', 'boiling', 'brown', 'butte', 'chili', 'cider', 'cloves', 'dark', 'essence', 'extract', 'fine', 'firm', 'flakes', 'granulated', 'green', 'light', 'olive', 'peppers', 'powder', 'powdered', 'real', 'red', 'soda', 'unsalted', 'vinegar', 'white', 'garlic', 'sugar', 'water']


# Get the default stop words list from NLTK
default_stop_words = stopwords.words('english')


# Merge the default and additional stop words list
stop_words = default_stop_words + additional_stop_words


# Create a TfidfVectorizer with custom stop words
tfidf = TfidfVectorizer(stop_words=stop_words)


# Fill any missing values in the RecipeIngredientParts column with an empty string
recipes['RecipeIngredientParts'] = recipes['RecipeIngredientParts'].fillna("")

# Fit and transform the tfidf matrix using the RecipeIngredientParts column
tfidf_matrix = tfidf.fit_transform(recipes['RecipeIngredientParts'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(recipes.index, index=recipes['Name']).drop_duplicates()


def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = enumerate(cosine_sim[idx])
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:5]

    sim_index = [i[0] for i in sim_scores]
    #print (recipes['Name'].iloc[sim_index])
    related_recipes = recipes.iloc[sim_index]
    return related_recipes


"""rel = get_recommendations("Biryani")
print(rel['Name'])"""

# return el recipe name ele wa2ef 3aleha fel variable da
"""recipe_name = "Biryani"
for recipe in get_recommendations(recipe_name):
    print(recipe)

"""
"""
def get_related_recipes(recipe_name):
    
    return df[]"""
