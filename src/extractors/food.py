from json import loads
from copy import deepcopy


def food_com(page, recipe):
    recipe['isBasedOnUrl'] = page.xpath(
        '//meta[@property="og:url"]')[0].attrib['content'].strip()
    data = loads(page.xpath(
        '//script[@type="application/ld+json"]')[0].text_content())
    for key in recipe.keys():
        if key in data:
            recipe[key] = deepcopy(data[key])
    recipe['recipeInstructions'] = data[
        'recipeInstructions']['itemListElement']
