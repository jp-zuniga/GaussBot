"""
Implementación de manejador de operaciones globales, encargado de matrices y vectores.
"""

from fractions import Fraction
from json import JSONDecodeError, dump, load

from src import FRAC_PREC
from src.models import FractionDecoder, FractionEncoder, Matriz, Vector
from src.utils import (
    LOGGER,
    MATRICES_PATH,
    SISTEMAS_PATH,
    VECTORES_PATH,
    format_proc_num,
)

from .mats_manager import MatricesManager
from .vecs_manager import VectoresManager


class OpsManager:
    """
    Manager principal, encargado de gestionar todas las operaciones matemáticas.
    """

    def __init__(
        self,
        mats_manager: MatricesManager | None = None,
        vecs_manager: VectoresManager | None = None,
    ) -> None:
        """
        Args:
            mats_manager: Manejador de matrices a utilizar para el sistema.
            vecs_manager: Manejador de vectores a utilizar para el sistema.

        Raises:
            TypeError: Si los argumentos dados no son
                       de tipo MatricesManager | VectoresManager.

        """

        if mats_manager is not None and not isinstance(mats_manager, MatricesManager):
            raise TypeError("Argumento inválido para 'mats_manager'.")

        if vecs_manager is not None and not isinstance(vecs_manager, VectoresManager):
            raise TypeError("Argumento inválido para 'vecs_manager'.")

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
        Multiplicar una matriz por un vector.

        Args:
            nombre_mat: Nombre de la matriz a multiplicar.
            nombre_vec: Nombre del vector a multiplicar.

        Raises:
            ArithmeticError: si la matriz y el vector no son
                             compatibles para la multiplicación.

        Returns:
            (str, str, Matriz): Procedimiento de la operación,
                                nombre de la matriz resultante y
                                la matriz resultante de la multiplicación.

        """

        mat: Matriz = self.mats_manager.mats_ingresadas[nombre_mat]
        vec: Vector = self.vecs_manager.vecs_ingresados[nombre_vec]
        if mat.columnas != len(vec):
            raise ArithmeticError(
                "El número de columnas de la matriz debe ser "
                "igual al número de componentes del vector.",
            )

        # inicializar la lista 2D de la matriz resultante
        multiplicacion: list[list[Fraction]] = [
            [Fraction(0) for _ in range(len(vec))] for _ in range(mat.filas)
        ]

        # realizar la multiplicacion
        for i in range(mat.filas):
            for j, componente in enumerate(vec.componentes):
                multiplicacion[i][j] += mat[i, j] * componente

        mat_resultante = Matriz(mat.filas, len(vec), valores=multiplicacion)
        nombre_mat_resultante = f"{nombre_mat}{nombre_vec}"

        mat_proc = Matriz(
            filas=mat.filas,
            columnas=len(vec),
            valores=[  # type: ignore[reportArgumentType]
                [
                    format_proc_num(
                        (
                            mat[i, j].limit_denominator(FRAC_PREC["prec"]),
                            vec.componentes[j].limit_denominator(FRAC_PREC["prec"]),
                        ),
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
        Escribir el diccionario de sistemas ingresados al archivo 'sistemas.json'.
        """

        # descomponer los objetos Matriz() en mats_manager.sis_ingresados
        # para que se guarden los atributos individuales del objeto,
        # en lugar de una referencia al objeto Matriz() completo
        sistemas_dict: dict[str, dict[str, bool | int | list[list[Fraction]]]] = {
            nombre: {
                "filas": mat.filas,
                "columnas": mat.columnas,
                "valores": mat.valores,
                "aumentada": mat.aumentada,
            }
            for nombre, mat in self.mats_manager.sis_ingresados.items()
        }

        # crear sistemas.json si no existe
        if not SISTEMAS_PATH.exists():
            SISTEMAS_PATH.parent.mkdir(parents=True, exist_ok=True)
            SISTEMAS_PATH.write_text("")
            LOGGER.info("Creando '%s'...", SISTEMAS_PATH)

        # si sis_ingresados esta vacio, dejar sistemas.json vacio y retornar
        if sistemas_dict == {}:
            SISTEMAS_PATH.write_text("")
            LOGGER.info(
                "No hay sistemas de ecuaciones para guardar, dejando archivo vacío...",
            )

            return

        with SISTEMAS_PATH.open(mode="w") as sistemas_file:
            dump(
                sistemas_dict,
                sistemas_file,
                indent=4,
                sort_keys=True,
                cls=FractionEncoder,
            )

            LOGGER.info(
                "Sistemas de ecuaciones guardados en '%s' exitosamente.",
                SISTEMAS_PATH,
            )

    def save_matrices(self) -> None:
        """
        Escribir el diccionario de matrices ingresadas al archivo 'matrices.json'.
        """

        # descomponer los objetos Matriz() en mats_manager.mats_ingresadas
        # para que se guarden los atributos individuales del objeto,
        # en lugar de una referencia al objeto Matriz() completo
        matrices_dict: dict[str, dict[str, bool | int | list[list[Fraction]]]] = {
            nombre: {
                "filas": mat.filas,
                "columnas": mat.columnas,
                "valores": mat.valores,
                "aumentada": mat.aumentada,
            }
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
        }

        # crear matrices.json si no existe
        if not MATRICES_PATH.exists():
            MATRICES_PATH.parent.mkdir(parents=True, exist_ok=True)
            MATRICES_PATH.write_text("")
            LOGGER.info("Creando '%s'...", MATRICES_PATH)

        # si mats_ingresadas esta vacio, dejar matrices.json vacio y retornar
        if matrices_dict == {}:
            MATRICES_PATH.write_text("")
            LOGGER.info("No hay matrices para guardar, dejando archivo vacío...")
            return

        with MATRICES_PATH.open(mode="w") as matrices_file:
            dump(
                matrices_dict,
                matrices_file,
                indent=4,
                sort_keys=True,
                cls=FractionEncoder,
            )

            LOGGER.info("Matrices guardadas en '%s' exitosamente.", MATRICES_PATH)

    def save_vectores(self) -> None:
        """
        Escribir el diccionario de vectores ingresados al archivo 'vectores.json'.
        """

        # descomponer los objetos Vector() en vecs_manager.vecs_ingresados
        # para que se guarden la lista de componentes directamente,
        # en lugar de una referencia al objeto Vector() completo
        vectores_dict: dict[str, list[Fraction]] = {
            nombre: vec.componentes
            for nombre, vec in self.vecs_manager.vecs_ingresados.items()
        }

        # crear vectores.json si no existe
        if not VECTORES_PATH.exists():
            VECTORES_PATH.parent.mkdir(parents=True, exist_ok=True)
            VECTORES_PATH.write_text("")
            LOGGER.info("Creando '%s'...", VECTORES_PATH)

        # si vecs_ingresados esta vacio, dejar vectores.json vacio y retornar
        if vectores_dict == {}:
            VECTORES_PATH.write_text("")
            LOGGER.info("No hay vectores para guardar, dejando archivo vacío...")
            return

        with VECTORES_PATH.open(mode="w") as vectores_file:
            dump(
                vectores_dict,
                vectores_file,
                indent=4,
                sort_keys=True,
                cls=FractionEncoder,
            )

            LOGGER.info("Vectores guardados en '%s' exitosamente.", VECTORES_PATH)

    def _load_sistemas(self) -> dict[str, Matriz]:
        """
        Cargar los sistemas guardados en el archivo 'sistemas.json'.

        Returns:
            dict[str, Matriz]: Diccionario con los sistemas cargados.

        """

        # si no existe sistemas.json, retornar un diccionario vacio
        if not SISTEMAS_PATH.exists():
            LOGGER.info("Archivo '%s' no existe...", SISTEMAS_PATH)
            return {}

        with SISTEMAS_PATH.open() as sistemas_file:
            try:
                sistemas_dict: dict = load(sistemas_file, cls=FractionDecoder)
                LOGGER.info("Sistemas de ecuaciones cargados exitosamente.")
                return {
                    nombre: Matriz(
                        matriz["filas"],
                        matriz["columnas"],
                        matriz["valores"],
                        matriz["aumentada"],
                    )
                    for nombre, matriz in sistemas_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info("Archivo '%s' está vacío...", SISTEMAS_PATH)
                else:
                    # si no, es un error de verdad
                    LOGGER.error(
                        "Error al leer archivo '%s':\n%s",
                        SISTEMAS_PATH,
                        str(j),
                    )
                return {}

    def _load_matrices(self) -> dict[str, Matriz]:
        """
        Carga las matrices guardadas en el archivo 'matrices.json'.

        Returns:
            dict[str, Matriz]: Diccionario con las matrices cargadas.

        """

        if not MATRICES_PATH.exists():
            LOGGER.info("Archivo '%s' no existe...", MATRICES_PATH)
            return {}

        with MATRICES_PATH.open() as matrices_file:
            try:
                matrices_dict: dict = load(matrices_file, cls=FractionDecoder)
                LOGGER.info("Matrices cargadas exitosamente.")
                return {
                    nombre: Matriz(
                        matriz["filas"],
                        matriz["columnas"],
                        matriz["valores"],
                        matriz["aumentada"],
                    )
                    for nombre, matriz in matrices_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info("Archivo '%s' vacío...", MATRICES_PATH)
                else:
                    # si no, es un error de verdad
                    LOGGER.error(
                        "Error al leer archivo '%s':\n%s",
                        MATRICES_PATH,
                        str(j),
                    )
                return {}

    def _load_vectores(self) -> dict[str, Vector]:
        """
        Carga los vectores guardados en el archivo 'vectores.json'.

        Returns:
            dict[str, Vector]: Diccionario con los vectores cargados.

        """

        if not VECTORES_PATH.exists():
            LOGGER.info("Archivo '%s' no existe...", VECTORES_PATH)
            return {}

        with VECTORES_PATH.open() as vectores_file:
            try:
                vectores_dict: dict = load(vectores_file, cls=FractionDecoder)
                LOGGER.info("Vectores cargados exitosamente.")
                return {
                    nombre: Vector(componentes)
                    for nombre, componentes in vectores_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info("Archivo '%s' vacío...", VECTORES_PATH)
                else:
                    # si no, es un error de verdad
                    LOGGER.error(
                        "Error al leer archivo '%s':\n%s",
                        VECTORES_PATH,
                        str(j),
                    )
                return {}
