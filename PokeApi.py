import requests
import os
import time
import json
from shutil import rmtree

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
         
        # Check
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
        if os.path.exists(poke_folder):
            print(f'The folder {self.poke_name} already exists.')
            
            #Check of folder has 2 items
            folder_archives = os.listdir(poke_folder)
            if len(folder_archives) != 2:
                #Remove folder
                print('An error was encountered, recreating a folder.')
                rmtree(poke_folder)
                os.mkdir(poke_folder)
            else:
                self.error_check = True    
        else:
            os.mkdir(poke_folder)
            
              
    def get_infos(self):
        #Get informations from the api
        try:
            res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.poke_id.lower()}/")
            
            if res.status_code == 200:
                return res.json()
            else:
                if res.status_code == 404:
                    print('Pokemon Not Found.')
                else:
                    print(f"Error: {res.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Um erro ocorreu durante a solicitação: {e}")
            

class Saver(Pokemon):
    def save(self):
        Saver.make_infos(self)
        Saver.save_infos(self)
        
    
    def save_infos(self):
        poke_folder = self.poke_folder
            
        #Save image
        with open(f'{poke_folder}\{self.poke_name}.png', "wb") as f:
            f.write(self.poke_image)
        
        #Save Json
        with open(f'{poke_folder}\{self.poke_name}.json', 'w') as f:
            json.dump(self.pokedex, f, indent=4)
            
        print(f'{self.poke_name} saved successfully.')
        
    
    def make_infos(self):
        self.types_url = []
        json = self.poke_json
        
        #pokedex infos
        pokedex = {}
        self.types = []
        
        #Name
        pokedex['name'] = self.poke_name
        
        #Height and Weight
        pokedex['infos'] = [f'{json["height"]/10} m',
                            f'{json["weight"]/10} kg']
        #Abilities
        pokedex['abilities'] = []
        for abi in json['abilities']:
            if abi['is_hidden'] == False:
                pokedex['abilities'].append(abi['ability'])
  
        #Gender
        pokedex['gender'] = Pokedex_infos.get_gender(self)
        
        #Types
        for type in json['types']:
            self.types.append(type['type']['name'].capitalize())
            self.types_url.append(type['type']['url'])
        pokedex['types'] = self.types

        #Defensive and Offensive
        pokedex['defensive_offensive'] = Pokedex_infos.get_buffs_debuffs(self)
        
        #Evolutions
        pokedex['evolutions'] = Pokedex_infos.evolution_chain(self)       
        
        self.pokedex = pokedex
        

class Pokedex_infos(Saver):
    def get_gender(self):
        #Genders
        dict_genders = {
            1: 'F', 2: 'M'
        }
        
        #Catch Gender
        list_gender = []
        for i in range(1,3):
            #Json
            gender_json = requests.get(f'https://pokeapi.co/api/v2/gender/{i}/').json()
            
            #Catcher
            for pokemon in gender_json['pokemon_species_details']:
                if pokemon['pokemon_species']['name'] == self.poke_name.lower():
                    list_gender.append(dict_genders[i])
        
        #Last Check
        if not list_gender:
            return 'Unknown'
        else:
            return '/'.join(list_gender)
        
    
    def get_buffs_debuffs(self):
        #infos
        damages_defenses = {
            'defensive': {
                'double_damage_from': [],
                'half_damage_from': []
            },
            'offensive': {
                'double_damage_to': [],
                'half_damage_to': []
            }   
        }
        
        def loop(json_infos):
            #info list maker
            tmp = []
            for item in json_infos:
                name = item['name']
                tmp.append(name.capitalize())
            return tmp
        
        #Requests types url
        for url in self.types_url:
            types_json = requests.get(url).json()
            
            #Save the infos
            for form in damages_defenses:
                for char in damages_defenses[form]:
                    damages_defenses[form][char].append(loop(types_json['damage_relations'][char]))
        
        return damages_defenses
    
    def evolution_chain(self):
        #GET evolution link
        res = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{self.poke_id}/').json()
        #GET evolution
        evo_res = requests.get(res["evolution_chain"]['url']).json()
        
        evo = []
        chain = evo_res['chain']
        while 'evolves_to' in evo_res['chain']:
            name = chain['species']['name'].capitalize()
            
            #Save evolution name
            if name == self.poke_name:
                evo.append(name.upper())
            else:
                evo.append(name)
            
            #Take the next evolution
            chain = chain['evolves_to']
            if not chain:
                break
            chain = chain[0]
        
        return evo

Pokemon(input('Insira o ID ou Nome do pokemon: '))

print('exiting...')
time.sleep(3)