from matrices import Matriz
from vectores import Vector
from utils import limpiar_pantalla

# interfaz del programa
# ----------------------------

def imprimir_menu() -> int:
    limpiar_pantalla()
    print("\n######################")
    print("### Menú Principal ###")
    print("######################\n")
    print("1. Operaciones de matrices")
    print("2. Operaciones de vectores")
    print("3. Cerrar programa")

    # validar la opcion ingresada
    try:
        option = int(input("\nSeleccione una opción: "))
        if option < 1 or option > 3: raise ValueError
    except ValueError:
        input("Error: Ingrese una opción válida!")
        return imprimir_menu()
    
    return option

def main_menu() -> None:
    mat = Matriz()
    vec = Vector()
    option = imprimir_menu()
    while option != 4:
        match option:
            case 1:
                mat.operaciones_matriciales()
                option = imprimir_menu()
                continue
            case 2:
                vec.operaciones_vectoriales()
                option = imprimir_menu()
                continue
            case 3: break
    
    input("Cerrando programa...")
    return None
