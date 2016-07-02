import multiprocessing
import os
import glob

from tqdm import tqdm

from extractors.default import *


def main():
    if not os.path.exists('../finished'):
        os.makedirs('../finished')
    for parser in availableParsers:
        if not os.path.exists('../finished/%s' % parser):
            os.makedirs('../finished/%s' % parser)
    fs = glob.glob('../testing/sites/*/*')
    fs = glob.glob('../testing/sites/cooks.com/*')
    for f in fs:
        print(f)
        parseRecipe(f)
    # processFile('../testing/sites/allrecipes.com/throwoff')
    fs = glob.glob('../testing/sites/*/*')
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    print("Processing %d files..." % len(fs))
    for i in tqdm(range(0, len(fs), 2 * multiprocessing.cpu_count())):
        p.map(parseRecipe, fs[i:i + 2 * multiprocessing.cpu_count()])

if __name__ == "__main__":
    main()
