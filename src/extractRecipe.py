import lxml.html
import sys
import json
import warnings
warnings.filterwarnings("ignore")
import traceback
from multiprocessing import Pool
import os
import copy

nullRecipe = json.load(open('../testing/recipe_example.json', 'r'))
text = open('../testing/sites/allrecipes.com/index.html', 'r').read()
page = lxml.html.fromstring(text)
recipe = copy.deepcopy(nullRecipe)
recipe['isBasedOnUrl'] = page.xpath(
    '//link[@id="canonicalUrl"]')[0].attrib['href'].strip()
recipe['author'] = page.xpath(
    '//span[@class="submitter__name"]')[0].text_content().strip()
recipe['name'] = page.xpath(
    '//meta[@property="og:title"]')[0].attrib['content'].strip()
recipe['description'] = page.xpath(
    '//div[@class="submitter__description"]')[0].text_content().strip().replace('"', '')
recipeInstructions = page.xpath(
    '//span[@class="recipe-directions__list--item"]')
recipe['recipeInstructions'] = []
for instruction in recipeInstructions:
    data = instruction.text_content().strip()
    if len(data) > 0:
        recipe['recipeInstructions'].append(data)
recipe['recipeYield'] = page.xpath(
    '//meta[@id="metaRecipeServings" and @itemprop="recipeYield"]')[0].attrib['content'].strip()
recipe['cookTime'] = page.xpath('//')
print(json.dumps(recipe, indent=2))
# fooScore = scores[0].xpath(
#     ".//div")[0].text_content().split(':')[1].split('/')[0].strip()
