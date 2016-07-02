def epicurious_com(page, recipe):
    recipe['datePublished'] = page.xpath(
        '//meta[@itemprop="datePublished"]')[0].attrib['content'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@rel="canonical"]')[0].attrib['href'].strip()
    recipe['author'] = page.xpath(
        '//meta[@itemprop="author"]')[0].attrib['content'].strip()
    recipe['name'] = page.xpath(
        '//meta[@itemprop="name"]')[0].attrib['content'].strip()
    recipe['description'] = page.xpath(
        '//meta[@name="description"]')[0].attrib['content'].strip()

    try:
        recipe['recipeCuisine'] = page.xpath(
            '//a[@itemprop="recipeCuisine"]')[0].text_content().strip()
    except:
        pass

    try:
        recipe['recipeCategory'] = page.xpath(
            '//a[@itemprop="recipeCategory"]')[0].text_content().strip()
    except:
        pass

    recipeInstructions = page.xpath(
        '//li[@class="preparation-step"]')
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
        '//li[@class="ingredient" and @itemprop="ingredients"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(ingredient.text_content().strip())
    recipe['aggregateRating']['ratingValue'] = page.xpath(
        '//meta[@itemprop="ratingValue"]')[0].attrib['content'].strip()
    recipe['aggregateRating']['reviewCount'] = page.xpath(
        '//span[@itemprop="reviewCount"]')[0].text_content()
    recipe['aggregateRating']['bestRating'] = page.xpath(
        '//meta[@itemprop="bestRating"]')[0].attrib['content'].strip()
    for nutrition in recipe['nutrition']:
        try:
            recipe['nutrition'][nutrition] = page.xpath(
                '//li[@class="nutrientLine__item--amount" and @itemprop="%s"]' % nutrition)[0].text_content()
        except:
            pass
