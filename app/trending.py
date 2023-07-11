from datapreprocessing import *

# eqn weightedrating= (v / (v + m)) * R + (m / (v + m)) * C
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
    return Popular_Recipes


'''
r= get_popular()
r= r[['RecipeId', 'Name', 'Images']]

print(r)
'''

'''
trending = get_popular()
trending = trending[['RecipeId', 'Name', 'Images']]
ret = {}
ret['recipes'] = trending
print(ret)
'''