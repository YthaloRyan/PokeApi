import requests
import os
import json

#URL para pegar evolution chain
# res = requests.get('https://pokeapi.co/api/v2/pokemon-species/charizard/')
res = requests.get('https://pokeapi.co/api/v2/pokedex/2/')

print(res)

#URL para pegar a linha de evolucao do pokemon
res2 = requests.get('https://pokeapi.co/api/v2/evolution-chain/2/')

print(res)
print(res.json())
with open('testes.json', 'w') as teste:
    json.dump(res.json(), teste, indent=4)