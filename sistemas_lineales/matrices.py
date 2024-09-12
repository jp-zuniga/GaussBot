from os import system
from fractions import Fraction
from validaciones import *

def pedir_matriz():
    system("cls || clear")
    M = []

    # try/except para validar el input
    try:
        filas = int(input("\nIngrese el número de ecuaciones: "))
        if filas <= 0: raise ValueError
        columnas = int(input("Ingrese el número de variables: ")) + 1 # agregar la columna de constantes
        if columnas <= 0: raise ValueError
    except ValueError:
        input("\nError: Ingrese un número entero positivo!")
        return pedir_matriz() # volver a pedir los datos si hay error
    
    # usar while loops para que no siga al siguiente elemento si el input no es un número
    i = j = 0    
    while i < filas:
        fila = []
        print(f"\nEcuación {i+1}:")
        while j < columnas:
            try:
                # cambiar el mensaje a imprimir dependiendo si se esta pidiendo una variable o la constante
                if j != columnas-1: mensaje = f"-> X{j+1} = "
                else: mensaje = "-> b = "

                elemento = float(Fraction(input(mensaje)).limit_denominator())
                fila.append(elemento) # solo se agrega el elemento e incrementa j si la conversion del input funciona
                j += 1
            except ValueError: input("\nError: Ingrese un número real!\n")
            except ZeroDivisionError: input("\nError: El denominador no puede ser cero!\n")
            
        i += 1; j = 0 # resetear j para la siguiente fila
        M.append(fila)

    return M

def resolver_sistema():
    M = pedir_matriz()
    print("\nMatriz inicial:")
    imprimir_matriz(M)

    rectangular = len(M) < len(M[0]) - 1 # -1 para no contar la columna aumentada
    if rectangular: M = resolver_rectangular(M)
    else: M = resolver_cuadrada(M)

    return M

def resolver_cuadrada(M):
    filas = len(M)
    columnas = len(M[0])
    consistente = validar_consistencia(M)
    if not consistente[0]:
        imprimir_resultado(M, consistente)
        return None
    
    print("\nResolviendo por el Método Gaussiano:")

    # recorrer todas las filas para hacer una matriz triangular superior
    for i in range(filas):
        diagonal = M[i][i]

        # si el diagonal es igual a 0, buscar otra fila que tenga un coeficiente diferente a 0 en esa misma posicion e intercambiar las filas
        if diagonal == 0:
            for x in range(filas):
                if M[x][i] != 0:
                    M[i], M[x] = M[x], M[i]
                    diagonal = M[i][i] # reasignar el diagonal despues del cambio de fila

                    print(f"\nF{i+1} <==> F{x+1}")
                    imprimir_matriz(M)
                    break
        
        # si el diagonal no es 1, dividir toda la fila por el diagonal para que sea 1
        if diagonal != 1 and diagonal != 0:
            for g in range(columnas):
                M[i][g] /= diagonal
            
            if diagonal == -1: print(f"\nF{i+1} => -F{i+1}")
            else: print(f"\nF{i+1} => F{i+1} / {str(Fraction(diagonal).limit_denominator())}")
            imprimir_matriz(M)
        

        # hacer 0 todo debajo del diagonal:
        for j in range(i+1, filas):
            if i != j:
                factor = M[j][i]
                if factor == 0: continue # si ya es 0, saltarlo

                for k in range(columnas):
                    M[j][k] -= factor * M[i][k]
                    
                print(f"\nF{j+1} => F{j+1} - ({str(Fraction(factor).limit_denominator())} * F{i+1})")
                imprimir_matriz(M)
        
    # recorrer todas las filas y columnas (de derecha a izquierda y abajo para arriba, respectivamente) para llegar a la matriz unidad
    for i in reversed(range(filas)): # desde filas-1 hasta 0
        for j in reversed(range(i)): # desde la fila i-1 hasta 0
            factor = M[j][i]
            if factor == 0: continue # si ya es 0, saltarlo

            for k in range(columnas):
                M[j][k] -= factor * M[i][k]

            print(f"\nF{j+1} => F{j+1} - ({str(Fraction(factor).limit_denominator())} * F{i+1})")
            imprimir_matriz(M)

    consistente = validar_consistencia(M)
    if consistente[0]:
        imprimir_resultado(M, consistente)
        return M # solo retornar la matriz si tiene solucion
    return None

def resolver_rectangular(M):
    M = reducir_matriz(M)

    consistente = validar_consistencia(M)
    if not consistente[0]:
        imprimir_resultado(M, consistente)
        return None
    
    escalonada_reducida = validar_escalonada_reducida(M)
    if escalonada_reducida:
        imprimir_resultado(M, [True, None])
        return M
    
    filas = len(M)
    columnas = len(M[0])
    soluciones = []  # para almacenar las soluciones de cada variable
    libres = encontrar_variables_libres(M)

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
                        expresion += f"{signo}{abs(coeficiente)}*X{k+1}" if abs(coeficiente) != 1 else f"{signo}X{k+1}"
                soluciones.append(f"| X{j+1} = " + expresion)
                break
    
    # imprimir las soluciones en orden
    soluciones = sorted(soluciones, key=lambda x: x[3])
    print("\n| Sistema no tiene solución única!")
    print("| Solución general encontrada:")
    for solucion in soluciones:
        print(solucion)

    return M

def reducir_matriz(M):
    filas = len(M)
    columnas = len(M[0])
    filas_pivotes = []

    consistente = validar_consistencia(M)
    if not consistente[0]:
        imprimir_resultado(M, consistente)
        return M
    elif validar_escalonada(M): return M

    print("\nReduciendo la matriz a su forma escalonada:")

    # encontrar los elementos pivotes y eliminar los elementos debajo de cada uno
    for j in range(columnas-1):
        for i in range(filas):
            if i in filas_pivotes: continue
            pivote = M[i][j]

            # si el elemento actual es 0, buscar otro elemento en la misma columna que no sea 0, e intercambiar las filas
            if pivote == 0:
                for h in range(i+1, filas):
                    if M[h][j] != 0:
                        M[i], M[h] = M[h], M[i]
                        pivote = M[i][j] # reasignar el pivote despues del intercambio

                        print(f"\nF{i+1} <==> F{h+1}")
                        imprimir_matriz(M)
                        break
            
            if pivote == 0: break # si sigue siendo 0, no hay pivote en esta columna
            filas_pivotes.append(i) # guardar el indice de la columna pivote

            for k in range(i+1, filas):
                factor = M[k][j] / pivote
                if factor == 0: continue

                for l in range(columnas):
                    M[k][l] -= factor * M[i][l]
                
                print(f"\nF{k+1} => F{k+1} - ({str(Fraction(factor).limit_denominator())} * F{i+1})")
                imprimir_matriz(M)
    
    # convertir los pivotes en 1 y eliminar los elementos encima de cada uno
    for j in reversed(range(columnas-1)):
        for i in reversed(range(filas)):
            if M[i][j] == 0: continue # si el elemento es 0, no es un pivote
            pivote = M[i][j]

            for l in range(columnas):
                M[i][l] /= pivote
            
            print(f"\nF{i+1} => F{i+1} / {str(Fraction(pivote).limit_denominator())}")
            imprimir_matriz(M)
            
            for k in range(i):
                factor = M[k][j]
                for l in range(columnas):
                    M[k][l] -= factor * M[i][l]
                
                print(f"\nF{k+1} => F{k+1} - ({str(Fraction(factor).limit_denominator())} * F{i+1})")
                imprimir_matriz(M)

            break # ir al siguiente pivote
    return M

def imprimir_resultado(M, validacion):
    filas = len(M)
    solucion, i = validacion

    if solucion:
        for i in range(filas):
            print("\n| Solución encontrada:", end='')
            print(f"\n| X{i+1} = {str(Fraction(M[i][-1]).limit_denominator())}", end='')
        input('')
    
    else:
        print(f"\n| En F{i+1}: 0 != {str(Fraction(M[i][-1]).limit_denominator())}")
        input("| Sistema es inconsistente!")

    return

def imprimir_matriz(M):
    filas = len(M)
    columnas = len(M[0])

    # calcular la longitud maxima de los elementos para alinearlos y siempre mantener el formato:
    # - crear una lista de las longitudes de todos los elementos de la matriz (con list comprehension)
    # - encontrar la longitud maxima en esa lista con la funcion max()
    max_len = max(len(str(Fraction(M[i][j]).limit_denominator())) for i in range(filas) for j in range(columnas))

    for i in range(filas):
        for j in range(columnas):
            # convertir el elemento actual a un string y ajustarlo a la derecha de la longitud maxima
            elemento = str(Fraction(M[i][j]).limit_denominator()).center(max_len)

            # si es el primer elemento, imprimir el | y una coma despues del elemento
            if j == 0:
                print(f"| {elemento}", end=", ")

            # si el es el ultimo elemento, cerrar el |, e imprimir un salto de linea
            elif j == columnas-1:
                print(f"{elemento} |")

            # si es un elemento en medio, solo imprimir la coma despues del elemento    
            else:
                print(f"{elemento}", end=", ")
    return
