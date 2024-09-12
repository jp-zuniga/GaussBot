from os import system
from matrices import resolver_sistema

def imprimir_menu():
    system('cls || clear')

    print("\n######################")
    print("### Menú Principal ###")
    print("######################\n")
    print("1. Resolver sistema de ecuaciones lineales")
    print("2. Cerrar programa")

    # try/except para validar la opcion ingresada
    try:
        option = int(input("\nSeleccione una opción: "))
        if option < 1 or option > 2: raise ValueError
    except ValueError:
        input("\nError: Ingrese una opción válida!")
        return imprimir_menu()
    
    return option

def main_menu():
    option = imprimir_menu()
    
    while True:
        if option == 1:
            M = resolver_sistema()

            while (True):
                continuar = input("\n¿Desea resolver otra matriz? (s/n) ")
                if continuar.lower() == 's': break
                elif continuar.lower() == 'n':
                    input("\nSaliendo del programa...")
                    break
                else:
                    input("\nOpción inválida...")
                    continue
            
            if continuar.lower() == 's': continue
            else: break

        elif option == 2:
            input("\nSaliendo del programa...")
            break
        else:
            input("\nOpción inválida, por favor intente de nuevo.")
    
    return
