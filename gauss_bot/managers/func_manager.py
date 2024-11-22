"""
Implementación de FuncManager.
Almacena y valida las funciones ingresadas por el usuario.
Se encarga de aplicar diferentes métodos para encontrar
raíces de las funciones ingresadas, y retorna los resultados.
"""

from decimal import (
    Decimal,
    getcontext,
)

from json import (
    dump,
    load,
    JSONDecodeError,
)

from os import (
    makedirs,
    path,
)

from typing import Union

from customtkinter import CTkImage as ctkImage
from sympy import (
    I,
    zoo,
    diff,
    lambdify,
)

from .. import FUNCIONES_PATH
from ..util_funcs import LOGGER
from ..models import Func

getcontext().prec = 20

MARGEN_ERROR = Decimal(1e-6)
MAX_ITERACIONES = 500


class FuncManager:
    """
    Se encarga de almacenar, validar y realizar
    operaciones con las funciones ingresadas por el usuario,
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

    def get_funcs(self) -> list[ctkImage]:
        """
        Obtiene las funciones guardadas en self.funcs_ingresadas
        y las retorna como string.
        """

        if not self._validar_funcs_ingresadas():
            return []

        funcs: list[ctkImage] = []
        for func in self.funcs_ingresadas.values():
            funcs.append(func.get_png())
        return funcs

    def biseccion(
        self,
        func: Func,
        intervalo: tuple[Decimal, Decimal],
        error: Decimal = MARGEN_ERROR
    ) -> Union[bool, tuple[Decimal, Decimal, int]]:

        """
        Implementación del método de bisección,
        un método cerrado para encontrar raíces de funciones.
        """

        if not func.es_continua(intervalo):
            return False

        a, b = a, b = float(intervalo[0]), float(intervalo[1])
        f = lambdify(func.variable, func.func_expr)

        f_a = f(a)
        f_b = f(b)
        if f_a * f_b > 0:
            return True

        i = 0
        while i <= MAX_ITERACIONES:
            i += 1
            c = (a + b) / 2
            f_c = f(c)
            if abs(f_c) < error:
                return (Decimal(c), Decimal(f_c), i)
            if f_a * f_c < 0:
                b = c
            elif f_b * f_c < 0:
                a = c
        return (Decimal(c), Decimal(f_c), -1)

    def falsa_posicion(
        self,
        func: Func,
        intervalo: tuple[Decimal, Decimal],
        error: Decimal = MARGEN_ERROR
    ) -> Union[bool, tuple[Decimal, Decimal, int]]:

        """
        Implementación del método de bisección,
        un método cerrado para encontrar raíces de funciones.
        """

        if not func.es_continua(intervalo):
            return False

        a, b = float(intervalo[0]), float(intervalo[1])
        f = lambdify(func.variable, func.func_expr)

        f_a = f(a)
        f_b = f(b)
        if f_a * f_b > 0:
            return True

        i = 0
        while i <= MAX_ITERACIONES:
            i += 1
            fa = f(a)
            fb = f(b)

            c = (fa * (a - b)) / fa - fb
            f_c = f(c)
            if abs(f_c) < error:
                return (Decimal(c), Decimal(f_c), i)

            if f_a * f_c < 0:
                b = c
            elif f_b * f_c < 0:
                a = c
        return (Decimal(c), Decimal(f_c), -1)

    def newton(
        self,
        func: Func,
        inicial: Decimal,
        error: Decimal = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES
    ) -> tuple[Decimal, Decimal, int, int]:

        """
        Implementación del método de Newton,
        un método abierto para encontrar raíces de funciones.
        """

        derivada = Func(f"{func.nombre[0]}'(x)", str(diff(func.func_expr, func.variable)))
        dominio_derivada = derivada.get_dominio()
        dominio_func = func.get_dominio()

        xi = float(inicial)
        if xi not in dominio_derivada:
            return (Decimal(xi), zoo, 0, 1)

        f = lambdify(func.variable, func.func_expr)
        f_prima = lambdify(func.variable, derivada.func_expr)

        fxi = f(xi)
        if abs(fxi) < error:
            return (Decimal(xi), Decimal(fxi), 1, I)

        i = 1
        while i <= max_its:
            i += 1
            fxi = f(xi)
            fxi_prima = f_prima(xi)

            if abs(fxi) < error:
                return (Decimal(xi), Decimal(fxi), i, I)
            if fxi_prima == 0:
                return (Decimal(xi), Decimal(fxi), i, -I)

            xi -= fxi / fxi_prima
            if xi not in dominio_func:
                return (Decimal(xi), Decimal(fxi), i, -1)
            if xi not in dominio_derivada:
                return (Decimal(xi), Decimal(fxi), i, 1)
        return (Decimal(xi), Decimal(fxi), max_its, zoo)

    def secante(
        self,
        func: Func,
        iniciales: tuple[Decimal, Decimal],
        error: Decimal = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES
    ) -> tuple[Decimal, Decimal, int, int]:

        """
        Implementación del método de la secante,
        un método abierto para encontrar raíces de funciones.
        """

        xi, xu = float(iniciales[0]), float(iniciales[1])
        f = lambdify(func.variable, func.func_expr)
        f_dominio = func.get_dominio()

        fxu = f(xu)
        if abs(fxu) < error:
            return (Decimal(xu), Decimal(fxu), 1, I)

        i = 1
        while i <= max_its:
            i += 1
            fxi = f(xi)
            fxu = f(xu)
            if abs(fxu) < error:
                return (Decimal(xu), Decimal(fxu), i, I)

            xi, xu = xu, xi
            xu = (fxu * (xi - xu)) / (fxi - fxu)
            if xu not in f_dominio:
                return (Decimal(xu), Decimal(fxu), i, -1)
        return (Decimal(xu), Decimal(fxu), max_its, zoo)

    def save_funciones(self) -> None:
        """
        Escribe el diccionario de funciones ingresados al archivo funciones.json,
        utilizando FractionEncoder() para escribir objetos ).
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

    def _validar_funcs_ingresadas(self) -> bool:
        """
        Valida si el diccionario de funciones ingresadas esta vacío o no.
        """

        if self.funcs_ingresadas == {}:
            return False
        return True
