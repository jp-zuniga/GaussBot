from fractions import Fraction
from validaciones import validar_consistencia, validar_escalonada_reducida, encontrar_variables_libres
from utils import Tuple, List, Matriz, limpiar_pantalla

# funciones para trabajar con matrices y resolver sistemas de ecuaciones
# --------------------------------------------------------------------------------

def pedir_matriz(aumentada=True, nombre='M') -> Matriz:
    M = []
    mensaje = ["ecuaciones", "variables"] if aumentada else ["filas", "columnas"]

    print(f"\nDatos de la matriz {nombre}:")
    print("----------------------------", end='')
    try:
        filas = int(input(f"\nIngrese el número de {mensaje[0]}: "))
        if filas <= 0: raise ValueError
        columnas = int(input(f"Ingrese el número de {mensaje[1]}: "))
        if columnas <= 0: raise ValueError
    except ValueError:
        input("\nError: Ingrese un número entero positivo!")
        return pedir_matriz(aumentada, nombre)
    
    fila_actual = 0
    if aumentada: columnas += 1 # si se esta pidiendo una matriz aumentada, incrementar las columnas por 1

    while fila_actual < filas:
        columna_actual = 0
        f = []

        print(f"\nFila {fila_actual+1}:")
        while columna_actual < columnas: 
            try:
                if not aumentada or columna_actual != columnas-1: mensaje = f"-> X{columna_actual+1} = "
                else: mensaje = "-> b = "

                elemento = Fraction(input(mensaje)).limit_denominator() # si el usuario ingresa algo invalido, se salta a los excepts
                f.append(elemento) # si no, se agrega el elemento y se incrementa columna_actual
                columna_actual += 1
            except ValueError: input("\nError: Ingrese un número real!")
            except ZeroDivisionError: input("\nError: El denominador no puede ser cero!")
            
        fila_actual += 1
        M.append(f)

    return M

def resolver_sistema() -> Matriz | None:
    M = pedir_matriz()
    limpiar_pantalla()
    M = reducir_matriz(M)
    if not M: return None # si reducir_matriz() retorna None, no se puede resolver el sistema
    
    libres = encontrar_variables_libres(M)
    if validar_escalonada_reducida(M) and not libres:
        # si la matriz esta en su forma escalonada reducida y no hay variables libres,
        imprimir_soluciones(M, unica=True, libres=None, validacion=(True, None)) # imprimir la solucion unica
        return M
    
    imprimir_soluciones(M, unica=False, libres=libres, validacion=(True, None)) # imprimir la solucion general
    return M

def reducir_matriz(M: Matriz) -> Matriz | None:
    filas = len(M)
    columnas = len(M[0])
    if not validar_matriz(M): return None

    print("\nMatriz inicial:")
    imprimir_matriz(M)
    print("\nReduciendo la matriz a su forma escalonada:")

    # encontrar los pivotes y eliminar los elementos debajo de ellos
    fila_actual = 0
    for j in range(columnas-1):
        fila_pivote = None
        maximo = 0

        # buscar la entrada con el valor mas grande para usarla como pivote
        for i in range(fila_actual, filas):
            if abs(M[i][j]) > maximo:
                maximo = M[i][j]
                fila_pivote = i
        
        # si fila_pivote sigue siendo None, significa que todas las entradas de la columna son 0
        # entonces no hay pivote y se pasa a la siguiente columna
        if fila_pivote is None or maximo == 0: continue

        # si la fila actual no es la pivote, se intercambian
        if fila_pivote != fila_actual:
            M[fila_actual], M[fila_pivote] = M[fila_pivote], M[fila_actual]
            print(f"\nF{fila_actual+1} <==> F{fila_pivote+1}")
            imprimir_matriz(M)
        
        # si el diagonal no es 1, dividir toda la fila por el diagonal para que sea 1
        if M[fila_actual][j] != 1 and M[fila_actual][j] != 0:
            pivote = M[fila_actual][j]
            for k in range(columnas):
                M[fila_actual][k] /= pivote

            if pivote == -1: print(f"\nF{fila_actual+1} => -F{fila_actual+1}")
            else: print(f"\nF{fila_actual+1} => F{fila_actual+1} / {str(pivote.limit_denominator())}")
            imprimir_matriz(M)

        # eliminar los elementos debajo del pivote
        for f in range(fila_actual+1, filas):
            if M[f][j] != 0:
                factor = M[f][j]
                for k in range(columnas):
                    M[f][k] -= factor * M[fila_actual][k]

                print(f"\nF{fila_actual+1} => F{fila_actual+1} - ({str(factor.limit_denominator())} * F{fila_pivote+1})")
                imprimir_matriz(M)

        fila_actual += 1 # ir a la siguiente fila

    # se termina de reducir la matriz, eliminando los elementos encima de los pivotes
    for i in reversed(range(filas)):
        try: columna_pivote = M[i].index(next(filter(lambda x: x != 0, M[i])))
        except StopIteration: columna_pivote = None
            
        # si columna_pivote es None, no hay entrada pivote en la fila, y se pasa a la siguiente
        if columna_pivote is None: continue

        # eliminar los elementos encima del pivote
        for f in reversed(range(i)):
            factor = M[f][columna_pivote]
            if factor == 0: continue
                
            for k in range(columnas):
                M[f][k] -= factor * M[i][k]
                
            print(f"\nF{f+1} => F{f+1} - ({str(factor.limit_denominator())} * F{i+1})")
            imprimir_matriz(M)

    # validar si la matriz resultante es consistente
    if not validar_matriz(M): return None
    return M

def despejar_variables(M: Matriz, libres: List[int]) -> List[str]:
    filas = len(M)
    columnas = len(M[0])
    ecuaciones = [] # almacenar las ecuaciones de cada variable
    for variable in libres:
        ecuaciones.append(f"| X{variable+1} es libre")
    
    # recorrer las filas para encontrar las ecuaciones de las variables
    for i in range(filas):
        for j in range(columnas-1):            
            if M[i][j] != 0:
                # construir la expresion para la variable en terminos de las variables libres
                constante = M[i][-1].limit_denominator()
                expresion = str(constante) if constante != 0 else ''

                # pasar las variables a la derecha de la ecuacion
                for k in range(j+1, columnas-1):
                    if M[i][k] != 0:
                        coeficiente = -M[i][k].limit_denominator()
                        signo = '+' if coeficiente > 0 else '-'
                        if len(expresion) > 0: signo = f" {signo} "
                        else: signo = '' if signo == '+' else '-'
                        expresion += f"{signo}{abs(coeficiente)}*X{k+1}" if abs(coeficiente) != 1 else f"{signo}X{k+1}"
                if expresion == '': expresion = '0'
                ecuaciones.append(f"| X{j+1} = " + expresion)
                break
    
    # retornar las ecuaciones en orden
    ecuaciones.sort(key=lambda x: x[3])
    return ecuaciones

def imprimir_soluciones(M: Matriz, unica: bool, validacion: Tuple, libres: List[int | None]) -> None:
    filas = len(M)
    solucion, fila_inconsistente = validacion # unpack la validacion

    if not solucion: # si no hay solucion, imprimir la fila inconsistente y retornar
        print(f"\n| En F{fila_inconsistente+1}: 0 != {str(M[fila_inconsistente][-1].limit_denominator())}")
        input("| Sistema es inconsistente!")
        return None
    elif unica: # imprimir la solucion unica
        print("\n| Solución encontrada:")
        for i in range(filas):
            if all(x == 0 for x in M[i]): continue
            print(f"| X{i+1} = {str(M[i][-1].limit_denominator())}")
        return None
    
    # si no se cumplieron las condiciones anteriores, el sistema tiene una solucion general
    ecuaciones = despejar_variables(M, libres)
    print("\n| Sistema no tiene solución única!")
    print("| Solución general encontrada:")
    for linea in ecuaciones: print(linea)
    return None

def imprimir_matriz(M: Matriz, vectorial=False) -> None:
    filas = len(M)
    columnas = len(M[0])

    # calcular la longitud maxima de los elementos para alinearlos y siempre mantener el formato:
    # - crear una lista de las longitudes de todos los elementos de la matriz
    # - encontrar la longitud maxima en esa lista con max()
    max_len = max(len(str(M[i][j].limit_denominator())) for i in range(filas) for j in range(columnas))

    for i in range(filas):
        for j in range(columnas):
            # convertir el elemento actual a un string y ajustarlo a la derecha de la longitud maxima
            elemento = str(M[i][j].limit_denominator()).center(max_len)

            # si es el primer elemento, imprimir el ( y una coma despues del elemento
            if j == 0: print(f"( {elemento}, ", end='')

            # si es el penultimo elemento, imprimir el | para separar las columnas
            elif j == columnas-2 and not vectorial: print(f"{elemento} |", end=' ')

            # si el es el ultimo elemento, cerrar el )
            elif j == columnas-1: print(f"{elemento} )")

            # si es un elemento en medio, solo imprimir la coma despues del elemento    
            else: print(f"{elemento}, ", end='')

    return None

def validar_matriz(M: Matriz) -> bool:
    consistente = validar_consistencia(M)
    if not consistente[0]:
        imprimir_soluciones(M, unica=False, libres=None, validacion=consistente)
        return False
    else: return True
