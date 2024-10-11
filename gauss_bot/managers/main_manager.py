from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager
from gauss_bot.utils import limpiar_pantalla

# TODO implementar calculo de determinantes en MatricesManager
# TODO implementar calculo de inversas en MatricesManager

# ? implementar metodo de analizar matriz en MatricesManager
# ? mejorar .procesar_operacion() en MatricesManager y VectoresManager
# ? implementar metodo de producto matriz-vector en OpsManager
# ? implementar opcion de mostrar procedimiento de todas las operaciones en MatricesManager y VectoresManager

class OpsManager:
    def __init__(self, mat_manager=None, vec_manager=None) -> None:
        self.mat_manager = MatricesManager(self) if mat_manager is None else mat_manager
        self.vec_manager = VectoresManager(self) if vec_manager is None else vec_manager

    def exec(self) -> None:
        while True:
            option = self.main_menu()
            match option:
                case 1:
                    self.mat_manager._mostrar_matrices(necesita_aumentada = -1)
                    input("Presione cualquier tecla para regresar al menú principal...")
                case 2:
                    self.vec_manager._mostrar_vectores()
                    input("Presione cualquier tecla para regresar al menú principal...")
                case 3:
                    self.mat_manager.menu_matrices()
                case 4:
                    self.vec_manager.menu_vectores()
                case 5:
                    input("=> Cerrando programa...")
                    break
        return None

    def main_menu(self) -> int:
        limpiar_pantalla()
        print("\n################")
        print("### GaussBot ###")
        print("################\n")
        print("1. Mostrar matrices")
        print("2. Mostrar vectores")
        print("3. Acceder a menú de matrices")
        print("4. Acceder a menú de vectores\n")
        print("5. Cerrar programa")
        try:
            option = int(input("\n=> Seleccione una opción: ").strip())
            if option < 1 or option > 5:
                raise ValueError
        except ValueError:
            input("=> Error: Ingrese una opción válida!")
            return self.main_menu()
        return option
