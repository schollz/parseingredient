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


def extract_epicurious(file):
    text = open(file, 'r', encoding="ISO-8859-1").read()
    page = lxml.html.fromstring(text)
    recipe = copy.deepcopy(nullRecipe)
    recipe['datePublished'] = page.xpath(
        '//meta[@itemprop="datePublished"]')[0].attrib['content'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@rel="canonical"]')[0].attrib['href'].strip()
    recipe['author'] = page.xpath(
        '//meta[@itemprop="author"]')[0].attrib['content'].strip()
    recipe['name'] = page.xpath(
        '//meta[@itemprop="name"]')[0].attrib['content'].strip()
    recipe['description'] = page.xpath(
        '//meta[@name="description"]')[0].attrib['content'].strip()
    recipeInstructions = page.xpath(
        '//li[@class="preparation-step"]')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    recipe['recipeYield'] = page.xpath(
        '//dd[@itemprop="recipeYield"]')[0].text_content().strip()
    try:
        recipe['cookTime'] = page.xpath(
            '//time[@itemprop="cookTime"]')[0].attrib['datetime'].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//dd[@class="active-time"]')[0].text_content()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//dd[@class="total-time"]')[0].text_content()
    except:
        pass
    ingredients = page.xpath(
        '//li[@class="ingredient" and @itemprop="ingredients"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(ingredient.text_content().strip())
    recipe['aggregateRating']['ratingValue'] = page.xpath(
        '//meta[@itemprop="ratingValue"]')[0].attrib['content'].strip()
    recipe['aggregateRating']['reviewCount'] = page.xpath(
        '//span[@itemprop="reviewCount"]')[0].text_content()
    recipe['aggregateRating']['bestRating'] = page.xpath(
        '//meta[@itemprop="bestRating"]')[0].attrib['content'].strip()
    for nutrition in recipe['nutrition']:
        try:
            recipe['nutrition'][nutrition] = page.xpath(
                '//li[@class="nutrientLine__item--amount" and @itemprop="%s"]' % nutrition)[0].text_content()
        except:
            pass
    hasher = hashlib.sha1()
    hasher.update(json.dumps(
        recipe['recipeIngredient'] + recipe['recipeInstructions']).encode('utf-8'))
    with open(os.path.join('../finished/allrecipes.com/', str(hasher.hexdigest()) + '.json'), 'w') as f:
        f.write(json.dumps(recipe, indent=2))
    print(json.dumps(recipe, indent=2))
