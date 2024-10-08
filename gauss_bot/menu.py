from matrices import OperacionesMatrices
from vectores import OperacionesVectores

from utils import limpiar_pantalla


def main() -> None:
    mat = OperacionesMatrices()
    vec = OperacionesVectores()
    option = main_menu()

    while option != 4:
        match option:
            case 1:
                mat.main_matrices()
                option = main_menu()
                continue
            case 2:
                vec.main_vectores()
                option = main_menu()
                continue
            case 3:
                break

    input("Cerrando programa...")
    return None


def main_menu() -> int:
    limpiar_pantalla()
    print("\n################")
    print("### GaussBot ###")
    print("################\n")
    print("1. Operaciones de matrices")
    print("2. Operaciones de vectores")
    print("3. Cerrar programa")

    try:
        option = int(input("\nSeleccione una opción: "))
        if option < 1 or option > 3:
            raise ValueError
    except ValueError:
        input("Error: Ingrese una opción válida!")
        return main_menu()

    return option
