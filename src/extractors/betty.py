def bettycrocker_com(page, recipe):
    # recipe['datePublished'] = page.xpath(
    #     '//meta[@itemprop="dateCreated"]')[0].attrib['content'].strip()
    try:
        recipe['isBasedOnUrl'] = page.xpath(
            '//link[@rel="canonical"]')[0].attrib['href'].strip()
    except:
        pass
    # recipe['author'] = page.xpath(
    #     '//span[@class="submitter__name"]')[0].text_content().strip()
    try:
        recipe['name'] = page.xpath(
            '//meta[@property="og:title"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipe['description'] = page.xpath(
            '//meta[@property="og:description"]')[0].attrib['content'].strip()
    except:
        pass
    try:
        recipeInstructions = page.xpath(
            '//span[@class="recipePartStepDescription"]')
    except:
        return
    recipe['recipeInstructions'] = []
    for instruction in recipeInstructions:
        data = instruction.text_content().strip()
        if len(data) > 0:
            recipe['recipeInstructions'].append(data)
    recipe['recipeYield'] = page.xpath(
        '//meta[@itemprop="recipeYield"]')[0].attrib['content'].strip()
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
    ingredients = page.xpath('//dl[@itemprop="ingredients"]')
    for ingredient in ingredients:
        recipe['recipeIngredient'].append(
            ' '.join(ingredient.text_content().strip().split()))
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
