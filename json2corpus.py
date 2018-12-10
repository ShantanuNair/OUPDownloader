import json
from pprint import pprint


for i in range(24,40):
    with open('data.json') as f:
    data = json.load(f)

    pprint(data)
