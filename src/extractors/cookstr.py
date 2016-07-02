def cookstr_com(page, recipe):
    recipe['datePublished'] = page.xpath(
        '//meta[@itemprop="datePublished"]')[0].attrib['content'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@rel="canonical"]')[0].attrib['href'].strip()
    try:
        recipe['author'] = page.xpath(
            '//div[@class="userAndPublicationDiv"]/h5')[0].text_content().replace('By ', '').strip()
    except:
        pass
    recipe['name'] = page.xpath(
        '//meta[@property="og:title"]')[0].attrib['content'].strip()
    try:
        recipe['description'] = page.xpath(
            '//p[@itemprop="description"]')[0].text_content().strip()
    except:
        pass
    recipeInstructions = page.xpath(
        '//div[@class="cells"]/div')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    try:
        recipe['recipeYield'] = page.xpath(
            '//span[@itemprop="recipeYield"]')[0].text_content().strip()
    except:
        pass
    # try:
    #     recipe['cookTime'] = page.xpath(
    #         '//meta[@itemprop="cookTime"]')[0].attrib['content'].strip()
    # except:
    #     pass
    # try:
    #     recipe['prepTime'] = page.xpath(
    #         '//meta[@itemprop="prepTime"]')[0].attrib['content'].strip()
    # except:
    #     pass
    try:
        for attr in page.xpath('//span[@class="attrLabel"]'):
            attrText = attr.text_content()
            if 'Total Time' in attrText:
                recipe['totalTime'] = attrText.replace(
                    'Total Time', '').strip()
    except:
        pass
    ingredients = page.xpath('//span[@itemprop="recipeIngredient"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(
            ' '.join(ingredient.text_content().strip().split()))
    # try:
    #     recipe['aggregateRating']['ratingValue'] = page.xpath(
    #         '//span[@itemprop="ratingValue"]')[0].text_content().strip()
    #     recipe['aggregateRating']['reviewCount'] = page.xpath(
    #         '//span[@itemprop="ratingCount"]')[0].text_content().strip()
    #     recipe['aggregateRating']['bestRating'] = '5'
    #     recipe['aggregateRating']['worstRating'] = '1'
    # except:
    #     pass
    # for nutrition in recipe['nutrition']:
    #     try:
    #         recipe['nutrition'][nutrition] = page.xpath(
    #             '//span[@itemprop="%s"]' % nutrition)[0].text_content().strip()
    #     except:
    #         pass

    return recipe
