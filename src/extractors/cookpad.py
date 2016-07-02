def cookpad_com(page, recipe):
    try:
        recipe['datePublished'] = page.xpath(
            '//time[@itemprop="datePublished"]')[0].attrib['datetime'].strip()
    except:
        pass
    try:
        recipe['isBasedOnUrl'] = page.xpath(
            '//link[@rel="canonical"]')[0].attrib['href'].strip()
    except:
        pass
    try:
        recipe['author'] = page.xpath(
            '//span[@itemprop="author"]')[0].text_content().strip()
    except:
        pass
    try:
        recipe['name'] = page.xpath(
            '//meta[@property="og:title"]')[0].attrib['content'].split('by ')[0].strip()
    except:
        pass
    try:
        recipe['description'] = page.xpath(
            '//meta[@name="description"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipeInstructions = page.xpath(
            '//p[@class="step__text"]')
    except:
        return
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    try:
        recipe['recipeYield'] = page.xpath(
            '//meta[@itemprop="recipeYield"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['cookTime'] = page.xpath(
            '//meta[@itemprop="cookTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['prepTime'] = page.xpath(
            '//meta[@itemprop="prepTime"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['totalTime'] = page.xpath(
            '//meta[@itemprop="totalTime"]')[0].attrib['content'].strip()
    except:
        pass
    ingredients = page.xpath('//div[@itemprop="ingredients"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(
            ' '.join(ingredient.text_content().strip().split()))
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
