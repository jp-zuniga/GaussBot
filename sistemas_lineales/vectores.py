from os import system
from fractions import Fraction

def imprimir_vectores(lista_vecs):
    if lista_vecs is None: print("\nNo hay vectores ingresados!")
    else:
        print("\nVectores ingresados:")
        for i in range(len(lista_vecs)):
            print(f"Vector {i+1}: {lista_vecs[i]}")
    
    return None

def menu_vectores(lista_vecs=None):
    system('cls || clear')
    print("\n###############################")
    print("### Operaciones de Vectores ###")
    print("###############################")
    imprimir_vectores(lista_vecs)
    print("\n1. Agregar un vector")
    print("2. Multiplicación escalar")
    print("3. Multiplicación de vectores")
    print("4. Suma de vectores")
    print("5. Resta de vectores")
    print("6. Regresar al menú principal")

    try:
        option = int(input("\nSeleccione una opción: "))
        if option < 1 or option > 6:
            raise ValueError
    except ValueError:
        input("\nError: Ingrese una opción válida!")
        return menu_vectores(lista_vecs)
    
    return option

def operaciones_vectores():
    lista_vecs = []
    option = menu_vectores(lista_vecs)

    while option != 6:
        match option:
            case 1:
                lista_vecs = agregar_vector(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue
            
            case 2:
                lista_vecs = mult_escalar(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue
            
            case 3:
                lista_vecs = mult_vectorial(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue

            case 4:
                lista_vecs = sumar_vectores(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue

            case 5:
                lista_vecs = restar_vectores(lista_vecs)
                option = menu_vectores(lista_vecs)
                continue

            case 6:
                input("\nRegresando al menú principal...")
                break

            case _:
                input("\nOpción inválida...")
                continue

    return None

def agregar_vector(lista_vecs):
    system('cls || clear')
    try:
        longitud = int(input("\n¿Cuántas dimensiones tiene el vector? "))
        vec = input(f"Ingrese los componentes (separados por espacios): ").split()
        if len(vec) != longitud: raise TypeError

        lista_vecs.append([float(Fraction(x)) for x in vec])
        input("Vector agregado exitosamente!")

    except TypeError: input("\nError: El vector no tiene las dimensiones correctas!")
    except ValueError: input("\nError: Ingrese un número real!")
    return lista_vecs

def mult_escalar(lista_vecs):
    system('cls || clear')
    try:
        imprimir_vectores(lista_vecs)
        vec_index = int(input("\n¿Cuál vector desea multiplicar escalarmente? "))-1
        escalar = float(input("Ingrese el escalar: "))

        lista_vecs[vec_index] = [x * escalar for x in lista_vecs[vec_index]]
        print(f"\nEl Vector {vec_index + 1} multiplicado por {escalar} es:")
        input(lista_vecs[vec_index])
    
    except IndexError: input(f"\nError: Vector {vec_index} no existe!")
    except ValueError: input("\nError: Ingrese un número real!")
    
    return lista_vecs

def mult_vectorial(lista_vecs):
    system('cls || clear')
    try:
        imprimir_vectores(lista_vecs)
        vec1_index = int(input("\Ingrese el primer vector a multiplicar: "))-1
        vec2_index = int(input("Ingrese el segundo vector a multiplicar: "))-1
        
        if len(lista_vecs[vec1_index]) != len(lista_vecs[vec2_index]): raise ValueError
        
        producto_punto = sum(lista_vecs[vec1_index][i] * lista_vecs[vec2_index][i] for i in range(len(lista_vecs[vec1_index])))
        input(f"\nEl producto punto de los vectores {vec1_index+1} y {vec2_index+1} es: {producto_punto}")
    
    except IndexError: input(f"\nError: Uno o ambos de los vectores ingresados no existen!")
    except ValueError: input("\nError: Los vectores deben tener la misma longitud!")
    return lista_vecs

def sumar_vectores(lista_vecs):
    system('cls || clear')
    try:
        imprimir_vectores(lista_vecs)
        vecs_indices = [int(i)-1 for i in input("\n¿Cuáles vectores desea sumar? (separados por espacios): ").split()]

        suma_vecs = [0 for _ in range(len(lista_vecs[0]))]
        for i in range(len(suma_vecs)):
            for j in vecs_indices:
                suma_vecs[i] += lista_vecs[j][i]
        
        print(f"\nLa suma de los vectores {vecs_indices} es:")
        input(suma_vecs)
    
    except IndexError: input(f"\nError: Al menos uno de los vectores ingresados no existen!")
    except ValueError: input("\nError: Los vectores deben tener la misma longitud!")
    return lista_vecs

def restar_vectores(lista_vecs):
    system('cls || clear')
    try:
        imprimir_vectores(lista_vecs)
        vecs_indices = [int(i) - 1 for i in input("\n¿Cuáles vectores desea restar? (separados por espacios): ").split()]

        resta_vecs = lista_vecs[vecs_indices[0]].copy()
        for j in vecs_indices:
            for i in range(len(resta_vecs)):
                resta_vecs[i] -= lista_vecs[j][i]
        
        print(f"\nLa resta de los vectores {vecs_indices} es:")
        input(resta_vecs)
    
    except IndexError: input(f"\nError: Al menos uno de los vectores ingresados no existen!")
    except ValueError: input("\nError: Los vectores deben tener la misma longitud!")    
    return lista_vecs
