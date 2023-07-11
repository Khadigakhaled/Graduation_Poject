from datapreprocessing import *

recipe_df = getCleanedRecipes()


def get_recipe_details(recipe_id):
    ret = recipes2.loc[recipes2['RecipeId'] == recipe_id]

    ret = pd.DataFrame(ret)
    if(str(ret['RecipeServings']) == "NA"):
        ret['RecipeServings'] = " "
    if(str(ret['CookTime']) == "NA"):
        ret['CookTime'] = " "
    if(str(ret['Calories']) == "NA"):
        ret['Calories'] = " "

    return ret