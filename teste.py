import requests
import os
import json

res = requests.get('https://pokeapi.co/api/v2/pokemon/10271/',
                   params={'limit': '10000'})

print(res)
print(res.json())
with open('testes.json', 'w') as teste:
    json.dump(res.json(), teste, indent=4)