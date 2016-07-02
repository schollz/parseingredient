import copy
import hashlib
import json
from collections import OrderedDict
import os.path
import lxml.html
f = 'index.html'
nullRecipe = json.load(
    open('../testing/recipe_example.json', 'r'), object_pairs_hook=OrderedDict)
text = open(f, 'r', encoding="ISO-8859-1").read()
page = lxml.html.fromstring(text)
recipe = copy.deepcopy(nullRecipe)
