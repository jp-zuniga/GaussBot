from os import system
from fractions import Fraction
from matrices import pedir_matriz

# funciones para realizar operaciones con vectores:
# -------------------------------------------------------

def imprimir_vectores(lista_vecs):
    if not lista_vecs: print("\nNo hay vectores ingresados!")
    else:
        print("\nVectores ingresados:")
        for nombre, vector in lista_vecs.items():
            vec = [str(Fraction(x).limit_denominator().limit_denominator()) for x in vector]
            print(f"{nombre}: {vec}")
    
    return None

def menu_vectores(lista_vecs=None):
    system('cls || clear')
    print("\n###############################")
    print("### Operaciones de Vectores ###")
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

def operaciones_vectores():
    lista_vecs = {}
    option = menu_vectores(lista_vecs)

    while option != 7:
        match option:
            case 1:
                lista_vecs = agregar_vector(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue

            case 2:
                system('cls || clear')
                A = pedir_matriz(False)
                u = ingresar_vector(len(A[0]))
                v = ingresar_vector(len(A[0]))
                matriz_por_suma_vectores(A, u, v)
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
                suma_resta_vecs(lista_vecs, True)
                option = menu_vectores(lista_vecs)
                continue

            case 6:
                suma_resta_vecs(lista_vecs, False)
                option = menu_vectores(lista_vecs)
                continue

            case 7:
                input("\nRegresando al menú principal...")
                break

            case _:
                input("\nOpción inválida...")
                continue

    return None

def agregar_vector(lista_vecs):
    system('cls || clear')
    try:
        nombre = input("Ingrese el nombre del vector (una letra minúscula): ").lower()
        if not nombre.isalpha() or len(nombre) is not 1: raise NameError
        longitud = int(input(f"¿Cuántas dimensiones tendrá el vector? "))
    except NameError:
        input("Error: Ingrese una letra alfabética!")
        return agregar_vector(lista_vecs)
    except ValueError:
        input("Error: Ingrese un número entero!")
        return agregar_vector(lista_vecs)

    vec = ingresar_vector(longitud)
    lista_vecs[nombre] = vec
    input(f"Vector agregado exitosamente!")
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
    system('cls || clear')
    try:
        imprimir_vectores(lista_vecs)
        vec_index = input("\n¿Cuál vector desea multiplicar escalarmente? ")
        if vec_index not in lista_vecs: raise KeyError(vec_index)
        escalar = Fraction(input("Ingrese el escalar: "))
    except KeyError:
        input(f"Error: El vector '{vec_index}' no existe!")
        return mult_escalar(lista_vecs)
    except ValueError:
        input("Error: Ingrese un número real!")
        return mult_escalar(lista_vecs)
    
    lista_vecs[vec_index] = [Fraction(x * escalar) for x in lista_vecs[vec_index]]
    imprimir_escalar = escalar if escalar.is_integer() else f"({str(Fraction(escalar))})*   "
    input(f"\n{imprimir_escalar}{vec_index} = {[str(Fraction(x).limit_denominator()) for x in lista_vecs[vec_index]]}")
    return lista_vecs

def mult_vectorial(lista_vecs):
    system('cls || clear')
    try:
        imprimir_vectores(lista_vecs)
        vec1 = input("Ingrese el nombre del primer vector: ")
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

def suma_resta_vecs(lista_vecs, option):
    system('cls || clear')
    try:
        imprimir_vectores(lista_vecs)
        operacion = "sumar" if option else "restar"
        input_vecs = [i for i in input(f"\n¿Cuáles vectores desea {operacion}? (separados por espacios): ").split()]

        for vec in input_vecs:
            if vec not in lista_vecs: raise KeyError(vec)
        if not all(len(lista_vecs[j]) == len(lista_vecs[input_vecs[0]]) for j in input_vecs):
            raise ArithmeticError    
    except KeyError as k:
        input(f"Error: El vector '{k}' no existe!")
        return suma_resta_vecs(lista_vecs)
    except ArithmeticError:
        input("Error: Los vectores deben tener la misma longitud!")
        return suma_resta_vecs(lista_vecs)
    
    if option: sumar_vectores(input_vecs, lista_vecs)
    else: restar_vectores(input_vecs, lista_vecs)
    return None

def sumar_vectores(input_vecs, lista_vecs):
    suma_vecs = [0 for _ in lista_vecs[input_vecs[0]]]
    for i in range(len(suma_vecs)):
        for j in input_vecs:
            suma_vecs[i] += lista_vecs[j][i]
    
    mensaje = ""
    for i in input_vecs:
        if i != input_vecs[-1]: mensaje += f"{i} + "
        else: mensaje += f"{i}"

    input(f"\n{mensaje} = {[str(Fraction(x).limit_denominator()) for x in suma_vecs]}")
    return None

def restar_vectores(input_vecs, lista_vecs):
    resta_vecs = lista_vecs[input_vecs[0]]
    for i in range(len(resta_vecs)):
        for j in input_vecs[1:]:
            resta_vecs[i] -= lista_vecs[j][i]
    
    mensaje = ""
    for i in input_vecs:
        if i != input_vecs[-1]: mensaje += f"{i} - "
        else: mensaje += f"{i}"

    input(f"\n{mensaje} = {[str(Fraction(x).limit_denominator()) for x in resta_vecs]}")
    return None

def matriz_por_suma_vectores(A, u, v):
    filas = len(A)
    columnas = len(A[0])

    resultado = []
    operaciones = []
    suma_vecs = [u[i] + v[i] for i in range(len(u))]

    lens = [len(str(x)) for x in u]
    for x in u: lens.append(len(str(x)))
    max_uv = max(lens)
    max_suma = max([len(str(x)) for x in suma_vecs])

    u_mas_v = [f"{u[y]} + {v[y]}" for y in range(len(u))]
    print(f"\nu + v:")
    for linea in u_mas_v: print(f"| {linea.center(max_uv)} | ")
    print("    =")
    for linea in suma_vecs: print(f"| {str(linea).center(max_suma)} |")

    for i in range(filas):
        resultado.append([A[i][j] * suma_vecs[j] for j in range(len(suma_vecs))])
    
    max_resultado = max(len(str(resultado[i][j])) for i in range(filas) for j in range(columnas))
    for j in range(filas):
        fila = ""
        for k in range(columnas):
            if k != columnas-1: fila += f"({A[j][k]}*{suma_vecs[k]}) + "
            else: fila += f"({A[j][k]}*{suma_vecs[k]})"
        
        operaciones.append("| " + fila.center(max_resultado) + " |")
    
    print("\nA(u + v):")
    for linea in operaciones: print(linea)
    print("    =")

    for linea in resultado: print(linea)
    resolver = input("\n¿Desea resolver la matriz como suma de productos (Au + Av)? (s/n) ")
    if resolver.lower() == 's':
        suma_matriz_por_vector(A, u, v)

    return resultado

def suma_matriz_por_vector(A, u, v):
    filas = len(A)
    columnas = len(A[0])

    resultado_u = []
    resultado_v = []
    operaciones_u = []
    operaciones_v = []

    for i in range(filas):
        resultado_u.append([A[i][j] * u[j] for j in range(len(u))])
        resultado_v.append([A[i][j] * v[j] for j in range(len(v))])

    max_resultado_u = max(len(str(resultado_u[i][j])) for i in range(filas) for j in range(columnas))
    max_resultado_v = max(len(str(resultado_v[i][j])) for i in range(filas) for j in range(columnas))

    for j in range(filas):
        fila_u = ""
        fila_v = ""
        for k in range(columnas):
            if k != columnas-1:
                fila_u += f"({A[j][k]}*{u[k]}) + "
                fila_v += f"({A[j][k]}*{v[k]}) + "
            else:
                fila_u += f"({A[j][k]}*{u[k]})"
                fila_v += f"({A[j][k]}*{v[k]})"

        operaciones_u.append("| " + fila_u.center(max_resultado_u) + " |")
        operaciones_v.append("| " + fila_v.center(max_resultado_v) + " |")

    print("\nAu:")
    for linea in operaciones_u: print(linea)
    print("    =")
    for linea in resultado_u: print(linea)

    print("\nAv:")
    for linea in operaciones_v: print(linea)
    print("    =")
    for linea in resultado_v: print(linea)

    resultado = [[resultado_u[i][j] + resultado_v[i][j] for j in range(columnas)] for i in range(filas)]
    max_resultado = max(len(str(resultado[i][j])) for i in range(filas) for j in range(columnas))

    operaciones = []
    for j in range(filas):
        fila = ""
        for k in range(columnas):
            if k != columnas-1:
                fila += f"({resultado_u[j][k]} + {resultado_v[j][k]}) + "
            else:
                fila += f"({resultado_u[j][k]} + {resultado_v[j][k]})"

        operaciones.append("| " + fila.center(max_resultado) + " |")

    print("\nAu + Av:")
    for linea in operaciones: print(linea)
    print("    =")
    for linea in resultado: print(linea)
    input()

    return resultado
