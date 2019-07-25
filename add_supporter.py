import json
import os

try:
    with open('supporters.json', 'r') as f:
        data = json.load(f)
except:
    print('No supporters file exists, will create')
    data = {}

name = input('Name: ')
amount = input('Amount: ')

if not amount.startswith('$'):
    amount = '$' + amount

data[name] = {}
data[name]['amount'] = amount

with open('supporters.json', 'w+') as f:
    json.dump(data, f, indent=2)
