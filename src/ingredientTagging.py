import json
import os
import subprocess
import shutil
import copy
import multiprocessing

from tqdm import tqdm

def getAllFiles():
	if not os.path.exists('json_file_list'):
		os.system("tree -Ufai -P '*.json' -I '*.it.*' -o json_file_list ../finished")
	fs = open('json_file_list','r').read().split("\n")
	return fs

def processFile(f):
	if os.path.exists(f+'.it') or '.it' in f or '.json' not in f:
		return
	data = json.load(open(f,'r'))
	baseName = f.split("/")[-1]
	try:
		os.mkdir(os.path.join("/tmp/"+baseName))
	except:
		pass
	try:
		inputTxt = os.path.join("/tmp/"+baseName,"input.txt")
		resultsTxt = os.path.join("/tmp/"+baseName,"results.txt")

		with open(inputTxt,"w") as fwrite:
			for ingredient in data['recipeIngredient']:
				fwrite.write(ingredient.strip() + "\n")

		cmd = "python /home/phi/Downloads/ingredient-phrase-tagger/lib/testing/parse-ingredients.py " + inputTxt
		with open(resultsTxt,"w") as fwrite:
			fwrite.write(subprocess.check_output(cmd.split(), universal_newlines=True))

		cmd = "python /home/phi/Downloads/ingredient-phrase-tagger/lib/testing/convert-to-json.py " + resultsTxt
		resultJson = json.loads(subprocess.check_output(cmd.split(), universal_newlines=True))
		data['recipeIngredientTagged'] = copy.deepcopy(resultJson)
		with open(f+'.it','w') as fwrite:
			fwrite.write(json.dumps(data,indent=2))
		shutil.rmtree(os.path.join("/tmp/"+baseName))
	except:
		return

print("Getting all the files...")
fs = getAllFiles()
p = multiprocessing.Pool(multiprocessing.cpu_count())
print("Processing %d files..." % len(fs))
for i in tqdm(range(0, len(fs), 8 * multiprocessing.cpu_count())):
    p.map(processFile, fs[i:i + 8 * multiprocessing.cpu_count()])
