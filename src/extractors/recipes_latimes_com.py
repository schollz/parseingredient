def recipes_latimes_com(page, recipe):
    print(recipe['file'])
    try:
        recipe['datePublished'] = page.xpath(
            '//time[@itemprop="datePublished"]')[0].attrib['datetime'].strip()
    except:
        pass
    try:
        recipe['isBasedOnUrl'] = page.xpath(
            '//link[@rel="canonical"]')[0].attrib['href'].strip()
    except:
        return
    try:
        recipe['author'] = page.xpath(
            '//span[@itemprop="author"]')[0].text_content().strip()
    except:
        pass
    try:
        recipe['name'] = page.xpath(
            '//h1[@itemprop="name"]')[0].text_content().strip()
    except:
        return
    recipe['description'] = ' '.join(page.xpath(
        '//meta[@property="og:description"]')[0].attrib['content'].replace('Read more', '').split())
    recipeInstructions = page.xpath(
        '//div[@itemprop="recipeInstructions"]/p')
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip().replace('Step ', '')
        if len(data) > 1:
            recipe['recipeInstructions'].append(data[1:])
    # recipe['recipeYield'] = page.xpath(
    #     '//meta[@itemprop="recipeYield"]')[0].attrib['content'].strip()
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
    # try:
    #     recipe['totalTime'] = page.xpath(
    #         '//meta[@itemprop="totalTime"]')[0].attrib['content'].strip()
    # except:
    #     pass
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
