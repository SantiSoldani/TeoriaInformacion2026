'''
14. Realizar una función booleana en Python que reciba como parámetros dos listas paralelas
que contengan las palabras código de una codificación y sus respectivas probabilidades, y
determine si se trata de un código compacto.
'''
from FuncionesTp3 import esCompacto

c7 = ["==","<","<=",">",">=","<>"]
c8 = [")", "[]", "]]", "([", "[()]", "([)]"]
c9 = ["/", "*", "-", "*", "++", "+-"]
c10 = [".," , ";" , ",," , ":" , "..." , ",:;"]

codigos = [c7,c8,c9,c10]
probabilidades = [0.1,0.5,0.1,0.2,0.05,0.05]

for codigo in codigos:
    print("Codigo: ", codigo)
    print("Es compacto: ", esCompacto(codigo,probabilidades))
    print()
