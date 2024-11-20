"""
Implementación de FuncManager.
Almacena y valida las funciones ingresadas por el usuario.
"""

from json import (
    dump,
    load,
    JSONDecodeError,
)

from os import (
    makedirs,
    path,
)

from gauss_bot.models import Func
from gauss_bot import (
    FUNCIONES_PATH,
    LOGGER,
)


class FuncManager:
    """
    Se encarga de almacenar y validar
    las funciones ingresadas por el usuario,
    para su uso en los módulos de análisis numérico.
    """

    def __init__(self, funcs_ingresadas=None):
        """
        * TypeError: Si funcs_ingresadas no es un dict[str, Func]
        """

        if funcs_ingresadas is None:
            self.funcs_ingresadas: dict[str, Func] = self._load_funcs()  # type: ignore

        elif (
            isinstance(funcs_ingresadas, dict)
            and
            all(
                isinstance(k, str) and isinstance(v, Func)
                for k, v in funcs_ingresadas.items()
            )
        ):
            self.funcs_ingresadas = funcs_ingresadas

        else:
            raise TypeError("Argumento inválido para 'funcs_ingresadas'!")

    def save_funciones(self) -> None:
        """
        Escribe el diccionario de funciones ingresados al archivo funciones.json,
        utilizando FractionEncoder() para escribir objetos Fraction().
        """

        # descomponer los objetos Func() en self.funcs_ingresadas
        # para que se guarden los atributos individuales del objeto,
        # en lugar de una referencia al objeto Func() completo
        funciones_dict = {
            nombre: {
                "nombre": func.nombre,
                "expr": str(func.func_expr),
                "latexified": func.latexified,
            } for nombre, func in self.funcs_ingresadas.items()
        }

        # crear funciones.json si no existe
        if not path.exists(FUNCIONES_PATH):
            makedirs(path.dirname(FUNCIONES_PATH), exist_ok=True)
            LOGGER.info("Creando archivo 'funciones.json'...")

        # si funcs_ingresadas esta vacio, dejar funciones.json vacio y retornar
        if funciones_dict == {}:
            with open(FUNCIONES_PATH, "w", encoding="utf-8") as _:
                LOGGER.info(
                    "No hay funciones para guardar, " +
                    "dejando 'funciones.json' vacío..."
                )
            return

        with open(FUNCIONES_PATH, mode="w", encoding="utf-8") as funciones_file:
            dump(
                funciones_dict,
                funciones_file,
                indent=4,
                sort_keys=True,
            )

            LOGGER.info(
                "Funciones guardadas en 'funciones.json'!"
            )

    def _load_funcs(self) -> dict[str, Func]:
        """
        Carga las funciones almacenadas en 'funciones.json'.
        """

        # si no existe funciones.json, retornar un diccionario vacio
        if not path.exists(FUNCIONES_PATH):
            LOGGER.info("Archivo 'funciones.json' no existe...")
            return {}

        with open(FUNCIONES_PATH, mode="r", encoding="utf-8") as funciones_file:
            try:
                funciones_dict: dict = load(funciones_file)
                LOGGER.info("Funciones cargadas!")
                return {
                    nombre: Func(
                        nombre=func["nombre"],
                        expr=func["expr"],
                        latexified=func["latexified"],
                    ) for nombre, func in funciones_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info("Archivo 'funciones.json' vacío...")
                else:
                    # si no, es un error de verdad
                    LOGGER.error(
                        "Error al leer archivo 'funciones.json':\n%s", str(j)
                    )
                return {}
