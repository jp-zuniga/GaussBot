"""
Implementación de RaicesFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

from decimal import (
    Decimal,
    getcontext,
)

from random import randint
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from tkinter import Variable
from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from sympy import (
    I,
    zoo,
)

from ....msg_frame_funcs import place_msg_frame
from ....util_funcs import generate_sep
from ....models import Func
from ....managers import (
    MARGEN_ERROR,
    MAX_ITERACIONES,
    FuncManager,
)

from ...custom import (
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
)

if TYPE_CHECKING:
    from ... import GaussUI
    from .. import AnalisisFrame

getcontext().prec = 12  # precision de decimales

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
    ) -> None:

        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)

        self.metodo_frame = ctkFrame(self, fg_color="transparent")
        self.datos_frame = ctkFrame(self, fg_color="transparent")
        self.resultado = ctkFrame(self, fg_color="transparent")
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
        self.metodo_actual: int = -1
        self.selected_func: Func

        self.a_entry: CustomEntry
        self.b_entry: CustomEntry
        self.xi_entry: CustomEntry
        self.xu_entry: CustomEntry
        self.error_entry: CustomEntry
        self.iteraciones_entry: CustomEntry

        self.func_select = CustomDropdown(
            self,
            variable=Variable(
                value="Seleccione una función para encontrar sus raíces:",
            ), values=self.nombres_funcs,
            command=self.mostrar_func,
        )

        self.func_select.grid(row=0, column=0, pady=5, sticky="n")

    def mostrar_func(self, nombre_func: str) -> None:
        """
        Muestra la función seleccionada en el dropdown,
        y crea un dropdown para seleccionar el método a utilizar.
        """

        self.metodo_frame.grid(row=1, column=0, pady=5, sticky="n")
        self.selected_func = self.func_manager.funcs_ingresadas[nombre_func]

        for widget in self.metodo_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.datos_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        ctkLabel(
            self.metodo_frame,
            text="",
            image=self.selected_func.get_png(),
        ).grid(row=0, column=0, pady=5, sticky="n")

        ctkLabel(
            self.metodo_frame,
            text="",
            image=generate_sep(False, (300, 5)),
        ).grid(row=1, column=0, sticky="n")

        CustomDropdown(
            self.metodo_frame,
            variable=Variable(value="Seleccione un método para encontrar las raíces:"),
            values=list(self.metodos.keys()),
            command=self.mostrar_datos,
        ).grid(row=2, column=0, pady=5, sticky="n")

    def mostrar_datos(self, metodo: str) -> None:
        """
        Muestra los campos necesarios para ingresar los datos
        requeridos por el método seleccionado.
        """

        self.datos_frame.grid(row=2, column=0, pady=5, sticky="n")
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        if self.metodos.get(metodo, None) is None:
            raise ValueError("Argumento inválido para 'metodo'!")

        if (
            self.metodo_actual == self.metodos[metodo]
            and
            not self.datos_frame.winfo_children()
        ):
            return

        if (
            self.metodo_actual == 0 and self.metodos[metodo] == 1
            or
            self.metodo_actual == 1 and self.metodos[metodo] == 0
        ):
            self.limpiar_inputs()
            return

        for widget in self.datos_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        self.metodo_actual = self.metodos[metodo]
        match self.metodo_actual:
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

        ctkLabel(
            self.datos_frame,
            text="Intervalo:",
        ).grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ne")

        self.a_entry = CustomEntry(
            self.datos_frame,
            width=60,
            placeholder_text=str(randint(-10, -1))
        )

        self.a_entry.grid(row=0, column=1, padx=5, pady=(5, 2), sticky="ne")
        ctkLabel(
            self.datos_frame,
            text=",",
            font=("Roboto", 18),
        ).grid(row=0, column=2, padx=2, pady=(5, 2), sticky="nw")

        self.b_entry = CustomEntry(
            self.datos_frame,
            width=60,
            placeholder_text=str(randint(1, 10))
        )

        self.b_entry.grid(row=0, column=3, padx=5, pady=(5, 2), sticky="nw")
        ctkLabel(
            self.datos_frame,
            text="Margen de error:",
        ).grid(row=1, column=0, padx=5, pady=(2, 5), sticky="ne")

        self.error_entry = CustomEntry(self.datos_frame)
        self.error_entry.insert(0, f"{float(MARGEN_ERROR):.6f}")
        self.error_entry.grid(
            row=1, column=1,
            columnspan=3,
            padx=5, pady=(2, 5),
            sticky="nw",
        )

        ctkButton(
            self.datos_frame,
            height=30,
            text="Encontrar raíz",
            command=self.leer_datos
        ).grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def setup_abierto(self, newton: bool) -> None:
        """
        Configura self.datos_frame para aceptar input
        de valor inicial, margen de error y máximo de iteraciones
        para el método de Newton.
        """

        ctkLabel(
            self.datos_frame,
            text="Valor inicial:"
                 if newton
                 else
                 "Valores iniciales:",
        ).grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ne")

        xi_width = 140 if newton else 60
        self.xi_entry = CustomEntry(
            self.datos_frame,
            width=xi_width,
            placeholder_text=str(randint(-10, 10))
        )

        if not newton:
            self.xu_entry = CustomEntry(
                self.datos_frame,
                width=60,
                placeholder_text=str(randint(-10, 10))
            )

            self.xi_entry.grid(row=0, column=1, padx=5, pady=(5, 2), sticky="nw")
            ctkLabel(
                self.datos_frame,
                text=",",
                font=("Roboto", 18),
            ).grid(row=0, column=2, padx=2, pady=(5, 2), sticky="nw")

            self.xu_entry.grid(
                row=0, column=3,
                padx=5, pady=(5, 2),
                sticky="nw",
            )
        else:
            self.xi_entry.grid(
                row=0, column=1,
                columnspan=3,
                padx=5, pady=(5, 2),
                sticky="nw",
            )

        ctkLabel(
            self.datos_frame,
            text="Margen de error:",
        ).grid(row=2, column=0, padx=5, pady=2, sticky="ne")

        self.error_entry = CustomEntry(self.datos_frame)
        self.error_entry.insert(0, f"{float(MARGEN_ERROR):.6f}")
        self.error_entry.grid(
            row=2, column=1,
            columnspan=3,
            padx=5, pady=2,
            sticky="nw",
        )

        ctkLabel(
            self.datos_frame,
            text="Máximo de iteraciones:",
        ).grid(row=3, column=0, padx=5, pady=(2, 5), sticky="ne")

        self.iteraciones_entry = CustomEntry(self.datos_frame)
        self.iteraciones_entry.insert(0, MAX_ITERACIONES)
        self.iteraciones_entry.grid(
            row=3, column=1,
            columnspan=3,
            padx=5, pady=(2, 5),
            sticky="nw",
        )

        ctkButton(
            self.datos_frame,
            height=30,
            text="Encontrar raíz",
            command=self.leer_datos
        ).grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def leer_datos(self) -> None:
        """
        Lee y valida los datos ingresados por el usuario
        en las widgets de self.datos_frame.
        """

        self.resultado.grid(row=3, column=0, pady=5, sticky="n")
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        dominio = self.selected_func.get_dominio()
        if self.metodo_actual in (0, 1):  # metodos cerrados
            try:
                a = Decimal(self.a_entry.get())
                b = Decimal(self.b_entry.get())
                error = Decimal(self.error_entry.get())

                if a > b:
                    raise ArithmeticError(
                        "En un intervalo, el número menor debe ir primero!"
                    )
                if a not in dominio or b not in dominio:
                    raise ArithmeticError(
                        "Los extremos del intervalo no son parte del " +
                       f"dominio de {self.selected_func.nombre}!"
                    )

                self.calc_raiz(vals_iniciales=(a, b), error=error)
            except (ValueError, ZeroDivisionError, ArithmeticError) as e:
                self.msg_frame = place_msg_frame(
                    parent_frame=self.resultado,
                    msg_frame=self.msg_frame,
                    msg=str(e),
                    tipo="error",
                )

                return

        elif self.metodo_actual in (2, 3):  # metodos abiertos
            try:
                xi = Decimal(self.xi_entry.get())
                error = Decimal(self.error_entry.get())
                max_its = int(self.iteraciones_entry.get())
                if max_its <= 0:
                    raise ValueError(
                        "Debe ingresar un número entero positivo "+
                        "para el máximo de iteraciones!"
                    )

                if xi not in dominio:
                    adj = "primer " if self.metodo_actual == 3 else ""
                    raise ArithmeticError(
                        f"El {adj}valor inicial no es parte del " +
                        f"dominio de {self.selected_func.nombre}!"
                    )

                if self.metodo_actual == 3:
                    xu = Decimal(self.xu_entry.get())
                    vals = (xi, xu)
                    if xu not in dominio:
                        raise ArithmeticError(
                            "El segundo valor inicial no es parte del " +
                            f"dominio de {self.selected_func.nombre}!"
                        )
                else:
                    vals = xi  # type: ignore

                self.calc_raiz(vals_iniciales=vals, error=error, max_its=max_its)
            except (ValueError, ZeroDivisionError, ArithmeticError) as e:
                if isinstance(e, ValueError) and "Decimal" in str(e):
                    error_substr = (
                        "el valor inicial"
                        if self.metodo_actual == 2
                        else "lost valores iniciales"
                    )

                    error_msg = (
                        "Debe ingresar números racionales para "+
                       f"{error_substr} y margen de error!"
                    )
                elif isinstance(e, ValueError) and "int" in str(e):
                    error_msg = (
                        "Debe ingresar números enteros positivos " +
                        "para el máximo de iteraciones!"
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

                return

    def calc_raiz(self, **kwargs) -> None:
        """
        Calcula la raíz de self.func_selecccionada
        utilizando self.metodo_actual.

        Kwargs válidos:
        - Para métodos cerrados:
            - vals_iniciales: tuple[Decimal, Decimal]
        - Para métodos abiertos:
            - vals_iniciales: Union[Decimal, tuple[Decimal, Decimal]]
            - max_its: int (<= 0) = 500
        - error = Decimal(1, 1000000)
        """

        match self.metodo_actual:
            case 0:
                resultado = self.func_manager.biseccion(
                    func=self.selected_func,
                    intervalo=kwargs.pop("vals_iniciales"),
                    error=kwargs.pop("error"),
                )
            case 1:
                resultado = self.func_manager.falsa_posicion(
                    func=self.selected_func,
                    intervalo=kwargs.pop("vals_iniciales"),
                    error=kwargs.pop("error"),
                )
            case 2:
                resultado = self.func_manager.newton(  # type: ignore
                    func=self.selected_func,
                    inicial=kwargs.pop("vals_iniciales"),
                    error=kwargs.pop("error"),
                    max_its=kwargs.pop("max_its"),
                )
            case 3:
                resultado = self.func_manager.secante(  # type: ignore
                    func=self.selected_func,
                    iniciales=kwargs.pop("vals_iniciales"),
                    error=kwargs.pop("error"),
                    max_its=kwargs.pop("max_its"),
                )
        if self.metodo_actual in (0, 1):
            self.mostrar_r_cerrado(resultado)  # type: ignore
        elif self.metodo_actual in (2, 3):
            self.mostrar_r_abierto(resultado)  # type: ignore

    def mostrar_r_cerrado(
        self,
        resultado: Union[bool, tuple[Decimal, Decimal, int]],
    ) -> None:

        """
        Se encarga de mostrar los resultados de métodos cerrados.
        """

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

        error = Decimal(self.error_entry.get())
        x, fx, its = resultado

        x_igual = rf"x = {format(x.normalize(), "f")}"
        fx_igual = rf"f(x) = {format(fx.normalize(), "f")}"

        raiz_img = Func.latex_to_png(
            nombre=f"resultado_cerrado_{self.selected_func.nombre}",
            misc_str=rf"{x_igual}" + r"\\[1em]" + rf"{fx_igual}",
            font_size=60,
        )

        tipo_metodo = "bisección" if self.metodo_actual == 0 else "falsa posición"
        if its == -1:
            border_color = "#ff3131"
            interpretacion = (
                f"Después de {MAX_ITERACIONES} iteraciones, no se encontró " +
                f"una raíz dentro del margen de error {error.normalize()}!\n" +
                 "Raíz aproximada encontrada:"
            )
        else:
            border_color = None
            interpretacion = (
                f"El método de {tipo_metodo} converge después de {its} iteraciones!\n" +
                f"Raíz{" " if fx == 0 else " aproximada "}encontrada: "
            )

        ctkLabel(
            self.resultado,
            text=interpretacion,
        ).grid(row=0, column=0, pady=5, sticky="n")

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.msg_frame,
            img=raiz_img,
            border_color=border_color,
            tipo="resultado",
            row=1,
        )

    def mostrar_r_abierto(
        self,
        resultado: tuple[Decimal, Decimal, int, bool],
    ) -> None:

        """
        Se encarga de mostrar los resultados de métodos abiertos.
        """

        tipo_metodo = "Newton" if self.metodo_actual == 2 else "la secante"
        x, fx, its, flag = resultado
        x_igual = rf"x = {format(x.normalize(), "f")}"
        fx_igual = rf"f(x) = {format(fx.normalize(), "f")}"

        if flag is not I:
            raiz_img = None
            border_color = "#ff3131"

            if flag is -I:
                interpretacion = (
                    f"En la iteración {its}:\n" +
                     "La derivada de la función es igual a 0 en " +
                    f"{format(x.normalize(), "f")}!"
                )
            elif flag == -1:
                interpretacion = (
                    f"En la iteración {its}:\n" +
                    f"{format(x.normalize(), "f")} no es parte del " +
                    f"dominio de {self.selected_func.nombre}"
                )
            elif flag == 1:
                interpretacion = (
                    f"En la iteración {its}:\n" +
                    f"{format(x.normalize(), "f")} no es parte del " +
                    f"dominio de {self.selected_func.nombre[0]}'(x)!"
                )
            elif flag is zoo:
                interpretacion = (
                    f"El método de {tipo_metodo} no converge " +
                    f"después de {its} iteraciones!"
                )
        else:
            border_color = None
            interpretacion = (
                f"El método de {tipo_metodo} converge después de {its} iteraciones!\n" +
                f"Raíz{" " if fx == 0 else " aproximada "}encontrada: "
            )

            raiz_img = Func.latex_to_png(
                nombre=f"resultado_abierto_{self.selected_func.nombre}",
                misc_str=rf"{x_igual}" + r"\\[1em]" + rf"{fx_igual}",
                font_size=60,
            )

            ctkLabel(
                self.resultado,
                text=interpretacion,  # pylint: disable=E0606
            ).grid(row=0, column=0, pady=5, sticky="n")

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.msg_frame,
            msg=interpretacion if flag is not I else None,
            img=raiz_img,
            border_color=border_color,
            tipo="resultado",
            row=1,
        )

    def limpiar_inputs(self) -> None:
        """
        Limpia el texto de todos los entries
        de datos en self.datos_frame.
        """

        for widget in self.datos_frame.winfo_children():
            if (
                isinstance(widget, CustomEntry) and
                widget.get() != "" and
                widget.get() != f"{float(MARGEN_ERROR):.6f}"
            ):
                widget.delete(0, "end")

    def update_frame(self):
        """
        Configura todos los backgrounds de los widgets
        por si hubo un cambio de modo de apariencia.
        """

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.func_select.configure(values=self.nombres_funcs)

        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore
            if isinstance(widget, ctkFrame):
                for subwidget in widget.winfo_children():  # type: ignore
                    subwidget.configure(bg_color="transparent")  # type: ignore
