'''16. Generar aleatoriamente un mensaje de N símbolos codificados.'''

from FuncionesTp3 import generaMensaje


c7 = ["==", "<", "<=", ">", ">=", "<>"]
probabilidades = [0.1, 0.5, 0.1, 0.2, 0.05, 0.05]

print(generaMensaje(10, c7, probabilidades))
