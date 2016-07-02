import copy
import hashlib
import json
from collections import OrderedDict
import os.path

from extractors.allrecipes import allrecipes_com
from extractors.food import food_com
from extractors.epicurious import epicurious_com
from extractors.cooks import cooks_com
from extractors.bbcfood import bbc_co_uk_food
from extractors.betty import bettycrocker_com
from extractors.chowhound import chowhound_com
from extractors.foodandwine import foodandwine_com
from extractors.kraftrecipes import kraftrecipes_com
from extractors.foodnetwork import foodnetwork_com
from extractors.myrecipes import myrecipes_com
from extractors.recipes_latimes_com import recipes_latimes_com
from extractors.seriouseats import seriouseats_com

import lxml.html

nullRecipe = json.load(
    open('../testing/recipe_example.json', 'r'), object_pairs_hook=OrderedDict)

availableParsers = ['allrecipes.com',
                    'epicurious.com',
                    'cooks.com',
                    'food.com',
                    'foodnetwork.com',
                    'bbc.co.uk.food',
                    'bettycrocker.com',
                    'chowhound.com',
                    'foodandwine.com',
                    'myrecipes.com',
                    'recipes.latimes.com',
                    'seriouseats.com',
                    'kraftrecipes.com']


def parseRecipe(f):
    for parser in availableParsers:
        if '/' + parser + '/' in f:
            print(f, parser)
            extractRecipe(f, parser)


def extractRecipe(f, parser):
    text = open(f, 'r', encoding="ISO-8859-1").read()
    page = lxml.html.fromstring(text)
    if len(page) == 0:
        return
    recipe = copy.deepcopy(nullRecipe)
    recipe['file'] = f
    globals()[parser.replace('.', '_')](page, recipe)
    del recipe['file']
    hasher = hashlib.sha1()
    try:
        hashArray = recipe['recipeIngredient'] + recipe['recipeInstructions']
    except:
        return
    hasher.update(json.dumps(hashArray).encode('utf-8'))
    with open(os.path.join('../finished/' + parser + '/', str(hasher.hexdigest()) + '.json'), 'w') as f:
        f.write(json.dumps(recipe, indent=2))
    print(recipe)
