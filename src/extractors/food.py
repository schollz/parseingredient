import os
import copy
from collections import OrderedDict
import time
import glob
import hashlib
import json
import warnings
warnings.filterwarnings("ignore")

import lxml.html

nullRecipe = json.load(
    open('../testing/recipe_example.json', 'r'), object_pairs_hook=OrderedDict)


def extract_food(file):
    text = open(file, 'r', encoding="ISO-8859-1").read()
    page = lxml.html.fromstring(text)
    recipe = copy.deepcopy(nullRecipe)
    recipe['isBasedOnUrl'] = page.xpath(
        '//meta[@property="og:url"]')[0].attrib['content'].strip()
    data = json.loads(page.xpath(
        '//script[@type="application/ld+json"]')[0].text_content())
    for key in recipe.keys():
        if key in data:
            recipe[key] = copy.deepcopy(data[key])
    recipe['recipeInstructions'] = data[
        'recipeInstructions']['itemListElement']
    hasher = hashlib.sha1()
    hasher.update(json.dumps(
        recipe['recipeIngredient'] + recipe['recipeInstructions']).encode('utf-8'))
    with open(os.path.join('../finished/food.com/', str(hasher.hexdigest()) + '.json'), 'w') as f:
        f.write(json.dumps(recipe, indent=2))
    print(json.dumps(recipe, indent=2))
