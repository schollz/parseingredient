import multiprocessing
import os

from extractors.allrecipes import *
from extractors.epicurious import *
from tqdm import tqdm


def processFile(f):
    if 'allrecipes.com' in f:
        extract_allrecipes(f)
    if 'epicurious' in f:
        extract_epicurious(f)


def main():
    if not os.path.exists('../finished'):
        os.makedirs('../finished')
    if not os.path.exists('../finished/allrecipes.com'):
        os.makedirs('../finished/allrecipes.com')
    if not os.path.exists('../finished/epicurious.com'):
        os.makedirs('../finished/epicurious.com')
    fs = glob.glob('../testing/sites/epicurious.com/*')
    processFile(fs[1])
    # processFile(fs[0])
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    print("Processing %d files..." % len(fs))
    for i in tqdm(range(0, len(fs), 2 * multiprocessing.cpu_count())):
        p.map(processFile, fs[i:i + 2 * multiprocessing.cpu_count()])

if __name__ == "__main__":
    main()
