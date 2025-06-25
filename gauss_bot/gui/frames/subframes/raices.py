"""
Implementación de RaicesFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

from decimal import Decimal
from fractions import Fraction
from random import randint
from tkinter import Variable
from typing import TYPE_CHECKING, Optional, Union

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkToplevel as ctkTop,
)
from sympy import Contains, I, Interval, zoo

from ...custom import CustomDropdown, CustomEntry, IconButton
from ...custom.adapted import CustomScrollFrame, CustomTable
from ....managers import MARGEN_ERROR, MAX_ITERACIONES, FuncManager
from ....models import Func
from ....utils import INFO_ICON, generate_sep, place_msg_frame, set_icon

if TYPE_CHECKING:
    from .. import AnalisisFrame
    from ... import GaussUI


class RaicesFrame(CustomScrollFrame):
    """
    Frame que permite encontrar las raíces de una función.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "AnalisisFrame",
        func_manager: FuncManager,
        **kwargs,
    ) -> None:
        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager

        self.metodo_frame = ctkFrame(self, fg_color="transparent")
        self.datos_frame = ctkFrame(self, fg_color="transparent")
        self.resultado = ctkFrame(self, fg_color="transparent")

        self.columnconfigure(0, weight=1)
        self.metodo_frame.columnconfigure(0, weight=1)
        self.datos_frame.columnconfigure(0, weight=1)
        self.datos_frame.columnconfigure(3, weight=1)
        self.resultado.columnconfigure(0, weight=1)

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.metodos: dict[str, int] = {
            "Método de Bisección": 0,
            "Método de Falsa Posición": 1,
            "Método de Newton": 2,
            "Método de la Secante": 3,
        }

        self.msg_frame: Optional[ctkFrame] = None
        self.met_actual: int = -1
        self.table_hidden: bool = True

        self.func: Func

        self.a_entry: CustomEntry
        self.b_entry: CustomEntry
        self.xi_entry: CustomEntry
        self.xn_entry: CustomEntry
        self.error_entry: CustomEntry
        self.iteraciones_entry: CustomEntry
        self.tabla_its: CustomTable

        self.func_select = CustomDropdown(
            self,
            width=40,
            values=self.nombres_funcs,
            variable=Variable(
                value="Seleccione una función para encontrar sus raíces:"
            ),
            command=self.mostrar_func,
        )

        self.func_select.grid(row=0, column=0, pady=5, sticky="n")

    def mostrar_func(self, nombre_str: str) -> None:
        """
        Muestra la función seleccionada en el dropdown,
        y crea un dropdown para seleccionar el método a utilizar.
        """

        self.metodo_frame.grid(row=1, column=0, pady=5, sticky="n")
        self.func = self.func_manager.funcs_ingresadas[nombre_str]

        for widget in self.metodo_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.datos_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        ctkLabel(self.metodo_frame, text="", image=self.func.get_png()).grid(
            row=0, column=0, pady=5, sticky="n"
        )

        ctkLabel(self.metodo_frame, text="", image=generate_sep(False, (250, 5))).grid(
            row=1, column=0, sticky="n"
        )

        CustomDropdown(
            self.metodo_frame,
            variable=Variable(value="Seleccione un método para encontrar las raíces:"),
            values=list(self.metodos.keys()),
            command=self.setup_datos,
        ).grid(row=2, column=0, pady=5, sticky="n")

    def setup_datos(self, metodo: str) -> None:
        """
        Muestra los campos necesarios para ingresar los datos
        requeridos por el método seleccionado.
        """

        self.datos_frame.grid(row=2, column=0, pady=5, sticky="n")
        for widget in self.datos_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        if any(term in str(self.func.expr) for term in ("sin", "cos", "tan")):
            IconButton(
                self.metodo_frame,
                app=self.app,
                image=INFO_ICON,
                tooltip_text="\nNota: las funciones trigonométricas"
                + "\ndeben recibir argumentos en radianes.\n",
            ).grid(row=3, column=0, pady=(5, 0), sticky="n")

        self.met_actual = self.metodos[metodo]
        match self.met_actual:
            case 0:
                self.setup_cerrado()
            case 1:
                self.setup_cerrado()
            case 2:
                self.setup_abierto(newton=True)
            case 3:
                self.setup_abierto(newton=False)

    def setup_cerrado(self) -> None:
        """
        Configura self.datos_frame para aceptar input
        de intervalo y margen de error para métodos cerrados.
        """

        ctkLabel(self.datos_frame, text="Intervalo:").grid(
            row=0, column=0, padx=5, pady=(5, 2), sticky="ne"
        )

        self.a_entry = CustomEntry(
            self.datos_frame, width=60, placeholder_text=str(randint(-10, -1))
        )

        self.a_entry.grid(row=0, column=1, padx=5, pady=(5, 2), sticky="ne")
        ctkLabel(self.datos_frame, text=",", font=ctkFont(size=18)).grid(
            row=0, column=2, padx=3, pady=(5, 2), sticky="nw"
        )

        self.b_entry = CustomEntry(
            self.datos_frame, width=60, placeholder_text=str(randint(1, 10))
        )

        self.b_entry.grid(row=0, column=3, padx=5, pady=(5, 2), sticky="nw")
        ctkLabel(self.datos_frame, text="Margen de error:").grid(
            row=1, column=0, padx=5, pady=(2, 5), sticky="ne"
        )

        self.error_entry = CustomEntry(self.datos_frame)
        self.error_entry.insert(0, format(MARGEN_ERROR.normalize(), "f"))
        self.error_entry.grid(
            row=1, column=1, columnspan=3, padx=5, pady=(2, 5), sticky="nw"
        )

        self.a_entry.bind("<Up>", lambda _: self.error_entry.focus_set())
        self.a_entry.bind("<Down>", lambda _: self.error_entry.focus_set())
        self.a_entry.bind("<Left>", lambda _: self.b_entry.focus_set())
        self.a_entry.bind("<Right>", lambda _: self.b_entry.focus_set())
        self.a_entry.bind("<Return>", lambda _: self.leer_datos())

        self.b_entry.bind("<Up>", lambda _: self.error_entry.focus_set())
        self.b_entry.bind("<Down>", lambda _: self.error_entry.focus_set())
        self.b_entry.bind("<Left>", lambda _: self.a_entry.focus_set())
        self.b_entry.bind("<Right>", lambda _: self.a_entry.focus_set())
        self.b_entry.bind("<Return>", lambda _: self.leer_datos())

        self.error_entry.bind("<Up>", lambda _: self.b_entry.focus_set())
        self.error_entry.bind("<Down>", lambda _: self.a_entry.focus_set())
        self.error_entry.bind("<Return>", lambda _: self.leer_datos())

        ctkButton(
            self.datos_frame, height=30, text="Encontrar raíz", command=self.leer_datos
        ).grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def setup_abierto(self, newton: bool) -> None:
        """
        Configura self.datos_frame para aceptar input
        de valor inicial, margen de error y máximo de iteraciones
        para el método de Newton.
        """

        ctkLabel(
            self.datos_frame, text="Valor inicial:" if newton else "Valores iniciales:"
        ).grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ne")

        xi_width = 140 if newton else 60
        self.xi_entry = CustomEntry(
            self.datos_frame, width=xi_width, placeholder_text=str(randint(-10, 10))
        )

        if not newton:
            self.xn_entry = CustomEntry(
                self.datos_frame, width=60, placeholder_text=str(randint(-10, 10))
            )

            self.xi_entry.grid(row=0, column=1, padx=5, pady=(5, 2), sticky="nw")
            ctkLabel(self.datos_frame, text=",", font=ctkFont(size=18)).grid(
                row=0, column=2, padx=2, pady=(5, 2), sticky="nw"
            )

            self.xn_entry.grid(row=0, column=3, padx=5, pady=(5, 2), sticky="nw")
        else:
            self.xi_entry.grid(
                row=0, column=1, columnspan=3, padx=5, pady=(5, 2), sticky="nw"
            )

        ctkLabel(self.datos_frame, text="Margen de error:").grid(
            row=2, column=0, padx=5, pady=2, sticky="ne"
        )

        self.error_entry = CustomEntry(self.datos_frame)
        self.error_entry.insert(0, format(MARGEN_ERROR.normalize(), "f"))
        self.error_entry.grid(
            row=2, column=1, columnspan=3, padx=5, pady=2, sticky="nw"
        )

        ctkLabel(self.datos_frame, text="Máximo de iteraciones:").grid(
            row=3, column=0, padx=5, pady=(2, 5), sticky="ne"
        )

        self.iteraciones_entry = CustomEntry(self.datos_frame)
        self.iteraciones_entry.insert(0, MAX_ITERACIONES)
        self.iteraciones_entry.grid(
            row=3, column=1, columnspan=3, padx=5, pady=(2, 5), sticky="nw"
        )

        self.xi_entry.bind("<Up>", lambda _: self.iteraciones_entry.focus_set())
        self.xi_entry.bind("<Down>", lambda _: self.error_entry.focus_set())
        self.xi_entry.bind("<Return>", lambda _: self.leer_datos())

        if not newton:
            self.xn_entry.bind("<Up>", lambda _: self.iteraciones_entry.focus_set())
            self.xn_entry.bind("<Down>", lambda _: self.error_entry.focus_set())
            self.xn_entry.bind("<Left>", lambda _: self.xi_entry.focus_set())
            self.xn_entry.bind("<Right>", lambda _: self.xi_entry.focus_set())
            self.xn_entry.bind("<Return>", lambda _: self.leer_datos())
            self.xi_entry.bind("<Left>", lambda _: self.xn_entry.focus_set())
            self.xi_entry.bind("<Right>", lambda _: self.xn_entry.focus_set())
            self.error_entry.bind("<Up>", lambda _: self.xn_entry.focus_set())
        else:
            self.error_entry.bind("<Up>", lambda _: self.xi_entry.focus_set())

        self.error_entry.bind("<Down>", lambda _: self.iteraciones_entry.focus_set())
        self.error_entry.bind("<Return>", lambda _: self.leer_datos())
        self.iteraciones_entry.bind("<Up>", lambda _: self.error_entry.focus_set())
        self.iteraciones_entry.bind("<Down>", lambda _: self.xi_entry.focus_set())
        self.iteraciones_entry.bind("<Return>", lambda _: self.leer_datos())

        ctkButton(
            self.datos_frame, height=30, text="Encontrar raíz", command=self.leer_datos
        ).grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def leer_datos(self) -> None:
        """
        Llama los métodos de leer los datos
        correspondientes al método seleccionado.
        """

        self.resultado.grid(row=3, column=0, pady=5, sticky="n")
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        dominio = self.func.get_dominio()
        if self.met_actual in (0, 1):  # metodos cerrados
            self.ld_cerrado(dominio)
        elif self.met_actual in (2, 3):  # metodos abiertos
            self.ld_abierto(dominio)

    def ld_cerrado(self, dominio: Interval) -> None:
        """
        Lee y valida los datos para métodos cerrados.
        en las widgets de self.datos_frame.
        """

        try:
            a = Decimal(float(self.handle_pi(self.a_entry.get())))
            b = Decimal(float(self.handle_pi(self.b_entry.get())))
            error = Decimal(float(self.handle_pi(self.error_entry.get())))

            if a > b:
                raise ArithmeticError(
                    "En un intervalo, el número menor debe ir primero!"
                )
            if a == b:
                raise ArithmeticError("Los extremos del intervalo deben ser distintos!")
            if a not in dominio or b not in dominio:
                raise ArithmeticError(
                    "Los extremos del intervalo no son parte del "
                    + f"dominio de {self.func.nombre}!"
                )

            self.calc_raiz(vals_iniciales=(a, b), error=error)
        except (ValueError, ArithmeticError, NotImplementedError) as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
            )

    def ld_abierto(self, dominio: Interval) -> None:
        """
        Lee y valida los datos para métodos abiertos.
        en las widgets de self.datos_frame.
        """

        try:
            xi = Decimal(float(self.handle_pi(self.xi_entry.get())))
            error = Decimal(float(self.handle_pi(self.error_entry.get())))
            max_its = int(self.iteraciones_entry.get())

            if max_its <= 0:
                raise ValueError(
                    "Debe ingresar un número entero positivo "
                    + "para el máximo de iteraciones!"
                )

            try:
                if xi not in dominio:
                    adj = "primer " if self.met_actual == 3 else ""
                    raise ArithmeticError(
                        f"El {adj}valor inicial no es parte del "
                        + f"dominio de {self.func.nombre}!"
                    )
            except TypeError as t:
                if not Contains(xi, dominio):
                    raise ArithmeticError(str(t)) from t

            if self.met_actual == 3:
                xn = Decimal(float(self.handle_pi(self.xn_entry.get())))
                vals = (xi, xn)

                try:
                    if xn not in dominio:
                        raise ArithmeticError(
                            "El segundo valor inicial no es parte del "
                            + f"dominio de {self.func.nombre}!"
                        )
                except TypeError as t:
                    if not Contains(xn, dominio):
                        raise ArithmeticError(str(t)) from t

                if xi == xn:
                    raise ArithmeticError("Los valores iniciales deben ser distintos!")

            else:
                vals = xi  # type: ignore

            self.calc_raiz(vals_iniciales=vals, error=error, max_its=max_its)
        except (
            ValueError,
            ZeroDivisionError,
            ArithmeticError,
            NotImplementedError,
        ) as e:
            if isinstance(e, ValueError) and "Fraction" in str(e):
                error_substr = (
                    "el valor inicial"
                    if self.met_actual == 2
                    else "lost valores iniciales"
                )

                error_msg = (
                    "Debe ingresar números racionales para "
                    + f"{error_substr} y margen de error!"
                )
            elif isinstance(e, ValueError) and "int" in str(e):
                error_msg = (
                    "Debe ingresar números enteros positivos "
                    + "para el máximo de iteraciones!"
                )
            elif isinstance(e, ZeroDivisionError):
                error_msg = "El denominador no puede ser 0!"
            else:
                error_msg = str(e)

            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado,
                msg_frame=self.msg_frame,
                msg=error_msg,
                tipo="error",
            )

    def calc_raiz(self, **kwargs) -> None:
        """
        Calcula la raíz de self.func_selecccionada
        utilizando self.met_actual.

        kwargs válidos:
        - Para métodos cerrados:
            - vals_iniciales: tuple[Decimal, Decimal]
        - Para métodos abiertos:
            - vals_iniciales: Union[Decimal, tuple[Decimal, Decimal]]
            - max_its: int (<= 0) = 100
        - error = Decimal(1e-4)
        """

        match self.met_actual:
            case 0:
                resultado = FuncManager.biseccion(
                    func=self.func,
                    intervalo=kwargs.pop("vals_iniciales"),
                    error=kwargs.pop("error"),
                )
            case 1:
                resultado = FuncManager.falsa_posicion(
                    func=self.func,
                    intervalo=kwargs.pop("vals_iniciales"),
                    error=kwargs.pop("error"),
                )
            case 2:
                resultado = FuncManager.newton(  # type: ignore
                    func=self.func,
                    inicial=kwargs.pop("vals_iniciales"),
                    error=kwargs.pop("error"),
                    max_its=kwargs.pop("max_its"),
                )
            case 3:
                resultado = FuncManager.secante(  # type: ignore
                    func=self.func,
                    iniciales=kwargs.pop("vals_iniciales"),
                    error=kwargs.pop("error"),
                    max_its=kwargs.pop("max_its"),
                )
        if self.met_actual in (0, 1):
            self.mostrar_r_cerrado(resultado)  # type: ignore
        elif self.met_actual in (2, 3):
            self.mostrar_r_abierto(resultado)  # type: ignore

    def mostrar_r_cerrado(
        self, resultado: Union[bool, tuple[Decimal, Decimal, list, int]]
    ) -> None:
        """
        Se encarga de mostrar los resultados de métodos cerrados.
        """

        tipo_metodo = "bisección" if self.met_actual == 0 else "falsa posición"
        if isinstance(resultado, bool):
            if resultado:
                error_msg = "La función no cambia de signo en el intervalo indicado!"
            else:
                error_msg = "La función no es continua en el intervalo indicado!"
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado,
                msg_frame=self.msg_frame,
                msg=error_msg,
                tipo="error",
            )

            return

        x, fx, registro, its = resultado
        x_igual = rf"{self.func.var} = {format(x.normalize(), 'f')}"
        fx_igual = rf"{self.func.nombre} = {format(fx.normalize(), 'f')}"

        raiz_img = Func.latex_to_png(
            output_file="resultado_"
            + f"{'biseccion' if self.met_actual == 0 else 'fp'}"
            + f"_{self.func.nombre}",
            misc_str=rf"{x_igual}" + r"\\[1em]" + rf"{fx_igual}",
        )

        if its == -1:
            border_color = "#ff3131"
            interpretacion = (
                f"El método de {tipo_metodo} no converge "
                + f"después de {MAX_ITERACIONES} iteraciones!"
            )
        else:
            border_color = None
            interpretacion = (
                f"El método de {tipo_metodo} converge después de {its} iteraciones!\n"
                + f"Raíz{' ' if fx == 0 else ' aproximada '}encontrada: "
            )

            ctkLabel(self.resultado, text=interpretacion).grid(
                row=0, column=0, pady=5, sticky="n"
            )

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.msg_frame,
            msg=interpretacion if its == -1 else None,
            img=raiz_img if its != -1 else None,
            border_color=border_color,
            tipo="resultado",
            row=1,
        )

        ctkButton(
            self.resultado,
            height=30,
            text="Mostrar registro de iteraciones",
            command=lambda: self.toggle_tabla(registro),
        ).grid(row=2, column=0, ipadx=5, pady=5, sticky="n")

    def mostrar_r_abierto(
        self, resultado: tuple[Decimal, Decimal, list, int, bool]
    ) -> None:
        """
        Se encarga de mostrar los resultados de métodos abiertos.
        """

        tipo_metodo = "Newton" if self.met_actual == 2 else "la secante"
        x, fx, registro, its, flag = resultado

        x_igual = rf"{self.func.var} = {format(x.normalize(), 'f')}"
        fx_igual = rf"{self.func.nombre} = {format(fx.normalize(), 'f')}"

        if flag != I:
            raiz_img = None
            border_color = "#ff3131"

            if flag == -I:
                interpretacion = (
                    f"En la iteración {its}:\n"
                    + "La derivada de la función es igual a 0 en "
                    + f"{format(x.normalize(), 'f')}!"
                )
            elif flag == -1:
                interpretacion = (
                    f"En la iteración {its}:\n"
                    + f"{format(x.normalize(), 'f')} no es parte del "
                    + f"dominio de {self.func.nombre}"
                )
            elif flag == 1:
                interpretacion = (
                    f"En la iteración {its}:\n"
                    + f"{format(x.normalize(), 'f')} no es parte del "
                    + f"dominio de {self.func.nombre[0]}′(x)!"
                )
            elif flag == zoo:
                interpretacion = (
                    f"El método de {tipo_metodo} no converge "
                    + f"después de {its} iteraciones!"
                )
        else:
            border_color = None
            interpretacion = (
                f"El método de {tipo_metodo} converge después de {its} iteraciones!\n"
                + f"Raíz{' ' if fx == 0 else ' aproximada '}encontrada: "
            )

            raiz_img = Func.latex_to_png(
                output_file="resultado_"
                + f"{tipo_metodo.lower().strip('la')}_"
                + f"{self.func.nombre}",
                misc_str=rf"{x_igual}" + r"\\[1em]" + rf"{fx_igual}",
            )

            ctkLabel(
                self.resultado,
                text=interpretacion,  # pylint: disable=E0606
            ).grid(row=0, column=0, pady=5, sticky="n")

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.msg_frame,
            msg=interpretacion if flag != I else None,
            img=raiz_img,
            border_color=border_color,
            tipo="resultado",
            row=1,
        )

        ctkButton(
            self.resultado,
            height=30,
            text="Mostrar registro de iteraciones",
            command=lambda: self.toggle_tabla(registro),
        ).grid(row=2, column=0, ipadx=5, pady=5, sticky="n")

    def toggle_tabla(self, registro: list[list[str]]) -> None:
        """
        Muestra o esconde la registro de iteraciones.
        """

        if not self.table_hidden:
            return

        new_window = ctkTop(self.app)
        new_window.title("GaussBot: Registro de Iteraciones")
        new_window.geometry("1000x500")

        self.after(100, new_window.focus)
        self.after(250, lambda: set_icon(self.app, new_window))

        new_window.protocol("WM_DELETE_WINDOW", lambda: delete_window(new_window))

        self.tabla_its = CustomTable(new_window, registro)
        self.tabla_its.pack(expand=True, fill="both", padx=20, pady=20)
        self.table_hidden = False

        def delete_window(new_window: ctkTop) -> None:
            self.table_hidden = True
            new_window.destroy()

    def handle_pi(self, num_input: str) -> Fraction:
        """
        Procesar el input del usuario si ingresaron 'pi' en su número.
        """

        PI = Fraction(355, 133)
        if "pi" not in num_input:
            return Fraction(num_input)
        if "pi" == num_input:
            return PI
        if "/" in num_input:
            num, den = num_input.split("/")
            num_input = (
                num.replace("pi", "").replace("*", "").strip()
                if "pi" in num
                else den.replace("pi", "").replace("*", "").strip()
            )

            if "pi" in num:
                return (Fraction(num_input) * PI) / Fraction(den)
            return Fraction(num) / (Fraction(num_input) * PI)

        num_input = num_input.replace("pi", "").replace("*", "").strip()
        return Fraction(num_input) * PI

    def update_frame(self):
        """
        Configura todos los backgrounds de los widgets
        por si hubo un cambio de modo de apariencia.
        """

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.func_select.configure(
            values=self.nombres_funcs,
            variable=Variable(
                value="Seleccione una función para encontrar sus raíces:"
            ),
        )

        if not self.table_hidden:
            self.after(250, lambda: set_icon(self.app, self.tabla_its.parent))

        for widget in self.metodo_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.datos_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore
