import requests
from pprint import pprint
import json

nomes_pokemon = ["Pikachu", "34", "bulbasaur", "squirtle", "jigglypuff"]

class Pokemons:
    def __init__(self,poke_name):
        self.poke_id = poke_name
        self.poke_json = Pokemons.get_infos(self)
        Pokemons.poke_photo(self)
    
    
    def poke_photo(self):
        photo_link = self.poke_json['sprites']['other']['home']['front_default']
        print(photo_link)
    
    
    def get_infos(self): 
        try:
            res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.poke_id.lower()}")
            
            if res.status_code == 200:
                return res.json()
            else:
                print(f"A solicitação falhou com o código de status: {res.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Um erro ocorreu durante a solicitação: {e}")
        
        
for pokemon in nomes_pokemon:
    Pokemons(pokemon)