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
    JSONDecodeError,
    dump,
    load,
)
from os import (
    makedirs,
    path,
)
from typing import Any, Optional, Union

from customtkinter import CTkImage as ctkImage
from sympy import (
    I,
    diff,
    lambdify,
    zoo,
)
from sympy.sets import Contains

from ..models import Func
from ..utils import FUNCIONES_PATH, LOGGER

getcontext().prec = 8  # precision de los decimales

MARGEN_ERROR = Decimal(1e-4)
MAX_ITERACIONES = 100


class FuncManager:
    """
    Se encarga de almacenar, validar y realizar
    operaciones con las funciones ingresadas por el usuario,
    para su uso en los módulos de análisis numérico.
    """

    def __init__(self, funcs_ingresadas: Optional[dict[str, Func]] = None):
        """
        * TypeError: Si funcs_ingresadas no es un dict[str, Func]
        """

        if funcs_ingresadas is None:
            self.funcs_ingresadas: dict[str, Func] = self._load_funcs()

        elif isinstance(funcs_ingresadas, dict) and all(
            isinstance(k, str) and isinstance(v, Func)
            for k, v in funcs_ingresadas.items()
        ):
            self.funcs_ingresadas = funcs_ingresadas

        else:
            raise TypeError("Argumento inválido para 'funcs_ingresadas'!")

    def get_funcs(self) -> list[ctkImage]:
        """
        Obtiene las funciones guardadas en
        self.funcs_ingresadas y retorna sus imagenes.
        """

        if not self._validar_funcs_ingresadas():
            return []

        funcs: list[ctkImage] = []
        for func in self.funcs_ingresadas.values():
            funcs.append(func.get_png())
        return funcs

    @staticmethod
    def biseccion(
        func: Func, intervalo: tuple[Decimal, Decimal], error: Decimal = MARGEN_ERROR
    ) -> Union[bool, tuple[Decimal, Decimal, list, int]]:
        """
        Implementación del método de bisección,
        un método cerrado para encontrar raíces de funciones.
        """

        if not func.es_continua(intervalo):
            return False

        registro: list[str] = [
            [
                "Iteración",
                "a",
                "b",
                "c",
                "E",
                f"{func.nombre[0]}(a)",
                f"{func.nombre[0]}(b)",
                f"{func.nombre[0]}(c)",
            ]
        ]

        a, b = float(intervalo[0]), float(intervalo[1])
        f = lambdify(func.var, func.expr)

        fa: float = f(a)
        fb: float = f(b)
        if fa * fb > 0:
            return True

        i = 0
        while i < MAX_ITERACIONES:
            i += 1

            c = (a + b) / 2
            fc: float = f(c)
            fa = f(a)
            fb = f(b)
            registro.append(
                [
                    str(i),
                    format(Decimal(a).normalize(), "f"),
                    format(Decimal(b).normalize(), "f"),
                    format(Decimal(c).normalize(), "f"),
                    format(Decimal(fc).normalize(), "f"),
                    format(Decimal(fa).normalize(), "f"),
                    format(Decimal(fb).normalize(), "f"),
                    format(Decimal(fc).normalize(), "f"),
                ]
            )

            if abs(fc) < error:
                return (Decimal(c), Decimal(fc), registro, i)
            if fa * fc < 0:
                b = c
            elif fb * fc < 0:
                a = c
        return (Decimal(c), Decimal(fc), registro, -1)

    @staticmethod
    def falsa_posicion(
        func: Func, intervalo: tuple[Decimal, Decimal], error: Decimal = MARGEN_ERROR
    ) -> Union[bool, tuple[Decimal, Decimal, list, int]]:
        """
        Implementación del método de bisección,
        un método cerrado para encontrar raíces de funciones.
        """

        if not func.es_continua(intervalo):
            return False

        registro: list[str] = [
            [
                "Iteración",
                "a",
                "b",
                "x_r",
                "E",
                f"{func.nombre[0]}(a)",
                f"{func.nombre[0]}(b)",
                f"{func.nombre[0]}(x_r)",
            ]
        ]

        a, b = float(intervalo[0]), float(intervalo[1])
        f = lambdify(func.var, func.expr)

        fa: float = f(a)
        fb: float = f(b)
        if fa * fb > 0:
            return True

        i = 0
        while i < MAX_ITERACIONES:
            i += 1
            fa = f(a)
            fb = f(b)

            xr = b - (fb * (a - b)) / (fa - fb)
            fxr: float = f(xr)
            registro.append(
                [
                    str(i),
                    format(Decimal(a).normalize(), "f"),
                    format(Decimal(b).normalize(), "f"),
                    format(Decimal(xr).normalize(), "f"),
                    format(Decimal(fxr).normalize(), "f"),
                    format(Decimal(fa).normalize(), "f"),
                    format(Decimal(fb).normalize(), "f"),
                    format(Decimal(fxr).normalize(), "f"),
                ]
            )

            if abs(fxr) < error:
                return (Decimal(xr), Decimal(fxr), registro, i)
            if fa * fxr < 0:
                b = xr
            elif fb * fxr < 0:
                a = xr
        return (Decimal(xr), Decimal(fxr), registro, -1)

    @staticmethod
    def newton(
        func: Func,
        inicial: Decimal,
        error: Decimal = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES,
    ) -> tuple[Decimal, Decimal, list, int, Any]:
        """
        Implementación del método de Newton,
        un método abierto para encontrar raíces de funciones.
        """

        derivada = Func(
            f"{func.nombre[0]}′({func.var})",
            str(diff(func.expr, func.var)),
        )

        registro: list[str] = [
            [
                "Iteración",
                "x_i",
                "x_i + 1",
                "E",
                f"{func.nombre[0]}(x_i)",
                f"{func.nombre[0]}′(x_i)",
            ]
        ]

        dominio_derivada = derivada.get_dominio()
        dominio_func = func.get_dominio()
        f = lambdify(func.var, func.expr)
        f_prima = lambdify(func.var, derivada.expr)

        xi = float(inicial)
        try:
            if xi not in dominio_derivada:
                return (Decimal(xi), Decimal(float(f(xi))), registro, 0, 1)
        except TypeError:
            if not Contains(xi, dominio_derivada):
                return (Decimal(xi), Decimal(float(f(xi))), registro, 0, 1)

        i = 0
        while i < max_its:
            i += 1
            fxi: float = f(xi)
            fxi_prima: float = f_prima(xi)

            temp_xi = xi
            try:
                if temp_xi not in dominio_func:
                    return (Decimal(temp_xi), Decimal(fxi), registro, i, -1)
                if temp_xi not in dominio_derivada:
                    return (Decimal(temp_xi), Decimal(fxi), registro, i, 1)
            except TypeError:
                if not Contains(temp_xi, dominio_func):
                    return (Decimal(temp_xi), Decimal(fxi), registro, i, 1)
                if not Contains(temp_xi, dominio_derivada):
                    return (Decimal(temp_xi), Decimal(fxi), registro, i, 1)

            xi -= fxi / fxi_prima
            registro.append(
                [
                    str(i),
                    format(Decimal(temp_xi).normalize(), "f"),
                    format(Decimal(xi).normalize(), "f"),
                    format(Decimal(fxi).normalize(), "f"),
                    format(Decimal(fxi).normalize(), "f"),
                    format(Decimal(fxi_prima).normalize(), "f"),
                ]
            )

            if abs(fxi) < error:
                return (Decimal(xi), Decimal(fxi), registro, i, I)
            if fxi_prima == 0:
                return (Decimal(xi), Decimal(fxi), registro, i, -I)

        return (Decimal(xi), Decimal(fxi), registro, max_its, zoo)

    @staticmethod
    def secante(
        func: Func,
        iniciales: tuple[Decimal, Decimal],
        error: Decimal = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES,
    ) -> tuple[Decimal, Decimal, list[str], int, Any]:
        """
        Implementación del método de la secante,
        un método abierto para encontrar raíces de funciones.
        """

        registro: list[str] = [
            [
                "Iteración",
                "x_i − 1",
                "x_i",
                "x_i + 1",
            ]
        ]

        xi, xn = float(iniciales[0]), float(iniciales[1])
        f = lambdify(func.var, func.expr)
        f_dominio = func.get_dominio()

        i = 0
        while i < max_its:
            i += 1
            fxi, fxn = f(xi), f(xn)
            new_xn = xn - (fxn * (xi - xn)) / (fxi - fxn)

            registro.append(
                [
                    str(i),
                    format(Decimal(xi).normalize(), "f"),
                    format(Decimal(xn).normalize(), "f"),
                    format(Decimal(new_xn).normalize(), "f"),
                ]
            )

            if abs(fxn) < error:
                return (Decimal(xn), Decimal(fxn), registro, i, I)

            xi, xn = xn, new_xn
            if xn not in f_dominio:
                return (Decimal(xn), Decimal(fxn), registro, i, -1)
        return (Decimal(xn), Decimal(fxn), registro, max_its, zoo)

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
                "expr": str(func.expr),
                "latexified": func.latexified,
            }
            for nombre, func in self.funcs_ingresadas.items()
        }

        # crear funciones.json si no existe
        if not path.exists(FUNCIONES_PATH):
            makedirs(path.dirname(FUNCIONES_PATH), exist_ok=True)
            LOGGER.info("Creando archivo 'funciones.json'...")

        # si funcs_ingresadas esta vacio, dejar funciones.json vacio y retornar
        if funciones_dict == {}:
            with open(FUNCIONES_PATH, "w", encoding="utf-8") as _:
                LOGGER.info(
                    "No hay funciones para guardar, "
                    + "dejando 'funciones.json' vacío..."
                )
            return

        with open(FUNCIONES_PATH, mode="w", encoding="utf-8") as funciones_file:
            dump(
                funciones_dict,
                funciones_file,
                indent=4,
                sort_keys=True,
            )

        LOGGER.info("Funciones guardadas en 'funciones.json'!")

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
                    )
                    for nombre, func in funciones_dict.items()
                }
            except JSONDecodeError as j:
                if "(char 0)" in str(j):
                    # si la lectura del archivo fallo en
                    # el primer caracter, es que esta vacio
                    LOGGER.info("Archivo 'funciones.json' vacío...")
                else:
                    # si no, es un error de verdad
                    LOGGER.error("Error al leer archivo 'funciones.json':\n%s", str(j))
                return {}

    def _validar_funcs_ingresadas(self) -> bool:
        """
        Valida si el diccionario de funciones ingresadas esta vacío o no.
        """

        if self.funcs_ingresadas == {}:
            return False
        return True
