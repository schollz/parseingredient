import json
import os.path

import markovify

ingredientList = json.load(open("../finished/ingredients.json", "r"))


def getIngredient(ing):
    # Build the model.
    if os.path.exists("ingredients_model.json"):
        chain_json = json.load(open("ingredients_model.json", "r"))
        stored_chain = markovify.Chain.from_json(chain_json)
        text_model = markovify.Text.from_chain(chain_json)
    else:
        # Get raw text as string.
        with open("../finished/ingredients.txt") as f:
            text = f.read()
            text_model = markovify.NewlineText(text)
            with open("ingredients_model.json", "w") as f:
                f.write(json.dumps(text_model.chain.to_json()))
    sentence = ""
    while ing not in sentence:
        sentence = text_model.make_sentence().lower()
    print(sentence)


def getInstruction():
    # Build the model.
    if os.path.exists("instructions_model.json"):
        chain_json = json.load(open("instructions_model.json", "r"))
        stored_chain = markovify.Chain.from_json(chain_json)
        text_model = markovify.Text.from_chain(chain_json)
    else:
        # Get raw text as string.
        with open("../finished/instructions.txt") as f:
            text = f.read()
            text_model = markovify.NewlineText(text)
            with open("instructions_model.json", "w") as f:
                f.write(json.dumps(text_model.chain.to_json()))
    sentence = text_model.make_sentence().lower()
    return sentence


def getTitle():
    # Build the model.
    if os.path.exists("title_model.json"):
        chain_json = json.load(open("title_model.json", "r"))
        stored_chain = markovify.Chain.from_json(chain_json)
        text_model = markovify.Text.from_chain(chain_json)
    else:
        # Get raw text as string.
        with open("../finished/titles.txt") as f:
            text = f.read()
            text_model = markovify.NewlineText(text)
            with open("title_model.json", "w") as f:
                f.write(json.dumps(text_model.chain.to_json()))
    sentence = text_model.make_sentence().lower()
    return sentence


def hasIngredients(sentence):
    words = sentence.split()
    recipeIngredients = []
    for ingredient in ingredientList:
        if ingredient in words:
            recipeIngredients.append(ingredient)
    return recipeIngredients

foo = getTitle()
print(foo, hasIngredients(foo))

foo = getInstruction()
print(foo, hasIngredients(foo))
