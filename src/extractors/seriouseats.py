def seriouseats_com(page, recipe):
    # recipe['datePublished'] = page.xpath(
    #     '//time[@itemprop="datePublished"]')[0].attrib['datetime'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@rel="canonical"]')[0].attrib['href'].strip()
    recipe['author'] = page.xpath(
        '//meta[@name="author"]')[0].attrib['content'].strip()
    recipe['name'] = page.xpath(
        '//meta[@property="og:title"]')[0].attrib['content'].replace('Recipe', '').strip()
    recipe['description'] = page.xpath(
        '//meta[@name="description"]')[0].attrib['content'].strip()
    recipeInstructions = page.xpath(
        '//div[@class="recipe-procedure-text"]')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 1:
            recipe['recipeInstructions'].append(data)
    # try:
    #     recipe['cookTime'] = page.xpath(
    #         '//meta[@itemprop="cookTime"]')[0].attrib['content'].strip()
    # except:
    #     pass
    try:
        recipe['recipeYield'] = page.xpath(
            '//ul[@class="recipe-about"]/li')[0].text_content().split(':')[1].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//ul[@class="recipe-about"]/li')[1].text_content().split(':')[1].strip()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//ul[@class="recipe-about"]/li')[2].text_content().split(':')[1].strip()
    except:
        pass
    ingredients = page.xpath('//li[@itemprop="ingredients"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(ingredient.text_content().strip())
    # try:
    #     recipe['aggregateRating']['ratingValue'] = page.xpath(
    #         '//meta[@itemprop="ratingValue"]')[0].attrib['content'].strip()
    #     recipe['aggregateRating']['reviewCount'] = page.xpath(
    #         '//meta[@itemprop="reviewCount"]')[0].attrib['content'].strip()
    #     recipe['aggregateRating']['bestRating'] = '5'
    #     recipe['aggregateRating']['worstRating'] = '1'
    # except:
    #     pass
    # for nutrition in recipe['nutrition']:
    #     try:
    #         recipe['nutrition'][nutrition] = page.xpath(
    #             '//meta[@itemprop="%s"]' % nutrition)[0].attrib['content'].strip()
    #     except:
    #         pass

    return recipe
