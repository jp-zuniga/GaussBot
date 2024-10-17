from fractions import Fraction
from json import load
from os import path

from gauss_bot.models.vector import Vector

VECTORES_PATH = path.join(path.dirname(path.dirname(path.realpath(__file__))), "data", "vectores.json")


class VectoresManager:
    """
    Se encarga de almacenar los vectores ingresados por el usuario,
    realizar operaciones con ellos, y retornar los resultados.
    """

    def __init__(self, vecs_ingresados=None) -> None:
        if vecs_ingresados is None:
            self.vecs_ingresados = self.load_vectores()
        elif type(vecs_ingresados) is dict[str, Vector]:
            self.vecs_ingresados = vecs_ingresados
        else:
            raise TypeError("Argumento inválido para 'vecs_ingresados'!")

    def load_vectores(self) -> dict[str, Vector]:
        """
        Carga los vectores guardados en el archivo vectores.json y los retorna como un diccionario.
        """

        if not path.exists(VECTORES_PATH):
            return {}

        with open(VECTORES_PATH) as vectores_file:
            vectores_dict = load(vectores_file)
            return {nombre: Vector(componentes) for nombre, componentes in vectores_dict.items()}

    def get_vectores(self) -> str:
        """
        Obtiene los vectores guardados en self.vecs_ingresados y los retorna como un string.
        """

        if not self.validar_vecs_ingresados():
            return "\nNo hay vectores ingresados!"

        vectores = ""
        vectores += "\nVectores ingresados:\n"
        vectores += "---------------------------------------------\n"
        for nombre, vec in self.vecs_ingresados.items():
            vectores += f"{nombre}: {vec}\n"
        vectores += "---------------------------------------------"
        return vectores

    def sumar_vecs(self, nombre_vec1: str, nombre_vec2: str) -> tuple[str, Vector]:
        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        vec_suma = vec1 + vec2
        nombre_vec_suma = f"{nombre_vec1} + {nombre_vec2}"
        return (nombre_vec_suma, vec_suma)

    def restar_vecs(self, nombre_vec1: str, nombre_vec2: str) -> tuple[str, Vector]:
        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        vec_resta = vec1 - vec2
        nombre_vec_resta = f"{nombre_vec1} - {nombre_vec2}"
        return (nombre_vec_resta, vec_resta)

    def escalar_por_vector(self, escalar: Fraction, nombre_vec: str) -> tuple[str, Vector]:
        vec = self.vecs_ingresados[nombre_vec]
        vec_multiplicado = vec * escalar

        if escalar == Fraction(1):
            escalar_str = ""
        elif escalar == Fraction(-1):
            escalar_str = "-"
        elif escalar.is_integer():
            escalar_str = str(escalar)
        else:
            escalar_str = f"({escalar}) * "

        nombre_vec_multiplicado = f"{escalar_str}{nombre_vec}"
        return (nombre_vec_multiplicado, vec_multiplicado)

    def producto_punto(self, nombre_vec1: str, nombre_vec2: str) -> tuple[str, Fraction]:
        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        prod_punto = vec1 * vec2
        nombre_prod_punto = f"{nombre_vec1}.{nombre_vec2}"
        return (nombre_prod_punto, prod_punto)

    def validar_input_vec(self, input_vec: str) -> None:
        """
        Valida el vector seleccionado por el usuario.
        * KeyError: si el vector no existe en vecs_ingresados
        """

        if input_vec not in self.vecs_ingresados:
            raise KeyError(f"El vector '{input_vec}' no existe!")

    def validar_input_vecs(self, input_vecs: list[str]) -> None:
        """
        Valida los vectores seleccionados por el usuario.
        * KeyError: si uno de los vectores seleccionados no existe
        * ArithmeticError: si los vectores no tienen las mismas dimensiones
        """

        vec = next((vec for vec in input_vecs if vec not in self.vecs_ingresados), None)
        if vec is not None:
            raise KeyError(f"El vector '{vec}' no existe!")
        vec1, vec2 = input_vecs
        if len(vec1) != len(vec2):
            raise ArithmeticError("Los vectores no tienen las mismas dimensiones!")

    def validar_vecs_ingresados(self) -> bool:
        """
        Valida si el diccionario de vectores ingresados esta vacío o no.
        """

        if self.vecs_ingresados == {}:
            return False
        return True
