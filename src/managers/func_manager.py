"""
Implementación de FuncManager.
Almacena y valida las funciones ingresadas por el usuario.
Se encarga de aplicar diferentes métodos para encontrar
raíces de las funciones ingresadas, y retorna los resultados.
"""

from decimal import Decimal
from json import JSONDecodeError, dump, load

from customtkinter import CTkImage as ctkImage
from sympy import lambdify
from sympy.sets import Contains

from ..models import Func
from ..utils import FUNCIONES_PATH, LOGGER

MARGEN_ERROR = Decimal(1e-4)
MAX_ITERACIONES: int = 100


class FuncManager:
    """
    Manager de las funciones de la aplicación.
    Valida y almacena las funciones ingresadas por el usuario,
    y realiza operaciones sobre ellas.
    """

    def __init__(self, funcs_ingresadas: dict[str, Func] | None = None):
        """
        Args:
            funcs_ingresadas: Diccionario de funciones guardadas.

        Raises:
            TypeError: Si funcs_ingresadas no es un dict[str, Func].
        ---
        """

        if funcs_ingresadas is None:
            self.funcs_ingresadas: dict[str, Func] = self._load_funcs()
        elif isinstance(funcs_ingresadas, dict) and all(
            isinstance(k, str) and isinstance(v, Func)
            for k, v in funcs_ingresadas.items()
        ):
            self.funcs_ingresadas = funcs_ingresadas
        else:
            raise TypeError("¡Argumento inválido para 'funcs_ingresadas'!")

    def get_funcs(self) -> list[ctkImage]:
        """
        Obtener las imagenes de las funciones en 'self.funcs_ingresadas'.

        Returns:
            list[CTkImage]: Las imagenes de todas las funciones guardadas.
        ---
        """

        if not self._validar_funcs_ingresadas():
            return []

        funcs: list[ctkImage] = []
        for func in self.funcs_ingresadas.values():
            funcs.append(func.get_png())
        return funcs

    @staticmethod
    def biseccion(
        func: Func,
        intervalo: tuple[Decimal, Decimal],
        error: Decimal = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES,
    ) -> bool | tuple[Decimal, Decimal, list[list[str]], int]:
        """
        Implementación del método de bisección,
        un método cerrado para encontrar raíces de funciones.

        Args:
            func:      Función que se trabajará.
            intervalo: Dominio sobre cual se buscará la raíz.
            error:     Margen de error aceptable para terminar búsqueda.
            max_its:   Número máximo de iteraciones aceptable para terminar búsqueda.

        Returns:
            bool:
                Si el método de bisección no es aplicable a la función:
                True si la función no cambia de signo,
                False si no es continua en el intervalo.
            (Decimal, Decimal, list[list[str]], int):
                Valor x de raíz,
                valor y de raíz,
                registro de iteraciones e
                iteración final.
        ---
        """

        if not func.es_continua(intervalo):
            return False

        registro: list[list[str]] = [
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

        fa = float(f(a))
        fb = float(f(b))
        if fa * fb > 0:
            return True

        i: int = 0
        while i < MAX_ITERACIONES:
            i += 1

            c = float((a + b) / 2)
            fc = float(f(c))
            fa = float(f(a))
            fb = float(f(b))
            registro.append(
                [
                    str(i),
                    FuncManager._format_decimal(a),
                    FuncManager._format_decimal(b),
                    FuncManager._format_decimal(c),
                    FuncManager._format_decimal(fc),
                    FuncManager._format_decimal(fa),
                    FuncManager._format_decimal(fb),
                    FuncManager._format_decimal(fc),
                ]
            )

            if abs(fc) < error:
                return (Decimal(c), Decimal(fc), registro, i)
            if fa * fc < 0:
                b: float = c
            elif fb * fc < 0:
                a: float = c
        return (Decimal(c), Decimal(fc), registro, -1)

    @staticmethod
    def falsa_posicion(
        func: Func,
        intervalo: tuple[Decimal, Decimal],
        error: Decimal = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES,
    ) -> bool | tuple[Decimal, Decimal, list[list[str]], int]:
        """
        Implementación del método de bisección,
        un método cerrado para encontrar raíces de funciones.

        Args:
            func:      Función que se trabajará.
            intervalo: Dominio sobre cual se buscará la raíz.
            error:     Margen de error aceptable para terminar búsqueda.
            max_its:   Número máximo de iteraciones aceptable para terminar búsqueda.

        Returns:
            bool:
                Si el método de bisección no es aplicable a la función:
                True si la función no cambia de signo,
                False si no es continua en el intervalo.
            (Decimal, Decimal, list[list[str]], int):
                Valor x de raíz,
                valor y de raíz,
                registro de iteraciones e
                iteración final.
        ---
        """

        if not func.es_continua(intervalo):
            return False

        registro: list[list[str]] = [
            [
                "Iteración",
                "a",
                "b",
                "xᵣ",
                "E",
                f"{func.nombre[0]}(a)",
                f"{func.nombre[0]}(b)",
                f"{func.nombre[0]}(xᵣ)",
            ]
        ]

        a, b = float(intervalo[0]), float(intervalo[1])
        f = lambdify(func.var, func.expr)

        fa = float(f(a))
        fb = float(f(b))
        if fa * fb > 0:
            return True

        i: int = 0
        while i < MAX_ITERACIONES:
            i += 1
            fa = float(f(a))
            fb = float(f(b))

            xr = float(b - (fb * (a - b)) / (fa - fb))
            fxr = float(f(xr))
            registro.append(
                [
                    str(i),
                    FuncManager._format_decimal(a),
                    FuncManager._format_decimal(b),
                    FuncManager._format_decimal(xr),
                    FuncManager._format_decimal(fxr),
                    FuncManager._format_decimal(fa),
                    FuncManager._format_decimal(fb),
                    FuncManager._format_decimal(fxr),
                ]
            )

            if abs(fxr) < error:
                return (Decimal(xr), Decimal(fxr), registro, i)
            if fa * fxr < 0:
                b: float = xr
            elif fb * fxr < 0:
                a: float = xr
        return (Decimal(xr), Decimal(fxr), registro, -1)

    @staticmethod
    def newton(
        func: Func,
        inicial: Decimal,
        error: Decimal = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES,
    ) -> tuple[Decimal, Decimal, list[list[str]], int, int]:
        """
        Implementación del método de Newton,
        un método abierto para encontrar raíces de funciones.

        Args:
            func:    Función que se trabajará.
            inicial: Valor inicial de búsqueda.
            error:   Margen de error aceptable para terminar búsqueda.
            max_its: Número máximo de iteraciones aceptable para terminar búsqueda.

        Returns:
            bool:
                Si el método de bisección no es aplicable a la función:
                True si la función no cambia de signo,
                False si no es continua en el intervalo.
            (Decimal, Decimal, list[list[str]], int, int):
                Valor x de raíz,
                valor y de raíz,
                registro de iteraciones,
                iteración final y
                bandera de resultado (
                    -1: no se encontró raíz;
                     0: se encontró raíz dentro del margen de error;
                     1: se llegó a un valor fuera del dominio de la derivada;
                     2: se llegó a un valor fuera del dominio de la función.
                )
        ---
        """

        registro: list[list[str]] = [
            [
                "Iteración",
                "xᵢ",
                "xᵢ + 1",
                "E",
                f"{func.nombre[0]}(xᵢ)",
                f"{func.nombre[0]}'(xᵢ)",
            ]
        ]

        derivada = func.derivar()
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

        i: int = 0
        while i < max_its:
            i += 1
            fxi = float(f(xi))
            fxi_prima = float(f_prima(xi))

            temp_xi = xi
            try:
                if temp_xi not in dominio_func:
                    return (Decimal(temp_xi), Decimal(fxi), registro, i, 2)
                if temp_xi not in dominio_derivada:
                    return (Decimal(temp_xi), Decimal(fxi), registro, i, 1)
            except TypeError:
                if not Contains(temp_xi, dominio_func):
                    return (Decimal(temp_xi), Decimal(fxi), registro, i, 2)
                if not Contains(temp_xi, dominio_derivada):
                    return (Decimal(temp_xi), Decimal(fxi), registro, i, 1)

            xi -= fxi / fxi_prima
            registro.append(
                [
                    str(i),
                    FuncManager._format_decimal(temp_xi),
                    FuncManager._format_decimal(xi),
                    FuncManager._format_decimal(fxi),
                    FuncManager._format_decimal(fxi),
                    FuncManager._format_decimal(fxi_prima),
                ]
            )

            if abs(fxi) < error or fxi_prima == 0:
                return (Decimal(xi), Decimal(fxi), registro, i, 0)

        return (Decimal(xi), Decimal(fxi), registro, max_its, -1)

    @staticmethod
    def secante(
        func: Func,
        iniciales: tuple[Decimal, Decimal],
        error: Decimal = MARGEN_ERROR,
        max_its: int = MAX_ITERACIONES,
    ) -> tuple[Decimal, Decimal, list[list[str]], int, int]:
        """
        Implementación del método de la secante,
        un método abierto para encontrar raíces de funciones.

        Args:
            func:      Función que se trabajará.
            iniciales: Par de valores iniciales de búsqueda.
            error:     Margen de error aceptable para terminar búsqueda.
            max_its:   Número máximo de iteraciones aceptable para terminar búsqueda.

        Returns:
            bool:
                Si el método de bisección no es aplicable a la función:
                True si la función no cambia de signo,
                False si no es continua en el intervalo.
            (Decimal, Decimal, list[list[str]], int, int):
                Valor x de raíz,
                valor y de raíz,
                registro de iteraciones,
                iteración final y
                bandera de resultado (
                    -1: no se encontró raíz;
                     0: se encontró raíz dentro del margen de error;
                     1: se llegó a un valor fuera del dominio de la derivada;
                     2: se llegó a un valor fuera del dominio de la función.
                )
        ---
        """

        registro: list[list[str]] = [["Iteración", "xᵢ − 1", "xᵢ", "xᵢ + 1"]]

        xi, xn = float(iniciales[0]), float(iniciales[1])
        f = lambdify(func.var, func.expr)
        f_dominio = func.get_dominio()

        i: int = 0
        while i < max_its:
            i += 1
            fxi, fxn = float(f(xi)), float(f(xn))
            new_xn = float(xn - (fxn * (xi - xn)) / (fxi - fxn))

            registro.append(
                [
                    str(i),
                    FuncManager._format_decimal(xi),
                    FuncManager._format_decimal(xn),
                    FuncManager._format_decimal(new_xn),
                ]
            )

            if abs(fxn) < error:
                return (Decimal(xn), Decimal(fxn), registro, i, 0)

            xi, xn = xn, new_xn
            if xn not in f_dominio:
                return (Decimal(xn), Decimal(fxn), registro, i, 2)
        return (Decimal(xn), Decimal(fxn), registro, max_its, -1)

    @staticmethod
    def _format_decimal(num: int | float) -> str:
        """
        Formatear número para uso en registro de iteraciones.
        """

        return format(Decimal(num).normalize(), "f").replace("-", "−")

    def save_funciones(self) -> None:
        """
        Guardar las funciones ingresadas en el archivo de datos de funciones.
        """

        # descomponer los objetos Func() en self.funcs_ingresadas
        # para que se guarden los atributos individuales del objeto,
        # en lugar de una referencia al objeto Func() completo
        funciones_dict: dict[str, dict[str, str | bool]] = {
            nombre: {
                "nombre": func.nombre,
                "expr": str(func.expr),
                "latexified": func.latexified,
            }
            for nombre, func in self.funcs_ingresadas.items()
        }

        # crear funciones.json si no existe
        if not FUNCIONES_PATH.exists():
            FUNCIONES_PATH.parent.mkdir(parents=True, exist_ok=True)
            LOGGER.info("Creando archivo '%s'...", FUNCIONES_PATH)

        # si funcs_ingresadas esta vacio, dejar funciones.json vacio y retornar
        if funciones_dict == {}:
            FUNCIONES_PATH.write_text("")
            LOGGER.info("No hay funciones para guardar, dejando archivo vacío...")
            return

        with open(FUNCIONES_PATH, mode="w", encoding="utf-8") as funciones_file:
            dump(funciones_dict, funciones_file, indent=4, sort_keys=True)

        LOGGER.info("¡Funciones guardadas en '%s' exitosamente!", FUNCIONES_PATH)

    def _load_funcs(self) -> dict[str, Func]:
        """
        Cargar las funciones almacenadas en el archivo de datos de funciones.
        """

        # si no existe funciones.json, retornar un diccionario vacio
        if not FUNCIONES_PATH.exists():
            LOGGER.info("Archivo '%s' no existe...", FUNCIONES_PATH)
            return {}

        with open(FUNCIONES_PATH, mode="r", encoding="utf-8") as funciones_file:
            try:
                funciones_dict: dict = load(funciones_file)
                LOGGER.info("¡Funciones cargadas exitosamente!")
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
                    LOGGER.info("Archivo '%s' vacío...", FUNCIONES_PATH)
                else:
                    # si no, es un error de verdad
                    LOGGER.error(
                        "Error al leer archivo '%s':\n%s", FUNCIONES_PATH, str(j)
                    )
                return {}

    def _validar_funcs_ingresadas(self) -> bool:
        """
        Validar el diccionario de funciones.

        Returns:
            bool: Si el diccionario está vacío o no.
        ---
        """

        return self.funcs_ingresadas != {}
