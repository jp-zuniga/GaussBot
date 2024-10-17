from fractions import Fraction

from gauss_bot.models.matriz import Matriz
from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager
from gauss_bot.utils import limpiar_pantalla

# TODO: implementar opcion de mostrar procedimiento para todas las operaciones


class OpsManager:
    """
    Manager principal de la aplicación, encargado de gestionar todas las operaciones.
    Se encarga de llamar a los managers de matrices y vectores, para mostrar sus menus.
    También se encarga de realizar las operaciones de producto matriz-vector, ya que
    se requiere acceso a los diccionarios de matrices y de vectores para seleccionar.
    """

    def __init__(self, mats_manager=None, vecs_manager=None) -> None:
        self.mats_manager = MatricesManager({}, self) if mats_manager is None else mats_manager
        self.vecs_manager = VectoresManager({}, self) if vecs_manager is None else vecs_manager

    def exec(self) -> None:
        """
        Loop principal del programa, que muestra el menú principal y llama a los managers de matrices y vectores.
        """
        
        while True:
            option = self.main_menu()
            match option:
                case 1:
                    self.mats_manager.menu_matrices()
                case 2:
                    self.vecs_manager.menu_vectores()
                case 3:
                    input("=> Cerrando programa...")
                    break
        return

    def main_menu(self) -> int:
        """
        Imprime las opciones del menú principal, y se encarga validar y retornar la opción seleccionada.
        """
        
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
        """
        Realiza la multiplicación de una matriz por un vector, seleccionando ambos de los diccionarios de matrices y vectores.
        """
        
        limpiar_pantalla()
        if not self.mats_manager._validar_mats_ingresadas():
            return
        if not self.vecs_manager._validar_vecs_ingresados():
            return
        
        nombre_mat = self.mats_manager.seleccionar_mat("mv")
        if nombre_mat == "":
            return

        nombre_vec = self.vecs_manager.seleccionar("mv")
        if nombre_vec == "":
            return

        mat = self.mats_manager.mats_ingresadas[nombre_mat]
        vec = self.vecs_manager.vecs_ingresados[nombre_vec]
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
