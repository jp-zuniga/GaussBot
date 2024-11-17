"""
Implementación de RaicesFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

from fractions import Fraction
from os import path
from random import randint
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from tkinter import (
    TclError,
    Variable,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
)

from sympy import (
    And, Expr, FiniteSet,
    Interval, log,
    Set, Symbol, Pow,
    diff, lambdify, latex,
    parse_expr, solve,
    sqrt, symbols,
)

from sympy.parsing.sympy_parser import (
    standard_transformations,
    implicit_multiplication_application,
)

from gauss_bot import (
    DATA_PATH,
    ENTER_ICON,
    DROPDOWN_ICON,
    DROPUP_ICON,
    FX_ICON,
    delete_msg_frame,
    get_dict_key,
    generate_sep,
    generate_funcs,
    latex_to_png,
)

from gauss_bot.gui.custom import (
    CustomEntry,
    CustomDropdown,
    FuncDropdown,
    IconButton,
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import AnalisisFrame


TRANSFORMS = (standard_transformations + (implicit_multiplication_application,))
MARGEN_ERROR = Fraction(1, 1000000)
MAX_ITERACIONES = 500


class RaicesFrame(CustomScrollFrame):
    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "AnalisisFrame"
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.selectors: list[FuncDropdown] = []
        self.signos: list[CustomDropdown] = []
        self.arg_entries: list[ctkEntry] = []
        self.func = ""

        self.metodos: list[str] = [
            "Método de Bisección",
            "Método de Newton",
        ]

        self.a_entry: CustomEntry
        self.b_entry: CustomEntry
        self.xi_entry: CustomEntry
        self.error_entry: CustomEntry
        self.iteraciones_entry: CustomEntry

        self.collapse_button: Optional[ctkButton] = None
        self.msg_frame: Optional[ctkFrame] = None
        self.collapsed_terminos = True

        self.terminos_frame = ctkFrame(self)
        self.func_frame = ctkFrame(self)
        self.calc_frame = ctkFrame(self)

        terminos_label = ctkLabel(self, text="¿Cuántos términos tendrá la función?")
        self.terminos_entry = ctkEntry(self, width=30, placeholder_text="3")
        self.terminos_entry.bind("<Return>", lambda _: self.setup_terminos_frame())

        ingresar_button = IconButton(
            self,
            self.app,
            image=ENTER_ICON,
            tooltip_text="Ingresar términos",
            command=self.setup_terminos_frame,
        )

        terminos_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")
        self.terminos_entry.grid(row=0, column=1, padx=5, pady=5, sticky="new")
        ingresar_button.grid(row=0, column=2, ipady=3, pady=5, sticky="nw")

    def toggle_terminos_frame(self) -> None:
        if self.collapsed_terminos:
            self.terminos_frame.grid()
            if self.collapse_button is not None:
                self.collapse_button.configure(
                    image=DROPUP_ICON,
                    tooltip_text="Colapsar"
                )
        else:
            self.terminos_frame.grid_remove()
            if self.collapse_button is not None:
                self.collapse_button.configure(
                    image=DROPDOWN_ICON,
                    tooltip_text="Expandir"
                )
        self.collapsed_terminos = not self.collapsed_terminos
        self.update_frame()

    def setup_terminos_frame(self) -> None:
        self.terminos_frame.grid(row=1, column=0, columnspan=3, sticky="n")
        self.terminos_frame.columnconfigure(0, weight=1)
        self.terminos_frame.columnconfigure(1, weight=1)
        for widget in self.terminos_frame.winfo_children():
            widget.destroy()
        for widget in self.func_frame.winfo_children():
            widget.destroy()
        for widget in self.calc_frame.winfo_children():
            widget.destroy()

        if self.collapse_button is not None:
            self.collapse_button.destroy()

        delete_msg_frame(self.msg_frame)

        self.func_frame.grid_remove()
        self.calc_frame.grid_remove()
        self.signos.clear()
        self.selectors.clear()
        self.arg_entries.clear()
        self.func = ""

        try:
            num_terminos = int(self.terminos_entry.get())
        except ValueError:
            self.msg_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos para la cantidad de términos!"
            )
            self.msg_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return

        delete_msg_frame(self.msg_frame)

        sep1 = ctkLabel(
            self.terminos_frame,
            image=generate_sep(False, (300, 20)),
            text="",
        )

        sep2 = ctkLabel(
            self.terminos_frame,
            image=generate_sep(False, (300, 20)),
            text="",
        )

        fx_label = ctkLabel(
            self.terminos_frame,
            corner_radius=10,
            image=FX_ICON,
            text="",
        )

        sep1.grid(row=0, column=0, columnspan=3, sticky="n")
        fx_label.grid(row=1, column=0, columnspan=3, padx=5, ipady=5, pady=5, sticky="n")

        for i in range(num_terminos):
            signo = CustomDropdown(
                self.terminos_frame,
                width=60,
                values=["+", "−"],
                font=("Roboto", 18),
                dropdown_font=("Roboto", 18),
                dynamic_resizing=False,
            )

            dropdown = FuncDropdown(
                master=self.terminos_frame,
                app=self.app,
                button_text="Seleccione una familia de funciones:",
            )

            signo.grid(row=i + 2, column=0, padx=5, pady=5, sticky="ne")
            dropdown.options_button.grid(
                row=i + 2, column=1, columnspan=2, padx=5, pady=5, sticky="nw"
            )

            self.signos.append(signo)
            self.selectors.append(dropdown)

        leer_func_button = ctkButton(
            self.terminos_frame, text="Leer función", command=self.mostrar_func
        )

        leer_func_button.grid(row=num_terminos + 2, column=0, columnspan=3, pady=5, sticky="n")
        sep2.grid(row=num_terminos + 3, column=0, columnspan=3, sticky="n")
        self.collapsed_terminos = False

    def extract_func(self, dropdown: FuncDropdown, img: ctkImage) -> None:
        func_key = get_dict_key(dropdown.images, img)
        self.crear_arg_entry(dropdown, func_key)  # type: ignore

    def crear_arg_entry(self, dropdown: FuncDropdown, func_key: str) -> None:
        row, column = dropdown.options_button.grid_info()["row"], 2
        arg_entry = ctkEntry(
            self.terminos_frame,
            width=80,
            placeholder_text=generate_funcs(func_key),
        )

        self.arg_entries.append(arg_entry)
        self.bind_entry_keys(arg_entry, len(self.arg_entries) - 1)
        dropdown.options_button.grid(columnspan=1, sticky="new")
        arg_entry.grid(row=row, column=column, padx=5, pady=5, sticky="nw")

    def leer_arg_entries(self) -> str:
        func = ""
        for sig_entry, arg_entry in zip(self.signos, self.arg_entries):
            signo = sig_entry.get()
            arg = arg_entry.get()
            print("arg:", arg)
            if not arg.startswith(("+", "−")):
                arg = f"+{arg}"

            signos_iguales = (
                arg[0] == "+" and signo == "+"
                or
                arg[0] == "-" and signo == "−"
            )

            signos_distintos = (
                arg[0] == "+" and signo == "−"
                or
                arg[0] == "-" and signo == "+"
            )

            if arg[0] in ("+", "−"):
                arg = arg[1:]

            if signos_iguales:
                func += f"+{arg}"
            elif signos_distintos:
                func += f"-{arg}"
        print(func)
        return func

    def leer_func(self) -> None:
        self.func = self.leer_arg_entries()
        if "sen" in self.func:
            self.func = self.func.replace("sen", "sin")
        if "^" in self.func:
            self.func = self.func.replace("^", "**")

    def mostrar_func(self) -> None:
        for widget in self.func_frame.winfo_children():
            widget.destroy()
        for widget in self.calc_frame.winfo_children():
            widget.destroy()
        for widget in self.winfo_children():  # type: ignore
            if isinstance(widget, ctkLabel) and "converge" in widget._text:
                widget.destroy()


        self.func_frame.grid_remove()
        self.calc_frame.grid_remove()
        if self.collapse_button is not None:
            self.collapse_button.destroy()

        try:
            delete_msg_frame(self.msg_frame)
        except TclError:
            pass

        self.leer_func()
        parsed_func = parse_expr(self.func, transformations=TRANSFORMS)
        latex_func = latex(parsed_func, ln_notation=True)
        latex_func = r"f(x) = " + latex_func
        img = latex_to_png(latex_func, path.join(DATA_PATH, "func.png"))

        func_label = ctkLabel(
            self.func_frame,
            image=img,
            text="",
        )

        self.collapse_button = IconButton(
            self,
            self.app,
            image=DROPUP_ICON,
            tooltip_text="Colapsar",
            command=self.toggle_terminos_frame,
        )

        self.collapse_button.grid(row=2, column=0, columnspan=3, padx=5, sticky="n")
        self.func_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=1, sticky="n")
        func_label.grid(row=0, column=0, padx=5, pady=5)
        self.setup_calc_frame()

    def setup_calc_frame(self) -> None:
        for widget in self.calc_frame.winfo_children():
            widget.destroy()
        for widget in self.winfo_children():  # type: ignore
            if isinstance(widget, ctkLabel) and "converge" in widget._text:
                widget.destroy()

        self.calc_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.calc_frame.columnconfigure(0, weight=1)
        self.calc_frame.columnconfigure(3, weight=1)
        select_metodo = CustomDropdown(
            self.calc_frame,
            variable=Variable(value="Seleccione un método:"),
            values=self.metodos,
            command=self.setup_metodo,
        )

        select_metodo.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def setup_metodo(self, metodo: str) -> None:
        for widget in self.calc_frame.winfo_children():
            if (not isinstance(widget, CustomDropdown)
                or isinstance(widget, ResultadoFrame)):
                widget.destroy()
        for widget in self.winfo_children():  # type: ignore
            if isinstance(widget, ctkLabel) and "aíz" in widget._text:
                widget.destroy()

        match metodo:
            case "Método de Bisección":
                self.setup_biseccion()
            case "Método de Newton":
                self.setup_newton()
            case _:
                raise ValueError("Método inválido!")

    def setup_biseccion(self) -> None:
        intervalo_label = ctkLabel(self.calc_frame, text="Intervalo:")
        self.a_entry = CustomEntry(
            self.calc_frame,
            width=40,
            placeholder_text=randint(-10, -1)
        )

        and_label = ctkLabel(self.calc_frame, text=",", font=("Roboto", 18))
        self.b_entry = CustomEntry(
            self.calc_frame,
            width=40,
            placeholder_text=randint(1, 10)
        )

        error_label = ctkLabel(self.calc_frame, text="Margen de error:")
        self.error_entry = CustomEntry(self.calc_frame, width=102)
        self.error_entry.insert(0, f"{float(MARGEN_ERROR):.6f}")

        self.a_entry.bind("<Right>", lambda _: self.b_entry.focus_set())
        self.b_entry.bind("<Left>", lambda _: self.a_entry.focus_set())
        self.a_entry.bind("<Return>", lambda _: self.raiz_biseccion())
        self.b_entry.bind("<Return>", lambda _: self.raiz_biseccion())

        encontrar_button = ctkButton(
            self.calc_frame,
            height=30,
            text="Encontrar raíz",
            command=self.raiz_biseccion
        )

        intervalo_label.grid(row=1, column=0, padx=5, pady=(5, 2), sticky="ne")
        self.a_entry.grid(row=1, column=1, padx=5, pady=(5, 2), sticky="ne")
        and_label.grid(row=1, column=2, padx=3, pady=(5, 2), sticky="nw")
        self.b_entry.grid(row=1, column=3, padx=5, pady=(5, 2), sticky="nw")
        error_label.grid(row=2, column=0, padx=5, pady=(2, 5), sticky="ne")
        self.error_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=(2, 5), sticky="nw")
        encontrar_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def setup_newton(self) -> None:
        inicial_label = ctkLabel(self.calc_frame, text="Valor inicial:")
        self.xi_entry = CustomEntry(
            self.calc_frame,
            width=102,
            placeholder_text=randint(-10, 10)
        )

        error_label = ctkLabel(self.calc_frame, text="Margen de error:")
        self.error_entry = CustomEntry(self.calc_frame, width=102)
        iteraciones_label = ctkLabel(self.calc_frame, text="Máximo de iteraciones:")
        self.iteraciones_entry = CustomEntry(self.calc_frame, width=102)

        self.xi_entry.bind("<Return>", lambda _: self.raiz_newton())
        self.error_entry.insert(0, f"{float(MARGEN_ERROR):.6f}")
        self.iteraciones_entry.insert(0, MAX_ITERACIONES)

        encontrar_button = ctkButton(
            self.calc_frame,
            height=30,
            text="Encontrar raíz",
            command=self.raiz_newton
        )

        inicial_label.grid(row=1, column=0, padx=5, pady=(5, 2), sticky="ne")
        self.xi_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=(5, 2), sticky="nw")
        error_label.grid(row=2, column=0, padx=5, pady=2, sticky="ne")
        self.error_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=2, sticky="nw")
        iteraciones_label.grid(row=3, column=0, padx=5, pady=(2, 5), sticky="ne")
        self.iteraciones_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=(2, 5), sticky="nw")
        encontrar_button.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def raiz_biseccion(self) -> None:
        delete_msg_frame(self.msg_frame)
        try:
            a = Fraction(self.a_entry.get())
            b = Fraction(self.b_entry.get())
            error = Fraction(self.error_entry.get())
        except ValueError:
            self.msg_frame = ErrorFrame(
                self, "Debe ingresar números reales para el intervalo y margen de error!"
            )
            self.msg_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return
        delete_msg_frame(self.msg_frame)

        resultado = biseccion(self.func, (a, b), error)
        if resultado is False:
            self.msg_frame = ErrorFrame(
                self, f"La función no es continua en el intervalo [{float(a):.4f}, {float(b):.4f}]!"
            )
            self.msg_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return
        elif resultado is True:
            self.msg_frame = ErrorFrame(
                self, f"La función no cambia de signo en el intervalo [{float(a):.4f}, {float(b):.4f}]!"
            )
            self.msg_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return
        delete_msg_frame(self.msg_frame)

        x, fx, i = resultado
        x = Fraction(x).limit_denominator()
        fx = Fraction(fx).limit_denominator()

        x_igual = rf"x = {float(x):6f}"
        f_x_igual = rf"f(x) = {float(fx):6f}"

        func_img = latex_to_png(
            latex_str= rf"{x_igual}" +
                       r"\\[1em]" +
                       rf"{f_x_igual}",
            output_file=path.join(DATA_PATH, "func.png"),
            font_size=60,
        )

        if i == -1:
            interpretacion_label = ctkLabel(
                self,
                text=f"Después de {MAX_ITERACIONES} iteraciones, no se encontró " +
                     f"una raíz dentro del margen de error {float(error):.6f}!\n" +
                      "Raíz aproximada encontrada:"
            )

            self.msg_frame = ResultadoFrame(
                self, solo_header=True,
                resultado="", header="",
                border_color="#ff3131",
            )

            self.msg_frame.columnconfigure(0, weight=1)
            img_label = ctkLabel(self.msg_frame, text="", image=func_img)

            interpretacion_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            img_label.grid(row=0, column=0, padx=10, pady=(3, 10), sticky="n")
            self.msg_frame.grid(
                row=6,
                column=0,
                columnspan=3,
                ipadx=10,
                ipady=10,
                padx=5,
                pady=5,
                sticky="n",
            )

            return
        delete_msg_frame(self.msg_frame)

        tipo_raiz = "" if fx == 0 else "aproximada "
        interpretacion_label = ctkLabel(
            self,
            text=f"El método de bisección converge después de {i} iteraciones!\n" +
                 f"Raíz {tipo_raiz}encontrada: ",
        )

        self.msg_frame = ResultadoFrame(
            self, header="", resultado="", solo_header=True
        )

        self.msg_frame.columnconfigure(0, weight=1)
        img_label = ctkLabel(self.msg_frame, text="", image=func_img)

        interpretacion_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        img_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.msg_frame.grid(
            row=6,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
        )

    def raiz_newton(self) -> None:
        delete_msg_frame(self.msg_frame)
        try:
            xi = Fraction(self.xi_entry.get())
            error = Fraction(self.error_entry.get())
            iteraciones = int(self.iteraciones_entry.get())
        except ValueError as v:
            v_str = str(v)
            if "Fraction" in v_str:
                msj = "Debe ingresar números reales para el valor inicial y margen de error!"
            elif "int" in v_str:
                msj = "Debe ingresar un número entero positivo para el máximo de iteraciones!"

            self.msg_frame = ErrorFrame(self, msj)
            self.msg_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return
        delete_msg_frame(self.msg_frame)

        x, fx, i, division_cero = newton(self.func, xi, error, iteraciones)
        x = Fraction(x).limit_denominator()
        fx = Fraction(fx).limit_denominator()

        x_igual = rf"x = {float(x):6f}"
        fx_igual = rf"f(x) = {float(fx):6f}"

        func_img = latex_to_png(
            latex_str= rf"{x_igual}" +
                       r"\\[1em]" +
                       rf"{fx_igual}",
            output_file=path.join(DATA_PATH, "func.png"),
            font_size=60,
        )

        if division_cero or i == iteraciones:
            msj = (
                f"En la iteración {i}, la derivada de la función en el valor inicial es 0!"
                if division_cero
                else
                f"Después de {iteraciones} iteraciones, no se encontró " +
                f"una raíz dentro del margen de error {float(error):.6f}!"
            )

            interpretacion_label = ctkLabel(
                self, text=msj + "\nRaíz aproximada encontrada:"
            )

            self.msg_frame = ResultadoFrame(
                self, solo_header=True,
                resultado="", header="",
                border_color="#ff3131",
            )

            self.msg_frame.columnconfigure(0, weight=1)
            img_label = ctkLabel(self.msg_frame, text="", image=func_img)

            interpretacion_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            img_label.grid(row=0, column=0, padx=5, sticky="n")
            self.msg_frame.grid(
                row=6,
                column=0,
                columnspan=3,
                ipadx=10,
                ipady=10,
                padx=5,
                sticky="n",
            )

            return
        delete_msg_frame(self.msg_frame)

        self.msg_frame = ResultadoFrame(
            self, header="", resultado="", solo_header=True
        )

        self.msg_frame.columnconfigure(0, weight=1)
        img_label = ctkLabel(self.msg_frame, text="", image=func_img)
        tipo_raiz = "" if fx == 0 else "aproximada "

        interpretacion_label = ctkLabel(
            self,
            text=f"El método de Newton converge después de {i} iteraciones!\n" +
                 f"Raíz {tipo_raiz}encontrada: ",
        )

        interpretacion_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        img_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.msg_frame.grid(
            row=6,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
        )

    def bind_entry_keys(self, entry: ctkEntry, i: int) -> None:
        entry.bind("<Up>", lambda _: self.entry_move_up(i))
        entry.bind("<Down>", lambda _: self.entry_move_down(i))
        entry.bind("<Return>", lambda _: self.mostrar_func())

    def entry_move_up(self, i: int) -> None:
        if i > 0:
            self.arg_entries[i - 1].focus_set()
        elif i == 0:
            self.arg_entries[-1].focus_set()

    def entry_move_down(self, i: int) -> None:
        if i < len(self.arg_entries) - 1:
            self.arg_entries[i + 1].focus_set()
        elif i == len(self.arg_entries) - 1:
            self.arg_entries[0].focus_set()

    def update_frame(self):
        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
            if isinstance(widget, ctkFrame):
                for subwidget in widget.winfo_children():
                    subwidget.configure(bg_color="transparent")


def es_continua(sp_func: Expr, var: Symbol, intervalo: tuple[Fraction, Fraction]) -> bool:
    intervalo_set = Interval(intervalo[0], intervalo[1])
    discontinuities = FiniteSet()

    for term in sp_func.atoms(Pow):
        if term.exp.is_negative:
            solutions = solve(term.base, var)
            if isinstance(solutions, Set):
                discontinuities = discontinuities.union(solutions)
            elif isinstance(solutions, And):
                for sol in solutions.args:
                    discontinuities = discontinuities.union(FiniteSet(sol))
            else:
                discontinuities = discontinuities.union(FiniteSet(*solutions))

    for term in sp_func.atoms(log):
        solutions = solve(term.args[0] <= 0, var)
        if isinstance(solutions, Set):
            discontinuities = discontinuities.union(solutions)
        elif isinstance(solutions, And):
            for sol in solutions.args:
                discontinuities = discontinuities.union(FiniteSet(sol))
        else:
            discontinuities = discontinuities.union(FiniteSet(*solutions))

    for term in sp_func.atoms(sqrt):
        solutions = solve(term.args[0] < 0, var)
        if isinstance(solutions, Set):
            discontinuities = discontinuities.union(solutions)
        elif isinstance(solutions, And):
            for sol in solutions.args:
                discontinuities = discontinuities.union(FiniteSet(sol))
        else:
            discontinuities = discontinuities.union(FiniteSet(*solutions))

    for point in discontinuities:
        if intervalo_set.contains(point):
            return False
    return True


def biseccion(
    func_str: str,
    intervalo: tuple[Fraction, Fraction],
    error: Fraction = MARGEN_ERROR
) -> Union[bool, tuple[Fraction, Fraction, int]]:

    a, b = intervalo
    x = symbols("x")
    parsed_func: Expr = parse_expr(func_str, transformations=TRANSFORMS)
    f = lambdify(x, parsed_func)

    if not es_continua(parsed_func, x, intervalo):
        return False

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
        elif f_a * f_c < 0:
            b = c
        elif f_b * f_c < 0:
            a = c
        if i == MAX_ITERACIONES:
            return (c, f_c, -1)


def newton(
    func_str: str,
    xi: Fraction,
    error: Fraction = MARGEN_ERROR,
    max_its: int = MAX_ITERACIONES
) -> Union[tuple[Fraction, Fraction, int, bool]]:

    x = symbols("x")
    parsed_func: Expr = parse_expr(func_str, transformations=TRANSFORMS)

    f = lambdify(x, parsed_func)
    f_prima = lambdify(x, diff(parsed_func, x))

    fxi = f(float(xi))
    if abs(fxi) < error:
        return (xi, fxi, 1, False)

    for i in range(2, max_its + 1):
        fxi = f(float(xi))
        fxi_prima = f_prima(float(xi))

        if fxi_prima == 0:
            return (xi, fxi, i, True)

        xi -= fxi / fxi_prima
        fxi = f(float(xi))
        if abs(fxi) < error:
            return (xi, fxi, i, False)
    return (xi, fxi, max_its, False)
