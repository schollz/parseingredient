import multiprocessing
import os
import glob
import sys
import json

from tqdm import tqdm

from extractors.default import *


def main():
    if not os.path.exists('../finished'):
        os.makedirs('../finished')
    for parser in availableParsers:
        if not os.path.exists('../finished/%s' % parser):
            os.makedirs('../finished/%s' % parser)

    mypath = sys.argv[1]
    fs = []
    if os.path.exists('files.json'):
        fs = json.load(open('files.json', 'r'))
    else:
        for root, directories, filenames in os.walk(mypath):
            for filename in filenames:
                fs.append(os.path.join(root, filename))
        with open('files.json', 'w') as f:
            f.write(json.dumps(fs))

    # # Testing purposes
    # for f in fs:
    #     print(f)
    #     parseRecipe(f)

    # Process all
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    print("Processing %d files..." % len(fs))
    for i in tqdm(range(0, len(fs), 2 * multiprocessing.cpu_count())):
        p.map(parseRecipe, fs[i:i + 2 * multiprocessing.cpu_count()])

if __name__ == "__main__":
    main()
