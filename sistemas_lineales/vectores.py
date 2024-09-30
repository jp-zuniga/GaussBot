from fractions import Fraction
from validaciones import validar_lista_vecs
from matrices import pedir_matriz, imprimir_matriz
from utils import List, Matriz, Vector, Dict_Vectores, limpiar_pantalla

# funciones para realizar operaciones con vectores
# -------------------------------------------------------

def imprimir_vectores(lista_vecs: Dict_Vectores, matricial=False) -> None:
    if not lista_vecs:
        print("\nNo hay vectores ingresados!")
        return None

    mensaje = "seleccionados" if matricial else "ingresados"
    print(f"\nVectores {mensaje}:")
    for nombre, vector in lista_vecs.items():
        vec = [str(num.limit_denominator()) for num in vector]
        print(f"{nombre}: {vec}")
    
    return None

def menu_vectores(lista_vecs: Dict_Vectores) -> int:
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

def operaciones_vectoriales(lista_vecs: Dict_Vectores) -> Dict_Vectores:
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
                A = matriz_por_suma_vectores(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue
            case 3:
                limpiar_pantalla()
                lista_vecs = mult_escalar(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue
            case 4:
                limpiar_pantalla()
                lista_vecs = mult_vectorial(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue
            case 5:
                limpiar_pantalla()
                input_suma_resta(lista_vecs, option=True)
                option = menu_vectores(lista_vecs)
                continue
            case 6:
                limpiar_pantalla()
                input_suma_resta(lista_vecs, option=False)
                option = menu_vectores(lista_vecs)
                continue
            case 7: break
            case _:
                input("Opción inválida! Por favor, intente de nuevo...")
                continue

    input("Regresando al menú principal...")
    return lista_vecs

def agregar_vector(lista_vecs: Dict_Vectores) -> Dict_Vectores:
    try:
        nombre = input("Ingrese el nombre del vector (una letra minúscula): ").lower()
        if not nombre.isalpha() or len(nombre) != 1: raise NameError
        if nombre in lista_vecs: raise KeyError
        longitud = int(input(f"¿Cuántas dimensiones tendrá el vector? "))

    except NameError:
        input("Error: Ingrese solamente una letra minúscula!")
        return agregar_vector(lista_vecs)
    except KeyError:
        input(f"Error: Ya hay un vector con el nombre '{nombre}'!")
        return agregar_vector(lista_vecs)
    except ValueError:
        input("Error: Ingrese un número entero!")
        return agregar_vector(lista_vecs)

    vec = ingresar_vector(longitud)
    lista_vecs[nombre] = vec
    print(f"Vector agregado exitosamente!")

    match input("\n¿Desea agregar otro vector? (s/n) "):
        case 's': return agregar_vector(lista_vecs)
        case 'n': input("Regresando al menú de vectores...")
        case _: input("Opción inválida! Regresando al menú de vectores...")
    return lista_vecs

def ingresar_vector(longitud: int) -> Vector:
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

def mult_escalar(lista_vecs: Dict_Vectores) -> Dict_Vectores:
    if not validar_lista_vecs(lista_vecs): return lista_vecs
    try:
        limpiar_pantalla()
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
    except ZeroDivisionError:
        input("Error: El denominador no puede ser cero!")
        return mult_escalar(lista_vecs)
    
    lista_vecs[vec_nombre] = [Fraction(x*escalar) for x in lista_vecs[vec_nombre]]
    imprimir_escalar = escalar if escalar.is_integer() else f"({str(Fraction(escalar))})*"

    input(f"\n{imprimir_escalar}{vec_nombre} = {[str(x.limit_denominator()) for x in lista_vecs[vec_nombre]]}")
    return lista_vecs

def mult_vectorial(lista_vecs: Dict_Vectores) -> Dict_Vectores:
    if not validar_lista_vecs(lista_vecs): return lista_vecs
    try:
        imprimir_vectores(lista_vecs)
        input_vecs = input("\nIngrese los nombres de los dos vectores a multiplicar (separados por espacios): ").split()
        if len(input_vecs) != 2: raise IndexError

        vec1, vec2 = input_vecs
        for vec in input_vecs:
            if vec not in lista_vecs: raise KeyError(vec)

        if len(lista_vecs[vec1]) != len(lista_vecs[vec2]): raise ArithmeticError

    except IndexError:
        input("Error: Debe ingresar dos vectores para multiplicar!")
        return mult_vectorial(lista_vecs)
    except KeyError as k:
        input(f"Error: El vector '{k}' no existe!")
        return mult_vectorial(lista_vecs)
    except ArithmeticError:
        input("Error: Los vectores deben tener la misma longitud!")
        return mult_vectorial(lista_vecs)

    producto_punto = sum(i*j for i in lista_vecs[vec1] for j in lista_vecs[vec2])
    input(f"\n{vec1}.{vec2} = {str(producto_punto)}")
    return lista_vecs

def input_suma_resta(lista_vecs: Dict_Vectores, option: bool, matricial=False) -> None:
    if not validar_lista_vecs(lista_vecs): return lista_vecs
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
        error = "dos vectores para realizar el producto matriz-vector" if matricial else f"dos o más vectores para {operacion}"
        input(f"Error: Debe ingresar {error}!")
        return input_suma_resta(lista_vecs, option, matricial)
    except ArithmeticError:
        input("Error: Los vectores deben tener la misma longitud!")
        return input_suma_resta(lista_vecs, option, matricial)

    if matricial: return input_vecs
    if option:
        resultado = sumar_vectores(lista_vecs, input_vecs)
        signo = '+'
    else:
        resultado = restar_vectores(lista_vecs, input_vecs)
        signo = '-'

    mensaje = ""
    for i in input_vecs:
        if i != input_vecs[-1]: mensaje += f"{i} {signo} "
        else: mensaje += i

    input(f"\n{mensaje} = {[str(num.limit_denominator()) for num in resultado]}")
    return None

def sumar_vectores(lista_vecs: Dict_Vectores, input_vecs: List[str]) -> List[Fraction]:
    suma_vecs = [0 for _ in lista_vecs[input_vecs[0]]]
    for i in range(len(suma_vecs)):
        for j in input_vecs:
            suma_vecs[i] += lista_vecs[j][i]
    
    return suma_vecs

def restar_vectores(lista_vecs: Dict_Vectores, input_vecs: List[str]) -> List[Fraction]:
    resta_vecs = lista_vecs[input_vecs[0]]
    for i in range(len(resta_vecs)):
        for j in input_vecs[1:]:
            resta_vecs[i] -= lista_vecs[j][i]
    
    return resta_vecs

def matriz_por_suma_vectores(lista_vecs: Dict_Vectores) -> Matriz:
    if not validar_lista_vecs(lista_vecs): return None
    A = pedir_matriz(aumentada=False, nombre='A')
    limpiar_pantalla()

    input_vecs = input_suma_resta(lista_vecs, option=True, matricial=True) # pedir los vectores
    suma_vecs = sumar_vectores(input_vecs, lista_vecs) # sumar los vectores seleccionados por el usuario
    
    if len(A[0]) != len(lista_vecs[input_vecs[0]]): # validar las dimensiones
        input("\nError: Las dimensiones de A y los vectores no son compatibles!")
        return matriz_por_suma_vectores(lista_vecs)

    # calcular A(u + v)
    resultado = []
    for i in range(len(suma_vecs)):
        resultado.append(sum([A[i][j] * suma_vecs[j] for j in range(len(suma_vecs))]))
    
    # imprimir las operaciones realizadas
    imprimir_MPSV(A, lista_vecs, input_vecs, suma_vecs, resultado)

    match input("\nDesea comprobar la propiedad distributiva (A(u + v) = Au + Av)? (s/n) "):
        case 's': suma_matriz_por_vector(A, lista_vecs, input_vecs)
        case 'n': input("De acuerdo! Regresando al menú de vectores...")
        case _: input("Opción inválida! Regresando al menú de vectores...")
    return resultado

def suma_matriz_por_vector(A: Matriz, lista_vecs: Dict_Vectores, input_vecs: List[str]):
    limpiar_pantalla()
    u, v = lista_vecs[input_vecs[0]], lista_vecs[input_vecs[1]]
    mult_u = []
    mult_v = []

    # calcular Au y Av
    for i in range(len(u)):
        mult_u.append(sum([A[i][j] * u[j] for j in range(len(u))]))
        mult_v.append(sum([A[i][j] * v[j] for j in range(len(v))]))

    suma_mults = [i+j for i in mult_u for j in mult_v] # calcular Au + Av
    imprimir_SMPV(A, lista_vecs, input_vecs, [mult_u, mult_v], suma_mults) # imprimir las operaciones realizadas
    input("\nLa respuesta sigue siendo la misma, asi que la propiedad distributiva se cumple!")
    return None

def imprimir_MPSV(A: Matriz, lista_vecs: Dict_Vectores, input_vecs: List[str], suma_vecs: Vector, resultado: Matriz) -> None: 
    filas = len(A)
    columnas = len(A[0])
    u, v = lista_vecs[input_vecs[0]], lista_vecs[input_vecs[1]]

    limpiar_pantalla()
    print("\nMatriz A:")
    imprimir_matriz(A, vectorial=True)
    imprimir_vectores({input_vecs[0]: u, input_vecs[1]: v}, matricial=True)

    # encontrar la longitud maxima de todos los elementos de todas las listas (u, v, suma_vecs, A, resultado)
    lens_uv = [len(str(i)) for i in u]
    lens_uv += [len(str(j)) for j in v]
    max_uv = max(lens_uv)
    max_suma = max(len(str(k)) for k in suma_vecs)
    max_A = max(len(str(A[i][j])) for i in range(filas) for j in range(columnas))
    max_resultado = max(len(str(resultado[i])) for i in range(filas))

    # imprimir procedimiento de u + v
    print("\nu + v:")
    for i in range(len(u)):
        signo = '+' if v[i] > 0 else '-'
        igual = ' ' if (i != len(u) // 2) else '='

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
        igual = ' ' if (k != len(operaciones) // 2) else '='
        print(f"{operaciones[k]} {igual} [ {str(resultado[k]).center(max_resultado)} ]")

    return None

def imprimir_SMPV(A: Matriz, lista_vecs: Dict_Vectores, input_vecs: List[str], mults: List[Matriz], suma_mults: Matriz) -> None:
    filas = len(A)
    columnas = len(A[0])
    u, v = lista_vecs[input_vecs[0]], lista_vecs[input_vecs[1]]
    mult_u, mult_v = mults[0], mults[1]

    limpiar_pantalla()
    print("\nMatriz A:")
    imprimir_matriz(A, vectorial=True)
    imprimir_vectores({input_vecs[0]: u, input_vecs[1]: v}, matricial=True)

    # encontrar la longitud maxima de todos los elementos de todas las listas (u, v, A, mult_u, mult_v)
    lens_uv = [len(str(i)) for i in u]
    lens_uv += [len(str(j)) for j in v]
    max_mult_u = max(len(str(mult_u[i])) for i in range(filas))
    max_mult_v = max(len(str(mult_v[i])) for i in range(filas))
    max_A = max(len(str(A[i][j])) for i in range(filas) for j in range(columnas))
    max_suma_mults = max(len(str(suma_mults[i][j])) for i in range(filas) for j in range(columnas))

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
        igual = ' ' if (k != len(operaciones_u) // 2) else '='
        print(f"{operaciones_u[k]} {igual} [ {str(mult_u[k]).center(max_mult_u)} ]")

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
        igual = ' ' if (k != len(operaciones_v) // 2) else '='
        print(f"{operaciones_v[k]} {igual} [ {str(mult_v[k]).center(max_mult_v)} ]")

    # calcular y imprimir procedimiento de Au + Av
    print("\nAu + Av:")
    for i in range(filas):
        print(f"[ {str(mult_u[i]).center(max_mult_u)} + {str(mult_v[i]).center(max_mult_v)} ] = [ {str(suma_mults[i]).center(max_suma_mults)} ]")
    
    return None
