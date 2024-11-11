"""
Implementación de OpsManager.
Utilizado principalmente para contener
los datos de MatricesManager y VectoresManager.
"""

from fractions import Fraction
from json import (
    dump,
    load,
    JSONDecodeError
)

from os import (
    path,
    makedirs,
)

from gauss_bot import (
    SISTEMAS_PATH,
    MATRICES_PATH,
    VECTORES_PATH,
)

from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager
from gauss_bot.models import (
    FractionEncoder,
    FractionDecoder,
    Matriz,
    Vector,
)


class OpsManager:
    """
    Manager principal, encargado de gestionar todas las operaciones matemáticas.
    Esencialmente un wrapper para contener los datos de MatricesManager y VectoresManager.
    Se encarga de leer y escribir los datos a archivos .json,
    y de realizar la multiplicación de matrices por vectores.
    """

    def __init__(self, mats_manager=None, vecs_manager=None) -> None:
        if mats_manager is not None and not isinstance(mats_manager, MatricesManager):
            raise TypeError("Argumento inválido para 'mats_manager'!")
        if vecs_manager is not None and not isinstance(vecs_manager, VectoresManager):
            raise TypeError("Argumento inválido para 'vecs_manager'!")

        self.mats_manager = (
            MatricesManager(self._load_matrices(), self._load_sistemas())
            if mats_manager is None
            else mats_manager
        )

        self.vecs_manager = (
            VectoresManager(self._load_vectores())
            if vecs_manager is None
            else vecs_manager
        )

    def matriz_por_vector(self, nombre_mat: str, nombre_vec: str) -> tuple[str, Matriz]:
        """
        Realiza la multiplicación de una matriz por un vector.
        * ArithmeticError: si la matriz y el vector no son compatibles para la multiplicación.
        """

        mat = self.mats_manager.mats_ingresadas[nombre_mat]
        vec = self.vecs_manager.vecs_ingresados[nombre_vec]
        if mat.columnas != len(vec):
            raise ArithmeticError(
                "El número de columnas de la matriz debe ser " +
                "igual al número de componentes del vector!"
            )

        multiplicacion = [[Fraction(0) for _ in range(len(vec))] for _ in range(mat.filas)]
        for i in range(mat.filas):
            for j, componente in enumerate(vec.componentes):
                multiplicacion[i][j] += mat[i, j] * componente

        mat_resultante = Matriz(False, mat.filas, len(vec), multiplicacion)
        nombre_mat_resultante = f"{nombre_mat}{nombre_vec}"
        return (nombre_mat_resultante, mat_resultante)

    def save_sistemas(self) -> None:
        """
        Escribe el diccionario de sistemas ingresados al archivo sistemas.json,
        utilizando FractionEncoder para escribir objetos Fraction().
        """

        sistemas_dict = {
            nombre: {
                "aumentada": mat.aumentada,
                "filas": mat.filas,
                "columnas": mat.columnas,
                "valores": mat.valores
            } for nombre, mat in self.mats_manager.sis_ingresados.items()
        }

        if not path.exists(SISTEMAS_PATH):
            makedirs(path.dirname(SISTEMAS_PATH), exist_ok=True)

        if sistemas_dict == {}:
            with open(SISTEMAS_PATH, "w", encoding="utf-8") as _:
                pass
            return

        with open(SISTEMAS_PATH, mode="w", encoding="utf-8") as sistemas_file:
            dump(sistemas_dict, sistemas_file, indent=4, sort_keys=True, cls=FractionEncoder)

    def save_matrices(self) -> None:
        """
        Escribe el diccionario de matrices ingresadas al archivo matrices.json,
        utilizando FractionEncoder para escribir objetos Fraction().
        """

        matrices_dict = {
            nombre: {
                "aumentada": mat.aumentada,
                "filas": mat.filas,
                "columnas": mat.columnas,
                "valores": mat.valores
            } for nombre, mat in self.mats_manager.mats_ingresadas.items()
        }

        if not path.exists(MATRICES_PATH):
            makedirs(path.dirname(MATRICES_PATH), exist_ok=True)

        if matrices_dict == {}:
            with open(MATRICES_PATH, "w", encoding="utf-8") as _:
                pass
            return

        with open(MATRICES_PATH, mode="w", encoding="utf-8") as matrices_file:
            dump(matrices_dict, matrices_file, indent=4, sort_keys=True, cls=FractionEncoder)

    def save_vectores(self) -> None:
        """
        Escribe el diccionario de vectores ingresados al archivo vectores.json,
        utilizando FractionEncoder para escribir objetos Fraction().
        """

        vectores_dict = {
            nombre: vec.componentes
            for nombre, vec in self.vecs_manager.vecs_ingresados.items()
        }

        if not path.exists(VECTORES_PATH):
            makedirs(path.dirname(VECTORES_PATH), exist_ok=True)

        if vectores_dict == {}:
            with open(VECTORES_PATH, "w", encoding="utf-8") as _:
                pass
            return

        with open(VECTORES_PATH, "w", encoding="utf-8") as vectores_file:
            dump(vectores_dict, vectores_file, indent=4, sort_keys=True, cls=FractionEncoder)

    def _load_sistemas(self) -> dict[str, Matriz]:
        """
        Carga los sistemas guardados en el archivo sistemas.json,
        utilizando FractionDecoder para leer objetos Fraction(),
        y los retorna como un diccionario.
        """

        if not path.exists(SISTEMAS_PATH):
            return {}

        with open(SISTEMAS_PATH, mode="r", encoding="utf-8") as sistemas_file:
            try:
                sistemas_dict: dict = load(sistemas_file, cls=FractionDecoder)
            except JSONDecodeError:
                return {}

            sistemas_file.seek(0)
            sistemas_dict = load(sistemas_file, cls=FractionDecoder)
            return {
                nombre: Matriz(
                    matriz["aumentada"],
                    matriz["filas"],
                    matriz["columnas"],
                    matriz["valores"],
                ) for nombre, matriz in sistemas_dict.items()
            }

    def _load_matrices(self) -> dict[str, Matriz]:
        """
        Carga las matrices guardadas en el archivo matrices.json,
        utilizando FractionDecoder para leer objetos Fraction(),
        y las retorna como un diccionario.
        """

        if not path.exists(MATRICES_PATH):
            return {}

        with open(MATRICES_PATH, mode="r", encoding="utf-8") as matrices_file:
            try:
                matrices_dict: dict = load(matrices_file, cls=FractionDecoder)
            except JSONDecodeError:
                return {}

            matrices_file.seek(0)
            matrices_dict = load(matrices_file, cls=FractionDecoder)
            return {
                nombre: Matriz(
                    matriz["aumentada"],
                    matriz["filas"],
                    matriz["columnas"],
                    matriz["valores"],
                ) for nombre, matriz in matrices_dict.items()
            }

    def _load_vectores(self) -> dict[str, Vector]:
        """
        Carga los vectores guardados en el archivo vectores.json,
        utilizando FractionDecoder para leer objetos Fraction(),
        y los retorna como un diccionario.
        """

        if not path.exists(VECTORES_PATH):
            return {}

        with open(VECTORES_PATH, mode="r", encoding="utf-8") as vectores_file:
            try:
                vectores_dict: dict = load(vectores_file, cls=FractionDecoder)
            except JSONDecodeError:
                return {}

            vectores_file.seek(0)
            vectores_dict = load(vectores_file, cls=FractionDecoder)
            return {
                nombre: Vector(componentes)
                for nombre, componentes in vectores_dict.items()
            }
