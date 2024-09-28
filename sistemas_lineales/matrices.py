from fractions import Fraction
from validaciones import *

# funciones para trabajar con matrices y resolver sistemas de ecuaciones:
# --------------------------------------------------------------------------------

def pedir_matriz(aumentada=True, nombre='M'):
    M = []
    output = ["ecuaciones", "variables"] if aumentada else ["filas", "columnas"]
    print("\nDatos de la matriz " + nombre + ":")
    print("-------------------------------", end='')

    # try/except para validar el input
    try:
        filas = int(input(f"\nIngrese el número de {output[0]}: "))
        if filas <= 0: raise ValueError
        columnas = int(input(f"Ingrese el número de {output[1]}: "))
        if columnas <= 0: raise ValueError
    except ValueError:
        input("\nError: Ingrese un número entero positivo!")
        return pedir_matriz(False, 'A') # volver a pedir los datos si hay error
    
    # usar while loops para que solo siga al siguiente 
    i = j = 0
    if aumentada: columnas += 1 # +1 para la columna aumentada si se llama con True
    while i < filas:
        fila = []
        print(f"\nFila {i+1}:")
        while j < columnas: 
            try:
                # cambiar el mensaje a imprimir dependiendo si se esta pidiendo una variable o la constante
                if not aumentada: mensaje = f"-> X{j+1} = "
                else:
                    if j != columnas-1: mensaje = f"-> X{j+1} = "
                    else: mensaje = "-> b = "

                elemento = Fraction(input(mensaje)).limit_denominator()
                fila.append(elemento) # solo se agrega el elemento e incrementa j si la conversion del input funciona
                j += 1
            except ValueError: input("\nError: Ingrese un número real!")
            except ZeroDivisionError: input("\nError: El denominador no puede ser cero!")
            
        i += 1; j = 0 # resetear j para la siguiente fila
        M.append(fila)

    return M

def resolver_sistema():
    M = pedir_matriz()
    limpiar_pantalla()
    M = reducir_matriz(M)
    if not M: return None

    consistente = validar_consistencia(M)
    if not consistente[0]:
        imprimir_resultado(M, consistente)
        return None
    
    escalonada_reducida = validar_escalonada_reducida(M)
    libres = encontrar_variables_libres(M)
    if escalonada_reducida and not libres:
        imprimir_resultado(M, [True, None])
        return M
    
    filas = len(M)
    columnas = len(M[0])
    soluciones = []  # para almacenar las soluciones de cada variable

    for variable in libres:
        soluciones.append(f"| X{variable+1} es libre")
    
    # recorrer las filas para encontrar las soluciones de las variables
    for i in range(filas):
        for j in range(columnas-1):            
            if M[i][j] != 0:
                # construir la expresion para la variable en terminos de las variables libres
                constante = Fraction(M[i][-1]).limit_denominator()
                expresion = str(constante) if constante != 0 else ""

                # pasar las variables a la derecha de la ecuacion
                for k in range(j+1, columnas-1):
                    if M[i][k] != 0:
                        coeficiente = Fraction(-M[i][k]).limit_denominator()
                        signo = "+" if coeficiente > 0 else "-"
                        if len(expresion) > 0: signo = " " + signo + " "
                        else: signo = "" if signo == "+" else "-"
                        expresion += f"{signo}{abs(coeficiente)}*X{k+1}" if abs(coeficiente) != 1 else f"{signo}X{k+1}"
                if expresion == "": expresion = "0"
                soluciones.append(f"| X{j+1} = " + expresion)
                break
    
    # imprimir las soluciones en orden
    soluciones.sort(key=lambda x: x[3])
    print("\n| Sistema no tiene solución única!")
    print("| Solución general encontrada:")
    for solucion in soluciones: print(solucion)

    return M

def reducir_matriz(M):
    filas = len(M)
    columnas = len(M[0])

    consistente = validar_consistencia(M)
    if not consistente[0]:
        imprimir_resultado(M, consistente)
        return None

    print("\nMatriz inicial:")
    imprimir_matriz(M)
    print("\nReduciendo la matriz a su forma escalonada:\n")

    # encontrar los pivotes y eliminar los elementos debajo de ellos
    fila_actual = 0
    for j in range(columnas-1):
        fila_pivote = None
        maximo = 0

        # buscar la entrada con el valor mas grande para usarla como pivote
        for i in range (fila_actual, filas):
            if abs(M[i][j]) > maximo:
                maximo = M[i][j]
                fila_pivote = i
        
        # si fila_pivote sigue siendo None, significa que todas las entradas de la columna son 0 y no hay pivote
        if fila_pivote is None or maximo == 0: continue # entonces se pasa a la siguiente columna

        # si la fila actual no es la pivote, se intercambian
        if fila_pivote != fila_actual:
            M[fila_actual], M[fila_pivote] = M[fila_pivote], M[fila_actual]
            print(f"F{fila_actual+1} <==> F{fila_pivote+1}")
            imprimir_matriz(M)
        
        # si el diagonal no es 1, dividir toda la fila por el diagonal para que sea 1
        if M[fila_actual][j] != 1 and M[fila_actual][j] != 0:
            pivote = M[fila_actual][j]
            for k in range(columnas):
                M[fila_actual][k] /= pivote

            if pivote == -1: print(f"\nF{fila_actual+1} => -F{fila_actual+1}")
            else: print(f"\nF{fila_actual+1} => F{fila_actual+1} / {str(Fraction(pivote).limit_denominator())}")
            imprimir_matriz(M)

        # eliminar los elementos debajo del pivote
        for f in range (fila_actual+1, filas):
            if M[f][j] != 0:
                factor = M[f][j]
                for k in range(columnas):
                    M[f][k] -= factor * M[fila_actual][k]

                print(f"\nF{fila_actual+1} => F{fila_actual+1} - ({str(Fraction(factor).limit_denominator())} * F{fila_pivote+1})")
                imprimir_matriz(M)

        fila_actual += 1 # ir a la siguiente fila

    # se termina de reducir la matriz, eliminando los elementos encima de los pivotes
    for i in reversed(range(filas)):
        columna_pivote = None
        for k in range(columnas-1): # buscar el pivote de la fila actual
            if M[i][k] != 0:
                columna_pivote = k
                break
            
        # si columna_pivote sigue siendo None, no hay entrada pivote en la fila, y se pasa a la siguiente
        if columna_pivote is None: continue

        # eliminar los elementos encima del pivote
        for f in reversed(range(i)):
            if M[f][columna_pivote] != 0:
                factor = M[f][columna_pivote]
                for k in range(columnas):
                    M[f][k] -= factor * M[i][k]
                    
                print(f"\nF{f+1} => F{f+1} - ({str(Fraction(factor).limit_denominator())} * F{i+1})")
                imprimir_matriz(M)

    return M

def imprimir_resultado(M, validacion, libres=None):
    filas = len(M)
    solucion, i = validacion

    if solucion:
        print("\n| Solución encontrada:", end='')
        for i in range(filas):
            if all(val == 0 for val in M[i]): continue
            print(f"\n| X{i+1} = {str(Fraction(M[i][-1]).limit_denominator())}", end='')
        input('')
    
    else:
        print(f"\n| En F{i+1}: 0 != {str(Fraction(M[i][-1]).limit_denominator())}")
        input("| Sistema es inconsistente!")

    return None

def imprimir_matriz(M, vectorial=False):
    filas = len(M)
    columnas = len(M[0])

    # calcular la longitud maxima de los elementos para alinearlos y siempre mantener el formato:
    # - crear una lista de las longitudes de todos los elementos de la matriz (con una list comprehension)
    # - encontrar la longitud maxima en esa lista con la funcion max()
    max_len = max(len(str(Fraction(M[i][j]).limit_denominator())) for i in range(filas) for j in range(columnas))

    for i in range(filas):
        for j in range(columnas):
            # convertir el elemento actual a un string y ajustarlo a la derecha de la longitud maxima
            elemento = str(Fraction(M[i][j]).limit_denominator()).center(max_len)

            # si es el primer elemento, imprimir el ( y una coma despues del elemento
            if j == 0: print(f"( {elemento}", end=", ")

            # si es el penultimo elemento, imprimir el ) para separar las variables de las constantes
            elif j == columnas-2 and not vectorial: print(f"{elemento} |", end=' ')

            # si el es el ultimo elemento, cerrar el ), e imprimir un salto de linea
            elif j == columnas-1: print(f"{elemento} )")

            # si es un elemento en medio, solo imprimir la coma despues del elemento    
            else: print(f"{elemento}", end=", ")

    return None
