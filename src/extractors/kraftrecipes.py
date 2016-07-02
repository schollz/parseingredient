def kraftrecipes_com(page, recipe):
    # recipe['datePublished'] = page.xpath(
    #     '//meta[@itemprop="dateCreated"]')[0].attrib['content'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@rel="canonical"]')[0].attrib['href'].strip()
    recipe['author'] = page.xpath(
        '//span[@itemprop="author"]')[0].text_content().strip()
    recipe['name'] = page.xpath(
        '//meta[@name="title"]')[0].attrib['content'].strip()
    recipe['description'] = page.xpath(
        '//meta[@name="description"]')[0].attrib['content'].strip()
    recipeInstructions = page.xpath(
        '//ul[@itemprop="recipeInstructions"]/li/div')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    recipe['recipeYield'] = page.xpath(
        '//span[@itemprop="servingSize"]')[0].text_content().strip()
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
    try:
        recipe['aggregateRating']['ratingValue'] = page.xpath(
            '//meta[@itemprop="ratingValue"]')[0].attrib['content'].strip()
        recipe['aggregateRating']['reviewCount'] = page.xpath(
            '//meta[@itemprop="reviewCount"]')[0].attrib['content'].strip()
        recipe['aggregateRating']['bestRating'] = '5'
        recipe['aggregateRating']['worstRating'] = '1'
    except:
        pass
    for nutrition in recipe['nutrition']:
        try:
            recipe['nutrition'][nutrition] = page.xpath(
                '//meta[@itemprop="%s"]' % nutrition)[0].attrib['content'].strip()
        except:
            pass

    return recipe
