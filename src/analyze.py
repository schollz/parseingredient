import json
import os

from tqdm import tqdm

mypath = "../finished"
fs = []
for root, directories, filenames in os.walk(mypath):
    for filename in filenames:
        fs.append(os.path.join(root, filename))

numberWithScores = 0
for i in tqdm(range(0,len(fs),500)):
    f = fs[i]
    j = json.load(open(f, "r"))
    numberWithScores += int(j['aggregateRating']['ratingValue'] !=
                            None and float(j['aggregateRating']['ratingValue']) > 0)
print("%2.1f%% have scores" % float(100.0 * float(numberWithScores) / float(len(list(range(0,len(fs),500))))))
print("%d total" % len(fs))
