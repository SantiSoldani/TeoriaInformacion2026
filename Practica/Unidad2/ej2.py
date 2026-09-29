''' 
2. Implementar funciones en Python que resuelvan lo siguiente:
a. Dada una cadena de caracteres que representa un mensaje emitido por una fuente
de memoria nula, devolver dos listas paralelas que contengan: el alfabeto de la
fuente y las probabilidades de cada símbolo.
b. Dados un número entero N, una lista que contenga el alfabeto de una fuente y otra
con las probabilidades de cada símbolo, simular la generación de una cadena de
caracteres de longitud N emitida por esa fuente.
'''

import math
import random

mensaje = 'AAAAAAAAAABBCCBCBCAA'

def alfabeto_y_probabilidades(cadena):
    # Devuelve el alfabeto y las probabilidades de los simbolos, ordenados de manera ascendente.
    alfabeto = sorted(set(cadena))
    probabilidades = [cadena.count(simbolo)/len(cadena) for simbolo in alfabeto]
    return alfabeto, probabilidades

def generacion_cadena(N, alfabeto, probabilidades) -> str:
    probabilidades_acumuladas = [sum(probabilidades[:i+1]) for i in range(len(probabilidades))]
    cadena = ""
    for _ in range(N):
        r = random.random()
        for i in range(len(alfabeto)):
            if r <= probabilidades_acumuladas[i]:
                cadena += alfabeto[i]
                break

    return cadena

if __name__ == '__main__':
    mensaje = 'AAAAAAAAAABBCCBCBCAA'
    alfabeto, probabilidades = alfabeto_y_probabilidades(mensaje)
    print("Alfabeto: ", alfabeto)
    print("Probabilidades: ", probabilidades)

    mensaje_2 = generacion_cadena(20, alfabeto, probabilidades)
    alfabeto_2, probabilidades_2 = alfabeto_y_probabilidades(mensaje_2)
    print("Alfabeto simulado: ", alfabeto_2)
    print("Probabilidades simuladas: ", probabilidades_2)