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
recipe['name'] = page.xpath(
    '//meta[@property="og:title"]')[0].attrib['content'].strip()
print(recipe['name'])
# fooScore = scores[0].xpath(
#     ".//div")[0].text_content().split(':')[1].split('/')[0].strip()
