import multiprocessing
import os

from tqdm import tqdm

from extractors.allrecipes import *
from extractors.epicurious import *
from extractors.cooks import *
from extractors.food import *


def processFile(f):
    if 'allrecipes.com' in f:
        extract_allrecipes(f)
    elif 'epicurious' in f:
        extract_epicurious(f)
    elif 'cooks.com' in f:
        extract_cooks(f)
    elif 'food.com' in f:
        extract_food(f)


def main():
    if not os.path.exists('../finished'):
        os.makedirs('../finished')
    if not os.path.exists('../finished/allrecipes.com'):
        os.makedirs('../finished/allrecipes.com')
    if not os.path.exists('../finished/epicurious.com'):
        os.makedirs('../finished/epicurious.com')
    if not os.path.exists('../finished/cooks.com'):
        os.makedirs('../finished/cooks.com')
    if not os.path.exists('../finished/food.com'):
        os.makedirs('../finished/food.com')
    fs = glob.glob('../testing/sites/food.com/*')
    # fs = glob.glob('../testing/sites/*/*')
    processFile(fs[1])
    # processFile(fs[0])
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    print("Processing %d files..." % len(fs))
    for i in tqdm(range(0, len(fs), 2 * multiprocessing.cpu_count())):
        p.map(processFile, fs[i:i + 2 * multiprocessing.cpu_count()])

if __name__ == "__main__":
    main()
