import json


def chowhound_com(page, recipe):
    # recipe['datePublished'] = page.xpath(
    #     '//meta[@itemprop="dateCreated"]')[0].attrib['content'].strip()
    for page2 in page.xpath('//a[@rel="nofollow"]'):
        if 'data-sharetitle' in page2.attrib:
            recipe['name'] = page2.attrib['data-sharetitle']
        if 'data-sharedescription' in page2.attrib:
            recipe['description'] = page2.attrib['data-sharedescription']
        if 'data-shareurl' in page2.attrib:
            recipe['isBasedOnUrl'] = page2.attrib['data-shareurl']
    try:
        recipe['description'] = ' '.join(page.xpath(
            '//div[@itemprop="description"]/p')[0].text_content().split())
    except:
        pass
    recipe['author'] = page.xpath(
        '//span[@itemprop="author"]')[0].text_content().strip()
    recipeInstructions = page.xpath(
        '//div[@itemprop="recipeInstructions"]/ol/li')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = ' '.join(instruction.text_content().strip().split())
        if len(data) > 0:
            recipe['recipeInstructions'].append(data[1:])
    recipe['recipeYield'] = page.xpath(
        '//span[@itemprop="recipeYield"]')[0].text_content().strip()
    try:
        recipe['cookTime'] = page.xpath(
            '//time[@itemprop="cookTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//time[@itemprop="prepTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//time[@itemprop="totalTime"]')[0].attrib['content'].strip()
    except:
        pass
    ingredients = page.xpath('//li[@itemprop="ingredients"]')
    for ingredient in ingredients:
        ingredientText = ingredient.text_content().strip()
        if len(ingredientText) > 0:
            recipe['recipeIngredient'].append(ingredientText)
    try:
        recipe['aggregateRating']['ratingValue'] = page.xpath(
            '//span[@itemprop="ratingValue"]')[0].text_content().strip()
        recipe['aggregateRating']['reviewCount'] = page.xpath(
            '//span[@itemprop="reviewCount"]')[0].text_content().strip()
        recipe['aggregateRating']['bestRating'] = '5'
        recipe['aggregateRating']['worstRating'] = '0'
    except:
        pass
    # for nutrition in recipe['nutrition']:
    #     try:
    #         recipe['nutrition'][nutrition] = page.xpath(
    #             '//meta[@itemprop="%s"]' % nutrition)[0].attrib['content'].strip()
    #     except:
    #         pass

    return recipe
