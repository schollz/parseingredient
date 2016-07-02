def yummly_com(page, recipe):
    # recipe['datePublished'] = page.xpath(
    #     '//time[@itemprop="datePublished"]')[0].attrib['datetime'].strip()
    recipe['isBasedOnUrl'] = page.xpath(
        '//link[@rel="alternate"]')[0].attrib['href'].strip()
    # recipe['author'] = page.xpath(
    #     '//span[@itemprop="author"]')[0].text_content().strip()
    recipe['name'] = page.xpath(
        '//meta[@property="og:title"]')[0].attrib['content'].strip()
    recipe['description'] = page.xpath(
        '//meta[@name="description"]')[0].attrib['content'].strip()
    # recipeInstructions = page.xpath(
    #     '//div[@itemprop="recipeInstructions"]/p')
    recipe['recipeInstructions'] = []
    # for instruction in recipeInstructions:
    #     data = instruction.text_content().strip().replace('Step ', '')
    #     if len(data) > 1:
    #         recipe['recipeInstructions'].append(data[1:])
    recipe['recipeYield'] = page.xpath(
        '//p[@itemprop="recipeYield"]')[0].text_content().strip()
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
    ingredients = page.xpath('//li[@itemprop="ingredients"]')
    for ingredient in ingredients:
        ingredientText = ' '.join(ingredient.text_content().strip().split())
        recipe['recipeIngredient'].append(ingredientText)
    try:
        recipe['aggregateRating']['ratingValue'] = page.xpath(
            '//meta[@itemprop="ratingValue"]')[0].attrib['content'].strip()
        recipe['aggregateRating']['reviewCount'] = page.xpath(
            '//meta[@itemprop="reviewCount"]')[0].attrib['content'].strip()
        recipe['aggregateRating']['bestRating'] = '5'
        recipe['aggregateRating']['worstRating'] = '1'
    except:
        pass
    recipe['nutrition']['calories'] = page.xpath(
        '//li[@class="nutrition-data"]/span[@class="bd"]')[0].text_content().strip()

    return recipe
