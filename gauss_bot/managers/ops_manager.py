from fractions import Fraction
from json import (
    JSONEncoder,
    JSONDecoder,
    dump,
    load
)

from os import path

from gauss_bot.models.Matriz import Matriz
from gauss_bot.models.Vector import Vector
from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager

MATRICES_PATH = path.join(path.dirname(path.dirname(path.realpath(__file__))), "data", "matrices.json")
VECTORES_PATH = path.join(path.dirname(path.dirname(path.realpath(__file__))), "data", "vectores.json")


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

        self.mats_manager = (
            MatricesManager(self.load_matrices())
            if mats_manager is None
            else mats_manager
        )

        self.vecs_manager = (
            VectoresManager(self.load_vectores())
            if vecs_manager is None
            else vecs_manager
        )

    def producto_matriz_vector(self, nombre_mat: str, nombre_vec: str) -> tuple[str, Matriz]:
        """
        Realiza la multiplicación de una matriz por un vector.
        """

        mat = self.mats_manager.mats_ingresadas[nombre_mat]
        vec = self.vecs_manager.vecs_ingresados[nombre_vec]
        if mat.columnas != len(vec):
            raise ArithmeticError("El número de columnas de la matriz debe ser igual al número de componentes del vector!")

        multiplicacion = [[Fraction(0) for _ in range(len(vec))] for _ in range(mat.filas)]
        for i in range(mat.filas):
            for j, componente in enumerate(vec.componentes):
                multiplicacion[i][j] += mat[i, j] * componente

        mat_resultante = Matriz(False, mat.filas, len(vec), multiplicacion)
        nombre_mat_resultante = f"{nombre_mat}{nombre_vec}"
        return (nombre_mat_resultante, mat_resultante)

    def load_matrices(self) -> dict[str, Matriz]:
        """
        Carga las matrices guardadas en el archivo matrices.json y las retorna como un diccionario.
        """

        if not path.exists(MATRICES_PATH):
            return {}

        with open(MATRICES_PATH) as matrices_file:
            matrices_dict = load(matrices_file, cls=FractionDecoder)
            return {
                nombre: Matriz(matriz["aumentada"], matriz["filas"], matriz["columnas"], matriz["valores"])
                for nombre, matriz in matrices_dict.items()
            }

    def load_vectores(self) -> dict[str, Vector]:
        """
        Carga los vectores guardados en el archivo vectores.json y los retorna como un diccionario.
        """

        if not path.exists(VECTORES_PATH):
            return {}

        with open(VECTORES_PATH) as vectores_file:
            vectores_dict = load(vectores_file, cls=FractionDecoder)
            return {nombre: Vector(componentes) for nombre, componentes in vectores_dict.items()}

    def save_matrices(self):
        matrices_dict = {
            nombre: {
                "aumentada": mat.aumentada,
                "filas": mat.filas,
                "columnas": mat.columnas,
                "valores": mat.valores
            } for nombre, mat in self.mats_manager.mats_ingresadas.items()
        }

        with open(MATRICES_PATH, 'w') as matrices_file:
            dump(matrices_dict, matrices_file, indent=4, cls=FractionEncoder)

    def save_vectores(self):
        vectores_dict = {
            nombre: vec.componentes
            for nombre, vec in self.vecs_manager.vecs_ingresados.items()
        }

        with open(VECTORES_PATH, 'w') as vectores_file:
            dump(vectores_dict, vectores_file, indent=4, cls=FractionEncoder)


class FractionEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Fraction):
            return {
                "__type__": "Fraction",
                "numerator": obj.numerator,
                "denominator": obj.denominator
            }

        return super().default(obj)


class FractionDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "__type__" in obj and obj["__type__"] == "Fraction":
            return Fraction(obj["numerator"], obj["denominator"])
        return obj
