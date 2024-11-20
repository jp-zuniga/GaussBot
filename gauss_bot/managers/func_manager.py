"""
Implementación de FuncManager.
Almacena y valida las funciones ingresadas por el usuario.
Se encarga de aplicar diferentes métodos para encontrar
raíces de las funciones ingresadas, y retorna los resultados.
"""

from fractions import Fraction
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
    diff,
    lambdify,
)

from gauss_bot.models import Func
from gauss_bot import (
    FUNCIONES_PATH,
    LOGGER,
)

MARGEN_ERROR = Fraction(1, 1000000)
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
        intervalo: tuple[Fraction, Fraction],
        error: Fraction = MARGEN_ERROR
    ) -> Union[bool, tuple[Fraction, Fraction, int]]:

        """
        Implementación del método de bisección,
        un método cerrado para encontrar raíces de funciones.
        """

        a, b = intervalo
        f = lambdify(func.variable, func.func_expr)

        f_a = Fraction(f(float(a)))
        f_b = Fraction(f(float(b)))
        if f_a * f_b > 0:
            return True

        i = 0
        while True:
            i += 1
            c = (a + b) / 2
            f_c = Fraction(f(float(c)))
            if f_c == 0 or abs(f_c) < error:
                return (c, f_c, i)
            if f_a * f_c < 0:
                b = c
            elif f_b * f_c < 0:
                a = c
            if i == MAX_ITERACIONES:
                return (c, f_c, -1)

    def falsa_posicion(
        self,
        func: Func,
        intervalo: tuple[Fraction, Fraction],
        error: Fraction = MARGEN_ERROR
    ) -> Union[bool, tuple[Fraction, Fraction, int]]:

        """
        Implementación del método de bisección,
        un método cerrado para encontrar raíces de funciones.
        """

        a, b = intervalo
        f = lambdify(func.variable, func.func_expr)


        f_a = Fraction(f(float(a)))
        f_b = Fraction(f(float(b)))
        if f_a * f_b > 0:
            return True

        i = 0
        while True:
            i += 1
            c = (f(float(a)) * (a - b)) / f(float(a)) - f(float(b))
            f_c = Fraction(f(float(c)))
            if f_c == 0 or abs(f_c) < error:
                return (c, f_c, i)
            if f_a * f_c < 0:
                b = c
            elif f_b * f_c < 0:
                a = c
            if i == MAX_ITERACIONES:
                return (c, f_c, -1)

    def newton(
        self,
        func: Func,
        xi: Fraction,
        error: Fraction = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES
    ) -> Union[tuple[Fraction, Fraction, int, bool]]:

        """
        Implementación del método de Newton,
        un método abierto para encontrar raíces de funciones.
        """


        f = lambdify(func.variable, func.func_expr)
        f_prima = lambdify(func.variable, diff(func.func_expr, func.variable))

        fxi = f(float(xi))
        if abs(fxi) < error:
            return (xi, fxi, 1, False)

        for i in range(2, max_its + 1):
            fxi = f(float(xi))
            fxi_prima = f_prima(float(xi))

            if abs(fxi) < error:
                return (xi, fxi, i, True)

            xi -= fxi / fxi_prima
            fxi = f(float(xi))
            if abs(fxi) < error:
                return (xi, fxi, i, False)
        return (xi, fxi, max_its, False)

    def secante(
        self,
        func: Func,
        iniciales: tuple[Fraction, Fraction],
        error: Fraction = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES
    ) -> Union[tuple[Fraction, Fraction, int, bool]]:

        """
        Implementación del método de la secante,
        un método abierto para encontrar raíces de funciones.
        """

        xi, xu = iniciales
        f = lambdify(func.variable, func.func_expr)
        fxu = f(float(xu))

        if abs(fxu) < error:
            return (xu, fxu, 1, False)

        for i in range(2, max_its + 1):
            fxu = f(float(xu))
            if abs(fxu) < error:
                return (xu, fxu, i, True)

            temp = xu
            xu -= (fxu * (xi - xu)) / (f(float(xi)) - fxu)
            fxu = f(float(xu))
            if abs(fxu) < error:
                return (xu, fxu, i, False)
            xi = temp
        return (xu, fxu, max_its, False)

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

    def _validar_funcs_ingresadas(self) -> bool:
        """
        Valida si el diccionario de funciones ingresadas esta vacío o no.
        """

        if self.funcs_ingresadas == {}:
            return False
        return True
