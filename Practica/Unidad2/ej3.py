'''
3. Suponiendo una fuente de memoria nula, dada por el resultado de la tirada de un dado,
calcular la entropía en los siguientes casos:
a. Los sucesos son equiprobables
b. Las probabilidades son: P(1) = 1/9, P(2) = 1/6, P(3) = 1/9, P(4) = 1/9, P(5) = 1/6 y
P(6) = 1/3
'''

from ej1 import entropia_fuente


if __name__ == '__main__':
    # Código de prueba que solo querés ejecutar directamente
    probabilidades_equiprobables = [1/6]*6
    probabilidades_aleatorias = [1/9,1/6,1/9,1/9,1/6,1/3]
    print("Entropia de la fuente con probabilidades equiprobables: ",entropia_fuente(probabilidades_equiprobables))
    print("Entropia de la fuente con probabilidades aleatorias: ",entropia_fuente(probabilidades_aleatorias))


