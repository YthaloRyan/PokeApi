import os

# Obtém o diretório atual do arquivo .py
diretorio_atual = os.getcwd()
print(diretorio_atual)
# Nome da nova pasta que você deseja criar
nome_pasta = "minha_pasta"

# Caminho completo para a nova pasta
caminho_pasta = os.path.join(diretorio_atual, nome_pasta)

# # Verifica se a pasta já existe
# if not os.path.exists(caminho_pasta):
#     # Cria a pasta se ela não existir
#     os.mkdir(caminho_pasta)
#     print(f'A pasta "{nome_pasta}" foi criada com sucesso no diretório atual.')
# else:
#     print(f'The folder "{no}" já existe no diretório atual.')