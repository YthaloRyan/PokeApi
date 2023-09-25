import requests
import os
import json

#URL para pegar evolution chain
res = requests.get('https://pokeapi.co/api/v2/pokemon-species/25/')

#URL padrao
# res = requests.get('https://pokeapi.co/api/v2/pokemon/25/')

#URL form
# res = requests.get('https://pokeapi.co/api/v2/pokemon-form/25/')

#URL gender
# res = requests.get('https://pokeapi.co/api/v2/gender/3/')

#URL type
res = requests.get('https://pokeapi.co/api/v2/type/3/')



#URL para pegar a linha de evolucao do pokemon
# res2 = requests.get('https://pokeapi.co/api/v2/evolution-chain/2/')

print(res)

with open('testes.json', 'w') as teste:
    json.dump(res.json(), teste, indent=4)