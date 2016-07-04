import json
from collections import defaultdict


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


def fixName(name):
    newName = ""
    name = name.lower()
    name = name.replace('raw', '')
    names = name.split(',')
    for name in names[::-1]:
        if "with" not in name:
            newName += name + " "
    for name in names[::-1]:
        if "with" in name:
            newName += name + " "
    return ' '.join(newName.split())

foodDes = open('FOOD_DES.txt', 'r', encoding="ISO-8859-1").read().split("\n")
sr = recursive_defaultdict()
for line in foodDes:
    try:
        data = line.split('~^~')
        sr[data[0][1:]]['long_desc'] = fixName(data[2])
        sr[data[0][1:]]['shrt_desc'] = fixName(data[3])
    except:
        pass

foodWeight = open('WEIGHT.txt', 'r', encoding="ISO-8859-1").read().split("\n")
for line in foodWeight:
    data = line.split('^')
    dataId = data[0][1:-1]
    weight = recursive_defaultdict()
    try:
        weight["qty"] = float(data[2])
    except:
        continue
    weight["unit"] = data[3][1:-1]
    weight["g"] = float(data[4])
    if 'weight' not in sr[dataId]:
        sr[dataId]['weight'] = []
    sr[dataId]['weight'].append(weight)

with open('sr28.json', 'w') as f:
    f.write(json.dumps(sr, indent=2))
