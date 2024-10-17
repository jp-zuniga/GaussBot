from fractions import Fraction

from gauss_bot.models.matriz import Matriz
from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager


class OpsManager:
    """
    Manager principal, encargado de gestionar todas las operaciones matemáticas.
    Esencialmente un wrapper para contener los datos de  MatricesManager y VectoresManager.
    Se encarga de realizar las multiplicaciones de matriz-vector, ya que contiene todos los datos necesarios.
    """

    def __init__(self, mats_manager=None, vecs_manager=None) -> None:
        if mats_manager is not None and not isinstance(mats_manager, MatricesManager):
            raise TypeError("Argumento inválido para 'mats_manager'!")
        if vecs_manager is not None and not isinstance(vecs_manager, VectoresManager):
            raise TypeError("Argumento inválido para 'vecs_manager'!")
        self.mats_manager = MatricesManager() if mats_manager is None else mats_manager
        self.vecs_manager = VectoresManager() if vecs_manager is None else vecs_manager

    def producto_matriz_vector(self, nombre_mat: str, nombre_vec: str) -> tuple[str, Matriz]:
        """
        Realiza la multiplicación de una matriz por un vector.
        """

        mat = self.mats_manager.mats_ingresadas[nombre_mat]
        vec = self.vecs_manager.vecs_ingresados[nombre_vec]
        if mat.columnas != len(vec):
            raise ArithmeticError("Error: El número de columnas de la matriz debe ser igual al número de componentes del vector!")

        multiplicacion = [[Fraction(0) for _ in range(len(vec))] for _ in range(mat.filas)]
        for i in range(mat.filas):
            for j, componente in enumerate(vec.componentes):
                multiplicacion[i][j] += mat[i, j] * componente

        mat_resultante = Matriz(False, mat.filas, len(vec), multiplicacion)
        nombre_mat_resultante = f"{nombre_mat}{nombre_vec}"
        return (nombre_mat_resultante, mat_resultante)
