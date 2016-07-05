import json
import os

from tqdm import tqdm


os.chdir('../finished')
print("Generating index of files...")
os.system("tree -Ufai -P '*.json.it' -I '*.it.it' -o finished.index")

print("Opening file index...")
fs = open('finished.index', 'r').read().split('\n')

print("Analyzing...")
numberWithScores = 0
ingredientList = set()
for i in tqdm(range(0, len(fs), 500)):
    f = fs[i]
    try:
        j = json.load(open(f, "r"))
    except:
        pass
    for ingredient in j['recipeIngredientTagged']:
        ingredientList.update(ingredient['name'])
    numberWithScores += int(j['aggregateRating']['ratingValue'] !=
                            None and float(j['aggregateRating']['ratingValue']) > 0)
print("%2.1f%% have scores" % float(
    100.0 * float(numberWithScores) / float(len(list(range(0, len(fs), 500))))))
print("%d total" % len(fs))
with open('ingredients.json', 'w') as f:
    f.write(json.dumps(list(ingredientList), indent=2))
