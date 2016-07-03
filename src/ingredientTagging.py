import json
import os
import subprocess
import shutil
import copy

from tqdm import tqdm

def getAllFiles():
	mypath = "../finished"
	fs = []
	for root, directories, filenames in os.walk(mypath):
	    for filename in filenames:
	        fs.append(os.path.join(root, filename))
	return fs

def processFile(f):
	if os.path.exists(f+'.it'):
		return
	data = json.load(open(f,'r'))
	baseName = f.split("/")[-1]
	try:
		os.mkdir(os.path.join("/tmp/"+baseName))
	except:
		pass
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

print("Getting all the files...")
fs = getAllFiles()
for i in tqdm(range(len(fs))):
	processFile(fs[i])