from os import system
from matrices import resolver_sistema
from vectores import operaciones_vectores

# interfaz del programa:
# ----------------------------

def imprimir_menu():
    system('cls || clear')
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
                system('cls || clear')
                M = resolver_sistema()

                while (True):
                    continuar = input("\n¿Desea resolver otra matriz? (s/n) ")
                    if continuar.lower() == 's': break
                    elif continuar.lower() == 'n':
                        input("\nCerrando programa...")
                        break
                    else:
                        input("\nOpción inválida...")
                        continue
                
                if continuar.lower() == 's': continue
                else:
                    option = 3
                    break
            
            case 2:
                operaciones_vectores()
                return main_menu()

            case 3:
                input("\nSaliendo del programa...")
                break

            case _: input("\nOpción inválida, por favor intente de nuevo.")
    
    return None
