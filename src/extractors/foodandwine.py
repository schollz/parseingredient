def foodandwine_com(page, recipe):
    recipe['datePublished'] = page.xpath(
        '//span[@class="published_date"]')[0].text_content().strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@rel="canonical"]')[0].attrib['href'].strip()
    recipe['author'] = page.xpath(
        '//span[@class="slide_authors"]')[0].text_content().strip()
    recipe['name'] = page.xpath(
        '//meta[@property="og:title"]')[0].attrib['content'].strip()
    recipe['description'] = page.xpath(
        '//meta[@name="description"]')[0].attrib['content'].strip()
    recipeInstructions = page.xpath(
        '//span[@class="steps-list__item__text"]')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    recipe['recipeYield'] = page.xpath(
        '//span[@itemprop="recipeYield"]')[0].text_content().strip()
    try:
        recipe['cookTime'] = page.xpath(
            '//time[@itemprop="cookTime"]')[0].attrib['datetime'].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//time[@itemprop="prepTime"]')[0].attrib['datetime'].strip()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//time[@itemprop="totalTime"]')[0].attrib['datetime'].strip()
    except:
        pass
    ingredients = page.xpath('//span[@itemprop="ingredients"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(
            ingredient.text_content().strip())
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
