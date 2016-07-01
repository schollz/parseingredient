import multiprocessing
import os

from tqdm import tqdm

from extractors.allrecipes import *
from extractors.epicurious import *
from extractors.cooks import *


def processFile(f):
    if 'allrecipes.com' in f:
        extract_allrecipes(f)
    if 'epicurious' in f:
        extract_epicurious(f)
    if 'cooks.com' in f:
        extract_cooks(f)


def main():
    if not os.path.exists('../finished'):
        os.makedirs('../finished')
    if not os.path.exists('../finished/allrecipes.com'):
        os.makedirs('../finished/allrecipes.com')
    if not os.path.exists('../finished/epicurious.com'):
        os.makedirs('../finished/epicurious.com')
    if not os.path.exists('../finished/cooks.com'):
        os.makedirs('../finished/cooks.com')
    fs = glob.glob('../testing/sites/cooks.com/*')
    # fs = glob.glob('../testing/sites/*/*')
    processFile(fs[1])
    # processFile(fs[0])
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    print("Processing %d files..." % len(fs))
    for i in tqdm(range(0, len(fs), 2 * multiprocessing.cpu_count())):
        p.map(processFile, fs[i:i + 2 * multiprocessing.cpu_count()])

if __name__ == "__main__":
    main()
