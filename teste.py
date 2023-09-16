import requests
import os

# URL da imagem que você deseja baixar
url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/25.png"

# Envie uma solicitação GET para a URL para obter o conteúdo da imagem
response = requests.get(url)

# Verifique se a solicitação foi bem-sucedida (código de status 200)
if response.status_code == 200:
    # Especifique o caminho local onde você deseja salvar a imagem
    
    caminho_local = os.getcwd()
    

    # Abra o arquivo em modo binário para gravar a imagem
    with open(caminho_local, "wb") as file:
        file.write(response.content)

    print(f'Imagem salva em "{caminho_local}"')
else:
    print("Falha ao baixar a imagem. Código de status:", response.status_code)