"""
Implementación de OpsManager.
Utilizado principalmente para contener
los datos de MatricesManager y VectoresManager.
"""

from fractions import Fraction
from json import JSONDecodeError, dump, load

from . import MatricesManager, VectoresManager
from ..models import FractionDecoder, FractionEncoder, Matriz, Vector
from ..utils import LOGGER, MATRICES_PATH, SISTEMAS_PATH, VECTORES_PATH, format_proc_num


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

        if mats_manager is not None and not isinstance(mats_manager, MatricesManager):
            raise TypeError("¡Argumento inválido para 'mats_manager'!")

        if vecs_manager is not None and not isinstance(vecs_manager, VectoresManager):
            raise TypeError("¡Argumento inválido para 'vecs_manager'!")

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

    def mat_por_vec(self, nombre_mat: str, nombre_vec: str) -> tuple[str, str, Matriz]:
        """
        Realiza la multiplicación de una matriz por un vector.
        - ArithmeticError: si la matriz y el vector no son compatibles
                           para la multiplicación.

        Retorna una tupla con:
        * str: procedimiento de la operación
        * str: nombre de la matriz resultante
        * Matriz(): objeto de la matriz resultante de la multiplicación.
        """

        mat = self.mats_manager.mats_ingresadas[nombre_mat]
        vec = self.vecs_manager.vecs_ingresados[nombre_vec]
        if mat.columnas != len(vec):
            raise ArithmeticError(
                "El número de columnas de la matriz debe ser "
                + "igual al número de componentes del vector."
            )

        # inicializar la lista 2D de la matriz resultante
        multiplicacion = [
            [Fraction(0) for _ in range(len(vec))] for _ in range(mat.filas)
        ]

        # realizar la multiplicacion
        for i in range(mat.filas):
            for j, componente in enumerate(vec.componentes):
                multiplicacion[i][j] += mat[i, j] * componente

        mat_resultante = Matriz(False, mat.filas, len(vec), multiplicacion)
        nombre_mat_resultante = f"{nombre_mat}{nombre_vec}"

        mat_proc = Matriz(
            aumentada=False,
            filas=mat.filas,
            columnas=len(vec),
            valores=[
                [
                    format_proc_num(  # type: ignore
                        (
                            mat[i, j].limit_denominator(1000),
                            vec.componentes[j].limit_denominator(1000),
                        )
                    )
                    for j in range(len(vec))
                ]
                for i in range(mat.filas)
            ],
        )

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n\n"
        proc += f"{nombre_vec}:\n{vec}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_resultante}:\n{mat_proc}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_resultante}:\n{mat_resultante}\n"
        proc += "---------------------------------------------"

        return (proc, nombre_mat_resultante, mat_resultante)

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
                "valores": mat.valores,
            }
            for nombre, mat in self.mats_manager.sis_ingresados.items()
        }

        # crear sistemas.json si no existe
        if not SISTEMAS_PATH.exists():
            SISTEMAS_PATH.parent.mkdir(parents=True, exist_ok=True)
            SISTEMAS_PATH.write_text("")
            LOGGER.info(f"Creando '{SISTEMAS_PATH}'...")

        # si sis_ingresados esta vacio, dejar sistemas.json vacio y retornar
        if sistemas_dict == {}:
            SISTEMAS_PATH.write_text("")
            LOGGER.info(
                "No hay sistemas de ecuaciones para guardar, dejando archivo vacío..."
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
                f"¡Sistemas de ecuaciones guardados en '{SISTEMAS_PATH}' exitosamente!"
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
                "valores": mat.valores,
            }
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
        }

        # crear matrices.json si no existe
        if not MATRICES_PATH.exists():
            MATRICES_PATH.parent.mkdir(parents=True, exist_ok=True)
            MATRICES_PATH.write_text("")
            LOGGER.info(f"Creando '{MATRICES_PATH}'...")

        # si mats_ingresadas esta vacio, dejar matrices.json vacio y retornar
        if matrices_dict == {}:
            MATRICES_PATH.write_text("")
            LOGGER.info("No hay matrices para guardar, dejando archivo vacío...")
            return

        with open(MATRICES_PATH, mode="w", encoding="utf-8") as matrices_file:
            dump(
                matrices_dict,
                matrices_file,
                indent=4,
                sort_keys=True,
                cls=FractionEncoder,
            )

            LOGGER.info(f"¡Matrices guardadas en '{MATRICES_PATH}' exitosamente!")

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
        if not VECTORES_PATH.exists():
            VECTORES_PATH.parent.mkdir(parents=True, exist_ok=True)
            VECTORES_PATH.write_text("")
            LOGGER.info(f"Creando '{VECTORES_PATH}'...")

        # si vecs_ingresados esta vacio, dejar vectores.json vacio y retornar
        if vectores_dict == {}:
            VECTORES_PATH.write_text("")
            LOGGER.info("No hay vectores para guardar, dejando archivo vacío...")
            return

        with open(VECTORES_PATH, "w", encoding="utf-8") as vectores_file:
            dump(
                vectores_dict,
                vectores_file,
                indent=4,
                sort_keys=True,
                cls=FractionEncoder,
            )

            LOGGER.info(f"¡Vectores guardados en '{VECTORES_PATH}' exitosamente!")

    def _load_sistemas(self) -> dict[str, Matriz]:
        """
        Carga los sistemas guardados en el archivo sistemas.json,
        utilizando FractionDecoder() para leer objetos Fraction().

        Retorna un diccionario con los sistemas cargados y sus nombres.
        """

        # si no existe sistemas.json, retornar un diccionario vacio
        if not SISTEMAS_PATH.exists():
            LOGGER.info(f"Archivo {SISTEMAS_PATH} no existe...")
            return {}

        with open(SISTEMAS_PATH, mode="r", encoding="utf-8") as sistemas_file:
            try:
                sistemas_dict: dict = load(sistemas_file, cls=FractionDecoder)
                LOGGER.info("¡Sistemas de ecuaciones cargados exitosamente!")
                return {
                    nombre: Matriz(
                        matriz["aumentada"],
                        matriz["filas"],
                        matriz["columnas"],
                        matriz["valores"],
                    )
                    for nombre, matriz in sistemas_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info(f"Archivo {SISTEMAS_PATH} está vacío...")
                else:
                    # si no, es un error de verdad
                    LOGGER.error(f"Error al leer archivo '{SISTEMAS_PATH}':\n{str(j)}")
                return {}

    def _load_matrices(self) -> dict[str, Matriz]:
        """
        Carga las matrices guardadas en el archivo matrices.json,
        utilizando FractionDecoder para leer objetos Fraction().

        Retorna un diccionario con las matrices cargadas y sus nombres.
        """

        if not MATRICES_PATH.exists():
            LOGGER.info(f"Archivo '{MATRICES_PATH}' no existe...")
            return {}

        with open(MATRICES_PATH, mode="r", encoding="utf-8") as matrices_file:
            try:
                matrices_dict: dict = load(matrices_file, cls=FractionDecoder)
                LOGGER.info("¡Matrices cargadas exitosamente!")
                return {
                    nombre: Matriz(
                        matriz["aumentada"],
                        matriz["filas"],
                        matriz["columnas"],
                        matriz["valores"],
                    )
                    for nombre, matriz in matrices_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info(f"Archivo '{MATRICES_PATH}' vacío...")
                else:
                    # si no, es un error de verdad
                    LOGGER.error(f"Error al leer archivo '{MATRICES_PATH}':\n{str(j)}")
                return {}

    def _load_vectores(self) -> dict[str, Vector]:
        """
        Carga los vectores guardados en el archivo vectores.json,
        utilizando FractionDecoder para leer objetos Fraction().

        Retorna un diccionario con los vectores cargados y sus nombres.
        """

        if not VECTORES_PATH.exists():
            LOGGER.info(f"Archivo '{VECTORES_PATH}' no existe...")
            return {}

        with open(VECTORES_PATH, mode="r", encoding="utf-8") as vectores_file:
            try:
                vectores_dict: dict = load(vectores_file, cls=FractionDecoder)
                LOGGER.info("¡Vectores cargados exitosamente!")
                return {
                    nombre: Vector(componentes)
                    for nombre, componentes in vectores_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info(f"Archivo '{VECTORES_PATH}' vacío...")
                else:
                    # si no, es un error de verdad
                    LOGGER.error(f"Error al leer archivo '{VECTORES_PATH}':\n{str(j)}")
                return {}
