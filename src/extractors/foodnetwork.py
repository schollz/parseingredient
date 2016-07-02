import json
import os.path
import datetime


def foodnetwork_com(page, recipe):
    # recipe['datePublished'] = page.xpath(
    #     '//meta[@itemprop="dateCreated"]')[0].attrib['content'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@itemprop="url"]')[0].attrib['href'].strip()
    recipe['author'] = page.xpath(
        '//span[@itemprop="name"]')[0].text_content().strip()
    recipe['name'] = page.xpath(
        '//meta[@property="og:title"]')[0].attrib['content'].split(':')[0].strip()
    recipe['description'] = page.xpath(
        '//meta[@property="twitter:description"]')[0].attrib['content'].strip()
    recipeInstructions = page.xpath(
        '//ul[@class="recipe-directions-list"]/li/p')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    recipe['recipeYield'] = page.xpath(
        '//meta[@itemprop="recipeYield"]')[0].attrib['content'].strip()
    try:
        recipe['cookTime'] = page.xpath(
            '//meta[@itemprop="cookTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//meta[@itemprop="prepTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//meta[@itemprop="totalTime"]')[0].attrib['content'].strip()
    except:
        pass
    ingredients = page.xpath('//li[@itemprop="ingredients"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(ingredient.text_content().strip())

    data = open(recipe['file'] + ".dat", 'r').read()
    data = "{" + data.split('({')[1].split('})')[0] + "}"
    dataJSON = json.loads(data)
    recipe['aggregateRating']['bestRating'] = '5'
    recipe['aggregateRating']['worstRating'] = '1'
    recipe['aggregateRating']['ratingValue'] = dataJSON[
        'streamInfo']['avgRatings']['_overall']
    recipe['aggregateRating']['reviewCount'] = dataJSON[
        'streamInfo']['threadCount']
    recipe['datePublished'] = datetime.datetime.fromtimestamp(
        int(dataJSON['streamInfo']['createDate']) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    # for nutrition in recipe['nutrition']:
    #     try:
    #         recipe['nutrition'][nutrition] = page.xpath(
    #             '//span[@itemprop="%s"]' % nutrition)[0].text_content().strip()
    #     except:
    #         pass

    return recipe
