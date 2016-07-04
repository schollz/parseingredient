import ujson as json
import os

from tqdm import tqdm

os.chdir("../finished")
if not os.path.exists("finished.index"):
	print("Generating file index")
	os.system("tree -Ufai -P '*.json.it' -I '*.it.it' -o finished.index")

fileIndex = open("finished.index", "r").read().split("\n")

print("Found %d files." % len(fileIndex))
with open("db.json","w") as db:
	db.write('{ "recipes": [\n')
	for i in tqdm(range(len(fileIndex))):
		f = fileIndex[i]
		if ".json.it" in f:
			fooJson = json.load(open(f, "r"))
			fooJson['id'] = f.split('/')[-1].split('.')[0]
			db.write(json.dumps(fooJson)+',\n')
		if i > 10000:
			break
	db.write('{"null":"null"} ] }')
