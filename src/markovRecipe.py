import json
import os.path

import markovify
from tqdm import tqdm

ingredientJson = json.load(open("../finished/ingredients.json", "r"))
ingredientList = []
for ingredient in ingredientJson:
    if ingredientJson[ingredient] > 100:
        ingredientList.append(ingredient)


print("Loading instructions model...")
if os.path.exists("instructions_model.json"):
    chain_json = json.load(open("instructions_model.json", "r"))
    stored_chain = markovify.Chain.from_json(chain_json)
    instructions_model = markovify.Text.from_chain(chain_json)
else:
    # Get raw text as string.
    with open("../finished/instructions.txt") as f:
        text = f.read()
        instructions_model = markovify.NewlineText(text)
        with open("instructions_model.json", "w") as f:
            f.write(json.dumps(instructions_model.chain.to_json()))


print("Loading title model...")
if os.path.exists("title_model.json"):
    chain_json = json.load(open("title_model.json", "r"))
    stored_chain = markovify.Chain.from_json(chain_json)
    title_model = markovify.Text.from_chain(chain_json)
else:
    # Get raw text as string.
    with open("../finished/titles.txt") as f:
        text = f.read()
        title_model = markovify.NewlineText(text)
        with open("title_model.json", "w") as f:
            f.write(json.dumps(title_model.chain.to_json()))


print("Loading ingredients model...")
if os.path.exists("ingredients_model.json"):
    chain_json = json.load(open("ingredients_model.json", "r"))
    stored_chain = markovify.Chain.from_json(chain_json)
    ingredients_model = markovify.Text.from_chain(chain_json)
else:
    # Get raw text as string.
    with open("../finished/ingredients.txt") as f:
        text = f.read()
        ingredients_model = markovify.NewlineText(text)
        with open("ingredients_model.json", "w") as f:
            f.write(json.dumps(ingredients_model.chain.to_json()))


def getIngredient(ing=""):
    sentence = ""
    if ing == "":
        sentence = ingredients_model.make_sentence(tries=1).lower()
    else:
        while ing not in sentence:
            sentence = ingredients_model.make_sentence(tries=1).lower()
    return sentence


def getInstruction(ing=""):
    sentence = ""
    if ing == "":
        sentence = instructions_model.make_sentence(tries=1).lower()
    else:
        while ing not in sentence:
            sentence = instructions_model.make_sentence(tries=1).lower()
    return sentence


def getTitle():
    sentence = title_model.make_sentence(tries=1).lower()
    return sentence


def hasIngredients(sentence):
    words = sentence.split()
    recipeIngredients = []
    for ingredient in ingredientList:
        if ingredient in words or ingredient + "s" in words:
            recipeIngredients.append(ingredient)
    return recipeIngredients

print("Generating titles...")
with open("markov_titles.txt", "w") as f:
    for i in tqdm(range(1000)):
        f.write(getTitle() + "\n")

print("Generating ingredients...")
with open("markov_ingredients.txt", "w") as f:
    for i in tqdm(range(1000)):
        f.write(getIngredient() + "\n")

print("Generating instructions...")
with open("markov_instructions.txt", "w") as f:
    for i in tqdm(range(1000)):
        f.write(getInstruction() + "\n")

# print("Generating recipe...")
# fullIngredients = []
#
#
# foo = getTitle()
# mainIngredient = hasIngredients(foo)
# print(foo, mainIngredient)
# fullIngredients += mainIngredient
#
# for ingredient in mainIngredient:
#     foo = getInstruction(ing=ingredient)
#     directionIngredients = hasIngredients(foo)
#     print(foo, directionIngredients)
#     fullIngredients += directionIngredients
#
# fullIngredients = list(set(fullIngredients))
# for ingredient in fullIngredients:
#     print(getIngredient(ingredient))
