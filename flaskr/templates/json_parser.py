import json

#Abrimos el archivo json

with open('catalogo.json') as f:
    catalogo_dict = json.load(f)

print catalogo_dict["peliculas"]
