
import math

def alfabeto_codigo(codigo) -> str:
    """9.a Obtiene una cadena de caracteres con el alfabeto código."""
    return "".join(sorted(set("".join(codigo))))

def longitudes_palabras(codigo) -> list:
    """9.b Genera una lista con las longitudes de las palabras utilizando comprensión de listas."""
    return [len(palabra) for palabra in codigo]

def Kraft(codigo):
    """9.c Calcula la sumatoria de la inecuación de Kraft utilizando las funciones anteriores."""
    r = len(alfabeto_codigo(codigo))
    li = longitudes_palabras(codigo)
    sumatoria = sum(r**(-l) for l in li)
    return round(sumatoria, 3)



def nosingular(codigo):
    for cod in codigo:
        if (codigo.count(cod)>1):
            return False
    return True



def instantaneo(codigo):
    for i in range(len(codigo)):
        for j in range(len(codigo)):
            if i != j and codigo[i].startswith(codigo[j]):
                return False
    return True 



def univoco(palabras):
    if not nosingular(palabras):
        return False

    U = set()
    n = len(palabras)

    # 1. diferencias iniciales
    for i in range(n):
        for j in range(n):
            if i != j and palabras[j].startswith(palabras[i]):
                resto = palabras[j][len(palabras[i]):]
                if resto:
                    U.add(resto)

    vistos = set()
    while U:
        if any(u in palabras for u in U):
            return False  # encontró contradicción
        if U in vistos:
            return True   # ya repitió → seguro es UD
        vistos.add(frozenset(U))

        # generar nuevos residuos
        nuevo = set()
        for u in U:
            for w in palabras:
                if w.startswith(u):
                    resto = w[len(u):]
                    if resto:
                        nuevo.add(resto)
                if u.startswith(w):
                    resto = u[len(w):]
                    if resto:
                        nuevo.add(resto)
        U = nuevo
    return True
 


def entropia(p, r=2):
    return p*(math.log(1/p)/math.log(r))



def entropia_fuente(probabilidades, r=2):
    acum=0
    for prob in probabilidades:
        acum+=entropia(prob, r)
    return acum



def informacion(p,n): 
    #N ES LA BASE, P ES LA PROBABILIDAD CON LA QUE SE CALCULARA LA INFORMACION
    return math.log(1/p) / math.log(n)



