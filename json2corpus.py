import json
import os
from pprint import pprint
from io import open

abstracts = ''

def preprocessText(text):
    removeNewlines(text)

def removeNewlines(text):
    text.replace("\n", "")

for i in range(24,40):
    for filename in os.listdir('year'+str(i)):
        print(filename)
        if filename.endswith('.json'):
            with open('year'+str(i)+'/'+filename) as f:
                data = json.load(f)
                abstract = data['abstract']
                # pprint(data)
                abstracts = abstracts + abstract + '\n'
print(abstracts)
corpus = open('abstracts.cor',mode="w",encoding="utf-8")
corpus.write(abstracts)

