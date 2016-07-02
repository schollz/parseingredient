def cooks_com(page, recipe):
    try:
        recipeInstructions = page.xpath(
            '//div[@class="instructions"]')
    except:
        return
    # recipe['datePublished'] = page.xpath(
    #     '//meta[@itemprop="datePublished"]')[0].attrib['content'].strip()
    try:
        recipe['isBasedOnUrl'] = page.xpath(
            '//input[@rel="shorturl"]')[0].attrib['value'].strip()
        recipe['author'] = page.xpath(
            '//meta[@name="author"]')[0].attrib['content'].strip()
        recipe['name'] = page.xpath(
            '//title')[0].text_content().strip()
    except:
        pass
    # recipe['description'] = page.xpath(
    #     '//meta[@name="description"]')[0].attrib['content'].strip()

    # try:
    #     recipe['recipeCuisine'] = page.xpath(
    #         '//a[@itemprop="recipeCuisine"]')[0].text_content().strip()
    # except:
    #     pass
    #
    # try:
    #     recipe['recipeCategory'] = page.xpath(
    #         '//a[@itemprop="recipeCategory"]')[0].text_content().strip()
    # except:
    #     pass

    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    try:
        recipe['recipeYield'] = page.xpath(
            '//dd[@itemprop="recipeYield"]')[0].text_content().strip()
    except:
        pass
    try:
        recipe['cookTime'] = page.xpath(
            '//time[@itemprop="cookTime"]')[0].attrib['datetime'].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//dd[@class="active-time"]')[0].text_content()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//dd[@class="total-time"]')[0].text_content()
    except:
        pass
    ingredients = page.xpath(
        '//span[@class="ingredient"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(ingredient.text_content().strip())
    try:
        recipe['aggregateRating']['ratingValue'] = page.xpath(
            '//span[@class="rating"]/span[@class="value-title"]')[0].attrib['title'].strip()
    except:
        pass
    try:
        recipe['aggregateRating']['reviewCount'] = page.xpath(
            '//span[@class="count"]/span[@class="value-title"]')[0].attrib['title'].strip()
        recipe['aggregateRating']['bestRating'] = '5'
        recipe['aggregateRating']['worstRating'] = '1'
    except:
        pass
    for nutrition in recipe['nutrition']:
        try:
            recipe['nutrition'][nutrition] = page.xpath(
                '//li[@class="nutrientLine__item--amount" and @itemprop="%s"]' % nutrition)[0].text_content()
        except:
            pass
