def allrecipes_com(page, recipe):
    try:
        recipe['datePublished'] = page.xpath(
            '//meta[@itemprop="dateCreated"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['isBasedOnUrl'] = page.xpath(
            '//link[@id="canonicalUrl"]')[0].attrib['href'].strip()
    except:
        pass
    try:
        recipe['author'] = page.xpath(
            '//span[@class="submitter__name"]')[0].text_content().strip()
    except:
        pass
    try:
        recipe['name'] = page.xpath(
            '//meta[@property="og:title"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['description'] = page.xpath(
            '//div[@class="submitter__description"]')[0].text_content().strip().replace('"', '')
    except:
        pass
    try:
        recipeInstructions = page.xpath(
            '//span[@class="recipe-directions__list--item"]')
    except:
        return
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    recipe['recipeYield'] = page.xpath(
        '//meta[@id="metaRecipeServings" and @itemprop="recipeYield"]')[0].attrib['content'].strip()
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
        recipe['recipeIngredient'].append(ingredient.text_content().strip())
    recipe['aggregateRating']['ratingValue'] = page.xpath(
        '//meta[@itemprop="ratingValue"]')[0].attrib['content'].strip()
    recipe['aggregateRating']['reviewCount'] = page.xpath(
        '//meta[@itemprop="reviewCount"]')[0].attrib['content'].strip()
    recipe['aggregateRating']['bestRating'] = '5'
    recipe['aggregateRating']['worstRating'] = '1'
    for nutrition in recipe['nutrition']:
        try:
            recipe['nutrition'][nutrition] = page.xpath(
                '//li[@class="nutrientLine__item--amount" and @itemprop="%s"]' % nutrition)[0].text_content()
        except:
            pass

    return recipe
