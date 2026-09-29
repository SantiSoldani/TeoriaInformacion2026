'''
9. Dada una lista que contiene las palabras código de una codificación, implementar
funciones en Python que resuelvan lo siguiente:
a. obtener una cadena de caracteres con el alfabeto código.
b. generar otra lista con las longitudes de las palabras (utilizar comprensión de listas).
c. calcular la sumatoria de la inecuación de Kraft (utilizar las funciones anteriores).
'''

from FuncionesTp3 import alfabeto_codigo, longitudes_palabras, Kraft

c1 = ['011','000','010','101','001','100']
c2 = ['110','100','101','001','110','010']
c3 = ['10','1100','0101','1011','0','110']
c4 = ['1101','10','1111','1100','1110','0']
c5 = ['011','0111','01','0','011111','01111']
c6 = ['1110','0','110','1101','1011','10']

c7 = ["==","<","<=",">",">=","<>"]
c8 = [")", "[]", "]]", "([", "[()]", "([)]"]
c9 = ["/", "*", "-", "*", "++", "+-"]
c10 = [".," , ";" , ",," , ":" , "..." , ",:;"]

codigos = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
i = 1
for codigo in codigos:
    print("Codigo: ", i)
    print("Alfabeto código: ", alfabeto_codigo(codigo))
    print("Longitudes: ", longitudes_palabras(codigo)) 
    print("Sumatoria Kraft: ", Kraft(codigo))
    i+=1
    print()
