import requests
from pprint import pprint
import os
import time

nomes_pokemon = [150]

#Get current directory
global cur_dir
cur_dir = os.getcwd()

#Create the directory for pokemons
pokes_dir = os.path.join(cur_dir,'pokemons')
if not os.path.exists(pokes_dir):
    os.mkdir(pokes_dir)

class Pokemon:
    def __init__(self,poke_id):
        #Request Archives
        self.poke_id = poke_id
        self.poke_json = Pokemon.get_infos(self)
        if self.poke_json is None:
            return None
        
        #Pokemon image and infromatios
        self.poke_name = self.poke_json['name'].capitalize()
        self.poke_image = Pokemon.poke_photo(self)
        if self.poke_image is None:
            return None
        
        #Main folder
        self.alpha_poke_folder = os.path.join(cur_dir, 'pokemons', self.poke_name[0])
        self.poke_folder = os.path.join(self.alpha_poke_folder, self.poke_name)
        
        #Create a folder for pokemon and save
        Pokemon.make_poke_dir(self)
          
        #temp
        # with open('testes.json', 'w') as teste:
        #     json.dump(self.poke_json, teste, indent=4)
            
        
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
            
            #Save all information
            Pokemon.save_poke_infos(self)
        else:
            print(f'The folder {self.poke_name} already exists.')
            
            
    def save_poke_infos(self):
        poke_folder = self.poke_folder
           
        #Save image
        with open(f'{poke_folder}\{self.poke_name}.png', "wb") as file:
            file.write(self.poke_image)
            
        print(f'{self.poke_name} saved successfully.')
    
    
    def get_infos(self):
        #Get informations from the api
        try:
            res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.poke_id.lower()}/")
            
            if res.status_code == 200:
                return res.json()
            else:
                print(f"A solicitação falhou com o código de status: {res.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Um erro ocorreu durante a solicitação: {e}")
                    
        
for pokemon in nomes_pokemon:
    Pokemon(str(pokemon))
    
print('exiting...')
time.sleep(3)