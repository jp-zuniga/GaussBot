from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager
from gauss_bot.utils import limpiar_pantalla

# TODO implementar calculo de determinantes en MatricesManager
# TODO implementar calculo de inversas en MatricesManager

# ? mejorar .procesar_operacion() en MatricesManager y VectoresManager
# ? implementer producto matriz-vector OpsManager

class OpsManager:
    def __init__(self, mat_manager: MatricesManager, vec_manager: VectoresManager) -> None:
        self.mat_manager = mat_manager
        self.vec_manager = vec_manager

    def start_exec_loop(self) -> None:
        while True:
            option = self.main_menu()
            match option:
                case 1:
                    self.mat_manager._mostrar_matrices(necesita_aumentada = -1)
                case 2:
                    self.vec_manager._mostrar_vectores()
                case 3:
                    self.mat_manager.menu_matrices()
                case 4:
                    self.vec_manager.menu_vectores()
                case 5:
                    input("Cerrando programa...")
                    break
        return None

    def main_menu(self) -> int:
        limpiar_pantalla()
        print("\n################")
        print("### GaussBot ###")
        print("################\n")
        print("1. Mostrar matrices")
        print("2. Mostrar vectores")
        print("3. Operaciones de matrices")
        print("4. Operaciones de vectores")
        print("5. Cerrar programa")
        try:
            option = int(input("\n=> Seleccione una opción: ").strip())
            if option < 1 or option > 5:
                raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.main_menu()
        return option
