'''
10. Desarrollar una función en Python que reciba: una lista con el alfabeto de una fuente, otra
con su distribución de probabilidades y un número entero N. Esta función debe generar
dos nuevas listas con la extensión de orden N y su distribución de probabilidades.
'''

'''
N=3

'''



def extension(alfabeto, probabilidades, N):
    if N <= 0:
        return [], []
    if N == 1:
        return list(alfabeto), list(probabilidades)

    # Obtenemos recursivamente la extensión de orden N - 1
    sub_alf, sub_prob = extension(alfabeto, probabilidades, N - 1)

    nueva_ext = []
    nuevas_prob = []
    for palabra, prob in zip(sub_alf, sub_prob):
        for simbolo, p in zip(alfabeto, probabilidades):
            nueva_ext.append(palabra + simbolo)
            nuevas_prob.append(prob * p)

    return nueva_ext, nuevas_prob


if __name__ == '__main__':
    alfabeto = ['A', 'B', 'C']
    probabilidades = [0.5, 0.2, 0.3]
    N = 5

    ext_alfabeto, ext_probabilidades = extension(alfabeto, probabilidades, N)

    print(f"Extensión de orden {N}:")
    print("Alf:  ", ext_alfabeto)
    print("Prob: ", [round(p, 4) for p in ext_probabilidades])
