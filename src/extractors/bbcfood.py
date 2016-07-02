def bbc_co_uk_food(page, recipe):
    # recipe['datePublished'] = page.xpath(
    #     '//meta[@itemprop="dateCreated"]')[0].attrib['content'].strip()
    # recipe['isBasedOnUrl'] = page.xpath(
    #     '//link[@id="canonicalUrl"]')[0].attrib['href'].strip()
    try:
        recipe['author'] = page.xpath(
            '//a[@itemprop="author"]')[0].text_content().strip()
    except:
        pass
    try:
        recipe['name'] = page.xpath(
            '//meta[@name="twitter:title"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['description'] = page.xpath(
            '//meta[@name="twitter:description"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipeInstructions = page.xpath(
            '//p[@class="recipe-method__list-item-text"]')
    except:
        return
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    recipe['recipeYield'] = page.xpath(
        '//p[@class="recipe-metadata__serving" and @itemprop="recipeYield"]')[0].text_content().strip()
    try:
        recipe['cookTime'] = page.xpath(
            '//p[@itemprop="cookTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//p[@itemprop="prepTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//p[@itemprop="totalTime"]')[0].attrib['content'].strip()
    except:
        pass
    ingredients = page.xpath('//li[@class="recipe-ingredients__list-item"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(ingredient.text_content().strip())
    # recipe['aggregateRating']['ratingValue'] = page.xpath(
    #     '//meta[@itemprop="ratingValue"]')[0].attrib['content'].strip()
    # recipe['aggregateRating']['reviewCount'] = page.xpath(
    #     '//meta[@itemprop="reviewCount"]')[0].attrib['content'].strip()
    # recipe['aggregateRating']['bestRating'] = '5'
    # for nutrition in recipe['nutrition']:
    #     try:
    #         recipe['nutrition'][nutrition] = page.xpath(
    #             '//li[@class="nutrientLine__item--amount" and @itemprop="%s"]' % nutrition)[0].text_content()
    #     except:
    #         pass

    return recipe
