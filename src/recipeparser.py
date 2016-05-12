import json
import re
import timeit
import sys

from parsimonious.grammar import Grammar
from fractions import Fraction
# grammar = Grammar(
#     """
#      bold_text  = bold_open text bold_close
#      text       = ~"[A-Z 0-9]*"i
#      bold_open  = "(("
#      bold_close = "))"
#      """)
# a = grammar.parse('((bold stuff))')
# for b in a:
#     print(b)

grammar = Grammar(
    """
     recipeItem  = quantity measurement ingredient
     measurement       =  "package" / "teaspoon" / "tsp" / "tablespoon" / "tbl" / "tbs" / "tbsp" / "T" / "fluid ounce" / "fl oz" / "gill" / "cup" / "pint" / "pt" / "fl pt" / "gallon" / "gal" / "pound" / "ounce"*
     quantity  = ~"[ 0-9\/]+"i
     ingredient = ~"[A-Z 0-9\.\-,]*"i
     """)


def parseRecipeItem(recipeItem):
    recipeItem = re.sub(r'\([^)]*\)', '', recipeItem)
    recipeItem = recipeItem.replace(",", "")
    item = {'ingredient': ''}
    for i, node in enumerate(grammar.parse(recipeItem).children):
        if i == 0:
            item['quantity'] = float(sum(Fraction(s)
                                         for s in node.text.split()))
        elif i == 1:
            item['measurement'] = node.text
            if len(node.text) == 0:
                item['measurement'] = 'whole'
        elif i == 2:
            if node.text[1] == ' ':
                item['ingredient'] = ' '.join(node.text.split(' ')[1:])
            else:
                item['ingredient'] = ' '.join(node.text.split(' ')[0:])
    return item

timed = timeit.timeit('parseRecipeItem("1 (16 ounce) package cottage cheese")',
                      "from __main__ import parseRecipeItem", number=1000)
print("parseRecipeItem takes %d us" % (timed * 1000000 / 1000))

tests = ["1/2 head napa cabbage, sliced thin",
         "1 3/4 cups chicken broth",
         "1/2 onion, sliced",
         "8 chicken thighs with skin and bones (2 1/4 lb)",
         "1 tablespoon olive oil",
         "1/4 teaspoon salt",
         "1 1/2 teaspoons all-purpose flour stirred together with 1 tablespoon water",
         "Accompaniment: egg noodles or rice (optional)"]

for test in tests:
    print(json.dumps(parseRecipeItem(test), indent=2))
