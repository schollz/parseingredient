import json
import os.path


def kraftrecipes_com(page, recipe):
    # recipe['datePublished'] = page.xpath(
    #     '//meta[@itemprop="dateCreated"]')[0].attrib['content'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@rel="canonical"]')[0].attrib['href'].strip()
    try:
        recipe['author'] = page.xpath(
            '//span[@itemprop="author"]')[0].text_content().strip()
    except:
        pass
    try:
        recipe['name'] = page.xpath(
            '//meta[@name="title"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['description'] = page.xpath(
            '//meta[@name="description"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipeInstructions = page.xpath(
            '//ul[@itemprop="recipeInstructions"]/li/div')
    except:
        return recipe
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    try:
        recipe['recipeYield'] = page.xpath(
            '//span[@itemprop="servingSize"]')[0].text_content().strip()
    except:
        pass
    try:
        recipe['cookTime'] = page.xpath(
            '//div[@itemprop="cookTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//div[@itemprop="prepTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//div[@itemprop="totalTime"]')[0].attrib['content'].strip()
    except:
        pass
    ingredients = page.xpath('//span[@itemprop="ingredients"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(ingredient.text_content().strip())

    if os.path.exists(recipe['file'] + ".dat"):
        data = open(recipe['file'] + ".dat", 'r').read()
        data = "{" + data.split('({')[1].split('})')[0] + "}"
        dataJSON = json.loads(data)
        print(json.dumps(dataJSON,indent=2))
        recipe['aggregateRating']['bestRating'] = '5'
        recipe['aggregateRating']['worstRating'] = '1'
        if len(dataJSON['BatchedResults']['q0']['Results']) > 0:
            recipe['aggregateRating']['ratingValue'] = dataJSON['BatchedResults'][
                'q0']['Results'][0]['ReviewStatistics']['AverageOverallRating']
            recipe['aggregateRating']['reviewCount'] = dataJSON['BatchedResults'][
                'q0']['Results'][0]['ReviewStatistics']['TotalReviewCount']


    for nutrition in recipe['nutrition']:
        try:
            recipe['nutrition'][nutrition] = page.xpath(
                '//span[@itemprop="%s"]' % nutrition)[0].text_content().strip()
        except:
            pass

    return recipe
