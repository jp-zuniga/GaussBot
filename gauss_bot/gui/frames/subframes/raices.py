"""
Implementación de RaicesFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

from fractions import Fraction
from random import choice
from os import path
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from PIL.ImageOps import invert
from PIL.Image import (
    Image,
    merge,
    open as open_img,
)

from tkinter import TclError
from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
)

from matplotlib.pyplot import (
    axis, close,
    rc, savefig,
    subplots, text,
)

from sympy import (
    And, Expr, FiniteSet,
    Interval, log, Set,
    Symbol, Pow,
    lambdify, latex,
    parse_expr, solve,
    sqrt, symbols,
)

from sympy.parsing.sympy_parser import (
    standard_transformations,
    implicit_multiplication_application,
)

from gauss_bot import (
    ASSET_PATH,
    DATA_PATH,
    FUNCTIONS,
    get_dict_key,
    resize_image,
)

from gauss_bot.gui.custom import (
    CustomDropdown,
    FuncDropdown,
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import EcuacionesFrame

TRANSFORMS = (standard_transformations + (implicit_multiplication_application,))
MARGEN_ERROR = Fraction(1, 1000000)
MAX_ITERACIONES = 1000


class RaicesFrame(CustomScrollFrame):
    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "EcuacionesFrame"
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.dropup_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_dropup_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_dropup_icon.png")),
            size=(18, 18),
        )

        self.dropdown_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_dropdown_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_dropdown_icon.png")),
            size=(18, 18),
        )

        self.selectors: list[FuncDropdown] = []
        self.signos: list[CustomDropdown] = []
        self.arg_entries: list[ctkEntry] = []
        self.func = ""

        self.a_entry: ctkEntry
        self.b_entry: ctkEntry
        self.error_entry: ctkEntry

        self.collapse_button: Optional[ctkButton] = None
        self.mensaje_frame: Optional[ctkFrame] = None
        self.collapsed_terminos = True

        self.terminos_frame = ctkFrame(self)
        self.func_frame = ctkFrame(self)
        self.calc_frame = ctkFrame(self)

        terminos_label = ctkLabel(self, text="¿Cuántos términos tendrá la función?")
        self.terminos_entry = ctkEntry(self, width=30, placeholder_text="3")
        self.terminos_entry.bind("<Return>", lambda _: self.setup_terminos_frame())

        enter_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_enter_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_enter_icon.png")),
            size=(18, 18),
        )

        ingresar_button = ctkButton(
            self,
            width=20,
            height=20,
            border_width=0,
            border_spacing=0,
            image=enter_icon,
            fg_color="transparent",
            bg_color="transparent",
            hover_color=self.app.theme_config["CTkFrame"]["top_fg_color"],
            text="",
            command=self.setup_terminos_frame,
        )

        terminos_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")
        self.terminos_entry.grid(row=0, column=1, padx=5, pady=5, sticky="new")
        ingresar_button.grid(row=0, column=2, ipady=3, pady=5, sticky="nw")

    def toggle_terminos_frame(self) -> None:
        if self.collapsed_terminos:
            self.terminos_frame.grid()
            if self.collapse_button is not None:
                self.collapse_button.configure(image=self.dropup_icon)
        else:
            self.terminos_frame.grid_remove()
            if self.collapse_button is not None:
                self.collapse_button.configure(image=self.dropdown_icon)
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

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.func_frame.grid_remove()
        self.calc_frame.grid_remove()
        self.signos.clear()
        self.selectors.clear()
        self.arg_entries.clear()
        self.func = ""

        try:
            num_terminos = int(self.terminos_entry.get())
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos para la cantidad de términos!"
            )
            self.mensaje_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        sep_icon = ctkImage(
            dark_image=open_img(
                path.join(ASSET_PATH, "light_hseparator.png")
            ),
            light_image=open_img(
                path.join(ASSET_PATH, "dark_hseparator.png")
            ),
            size=(300, 20),
        )

        sep1 = ctkLabel(
            self.terminos_frame,
            image=sep_icon,
            text="",
        )

        sep2 = ctkLabel(
            self.terminos_frame,
            image=sep_icon,
            text="",
        )

        fx = resize_image(FUNCTIONS["f(x)"], (3, 7))
        fx_label = ctkLabel(
            self.terminos_frame,
            corner_radius=10,
            image=fx,
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
            placeholder_text=generate_placeholders(func_key),
        )

        self.arg_entries.append(arg_entry)
        self.bind_entry_keys(arg_entry, len(self.arg_entries) - 1)
        dropdown.options_button.grid(columnspan=1, sticky="new")
        arg_entry.grid(row=row, column=column, padx=5, pady=5, sticky="nw")

    def leer_arg_entries(self) -> str:
        func = ""
        print(self.signos)
        print(self.arg_entries)
        for sig_entry, arg_entry in zip(self.signos, self.arg_entries):
            signo = sig_entry.get()
            arg = arg_entry.get()
            print("what the fuck", arg)
            if "+" not in arg or "−" not in arg:
                arg = f"+{arg}"

            signos_iguales = (
                arg[0] == "+" and signo == "+" or
                arg[0] == "-" and signo == "−"
            )

            signos_distintos = (
                arg[0] == "+" and signo == "−" or
                arg[0] == "-" and signo == "+"
            )

            if signos_iguales:
                func += f"+{arg[1:]}"
            elif signos_distintos:
                func += f"-{arg[1:]}"
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

        if self.mensaje_frame is not None:
            try:
                self.mensaje_frame.destroy()
            except TclError:
                pass
            self.mensaje_frame = None

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

        self.collapse_button = ctkButton(
            self,
            width=20,
            height=20,
            border_width=0,
            border_spacing=0,
            image=self.dropup_icon,
            fg_color="transparent",
            bg_color="transparent",
            hover_color=self.app.theme_config["CTkFrame"]["top_fg_color"],
            text="",
            command=self.toggle_terminos_frame,
        )

        self.collapse_button.grid(row=2, column=0, columnspan=3, padx=5, sticky="n")
        self.func_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=1, sticky="n")
        func_label.grid(row=0, column=0, padx=5, pady=5)
        self.update_idletasks()
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

        encontrar_label = ctkLabel(
            self.calc_frame, text="Encontrar las raíces de f(x) entre:"
        )

        self.a_entry = ctkEntry(self.calc_frame, width=40, placeholder_text="-10")
        and_label = ctkLabel(self.calc_frame, text="y")
        self.b_entry = ctkEntry(self.calc_frame, width=40, placeholder_text="10")

        error_label = ctkLabel(self.calc_frame, text="con un margen de error de:")
        self.error_entry = ctkEntry(self.calc_frame, width=80)
        self.error_entry.insert(0, f"{float(MARGEN_ERROR):.6f}")

        self.a_entry.bind("<Right>", lambda _: self.b_entry.focus_set())
        self.b_entry.bind("<Left>", lambda _: self.a_entry.focus_set())
        self.a_entry.bind("<Return>", lambda _: self.encontrar_raiz())
        self.b_entry.bind("<Return>", lambda _: self.encontrar_raiz())

        calc_button = ctkButton(
            self.calc_frame,
            text="Calcular por método de bisección",
            command=self.encontrar_raiz
        )

        encontrar_label.grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ne")
        self.a_entry.grid(row=0, column=1, padx=5, pady=(5, 2), sticky="ne")
        and_label.grid(row=0, column=2, padx=5, pady=(5, 2), sticky="nw")
        self.b_entry.grid(row=0, column=3, padx=5, pady=(5, 2), sticky="nw")
        error_label.grid(row=1, column=0, padx=5, pady=(2, 5), sticky="ne")
        self.error_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=(2, 5), sticky="nw")
        calc_button.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def encontrar_raiz(self) -> None:
        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            a = Fraction(self.a_entry.get())
            b = Fraction(self.b_entry.get())
            error = Fraction(self.error_entry.get())
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números reales para el intervalo/margen de error!"
            )
            self.mensaje_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        resultado = biseccion(self.func, (a, b), margen_e=error)
        if resultado is False:
            self.mensaje_frame = ErrorFrame(
                self, f"La función no es continua en el intervalo [{a}, {b}]!"
            )
            self.mensaje_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return
        elif resultado is True:
            self.mensaje_frame = ErrorFrame(
                self, f"La función no cambia de signo en el intervalo [{a}, {b}]!"
            )
            self.mensaje_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        x, f_x, i = resultado
        x = Fraction(x).limit_denominator()
        f_x = Fraction(f_x).limit_denominator()

        error_str = r"\textnormal{Margen de error: }" + rf"{float(error):.6f}"
        x_igual = rf"x = {float(x):6f}"
        f_x_igual = rf"f({float(x):6f}) = {float(f_x):6f}"

        func_img = latex_to_png(
            latex_str= rf"{error_str}" +
                       r"\\[1em]" +
                       rf"{x_igual}" +
                       r"\\[1em]" +
                       rf"{f_x_igual}",
            output_file=path.join(DATA_PATH, "func.png"),
            font_size=60,
        )

        if i == -1:
            self.mensaje_frame = ResultadoFrame(
                self, solo_header=True, resultado="",
                header=f"Despues de {MAX_ITERACIONES} iteraciones, no se encontró " +
                       f"una raíz dentro del margen de error {float(error):.6f}!\n" +
                        "Raíz aproximada encontrada:",
                border_color="#ff3131",
            )

            img_label = ctkLabel(self.mensaje_frame, text="", image=func_img)
            img_label.grid(row=1, column=0, padx=20, pady=(3, 10), sticky="n")
            self.mensaje_frame.grid(
                row=5,
                column=0,
                columnspan=3,
                ipadx=10,
                ipady=10,
                padx=5,
                pady=5,
                sticky="n",
            )
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self, header="", resultado="", solo_header=True
        )

        self.mensaje_frame.columnconfigure(0, weight=1)
        img_label = ctkLabel(self.mensaje_frame, text="", image=func_img)
        tipo_raiz = "" if x == 0 else "aproximada "

        interpretacion_label = ctkLabel(
            self,
            text=f"El metodo de bisección converge despues de {i} iteraciones!\n" +
                 f"Raíz {tipo_raiz}encontrada: ",
        )

        interpretacion_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        img_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.mensaje_frame.grid(
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
        self.update_scrollbar_visibility()
        self.update_idletasks()


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
    margen_e: Fraction = MARGEN_ERROR
) -> Union[bool, tuple[Fraction, Fraction, int]]:

    a, b = intervalo
    x = symbols("x", real=True)
    parsed_func: Expr = parse_expr(func_str, transformations=TRANSFORMS)
    f = lambdify(x, parsed_func)

    if not es_continua(parsed_func, x, intervalo):
        return False

    f_a = f(float(a))
    f_b = f(float(b))
    if f_a * f_b > 0:
        return True

    i = 0
    while True:
        i += 1
        c = (a + b) / 2
        f_c = f(float(c))
        if f_c == 0 or abs(f_c) < margen_e:
            return (c, f_c, i)
        elif f_a * f_c < 0:
            b = c
        elif f_b * f_c < 0:
            a = c
        if i == MAX_ITERACIONES:
            return (c, f_c, -1)


def valid_rand(start: int, end: int) -> list[int]:
    valid = list(range(start + 1, end))
    try:
        valid.remove(0)
        valid.remove(1)
    except ValueError:
        pass
    return valid


def generate_placeholders(func_key: str) -> str:
    placeholders: dict[str, str] = {
        "k": f"{choice(valid_rand(-10, 10))}",
        "x^n": f"x^{choice(valid_rand(-10, 10))}",
        "b^x": f"{choice(valid_rand(-10, 10))}^x",
        "e^x": f"e^{choice(valid_rand(-10, 10))}x",
        "ln(x)": f"ln({choice(valid_rand(1, 10))}x)",
        "log-b(x)": f"log_{choice(valid_rand(1, 10))}({choice(valid_rand(1, 10))}x)",
        "sen(x)": f"sen({choice(valid_rand(-10, 10))}x)-{choice(valid_rand(1, 10))}",
        "cos(x)": f"cos({choice(valid_rand(-10, 10))}x+{choice(valid_rand(1, 10))})",
        "tan(x)": f"tan({choice(valid_rand(-10, 10))}x-{choice(valid_rand(1, 10))})",
    }

    return placeholders[func_key]


def latexify_frac(frac: str) -> str:
    if "/" in frac:
        a, b = frac.split("/")
        return rf"\frac{{{a}}}{{{b}}}"
    return frac


def latex_to_png(latex_str: str, output_file: str, font_size: int = 75) -> ctkImage:
    rc("text", usetex=True)
    rc("font", family="serif")

    fig_length = 12 + (len(latex_str) // 10)
    fig_height = 2 if r"\\" not in latex_str else 2 + int(latex_str.count(r"\\") * 2)
    img_length = fig_length * 22
    img_height = fig_height * 22

    fig, _ = subplots(figsize=(fig_length, fig_height))
    axis("off")
    text(
        0.5,
        0.5,
        f"${latex_str}$",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=font_size,
    )

    savefig(
        output_file,
        format="png",
        transparent=True,
        pad_inches=0.5,
        dpi=200,
    )

    close(fig)

    img = open_img(output_file)
    img_inverted = transparent_invert(img)
    return ctkImage(
        dark_image=img_inverted,
        light_image=img,
        size=(img_length, img_height),
    )


def transparent_invert(img: Image) -> Image:
    r, g, b, a = img.split()
    rgb_inverted = invert(merge("RGB", (r, g, b)))
    return merge("RGBA", (*rgb_inverted.split(), a))
