from fractions import Fraction

from gauss_bot.clases.matriz import Matriz
from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager
from gauss_bot.utils import limpiar_pantalla

# TODO: implementar opcion de mostrar procedimiento para todas las operaciones en MatricesManager y VectoresManager
# TODO: simplificar ._despejar_variables()


class OpsManager:
    def __init__(self, mat_manager=None, vec_manager=None) -> None:
        self.mat_manager = MatricesManager({}, self) if mat_manager is None else mat_manager
        self.vec_manager = VectoresManager({}, self) if vec_manager is None else vec_manager

    def exec(self) -> None:
        while True:
            option = self.main_menu()
            match option:
                case 1:
                    self.mat_manager.menu_matrices()
                case 2:
                    self.vec_manager.menu_vectores()
                case 3:
                    input("=> Cerrando programa...")
                    break
        return

    def main_menu(self) -> int:
        limpiar_pantalla()
        print("\n################")
        print("### GaussBot ###")
        print("################\n")
        print("1. Acceder a menú de matrices")
        print("2. Acceder a menú de vectores\n")
        print("3. Cerrar programa")
        try:
            option = int(input("\n=> Seleccione una opción: ").strip())
            if option < 1 or option > 3:
                raise ValueError
        except ValueError:
            input("=> Error: Ingrese una opción válida!")
            return self.main_menu()
        return option

    def producto_matriz_vector(self) -> None:
        limpiar_pantalla()
        nombre_mat = self.mat_manager.seleccionar_mat("mv")
        if nombre_mat == "":
            return

        nombre_vec = self.vec_manager.seleccionar("mv")
        if nombre_vec == "":
            return

        mat = self.mat_manager.mats_ingresadas[nombre_mat]
        vec = self.vec_manager.vecs_ingresados[nombre_vec]
        if mat.columnas != len(vec):
            input("Error: El número de columnas de la matriz debe ser igual al número de componentes del vector!")
            return

        limpiar_pantalla()
        resultado = [[Fraction(0) for _ in range(len(vec))] for _ in range(mat.filas)]
        for i in range(mat.filas):
            for j, componente in enumerate(vec):
                resultado[i][j] += mat[i, j] * componente

        mat_resultante = Matriz(False, mat.filas, len(vec), resultado)
        print("\n---------------------------------------------")
        print(f"{nombre_mat}:")
        print(mat_resultante)
        print(f"{nombre_vec} = {vec}")
        print("---------------------------------------------")
        print(f"\n{nombre_mat}{nombre_vec}:")
        print(mat_resultante)

        return
