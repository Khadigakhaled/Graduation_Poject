import pandas as pd
import numpy as np

path = "recipes.csv"
recipes = pd.read_csv(path, nrows=25000)
# print(recipes.Name.head())
# print(recipes.columns)

# Function for counting Null values


def countNullValues(col):
    c = 0
    for i in col:
        if(i != i):
            c += 1
    return c


a = countNullValues(recipes.Description)
a

# Drop description, author Id, Author name, Date Published
recipes.drop(columns=['Description', 'AuthorId',
             'AuthorName', 'DatePublished'])

# Function for replacing Null Values


def replaceNullValue(column):
    j = 0
    for i in column:
        if(str(i) == 'nan'):
            column[j] = 'NA'
        j += 1
    return column


c = countNullValues(recipes.CookTime)
t = countNullValues(recipes.TotalTime)
p = countNullValues(recipes.PrepTime)
c, t, p

# Formatting CookTime and PrepTime
recipes.CookTime = recipes.CookTime.str.replace('PT', '')
recipes.PrepTime = recipes.PrepTime.str.replace('PT', '')
recipes.TotalTime = recipes.TotalTime.str.replace('PT', '')

recipes.TotalTime

countNullValues(recipes.Images)

# Splitting data over '", "' and ignoring the starting 'c("' and ending '")' for all
# For NA values in keywords column, replacing it by "NA"
# For character(0) value in Images column, replacing it with "character(0)"
# Ignoring any "\n" occurrence,
# For some special cases in Images column which begin with '"http' instead of more common'c("' and end normally instead of '")',
# making it to read characters from 1st index(character h) only and ignoring just the last '"' by the if-else conditional


def reformatColumns(columnTitle):
    L = []
    for i in columnTitle:
        if(type(i) == str):
            i = i.replace("NA", '"NA"')
            i = i.replace("character(0)", 'c("character(0)")')
            i = i.replace("\n", "")
            if(i[0:5] == '"http'):
                L.append([i[1:-1]])
            else:
                L.append(i[3:-2].split('", "'))
        else:
            L.append([])
    return L

# As there is no need of splitting, replacing some values and appending it to the list to be returned for each recipe


def reformatRecipe(recipe):
    L = []
    for i in recipe:
        i = i.replace("\n", "")
        i = i.replace('.", "', '. ')
        i = i.replace('c("', '')
        i = i.replace('")', '')
        L.append(i)
    return L


recipes.Images = reformatColumns(recipes.Images)


recipes.Images.head()

recipes.Keywords = reformatColumns(recipes.Keywords)


recipes.Keywords.head()

recipes.RecipeIngredientParts = reformatColumns(recipes.RecipeIngredientParts)


recipes.RecipeIngredientParts.head()

recipes.RecipeIngredientQuantities = reformatColumns(
    recipes.RecipeIngredientQuantities)


recipes.RecipeIngredientQuantities.head()

recipes.RecipeInstructions = reformatRecipe(recipes.RecipeInstructions)


recipes.RecipeInstructions.head()
# Removing TotalTime, DatePublished and RecipeYield columns
recipes = recipes[['RecipeId', 'Name',
                   'CookTime', 'PrepTime', 'TotalTime', 'Images',
                   'RecipeCategory', 'Keywords', 'RecipeIngredientQuantities', 'RecipeIngredientParts',
                   'AggregatedRating', 'ReviewCount', 'Calories', 'FatContent',
                   'SaturatedFatContent', 'CholesterolContent', 'SodiumContent', 'CarbohydrateContent',
                   'FiberContent', 'SugarContent', 'ProteinContent', 'RecipeServings', 'RecipeYield', 'RecipeInstructions']]
# print(recipes.shape)

# print(recipes.head())

# print(recipes.loc[55])

# df[df[“column_name”].str.contains(“string”)==False]
recipes2 = recipes[recipes["RecipeCategory"].str.contains("Pork") == False]

recipes2.RecipeCategory.value_counts()

pd.set_option('display.max_rows', None)

recipes2.RecipeCategory

recipes2.Name.duplicated().sum()

recipes2.Name.drop_duplicates(keep=False).shape


# print(recipes2.shape)
# print(recipes.shape)


def getCleanedRecipes():
    return recipes2


# preprocessing for reivews dataset
path = "reviews.csv"
reviews = pd.read_csv(path)

replaceNullValue(reviews.Review)

RatingCount = reviews.groupby('RecipeId')['Rating'].count()
RatingCount.sort_values(ascending=False, inplace=True)

RatingAverages = recipes[recipes['AggregatedRating'].notnull(
)]['AggregatedRating'].astype('int')
c = RatingAverages.mean()
m = RatingCount.quantile(0.50)

Trending_recipes = recipes2.merge(RatingCount, on='RecipeId')
Popular_Recipes = Trending_recipes[(Trending_recipes['Rating'] >= m) & (Trending_recipes['Rating'].notnull()) & (Trending_recipes['AggregatedRating'].notnull())][[
    'RecipeId', 'Name', 'RecipeCategory', 'Images', 'RecipeIngredientParts', 'RecipeIngredientQuantities',  'RecipeInstructions', 'Calories', 'AggregatedRating', 'Rating', 'ReviewCount']]

Popular_Recipes['Rating'] = Popular_Recipes['Rating'].astype('int')
Popular_Recipes['AggregatedRating'] = Popular_Recipes['AggregatedRating'].astype(
    'int')
"""
# eqn weightedrating= (v / (v + m)) * R + (m / (v + m)) * C


def weighted_Rating(x):
    v = x['Rating']
    R = x['AggregatedRating']
    return (v/(v+m) * R) + (m/(m+v) * c)


Popular_Recipes['weighted rating'] = Popular_Recipes.apply(
    weighted_Rating, axis=1)

Popular_Recipes = Popular_Recipes.iloc[:8]
Popular_Recipes = pd.DataFrame(Popular_Recipes)


def get_popular():
    return Popular_Recipes"""

# function splits sting with ,
