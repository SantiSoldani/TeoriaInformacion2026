'''
11. Dadas dos listas paralelas que contengan las palabras código de una codificación y sus
respectivas probabilidades, codificar funciones en Python que calculen:
a. la entropía de la fuente
b. la longitud media del código
'''

import FuncionesTp3 as functions

probabilidades = [0.1,0.5,0.1,0.2,0.05,0.05]
codigo = ["==","<","<=",">",">=","<>"]

r = len(set("".join(codigo))) #La base es la cantidad de simbolos diferentes del alfabeto codigo

print("Entropía de la fuente: ", round(functions.entropia_fuente(probabilidades, r), 3))
print("Longitud media del código: ", functions.longmedia(codigo,probabilidades))