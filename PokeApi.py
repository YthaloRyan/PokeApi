import requests
from pprint import pprint
import os
import time

nomes_pokemon = [i for i in range(1,10)]

#Get current directory
global cur_dir
cur_dir = os.getcwd()

#Create the directory for pokemons
pokes_dir = os.path.join(cur_dir,'pokemons')
if not os.path.exists(pokes_dir):
    os.mkdir(pokes_dir)

class Pokemon:
    def __init__(self,poke_id):
        self.error_check = False
        
        #Request Archives
        self.poke_id = str(poke_id)
        self.poke_json = Pokemon.get_infos(self)
        if self.poke_json is None:
            return None
        
        #Pokemon name
        self.poke_name = self.poke_json['name'].capitalize()
        
        #Main folder
        self.alpha_poke_folder = os.path.join(cur_dir, 'pokemons', self.poke_name[0])
        self.poke_folder = os.path.join(self.alpha_poke_folder, self.poke_name)
        
        #Create a folder for pokemon
        Pokemon.make_poke_dir(self)
        
        #tmp
        Saver.save_infos(self)
        
        #Check
        if self.error_check == True:
            return None
        
        #Catch the photo
        self.poke_image = Pokemon.poke_photo(self)
        if self.poke_image is None:
            return None
        
        #Save the informations
        Saver.save(self)
            
        
    def poke_photo(self):
        #Get the link from the json link
        photo_link = self.poke_json['sprites']['other']['home']['front_default']
        if photo_link is None:
            photo_link = self.poke_json['sprites']['other']['official-artwork']['front_default']
            if photo_link is None:
                print('Sprite Not Found')
                return None
  
        #Get the photo
        res = requests.get(photo_link)
        if res.status_code == 200:
            return res.content
        else:
            print(f"{self.poke_name} Image Error: {res.status_code}")
    
    
    def make_poke_dir(self):
        #Make Alphabetic folder
        alpha_poke_folder = self.alpha_poke_folder
        if not os.path.exists(alpha_poke_folder):
            os.mkdir(alpha_poke_folder)           
            
        #Make the folder with Pokemon name
        poke_folder = self.poke_folder
        if not os.path.exists(poke_folder):
            os.mkdir(poke_folder)
            
        else:
            print(f'The folder {self.poke_name} already exists.')
            self.error_check = True
              
    
    def get_infos(self):
        #Get informations from the api
        try:
            res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.poke_id.lower()}/")
            
            if res.status_code == 200:
                return res.json()
            else:
                print(f"Error: {res.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Um erro ocorreu durante a solicitação: {e}")
            

class Saver(Pokemon):
    def save(self):
        Saver.save_image(self)
        Saver.save_infos(self)
    
    
    def save_image(self):
        poke_folder = self.poke_folder
            
        #Save image
        with open(f'{poke_folder}\{self.poke_name}.png', "wb") as file:
            file.write(self.poke_image)
            
        print(f'{self.poke_name} saved successfully.')
        
    
    def save_infos(self):
        self.types_url = []
        poke_folder = self.poke_folder
        json = self.poke_json
        
        pokedex = {}
        infos = []
        types = []
        
        
        pokedex['name'] = self.poke_name
        
        
        infos.append(f'{json["height"]/10} m')
        infos.append(f'{json["weight"]/10} kg')
        
        pokedex['infos'] = infos
        
        pokedex['abilities'] = []
        
        for abi in json['abilities']:
            if abi['is_hidden'] == False:
                pokedex['abilities'].append(abi['ability'])
                
        
        
        
        pokedex['gender'] = Pokedex_infos.get_gender(self)
        for type in json['types']:
            types.append(type['type']['name'].capitalize())
            self.types_url.append(type['type']['url'])
        
        pokedex['types'] = types

        Pokedex_infos.get_buffs_debuffs(self)
        # print(infos)
        # print(pokedex)
        

class Pokedex_infos(Saver):
    def get_gender(self):
        dict_genders = {
            1: 'M',
            2: 'F'
        }
        
        list_gender = []
        for i in range(1,3):
            gender_json = requests.get(f'https://pokeapi.co/api/v2/gender/{i}/').json()
            
            for pokemon in gender_json['pokemon_species_details']:
                if pokemon['pokemon_species']['name'] == self.poke_name.lower():
                    list_gender.append(dict_genders[i])
        
        if not list_gender:
            return 'Unknown'
        else:
            return '/'.join(list_gender)
        
    
    def get_buffs_debuffs(self):
        infos = {
            0: 'double_damage_from',
            1: 'double_damage_to'
        }
        
        
        def loop(json_infos):
            for item in json_infos:
                print(item['name'])
        #Take the infos
        for url in self.types_url:
            types_json = requests.get(url).json()
            
            
            buff_list = [loop(types_json['damage_relations']['double_damage_to'])]
            debuff_list = [loop(types_json['damage_relations']['double_damage_from'])]
            
                
        
    
                
                    
        
# for pokemon in nomes_pokemon:
#     Pokemon(str(pokemon))

Pokemon((144))
print('exiting...')
time.sleep(3)