from copy import deepcopy
from fractions import Fraction

from gauss_bot.models.Matriz import Matriz
from gauss_bot.models.SistemaEcuaciones import SistemaEcuaciones


class MatricesManager:
    """
    Se encarga de almacenar las matrices ingresadas por el usuario,
    realizar operaciones con ellas, y retornar los resultados.
    """

    def __init__(self, mats_ingresadas=None) -> None:
        if mats_ingresadas is None:
            self.mats_ingresadas: dict[str, Matriz] = {}
        elif (isinstance(mats_ingresadas, dict)
              and all(isinstance(n, str) for n in mats_ingresadas.keys())
              and all(isinstance(m, Matriz) for m in mats_ingresadas.values())):
            self.mats_ingresadas = mats_ingresadas
        else:
            raise TypeError("Argumento inválido para 'mats_ingresadas'!")

    def get_matrices(self) -> str:
        """
        Obtiene las matrices guardadas en self.mats_ingresadas y las retorna como string.
        """

        if not self.validar_mats_ingresadas():
            return "\nNo hay matrices ingresadas!"

        matrices = "\nMatrices guardadas:\n"
        matrices += "---------------------------------------------"
        for nombre, mat in self.mats_ingresadas.items():
            matrices += f"\n{nombre}:\n"
            matrices += str(mat)
        matrices += "---------------------------------------------\n"
        return matrices

    def resolver_sistema(self, nombre_mat: str, metodo: str) -> tuple[str, SistemaEcuaciones]:
        mat_copia = deepcopy(self.mats_ingresadas[nombre_mat])
        sistema = SistemaEcuaciones(mat_copia)

        if metodo == "gj":
            sistema.gauss_jordan()
        elif metodo == "c":
            sistema.cramer(nombre_mat)
        else:
            raise ValueError("Argumento inválido para 'metodo'!")

        nombre_sistema = f"{nombre_mat}_r"
        return (nombre_sistema, sistema)

    def sumar_matrices(self, nombre_mat1: str, nombre_mat2: str) -> tuple[str, Matriz]:
        mat1 = self.mats_ingresadas[nombre_mat1]
        mat2 = self.mats_ingresadas[nombre_mat2]

        mat_suma = mat1 + mat2
        nombre_mat_suma = f"{nombre_mat1} + {nombre_mat2}"
        return (nombre_mat_suma, mat_suma)

    def restar_matrices(self, nombre_mat1: str, nombre_mat2: str) -> tuple[str, Matriz]:
        mat1 = self.mats_ingresadas[nombre_mat1]
        mat2 = self.mats_ingresadas[nombre_mat2]

        mat_resta = mat1 - mat2
        nombre_mat_resta = f"{nombre_mat1} − {nombre_mat2}"
        return (nombre_mat_resta, mat_resta)

    def escalar_por_matriz(self, escalar: Fraction, nombre_mat: str) -> tuple[str, Matriz]:
        mat = self.mats_ingresadas[nombre_mat]
        mat_multiplicado = mat * escalar

        if escalar == Fraction(1):
            escalar_str = ""
        elif escalar == Fraction(-1):
            escalar_str = "-"
        elif escalar.is_integer():
            escalar_str = str(escalar)
        else:
            escalar_str = f"({escalar}) * "

        nombre_mat_multiplicado = f"{escalar_str}{nombre_mat}"
        return (nombre_mat_multiplicado, mat_multiplicado)

    def mult_matricial(self, nombre_mat1: str, nombre_mat2: str) -> tuple[str, Matriz]:
        mat1 = self.mats_ingresadas[nombre_mat1]
        mat2 = self.mats_ingresadas[nombre_mat2]

        mat_mult = mat1 * mat2
        nombre_mat_mult = f"{nombre_mat1} * {nombre_mat2}"
        return (nombre_mat_mult, mat_mult)

    def transponer_matriz(self, nombre_mat: str) -> tuple[str, Matriz]:
        mat = self.mats_ingresadas[nombre_mat]
        nombre_mat_transpuesta = f"{nombre_mat}_t"
        mat_transpuesta = mat.transponer()
        return (nombre_mat_transpuesta, mat_transpuesta)

    def calcular_determinante(self, nombre_mat: str) -> tuple[Fraction, "Matriz", bool]:
        mat = self.mats_ingresadas[nombre_mat]
        return mat.calcular_det()

    def encontrar_inversa(self, nombre_mat: str) -> tuple[str, "Matriz", "Matriz", Fraction]:
        mat = self.mats_ingresadas[nombre_mat]
        nombre_mat_invertida = f"{nombre_mat}_i"
        inversa, adjunta, det = mat.invertir()
        return (nombre_mat_invertida, inversa, adjunta, det)

    def validar_input_mat(self, input_mat: str, operacion: str) -> None:
        """
        Valida la matriz seleccionada por el usuario.
        * KeyError: si la matriz seleccionada no existe
        * TypeError: si se resolverá un sistema de ecuaciones y la matriz seleccionada no es aumentada
        * ArithmeticError: si se desea calcular determinante y la matriz seleccionada no es cuadrada
        """

        if input_mat not in self.mats_ingresadas:
            raise KeyError(f"La matriz '{input_mat}' no existe!")
        if operacion == "se" and not self.mats_ingresadas[input_mat].aumentada:
            raise TypeError(f"La matriz '{input_mat}' no es aumentada; no representa un sistema de ecuaciones!")
        if operacion in ("d", "i") and not self.mats_ingresadas[input_mat].es_cuadrada():
            raise ArithmeticError(f"La matriz '{input_mat}' no es cuadrada; su determinante es indefinido!")

    def validar_input_mats(self, input_mats: list[str], operacion: str) -> None:
        """
        Valida las matrices seleccionadas por el usuario.
        * KeyError: si una de las matrices seleccionadas no existe
        * ArithmeticError: si las matrices no tienen las dimensiones válidas para la operación
        """

        mat = next((mat for mat in input_mats if mat not in self.mats_ingresadas), None)
        if mat is not None:
            raise KeyError(f"La matriz '{mat}' no existe!")

        mat1, mat2 = (
            self.mats_ingresadas[input_mats[0]],
            self.mats_ingresadas[input_mats[1]],
        )

        if operacion in ("s", "r"):
            dimensiones_validas = mat1.filas == mat2.filas and mat1.columnas == mat2.columnas
            if not dimensiones_validas:
                raise ArithmeticError("Las matrices no tienen las mismas dimensiones!")
        elif operacion == "m":
            dimensiones_validas = mat1.columnas == mat2.filas
            if not dimensiones_validas:
                raise ArithmeticError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz!")

    def validar_mats_ingresadas(self) -> bool:
        """
        Valida si el diccionario de matrices ingresadas esta vacío o no.
        """

        if self.mats_ingresadas == {}:
            return False
        return True
