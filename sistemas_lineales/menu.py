from matrices import resolver_sistema
from vectores import operaciones_vectoriales
from utils import limpiar_pantalla

# interfaz del programa
# ----------------------------

def imprimir_menu() -> int:
    limpiar_pantalla()
    print("\n######################")
    print("### Menú Principal ###")
    print("######################\n")
    print("1. Resolver sistema de ecuaciones lineales")
    print("2. Operaciones de vectores")
    print("3. Cerrar programa")

    # validar la opcion ingresada
    try:
        option = int(input("\nSeleccione una opción: "))
        if option < 1 or option > 3: raise ValueError
    except ValueError:
        input("\nError: Ingrese una opción válida!")
        return imprimir_menu()
    
    return option

def main_menu() -> None:
    lista_vecs = {}
    option = imprimir_menu()
    while option != 3:
        match option:
            case 1:
                limpiar_pantalla()
                M = resolver_sistema()
                match input("\n¿Desea resolver otro sistema? (s/n) "):
                    case 's': continue
                    case 'n':
                        input("Regresando al menú principal...")
                        option = imprimir_menu()
                        continue
                    case _:
                        input("Opción inválida! Regresando al menú principal...")
                        option = imprimir_menu()
                        continue
            case 2:
                lista_vecs = operaciones_vectoriales(lista_vecs)
                option = imprimir_menu()
                continue
            case 3: break
            case _: input("Opción inválida! Por favor, intente de nuevo...")
    
    input("Cerrando programa...")
    return None
