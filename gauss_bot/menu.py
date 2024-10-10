from gauss_bot.operaciones import OpsManager, MatricesManager, VectoresManager
from gauss_bot.utils import limpiar_pantalla

def main() -> None:
    manager = OpsManager(MatricesManager(), VectoresManager())
    option = main_menu()
    while option != 3:
        match option:
            case 1:
                manager.main()
                option = main_menu()
                continue
            case 2:
                break
    input("Cerrando programa...")
    return None

def main_menu() -> int:
    limpiar_pantalla()
    print("\n################")
    print("### GaussBot ###")
    print("################\n")
    print("1. Operaciones de matrices y vectores")
    print("2. Cerrar programa")
    try:
        option = int(input("\nSeleccione una opción: "))
        if option < 1 or option > 2:
            raise ValueError
    except ValueError:
        input("Error: Ingrese una opción válida!")
        return main_menu()
    return option
