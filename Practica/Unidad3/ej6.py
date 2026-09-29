'''6. Desarrollar funciones booleanas que clasifiquen palabras código.
Las implementaciones están centralizadas en Parcial-1/Funciones.py.
'''

from FuncionesTp3 import esNoSingular, esInstantaneo, esUnivoco


c1 = ['011', '000', '010', '101', '001', '100']
c2 = ['110', '100', '101', '001', '110', '010']
c3 = ['10', '1100', '0101', '1011', '0', '110']
c4 = ['1101', '10', '1111', '1100', '1110', '0']
c5 = ['011', '0111', '01', '0', '011111', '01111']
c6 = ['1110', '0', '110', '1101', '1011', '10']

codigos = [c1, c2, c3, c4, c5, c6]

for codigo in codigos:
    print("Codigo: ", codigo)
    print("No singular: ", esNoSingular(codigo))
    print("Instantáneo: ", esInstantaneo(codigo))
    print("Unívoco: ", esUnivoco(codigo))
    print()
