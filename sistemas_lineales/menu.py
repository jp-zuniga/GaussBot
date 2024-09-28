from matrices import resolver_sistema
from vectores import operaciones_vectoriales
from validaciones import limpiar_pantalla

# interfaz del programa:
# ----------------------------

def imprimir_menu():
    limpiar_pantalla()
    print("\n######################")
    print("### Menú Principal ###")
    print("######################\n")
    print("1. Resolver sistema de ecuaciones lineales")
    print("2. Operaciones de vectores")
    print("3. Cerrar programa")

    # try/except para validar la opcion ingresada
    try:
        option = int(input("\nSeleccione una opción: "))
        if option < 1 or option > 3: raise ValueError
    except ValueError:
        input("\nError: Ingrese una opción válida!")
        return imprimir_menu()
    
    return option

def main_menu():
    option = imprimir_menu()
    
    while option != 3:
        match option:
            case 1:
                limpiar_pantalla()
                M = resolver_sistema()

                continuar = input("\n¿Desea resolver otro sistema? (s/n) ")
                if continuar.lower() == 's': continue
                elif continuar.lower() == 'n':
                    input("Regresando al menú principal...")
                    option = imprimir_menu()
                    continue
                else:
                    input("Opción inválida! Regresando al menú principal...")
                    option = imprimir_menu()
                    continue
                
            
            case 2:
                operaciones_vectoriales()
                return main_menu()

            case 3: break
            case _: input("Opción inválida, por favor intente de nuevo.")
    
    input("Cerrando programa...")
    return None
