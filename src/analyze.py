import json
import os

from tqdm import tqdm


os.chdir('../finished')
# print("Generating index of files...")
# os.system("tree -Ufai -P '*.json.it' -I '*.it.it' -o finished.index")

print("Opening file index...")
fs = open('finished.index', 'r').read().split('\n')

print("Analyzing...")
finstructions = open('instructions.txt', 'w')
fingredients = open('ingredients.txt', 'w')
ftitles = open('titles.txt', 'w')
fingredistlist = open('ingredientList.txt','w')
for i in tqdm(range(0, len(fs))):
    f = fs[i]
    j = {}
    try:
        j = json.load(open(f, "r"))
    except:
        continue

    try:
        for instruction in j['recipeInstructions']:
            finstructions.write(instruction.strip().lower() + "\n")
    except:
        pass
    try:
        for ingredient in j['recipeIngredient']:
            fingredients.write(ingredient.strip().lower() + "\n")
    except:
        pass
    try:
        ftitles.write(j['name'].lower() + "\n")
    except:
        pass

    if ".json.it" not in f or 'recipeIngredientTagged' not in j:
        continue
    for i in range(len(j['recipeIngredientTagged'])):
        try:
            newIngredient = j['recipeIngredientTagged'][i][
                'name'].lower().replace(')', '').replace('(', '')
            fingredistlist.write(newIngredient + "\n")
        except:
            pass

finstructions.close()
fingredients.close()
ftitles.close()
fingredistlist.close()
