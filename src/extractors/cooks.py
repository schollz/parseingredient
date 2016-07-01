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


def extract_cooks(file):
    text = open(file, 'r', encoding="ISO-8859-1").read()
    page = lxml.html.fromstring(text)
    recipe = copy.deepcopy(nullRecipe)
    # recipe['datePublished'] = page.xpath(
    #     '//meta[@itemprop="datePublished"]')[0].attrib['content'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//input[@rel="shorturl"]')[0].attrib['value'].strip()
    recipe['author'] = page.xpath(
        '//meta[@name="author"]')[0].attrib['content'].strip()
    recipe['name'] = page.xpath(
        '//title')[0].text_content().strip()
    # recipe['description'] = page.xpath(
    #     '//meta[@name="description"]')[0].attrib['content'].strip()

    # try:
    #     recipe['recipeCuisine'] = page.xpath(
    #         '//a[@itemprop="recipeCuisine"]')[0].text_content().strip()
    # except:
    #     pass
    #
    # try:
    #     recipe['recipeCategory'] = page.xpath(
    #         '//a[@itemprop="recipeCategory"]')[0].text_content().strip()
    # except:
    #     pass

    recipeInstructions = page.xpath(
        '//div[@class="instructions"]')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    try:
        recipe['recipeYield'] = page.xpath(
            '//dd[@itemprop="recipeYield"]')[0].text_content().strip()
    except:
        pass
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
        '//span[@class="ingredient"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(ingredient.text_content().strip())
    try:
        recipe['aggregateRating']['ratingValue'] = page.xpath(
            '//span[@class="rating"]/span[@class="value-title"]')[0].attrib['title'].strip()
    except:
        pass
    try:
        recipe['aggregateRating']['reviewCount'] = page.xpath(
            '//span[@class="count"]/span[@class="value-title"]')[0].attrib['title'].strip()
    except:
        pass
    recipe['aggregateRating']['bestRating'] = '5'
    for nutrition in recipe['nutrition']:
        try:
            recipe['nutrition'][nutrition] = page.xpath(
                '//li[@class="nutrientLine__item--amount" and @itemprop="%s"]' % nutrition)[0].text_content()
        except:
            pass
    hasher = hashlib.sha1()
    hasher.update(json.dumps(
        recipe['recipeIngredient'] + recipe['recipeInstructions']).encode('utf-8'))
    with open(os.path.join('../finished/cooks.com/', str(hasher.hexdigest()) + '.json'), 'w') as f:
        f.write(json.dumps(recipe, indent=2))
    print(json.dumps(recipe, indent=2))
