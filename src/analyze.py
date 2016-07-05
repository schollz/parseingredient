import json
import os

from tqdm import tqdm


os.chdir('../finished')
# print("Generating index of files...")
# os.system("tree -Ufai -P '*.json.*' -I '*.it.it' -o finished.index")

print("Opening file index...")
fs = open('finished.index', 'r').read().split('\n')

print("Analyzing...")
numberWithScores = 0
ingredientList = set()
finstructions = open('instructions.txt', 'w')
fingredients = open('ingredients.txt', 'w')
ftitles = open('titles.txt', 'w')
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

    if ".json.it" not in f:
        continue
    for i in range(len(j['recipeIngredientTagged'])):
        try:
            ingredientList.update(
                [j['recipeIngredientTagged'][i]['name'].lower().replace(')', '').replace('(', '')])
        except:
            pass
    numberWithScores += int(j['aggregateRating']['ratingValue'] !=
                            None and float(j['aggregateRating']['ratingValue']) > 0)
finstructions.close()
fingredients.close()
print("%2.1f%% have scores" % float(
    100.0 * float(numberWithScores) / float(len(list(range(0, len(fs), 500))))))
print("%d total" % len(fs))
with open('ingredients.json', 'w') as f:
    f.write(json.dumps(list(ingredientList), indent=2))
