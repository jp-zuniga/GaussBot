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
)

from PIL.ImageOps import invert
from PIL.Image import (
    Image,
    merge,
    open as open_img,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
)

from matplotlib.pyplot import (
    axis,
    close,
    rc,
    savefig,
    subplots,
    text,
)

from sympy import (
    latex,
    parse_expr,
)

from sympy.parsing.sympy_parser import (
    standard_transformations,
    implicit_multiplication_application,
)

from gauss_bot import (
    ASSET_PATH,
    FUNCTIONS,
    get_dict_key,
)

from gauss_bot.gui.custom.custom_widgets import (
    CustomDropdown,
    CustomImageDropdown,
    resize_image,
)

from gauss_bot.gui.custom.custom_frames import (
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI
    from gauss_bot.gui.frames.ecuaciones import EcuacionesFrame


TRANSFORMS = (standard_transformations + (implicit_multiplication_application,))

MARGEN_ERROR = Fraction(1e-6)


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

        self.selectors: list[CustomImageDropdown] = []
        self.signos: list[CustomDropdown] = []
        self.arg_entries: list[ctkEntry] = []
        self.func = ""

        self.collapse_button: Optional[ctkButton] = None
        self.mensaje_frame: Optional[ctkFrame] = None
        self.collapsed_terminos = True

        self.terminos_frame = ctkFrame(self)
        self.calc_frame = ctkFrame(self)
        self.func_frame = ResultadoFrame(
            self,
            header="",
            resultado="",
            solo_header=True,
            border_color="#18c026"
        )

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
            self.update_scrollbar_visibility()
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
            fg_color=self.master_frame.tabview._segmented_button.cget("unselected_color"),
        )

        sep1.grid(row=0, column=0, columnspan=3, sticky="n")
        fx_label.grid(row=1, column=0, columnspan=3, padx=5, ipady=5, pady=5, sticky="n")

        for i in range(num_terminos):
            signo = CustomDropdown(
                self.terminos_frame,
                width=60,
                values=["+", "-"],
                font=("Roboto", 18),
                dropdown_font=("Roboto", 18),
                dynamic_resizing=False,
            )

            dropdown = CustomImageDropdown(
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

        self.terminos_frame.grid(row=1, column=0, columnspan=3, sticky="n")
        leer_func_button.grid(row=num_terminos + 2, column=0, columnspan=3, pady=5, sticky="n")
        sep2.grid(row=num_terminos + 3, column=0, columnspan=3, sticky="n")
        self.collapsed_terminos = False

    def extract_func(self, dropdown: CustomImageDropdown, img: ctkImage) -> None:
        func_key = get_dict_key(dropdown.images, img)
        self.crear_arg_entry(dropdown, func_key)  # type: ignore

    def crear_arg_entry(self, dropdown: CustomImageDropdown, func_key: str) -> None:
        row, column = dropdown.options_button.grid_info()["row"], 2
        arg_entry = ctkEntry(
            self.terminos_frame,
            width=80,
            placeholder_text=generate_placeholders(func_key),
        )

        self.arg_entries.append(arg_entry)
        self.bind_entry_keys(arg_entry, row)
        dropdown.options_button.grid(columnspan=1, sticky="new")
        arg_entry.grid(row=row, column=column, padx=5, pady=5, sticky="nw")

    def leer_arg_entries(self) -> str:
        func = ""
        for sig_entry, arg_entry in zip(self.signos, self.arg_entries):
            signo = sig_entry.get()
            arg = arg_entry.get()
            if arg[0] not in ("+", "-"):
                arg = f"+{arg}"

            signos_iguales = (
                arg[0] == "+" and signo == "+" or
                arg[0] == "-" and signo == "-"
            )

            signos_distintos = (
                arg[0] == "+" and signo == "-" or
                arg[0] == "-" and signo == "+"
            )

            if signos_iguales:
                func += f"+{arg[1:]}"
            elif signos_distintos:
                func += f"-{arg[1:]}"
        return func

    def leer_func(self) -> None:
        self.func = self.leer_arg_entries()
        print(self.func)
        if self.func.count("sen") > 0:
            self.func = self.func.replace("sen", "sin")
        if self.func.count("^") > 0:
            self.func = self.func.replace("^", "**")
        print(self.func)

    def mostrar_func(self) -> None:
        for widget in self.func_frame.winfo_children():
            widget.destroy()
        for widget in self.calc_frame.winfo_children():
            widget.destroy()

        self.func_frame.grid_remove()
        self.calc_frame.grid_remove()
        if self.collapse_button is not None:
            self.collapse_button.destroy()

        self.leer_func()
        parsed_func = parse_expr(self.func, transformations=TRANSFORMS)
        latex_func = latex(parsed_func, ln_notation=True)
        latex_func = r"f(x) = " + latex_func
        img = latex_to_png(latex_func, path.join(ASSET_PATH, "func.png"))

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
        self.calc_frame.columnconfigure(0, weight=1)
        self.calc_frame.columnconfigure(3, weight=1)

        encontrar_label = ctkLabel(
            self.calc_frame, text="Encontrar las raíces de f(x) entre:"
        )

        a_entry = ctkEntry(self.calc_frame, width=40, placeholder_text="-10")
        and_label = ctkLabel(self.calc_frame, text="y")
        b_entry = ctkEntry(self.calc_frame, width=40, placeholder_text="10")

        calc_button = ctkButton(
            self.calc_frame,
            text="Calcular por método de bisección",
            command=lambda: biseccion(
                self.func, Fraction(a_entry.get()), Fraction(b_entry.get())
            ),
        )

        self.calc_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        encontrar_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")
        a_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ne")
        and_label.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        b_entry.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
        calc_button.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def bind_entry_keys(self, entry: ctkEntry, i: int) -> None:
        entry.bind("<Up>", lambda _: self.entry_move_up(i))
        entry.bind("<Down>", lambda _: self.entry_move_down(i))
        entry.bind("<Return>", lambda _: self.mostrar_func())

    def entry_move_up(self, i: int) -> None:
        if i > 0:
            self.arg_entries[i - 1].focus_set()
        else:
            self.arg_entries[-1].focus_set()

    def entry_move_down(self, i: int) -> None:
        if i < len(self.arg_entries) - 1:
            self.arg_entries[i + 1].focus_set()
        else:
            self.arg_entries[0].focus_set()

    def update_frame(self):
        self.update_scrollbar_visibility()
        self.update_idletasks()


def biseccion(
    func_str: str, a: Fraction, b: Fraction, tol: Fraction = MARGEN_ERROR
) -> tuple[Fraction, int]:
    return (Fraction(0), 0)


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


def latex_to_png(latex_str: str, output_file: str) -> ctkImage:
    rc("text", usetex=True)
    rc("font", family="serif")

    fig_length = 12 + (len(latex_str) // 10)
    img_length = fig_length * 22

    fig, _ = subplots(figsize=(fig_length, 2))
    axis("off")
    text(
        0.5,
        0.5,
        f"${latex_str}$",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=75,
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
        size=(img_length, 40),
    )


def transparent_invert(img: Image) -> Image:
    r, g, b, a = img.split()
    rgb_inverted = invert(merge("RGB", (r, g, b)))
    return merge("RGBA", (*rgb_inverted.split(), a))
