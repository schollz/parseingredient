import json
import os.path

import markovify


def getIngredient(ing):
	# Build the model.
	if os.path.exists("ingredients_model.json"):
		chain_json = json.load(open("ingredients_model.json","r"))
		stored_chain = markovify.Chain.from_json(chain_json)
		text_model = markovify.Text.from_chain(chain_json)
	else:
		# Get raw text as string.
		with open("ingredients.txt") as f:
			text = f.read()
			text_model = markovify.NewlineText(text)
			with open("ingredients_model.json","w") as f:
				f.write(json.dumps(text_model.chain.to_json()))
	sentence = ""
	while ing not in sentence:
	    sentence = text_model.make_sentence().lower()
	print(sentence)


def getInstruction():
	# Build the model.
	if os.path.exists("instructions_model.json"):
		chain_json = json.load(open("instructions_model.json","r"))
		stored_chain = markovify.Chain.from_json(chain_json)
		text_model = markovify.Text.from_chain(chain_json)
	else:
		# Get raw text as string.
		with open("instructions.txt") as f:
			text = f.read()
			text_model = markovify.NewlineText(text)
			with open("instructions_model.json","w") as f:
				f.write(json.dumps(text_model.chain.to_json()))
	sentence = text_model.make_sentence().lower()
	print(sentence)


getInstruction()
getIngredient("chocolate")
getIngredient("beet")
