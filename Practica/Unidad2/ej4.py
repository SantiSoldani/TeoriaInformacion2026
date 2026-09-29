'''
Alfabeto {x, y, z} {0, 1} {A, B, C, D}
Probabilidades {0.5, 0.1, 0.4} {0.5, 0.5} {0.1, 0.3, 0.4, 0.2}
a. Obtener la cantidad de información de cada símbolo
b. Calcular la entropía de la fuente
'''

from ej1 import informacion, entropia_fuente

if __name__ == '__main__':
    alfabeto1 = ['x', 'y', 'z']
    probabilidades1 = [0.5, 0.1, 0.4]
    alfabeto2 = ['0', '1']
    probabilidades2 = [0.5, 0.5]
    alfabeto3 = ['A', 'B', 'C', 'D']
    probabilidades3 = [0.1, 0.3, 0.4, 0.2]
    
    print("Cantidad de informacion: ", [informacion(p) for p in probabilidades1])
    print("Entropia de la fuente: ", entropia_fuente(probabilidades1))
    print("Cantidad de informacion: ", [informacion(p) for p in probabilidades2])
    print("Entropia de la fuente: ", entropia_fuente(probabilidades2))
    print("Cantidad de informacion: ", [informacion(p) for p in probabilidades3])
    print("Entropia de la fuente: ", entropia_fuente(probabilidades3))