import json
import os.path
import operator
import time
from multiprocessing import Pool

import markovify
from tqdm import tqdm

removeWords = ['c', 'tsp', 'qt', 'lb', 'pkg', 'oz', 'med', 'tbsp', 'sm']

ingredients = {}
if not os.path.exists("ingredients.json"):
    print("Generating ingredient list...")
    ingredientList = open("../finished/ingredientList.txt",
                          "r").read().split("\n")
    for ingredient in ingredientList:
        for removeWord in removeWords:
            ingredient = ingredient.replace(removeWord + '. ', '')
        ingredient = ingredient.replace(' *', '')
        try:
            num = int(ingredient[0])
            ingredient = ' '.join(ingredient.split()[1:])
        except:
            pass
        try:
            num = int(ingredient[0])
            ingredient = ' '.join(ingredient.split()[1:])
        except:
            pass
        if ingredient == 'pepper' or ingredient == 'cup' or len(ingredient) <= 2 or 'salt' == ingredient[0:4] or 'black pepper' in ingredient:
            continue
        if ingredient not in ingredients:
            ingredients[ingredient] = 0
        ingredients[ingredient] += 1
    with open("ingredients.json", "w") as f:
        f.write(json.dumps(ingredients, indent=2))
else:
    print("Loading ingredient list...")
    ingredients = json.load(open("ingredients.json", "r"))
# sortedIngredients = sorted(
#     ingredients.items(), key=operator.itemgetter(1), reverse=True)
# for i in range(1000):
#     print(sortedIngredients[i])

if os.path.exists("instructions_model.json"):
    print("Loading instructions model...")
    chain_json = json.load(open("instructions_model.json", "r"))
    stored_chain = markovify.Chain.from_json(chain_json)
    instructions_model = markovify.Text.from_chain(chain_json)
else:
    print("Generating instructions model...")
    with open("../finished/instructions.txt") as f:
        text = f.read()
        instructions_model = markovify.NewlineText(text, state_size=3)
        with open("instructions_model.json", "w") as f:
            f.write(json.dumps(instructions_model.chain.to_json()))


if os.path.exists("title_model.json"):
    print("Loading title model...")
    chain_json = json.load(open("title_model.json", "r"))
    stored_chain = markovify.Chain.from_json(chain_json)
    title_model = markovify.Text.from_chain(chain_json)
else:
    print("Generaring title model...")
    with open("../finished/titles.txt") as f:
        text = f.read()
        title_model = markovify.NewlineText(text)
        with open("title_model.json", "w") as f:
            f.write(json.dumps(title_model.chain.to_json()))


if os.path.exists("ingredients_model.json"):
    print("Loading ingredients model...")
    chain_json = json.load(open("ingredients_model.json", "r"))
    stored_chain = markovify.Chain.from_json(chain_json)
    ingredients_model = markovify.Text.from_chain(chain_json)
else:
    print("Generaring ingredients model...")
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
        tries = 0
        while ing not in sentence:
            sentence = ingredients_model.make_sentence(tries=1).lower()
            tries += 1
            if tries > 100:
                break
    return sentence


def getInstruction(ing=""):
    sentence = ""
    if ing == "":
        sentence = instructions_model.make_sentence(tries=1).lower()
    else:
        tries = 0
        while ing not in sentence:
            sentence = instructions_model.make_sentence(tries=1).lower()
            tries += 1
            if tries > 100:
                break
    return sentence


def getTitle(num):
    sentence = title_model.make_sentence(tries=1, max_overlap_ratio=1)
    return sentence


def hasIngredients(sentence):
    try:
        words = sentence.replace('.', '').replace(
            ':', '').replace(',', '').split()
    except:
        return []
    recipeIngredients = []
    for ingredient in ingredients.keys():
        if ingredients[ingredient] < 50:
            continue
        if ingredient in words or ingredient + "s" in words:
            recipeIngredients.append(ingredient)
    return recipeIngredients

print("Generating titles...")
t = time.time()
with open("markov_titles.txt", "w") as f:
    for i in tqdm(range(100)):
        f.write(getTitle(i) + "\n")
print((time.time() - t) / 100.0)

# t = time.time()
# p = Pool(8)
# p.map(getTitle, range(500))
# print((time.time() - t) / 500.0)


print("Generating ingredients...")
t = time.time()
with open("markov_titles.txt", "w") as f:
    for i in tqdm(range(100)):
        f.write(getIngredient() + "\n")
print((time.time() - t) / 100.0)

print("Generating instrutions...")
t = time.time()
with open("markov_titles.txt", "w") as f:
    for i in tqdm(range(100)):
        f.write(getInstruction() + "\n")
print((time.time() - t) / 100.0)


def generateRecipe():
    recipe = {}
    print("Generating recipe...")
    recipe['ingredients'] = []
    recipe['title'] = getTitle(1)
    recipe['title_ingredients'] = hasIngredients(recipe['title'])
    recipe['ingredients'] += recipe['title_ingredients']
    recipe['directions'] = []
    recipe['direction_ingredients'] = []
    print("Getting directions")
    for ingredient in recipe['title_ingredients']:
        print(ingredient)
        instruct = getInstruction(ing=ingredient)
        ings = hasIngredients(instruct)
        recipe['ingredients'] += ings
        recipe['direction_ingredients'].append(ings)
        recipe['directions'].append(instruct)
    recipe['ingredients'] = list(set(recipe['ingredients']))
    recipe['ingredientList'] = []
    print("Getting ingredients")
    for ingredient in recipe['ingredients']:
        print(ingredient)
        recipe['ingredientList'].append(getIngredient(ingredient))
    print(json.dumps(recipe, indent=2))
    print("\n\n" + recipe['title'] + "\n\n" + "\n".join(recipe['ingredientList']
                                                        ) + "\n\n" + "\n".join(recipe['directions']))

# generateRecipe()
