import json
import os.path
import copy

def taste_com_au(page, recipe):
	try:
		jsonText = page.xpath('//script[@type="application/ld+json"]')[0].text_content()
	except:
		return recipe
	data = json.loads(jsonText)
	for key in data.keys():
		recipe[key] = copy.deepcopy(data[key])
	recipe['author'] = data['author']['name']
	try:
		recipe.pop('image',None)
	except:
		pass
	try:
		recipe.pop('url',None)
	except:
		pass
	recipe['aggregateRating']['bestRating'] = '5'
	recipe['aggregateRating']['worstRating'] = '1'
	recipe['isBasedOnUrl'] = data['url']

	for key in recipe['nutrition'].keys():
		text = recipe['nutrition'][key]
		try:
			text = recipe['nutrition'][key].split(": ")[1]
		except:
			pass
		recipe['nutrition'][key] = text
	return recipe

