from math import ceil
from fractions import Fraction
from matrices import pedir_matriz, imprimir_matriz
from validaciones import limpiar_pantalla

# funciones para realizar operaciones con vectores:
# -------------------------------------------------------

def imprimir_vectores(lista_vecs, matricial=False):
    mensaje = "seleccionados" if matricial else "ingresados"
    if not lista_vecs: print("\nNo hay vectores ingresados!")
    else:
        print(f"\nVectores {mensaje}:")
        for nombre, vector in lista_vecs.items():
            vec = [str(Fraction(x).limit_denominator().limit_denominator()) for x in vector]
            print(f"{nombre}: {vec}")
    
    return None

def menu_vectores(lista_vecs=None):
    limpiar_pantalla()
    print("\n###############################")
    print("### Operaciones Vectoriales ###")
    print("###############################")
    imprimir_vectores(lista_vecs)
    print("\n1. Agregar un vector\n")
    print("2. Producto matriz-vector")
    print("3. Multiplicación escalar")
    print("4. Multiplicación de vectores")
    print("5. Suma de vectores")
    print("6. Resta de vectores")
    print("7. Regresar al menú principal")

    try:
        option = int(input("\nSeleccione una opción: "))
        if option < 1 or option > 7: raise ValueError
    except ValueError:
        input("\nError: Ingrese una opción válida!")
        return menu_vectores(lista_vecs)
    
    return option

def operaciones_vectoriales():
    lista_vecs = {}
    option = menu_vectores(lista_vecs)

    while option != 7:
        match option:
            case 1:
                limpiar_pantalla()
                lista_vecs = agregar_vector(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue

            case 2:
                limpiar_pantalla()
                if not lista_vecs:
                    input("\nError: No hay vectores ingresados!")
                    option = menu_vectores(lista_vecs)
                    continue
                elif len(lista_vecs) == 1:
                    input("\nError: Deben haber al menos dos vectores ingresados!")
                    option = menu_vectores(lista_vecs)
                    continue
                
                A = pedir_matriz(False, 'A')
                A = matriz_por_suma_vectores(A, lista_vecs)
                option = menu_vectores(lista_vecs)
                continue
            
            case 3:
                lista_vecs = mult_escalar(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue
            
            case 4:
                lista_vecs = mult_vectorial(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue

            case 5:
                limpiar_pantalla()
                input_suma_resta(lista_vecs, True)
                option = menu_vectores(lista_vecs)
                continue

            case 6:
                limpiar_pantalla()
                input_suma_resta(lista_vecs, False)
                option = menu_vectores(lista_vecs)
                continue

            case 7: break
            case _:
                input("\nOpción inválida...")
                continue

    input("\nRegresando al menú principal...")
    return None

def agregar_vector(lista_vecs):
    limpiar_pantalla()
    try:
        nombre = input("Ingrese el nombre del vector (una letra minúscula): ").lower()
        if not nombre.isalpha() or len(nombre) != 1: raise NameError
        if nombre in lista_vecs: raise KeyError
        longitud = int(input(f"¿Cuántas dimensiones tendrá el vector? "))
    except NameError:
        input("Error: Ingrese solamente una letra minúscula!")
        return agregar_vector(lista_vecs)
    except ValueError:
        input("Error: Ingrese un número entero!")
        return agregar_vector(lista_vecs)
    except KeyError:
        input(f"Error: Ya hay un vector con el nombre '{nombre}'!")
        return agregar_vector(lista_vecs)

    vec = ingresar_vector(longitud)
    lista_vecs[nombre] = vec
    print(f"Vector agregado exitosamente!")

    continuar = input("\n¿Desea agregar otro vector? (s/n) ")
    if continuar.lower() == 's': return agregar_vector(lista_vecs)
    elif continuar.lower() == 'n': 
        input("Regresando al menú de vectores...")
        return lista_vecs
    else:
        input("Opción inválida! Regresando al menú de vectores...")
        return lista_vecs

def ingresar_vector(longitud):
    try:
        vec = [Fraction(x).limit_denominator() for x in input(f"\nIngrese los componentes (separados por espacios): ").split()]
        if len(vec) != longitud: raise TypeError
    except TypeError:
        input("Error: El vector no tiene las dimensiones correctas!")
        return ingresar_vector(longitud)
    except ValueError:
        input("Error: Ingrese un número real!")
        return ingresar_vector(longitud)

    return vec

def mult_escalar(lista_vecs):
    limpiar_pantalla()
    if not lista_vecs:
        input("\nError: No hay vectores ingresados!")
        return lista_vecs
    
    try:
        imprimir_vectores(lista_vecs)
        vec_nombre = input("\n¿Cuál vector desea multiplicar escalarmente? ")
        if vec_nombre not in lista_vecs: raise KeyError(vec_nombre)
        escalar = Fraction(input("Ingrese el escalar: "))
    except KeyError:
        input(f"Error: El vector '{vec_nombre}' no existe!")
        return mult_escalar(lista_vecs)
    except ValueError:
        input("Error: Ingrese un número real!")
        return mult_escalar(lista_vecs)
    
    lista_vecs[vec_nombre] = [Fraction(x*escalar) for x in lista_vecs[vec_nombre]]
    imprimir_escalar = escalar if escalar.is_integer() else f"({str(Fraction(escalar))})*"
    input(f"\n{imprimir_escalar}{vec_nombre} = {[str(Fraction(x).limit_denominator()) for x in lista_vecs[vec_nombre]]}")
    return lista_vecs

def mult_vectorial(lista_vecs):
    limpiar_pantalla()
    if not lista_vecs:
        input("\nError: No hay vectores ingresados!")
        return lista_vecs
    elif len(lista_vecs) == 1:
        input("\nError: Deben haber dos vectores ingresados!")
        return lista_vecs
    
    try:
        imprimir_vectores(lista_vecs)
        vec1 = input("\nIngrese el nombre del primer vector: ")
        if vec1 not in lista_vecs: raise KeyError(vec1)
        vec2 = input("Ingrese el nombre del segundo vector: ")
        if vec2 not in lista_vecs: raise KeyError(vec2)
        if len(lista_vecs[vec1]) != len(lista_vecs[vec2]): raise ArithmeticError    
    except KeyError as k:
        input(f"Error: El vector '{k}' no existe!")
        return mult_vectorial(lista_vecs)
    except ArithmeticError:
        input("Error: Los vectores deben tener la misma longitud!")
        return mult_vectorial(lista_vecs)

    producto_punto = sum(lista_vecs[vec1][i] * lista_vecs[vec2][i] for i in range(len(lista_vecs[vec1])))
    input(f"\n{vec1}.{vec2} = {str(Fraction(producto_punto))}")
    return lista_vecs

def input_suma_resta(lista_vecs, option, matricial=False):
    if not lista_vecs:
        input("\nError: No hay vectores ingresados!")
        return lista_vecs
    elif len(lista_vecs) == 1:
        input("\nError: Deben haber al menos dos vectores ingresados!")
        return lista_vecs
    
    try:
        imprimir_vectores(lista_vecs)
        operacion = "sumar" if option else "restar"
        input_vecs = input(f"\n¿Cuáles vectores desea {operacion}? (separados por espacios): ").split()
        if len(input_vecs) <= 1 or (matricial and len(input_vecs) != 2): raise IndexError

        for vec in input_vecs:
            if vec not in lista_vecs: raise KeyError(vec)
            
        if not all(len(lista_vecs[j]) == len(lista_vecs[input_vecs[0]]) for j in input_vecs):
            raise ArithmeticError
        
    except KeyError as k:
        input(f"Error: El vector '{k}' no existe!")
        return input_suma_resta(lista_vecs, option, matricial)
    except IndexError:
        error = "dos vectores para realizar el producto matriz-vector" if matricial else "dos o más vectores para sumar"
        input(f"Error: Debe ingresar {error}!")
        return input_suma_resta(lista_vecs, option, matricial)
    except ArithmeticError:
        input("Error: Los vectores deben tener la misma longitud!")
        return input_suma_resta(lista_vecs, option, matricial)

    if matricial: return input_vecs
    
    if option:
        resultado = sumar_vectores(input_vecs, lista_vecs)
        signo = "+"
    else:
        resultado = restar_vectores(input_vecs, lista_vecs)
        signo = "-"

    mensaje = ""
    for i in input_vecs:
        if i != input_vecs[-1]: mensaje += f"{i} {signo} "
        else: mensaje += f"{i}"

    input(f"\n{mensaje} = {[str(Fraction(x).limit_denominator()) for x in resultado]}")
    return None

def sumar_vectores(input_vecs, lista_vecs):
    suma_vecs = [0 for _ in lista_vecs[input_vecs[0]]]
    for i in range(len(suma_vecs)):
        for j in input_vecs:
            suma_vecs[i] += lista_vecs[j][i]
    
    return suma_vecs

def restar_vectores(input_vecs, lista_vecs):
    resta_vecs = lista_vecs[input_vecs[0]]
    for i in range(len(resta_vecs)):
        for j in input_vecs[1:]:
            resta_vecs[i] -= lista_vecs[j][i]
    
    return resta_vecs

def matriz_por_suma_vectores(A, lista_vecs):
    limpiar_pantalla()
    resultado = []
    
    input_vecs = input_suma_resta(lista_vecs, option=True, matricial=True) # pedir los vectores
    suma_vecs = sumar_vectores(input_vecs, lista_vecs) # sumar los vectores seleccionados
    u, v = lista_vecs[input_vecs[0]], lista_vecs[input_vecs[1]]
    
    if len(A[0]) != len(lista_vecs[input_vecs[0]]):
        input("\nError: Las dimensiones de A y los vectores no son compatibles!")
        return matriz_por_suma_vectores(A, lista_vecs)

    # calcular A(u + v)
    for i in range(len(suma_vecs)):
        resultado.append(sum([A[i][j] * suma_vecs[j] for j in range(len(suma_vecs))]))
    
    imprimir_MPSV(A, input_vecs, lista_vecs, suma_vecs, resultado) # imprimir las operaciones realizadas
    resolver = input("\nDesea comprobar la propiedad distributiva (A(u + v) = Au + Av)? (s/n) ")
    
    if resolver.lower() == 's': suma_matriz_por_vector(A, input_vecs, lista_vecs)
    elif resolver.lower() != 'n':
        input("Opción inválida! Regresando al menú de vectores...")
        return resultado

    return resultado

def suma_matriz_por_vector(A, input_vecs, lista_vecs):
    limpiar_pantalla()
    u, v = lista_vecs[input_vecs[0]], lista_vecs[input_vecs[1]]
    resultado_u = []
    resultado_v = []

    # calcular Au y Av
    for i in range(len(u)):
        resultado_u.append(sum([A[i][j] * u[j] for j in range(len(u))]))
        resultado_v.append(sum([A[i][j] * v[j] for j in range(len(v))]))

    imprimir_SMPV(A, input_vecs, lista_vecs, resultado_u, resultado_v) # imprimir las operaciones realizadas
    input("\nLa respuesta sigue siendo la misma, asi que la propiedad distributiva se cumple!")
    return resultado_u, resultado_v

def imprimir_MPSV(A, input_vecs, lista_vecs, suma_vecs, resultado): 
    filas = len(A)
    columnas = len(A[0])
    u, v = lista_vecs[input_vecs[0]], lista_vecs[input_vecs[1]]

    limpiar_pantalla()
    print("\nMatriz A:")
    imprimir_matriz(A, True)
    imprimir_vectores({input_vecs[0]: u, input_vecs[1]: v}, True)

    # guardar las longitudes de todos los elementos en u y v
    longitudes = [len(str(i)) for i in u]
    longitudes += [len(str(j)) for j in v]

    # encontrar la longitud maxima de todos los elementos de todas las listas (u, v, suma_vecs, A, resultado)
    max_uv = max(longitudes)
    max_suma = max(len(str(k)) for k in suma_vecs)
    max_A = max(len(str(A[i][j])) for i in range(filas) for j in range(columnas))
    max_resultado = max(len(str(resultado[i])) for i in range(filas))

    # imprimir procedimiento de u + v
    print("\nu + v:")
    for i in range(len(u)):
        signo = "+" if v[i] > 0 else "-"

        if len(u) % 2 == 0: igual = '=' if (i == ceil(len(u) / 2)) else ' '
        else: igual = '=' if (i == len(u) // 2) else ' '

        uv = f"{str(u[i]).center(max_uv)} {signo} {str(abs(v[i])).center(max_uv)}"
        print(f"[ {uv} ] {igual} [ {str(suma_vecs[i]).center(max_suma)} ]")

    # imprimir procedimiento de A(u + v)
    operaciones = []
    for j in range(filas):
        fila = ""
        for k in range(columnas):
            linea = f"({str(A[j][k]).center(max_A)} * {str(suma_vecs[k]).center(max_A)})"
            if k == 0: linea = f"[ {linea} + "
            elif k == columnas-1: linea = f"{linea} ]"
            else: linea = f"{linea} + "
            fila += linea
        
        operaciones.append(fila)

    print("\nA(u + v):")
    for k in range(len(operaciones)):
        if len(operaciones) % 2 == 0: igual = '=' if (k == ceil(len(operaciones) / 2)) else ' '
        else: igual = '=' if (k == len(operaciones) // 2) else ' '

        print(f"{operaciones[k]} {igual} [ {str(resultado[k]).center(max_resultado)} ]")

    return None

def imprimir_SMPV(A, input_vecs, lista_vecs, resultado_u, resultado_v):
    filas = len(A)
    columnas = len(A[0])
    u, v = lista_vecs[input_vecs[0]], lista_vecs[input_vecs[1]]

    limpiar_pantalla()
    print("\nMatriz A:")
    imprimir_matriz(A, True)
    imprimir_vectores({input_vecs[0]: u, input_vecs[1]: v}, True)

    # guardar las longitudes de todos los elementos en u y v
    longitudes = [len(str(i)) for i in u]
    longitudes += [len(str(j)) for j in v]

    # encontrar la longitud maxima de todos los elementos de todas las listas (u, v, A, resultado_u, resultado_v)
    max_A = max(len(str(A[i][j])) for i in range(filas) for j in range(columnas))
    max_resultado_u = max(len(str(resultado_u[i])) for i in range(filas))
    max_resultado_v = max(len(str(resultado_v[i])) for i in range(filas))

    # guardar procedimiento de Au
    operaciones_u = []
    for j in range(filas):
        fila = ""
        for k in range(columnas):
            linea = f"({str(A[j][k]).center(max_A)} * {str(u[k]).center(max_A)})"
            if k == 0: linea = f"[ {linea} + "
            elif k == columnas-1: linea = f"{linea} ]"
            else: linea = f"{linea} + "
            fila += linea
        
        operaciones_u.append(fila)

    print("\nAu:") # imprimir procedimiento
    for k in range(len(operaciones_u)):
        if len(operaciones_u) % 2 == 0: igual = '=' if (k == ceil(len(operaciones_u) / 2)) else ' '
        else: igual = '=' if (k == len(operaciones_u) // 2) else ' '

        print(f"{operaciones_u[k]} {igual} [ {str(resultado_u[k]).center(max_resultado_u)} ]")

    # guardar procedimiento de Av
    operaciones_v = []
    for j in range(filas):
        fila = ""
        for k in range(columnas):
            linea = f"({str(A[j][k]).center(max_A)} * {str(v[k]).center(max_A)})"
            if k == 0: linea = f"[ {linea} + "
            elif k == columnas-1: linea = f"{linea} ]"
            else: linea = f"{linea} + "
            fila += linea
        
        operaciones_v.append(fila)

    print("\nAv:") # imprimir procedimiento
    for k in range(len(operaciones_v)):
        if len(operaciones_v) % 2 == 0: igual = '=' if (k == ceil(len(operaciones_v) / 2)) else ' '
        else: igual = '=' if (k == len(operaciones_v) // 2) else ' '

        print(f"{operaciones_v[k]} {igual} [ {str(resultado_v[k]).center(max_resultado_v)} ]")

    # calcular y imprimir procedimiento de Au + Av
    resultado_suma = [resultado_u[i] + resultado_v[i] for i in range(filas)]
    max_resultado_suma = max(len(str(resultado_suma[i])) for i in range(filas))

    print("\nAu + Av:")
    for i in range(filas):
        print(f"[ {str(resultado_u[i]).center(max_resultado_u)} + {str(resultado_v[i]).center(max_resultado_v)} ] = [ {str(resultado_suma[i]).center(max_resultado_suma)} ]")
    
    return None
