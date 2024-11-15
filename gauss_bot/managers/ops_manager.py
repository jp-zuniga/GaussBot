"""
Implementación de OpsManager.
Utilizado principalmente para contener
los datos de MatricesManager y VectoresManager.
"""

from fractions import Fraction
from json import (
    JSONDecodeError,
    dump,
    load,
)

from os import (
    makedirs,
    path,
)

from gauss_bot import (
    SISTEMAS_PATH,
    MATRICES_PATH,
    VECTORES_PATH,
    LOGGER,
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
    Esencialmente un wrapper para contener los datos de matrices y vectores.
    Se encarga de leer y escribir los datos a archivos .json,
    y de realizar la multiplicación de matrices por vectores.
    """

    def __init__(self, mats_manager=None, vecs_manager=None) -> None:
        """
        * TypeError: si mats_manager/vecs_manager no son MatricesManager/VectoresManager
        """

        if (
            mats_manager is not None
            and
            not isinstance(mats_manager, MatricesManager)
        ):
            raise TypeError("Argumento inválido para 'mats_manager'!")

        if (
            vecs_manager is not None
            and
            not isinstance(vecs_manager, VectoresManager)
        ):
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
        - ArithmeticError: si la matriz y el vector no son compatibles
                           para la multiplicación.

        Retorna una tupla con:
        * str: nombre de la matriz resultante
        * Matriz(): objeto de la matriz resultante de la multiplicación.
        """

        mat = self.mats_manager.mats_ingresadas[nombre_mat]
        vec = self.vecs_manager.vecs_ingresados[nombre_vec]
        if mat.columnas != len(vec):
            raise ArithmeticError(
                "El número de columnas de la matriz debe ser " +
                "igual al número de componentes del vector!"
            )

        # inicializar la lista 2D de la matriz resultante
        multiplicacion = [
            [Fraction(0) for _ in range(len(vec))]
            for _ in range(mat.filas)
        ]

        # realizar la multiplicacion
        for i in range(mat.filas):
            for j, componente in enumerate(vec.componentes):
                multiplicacion[i][j] += mat[i, j] * componente

        mat_resultante = Matriz(False, mat.filas, len(vec), multiplicacion)
        nombre_mat_resultante = f"{nombre_mat}{nombre_vec}"
        return (nombre_mat_resultante, mat_resultante)

    def save_sistemas(self) -> None:
        """
        Escribe el diccionario de sistemas ingresados al archivo sistemas.json,
        utilizando FractionEncoder() para escribir objetos Fraction().
        """

        # descomponer los objetos Matriz() en mats_manager.sis_ingresados
        # para que se guarden los atributos individuales del objeto,
        # en lugar de una referencia al objeto Matriz() completo
        sistemas_dict = {
            nombre: {
                "aumentada": mat.aumentada,
                "filas": mat.filas,
                "columnas": mat.columnas,
                "valores": mat.valores
            } for nombre, mat in self.mats_manager.sis_ingresados.items()
        }

        # crear sistemas.json si no existe
        if not path.exists(SISTEMAS_PATH):
            makedirs(path.dirname(SISTEMAS_PATH), exist_ok=True)
            LOGGER.info("Creando archivo 'sistemas.json'...")

        # si sis_ingresados esta vacio, dejar sistemas.json vacio y retornar
        if sistemas_dict == {}:
            with open(SISTEMAS_PATH, "w", encoding="utf-8") as _:
                LOGGER.info(
                    "No hay sistemas de ecuaciones para guardar, " +
                    "dejando 'sistemas.json' vacío..."
                )
            return

        with open(SISTEMAS_PATH, mode="w", encoding="utf-8") as sistemas_file:
            dump(
                sistemas_dict,
                sistemas_file,
                indent=4,
                sort_keys=True,
                cls=FractionEncoder,
            )

            LOGGER.info(
                "Sistemas de ecuaciones guardados en 'sistemas.json'!"
            )

    def save_matrices(self) -> None:
        """
        Escribe el diccionario de matrices ingresadas al archivo matrices.json,
        utilizando FractionEncoder() para escribir objetos Fraction().
        """

        # descomponer los objetos Matriz() en mats_manager.mats_ingresadas
        # para que se guarden los atributos individuales del objeto,
        # en lugar de una referencia al objeto Matriz() completo
        matrices_dict = {
            nombre: {
                "aumentada": mat.aumentada,
                "filas": mat.filas,
                "columnas": mat.columnas,
                "valores": mat.valores
            } for nombre, mat in self.mats_manager.mats_ingresadas.items()
        }

        # crear matrices.json si no existe
        if not path.exists(MATRICES_PATH):
            makedirs(path.dirname(MATRICES_PATH), exist_ok=True)
            LOGGER.info("Creando archivo 'matrices.json'...")

        # si mats_ingresadas esta vacio, dejar matrices.json vacio y retornar
        if matrices_dict == {}:
            with open(MATRICES_PATH, "w", encoding="utf-8") as _:
                LOGGER.info(
                    "No hay matrices para guardar, " +
                    "dejando 'matrices.json' vacío..."
                )
            return

        with open(MATRICES_PATH, mode="w", encoding="utf-8") as matrices_file:
            dump(
                matrices_dict,
                matrices_file,
                indent=4,
                sort_keys=True,
                cls=FractionEncoder,
            )

            LOGGER.info(
                "Matrices guardadas en 'matrices.json'!"
            )

    def save_vectores(self) -> None:
        """
        Escribe el diccionario de vectores ingresados al archivo vectores.json,
        utilizando FractionEncoder() para escribir objetos Fraction().
        """

        # descomponer los objetos Vector() en vecs_manager.vecs_ingresados
        # para que se guarden la lista de componentes directamente,
        # en lugar de una referencia al objeto Vector() completo
        vectores_dict = {
            nombre: vec.componentes
            for nombre, vec in self.vecs_manager.vecs_ingresados.items()
        }

        # crear vectores.json si no existe
        if not path.exists(VECTORES_PATH):
            makedirs(path.dirname(VECTORES_PATH), exist_ok=True)
            LOGGER.info("Creando archivo 'vectores.json'...")

        # si vecs_ingresados esta vacio, dejar vectores.json vacio y retornar
        if vectores_dict == {}:
            with open(VECTORES_PATH, "w", encoding="utf-8") as _:
                LOGGER.info(
                    "No hay vectores para guardar, " +
                    "dejando 'vectores.json' vacío..."
                )
            return

        with open(VECTORES_PATH, "w", encoding="utf-8") as vectores_file:
            dump(
                vectores_dict,
                vectores_file,
                indent=4,
                sort_keys=True,
                cls=FractionEncoder,
            )

            LOGGER.info(
                "Vectores guardados en 'vectores.json'!"
            )

    def _load_sistemas(self) -> dict[str, Matriz]:
        """
        Carga los sistemas guardados en el archivo sistemas.json,
        utilizando FractionDecoder() para leer objetos Fraction().

        Retorna un diccionario con los sistemas cargados y sus nombres.
        """

        # si no existe sistemas.json, retornar un diccionario vacio
        if not path.exists(SISTEMAS_PATH):
            LOGGER.info("Archivo 'sistemas.json' no existe...")
            return {}

        with open(SISTEMAS_PATH, mode="r", encoding="utf-8") as sistemas_file:
            try:
                sistemas_dict: dict = load(sistemas_file, cls=FractionDecoder)
                LOGGER.info("Sistemas de ecuaciones cargados!")
                return {
                    nombre: Matriz(
                        matriz["aumentada"],
                        matriz["filas"],
                        matriz["columnas"],
                        matriz["valores"],
                    ) for nombre, matriz in sistemas_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info("Archivo 'sistemas.json' vacío...")
                else:
                    # si no, es un error de verdad
                    LOGGER.error(
                        "Error al leer archivo 'sistemas.json':\n%s", str(j)
                    )
                return {}

    def _load_matrices(self) -> dict[str, Matriz]:
        """
        Carga las matrices guardadas en el archivo matrices.json,
        utilizando FractionDecoder para leer objetos Fraction().

        Retorna un diccionario con las matrices cargadas y sus nombres.
        """

        if not path.exists(MATRICES_PATH):
            LOGGER.info("Archivo 'matrices.json' no existe...")
            return {}

        with open(MATRICES_PATH, mode="r", encoding="utf-8") as matrices_file:
            try:
                matrices_dict: dict = load(matrices_file, cls=FractionDecoder)
                LOGGER.info("Matrices cargadas!")
                return {
                    nombre: Matriz(
                        matriz["aumentada"],
                        matriz["filas"],
                        matriz["columnas"],
                        matriz["valores"],
                    ) for nombre, matriz in matrices_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info("Archivo 'matrices.json' vacío...")
                else:
                    # si no, es un error de verdad
                    LOGGER.error(
                        "Error al leer archivo 'matrices.json':\n%s", str(j)
                    )
                return {}

    def _load_vectores(self) -> dict[str, Vector]:
        """
        Carga los vectores guardados en el archivo vectores.json,
        utilizando FractionDecoder para leer objetos Fraction().

        Retorna un diccionario con los vectores cargados y sus nombres.
        """

        if not path.exists(VECTORES_PATH):
            LOGGER.info("Archivo 'vectores.json' no existe...")
            return {}

        with open(VECTORES_PATH, mode="r", encoding="utf-8") as vectores_file:
            try:
                vectores_dict: dict = load(vectores_file, cls=FractionDecoder)
                LOGGER.info("Vectores cargados!")
                return {
                    nombre: Vector(componentes)
                    for nombre, componentes in vectores_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info("Archivo 'vectores.json' vacío...")
                else:
                    # si no, es un error de verdad
                    LOGGER.error(
                        "Error al leer archivo 'vectores.json':\n%s", str(j)
                    )
                return {}
