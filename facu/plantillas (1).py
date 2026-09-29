# ==============================================================================
# PLANTILLAS PARA EL PARCIAL
# ------------------------------------------------------------------------------
# Cómo se usa:
#   1. Buscá el bloque de lo que te piden.
#   2. Copialo a borrador.py (debajo de la línea "from teoria_info_toolkit import *").
#   3. Cambiá SOLO lo que está marcado con  <-- CAMBIAR
#   4. Corré borrador.py. Después armar_entrega.py.
# Los prints ya están escritos: no hace falta tocarlos.
# Este archivo no se entrega. Si lo corrés, muestra todos los ejemplos.
# ==============================================================================

from teoria_info_toolkit import *


# ------------------------------------------------------------------------------
# BLOQUE 1: TE DAN UN MENSAJE (Parte 1 del parcial)
# ------------------------------------------------------------------------------
msg = ")[))[([()))()[[]](([[)))])))][))(][)[[[)()]))[)[])"   # <-- CAMBIAR (pegá el mensaje)
resolver_fuente(msg)


# ------------------------------------------------------------------------------
# BLOQUE 2: TE DAN UN CÓDIGO Y SUS PROBABILIDADES (Parte 2 del parcial)
# ------------------------------------------------------------------------------
codigos = ["/+", "*", "+-", "-", "*/"]         # <-- CAMBIAR (cada palabra entre comillas)
probs = [0.15, 0.25, 0.05, 0.45, 0.10]         # <-- CAMBIAR (en el mismo orden, con punto)
resolver_codigo(codigos, probs)
# Si el enunciado dice que X tiene más símbolos de los que aparecen, usá:
# resolver_codigo(codigos, probs, r=4)         # <-- r = cantidad de símbolos de X


# ------------------------------------------------------------------------------
# BLOQUE 3: TE DAN LA MATRIZ DE UNA FUENTE DE MARKOV
# Cada [ ] de adentro es una FILA (= estado "hacia"). Cada COLUMNA tiene que sumar 1.
# ------------------------------------------------------------------------------
M = [[1/2, 0,   0, 1/2],                       # <-- CAMBIAR (copiá la matriz fila por fila)
     [1/2, 0,   0, 0  ],
     [0,   1/2, 0, 0  ],
     [0,   1/2, 1, 1/2]]
resolver_markov(M, ["1", "2", "3", "4"])       # <-- CAMBIAR (nombres de los estados, en orden)


# ------------------------------------------------------------------------------
# BLOQUE 4: TE DAN EL GRAFO DE UNA FUENTE DE MARKOV
# Una línea por flecha: ("desde", "hacia", probabilidad). Los lazos también.
# Si el grafo NO tiene probabilidades, poné solo ("desde", "hacia") y se asumen
# equiprobables las flechas que salen de cada estado.
# ------------------------------------------------------------------------------
estados = ["A", "B", "C"]                      # <-- CAMBIAR
flechas = [("A", "A"),                         # <-- CAMBIAR (una por flecha)
           ("A", "B"),
           ("B", "A"),
           ("B", "B"),
           ("B", "C"),
           ("C", "B")]
resolver_markov(matriz_desde_grafo(estados, flechas), estados)


# ------------------------------------------------------------------------------
# BLOQUE 5: TE DAN SOLO PROBABILIDADES (fuente de memoria nula)
# ------------------------------------------------------------------------------
simbolos = ["A", "B", "C", "D"]                # <-- CAMBIAR
probs = [0.5, 0.25, 0.125, 0.125]              # <-- CAMBIAR
print("\nINFORMACIÓN DE CADA SÍMBOLO:")
for s, p in zip(simbolos, probs):
    print("   I(" + s + ") = log2(1/" + str(p) + ") =", round(cantidad_informacion(p), 2), "bits")
print("ENTROPÍA: H(S) =", round(entropia_fuente(probs), 2), "bits")
print("ENTROPÍA MÁXIMA: log2(" + str(len(probs)) + ") =", round(entropia_maxima(len(probs)), 2), "bits")


# ------------------------------------------------------------------------------
# BLOQUE 6: EXTENSIÓN DE ORDEN n (cualquier n)
# ------------------------------------------------------------------------------
simbolos = ["x", "y", "z"]                     # <-- CAMBIAR
probs = [0.5, 0.1, 0.4]                        # <-- CAMBIAR
n = 3                                          # <-- CAMBIAR (orden)
palabras, probs_n, h_n = extension_fuente(simbolos, probs, n)
print("\nEXTENSIÓN DE ORDEN", n, "->", len(palabras), "símbolos")
for pal, p in zip(palabras, probs_n):
    print("   P(" + pal + ") =", round(p, 4))
print("H(S^" + str(n) + ") =", round(h_n, 2), "bits   (n · H(S) =", round(n * entropia_fuente(probs), 2), ")")


# ------------------------------------------------------------------------------
# BLOQUE 7: PROBABILIDAD E INFORMACIÓN DE UN MENSAJE PUNTUAL (ej. "CADABA")
# ------------------------------------------------------------------------------
simbolos = ["A", "B", "C", "D"]                # <-- CAMBIAR
probs = [0.5, 0.25, 0.125, 0.125]              # <-- CAMBIAR
mensaje = "CADABA"                             # <-- CAMBIAR
P = dict(zip(simbolos, probs))
p_msg = 1
for s in mensaje:
    p_msg = p_msg * P[s]
print("\nMENSAJE", mensaje)
print("   P =", " · ".join(str(P[s]) for s in mensaje), "=", p_msg)
print("   I = log2(1/P) =", round(cantidad_informacion(p_msg), 2), "bits  (= suma de las I de cada símbolo)")


# ------------------------------------------------------------------------------
# BLOQUE 8: FUENTE BINARIA CON w
# ------------------------------------------------------------------------------
for w in [0.25, 0.75, 0.5, 1, 0]:              # <-- CAMBIAR (los valores de w)
    print("w =", w, "-> H =", round(entropia_binaria(w), 2), "bits")


# ------------------------------------------------------------------------------
# BLOQUE 9: CONSTRUIR UN CÓDIGO COMPACTO (Huffman)
# ------------------------------------------------------------------------------
probs = [0.15, 0.25, 0.05, 0.45, 0.10]         # <-- CAMBIAR
r = 2                                          # <-- CAMBIAR (cantidad de símbolos del código)
codigo, L = huffman(probs, r=r)
print("\nCÓDIGO DE HUFFMAN (r =", str(r) + "):")
for simbolo, palabra in sorted(codigo.items()):
    print("  ", simbolo, "->", palabra)
print("Longitud media L =", round(L, 2), "  |  H_r(S) =", round(entropia_fuente(probs, r), 2))
