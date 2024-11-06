"""
Implementación de RaicesFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

from random import randint
from os import path
from typing import (
    TYPE_CHECKING,
    Optional,
)

from PIL.Image import open as open_img

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

        enter_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_enter_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_enter_icon.png")),
            size=(18, 18),
        )

        terminos_label = ctkLabel(self, text="¿Cuántos términos tendrá la función?")
        self.terminos_entry = ctkEntry(self, width=60, placeholder_text="3")
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

        self.selectors: list[CustomImageDropdown] = []
        self.signos: list[CustomDropdown] = []
        self.arg_entries: list[ctkEntry] = []
        self.func = ""

        self.mensaje_frame: Optional[ctkFrame] = None

        self.func_frame: ResultadoFrame
        self.terminos_frame = ctkFrame(self)
        self.terminos_frame.columnconfigure(0, weight=1)
        self.terminos_frame.columnconfigure(1, weight=1)

        self.terminos_entry.bind("<Return>", lambda _: self.setup_terminos_frame())

        terminos_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")
        self.terminos_entry.grid(row=0, column=1, padx=5, pady=5, sticky="new")
        ingresar_button.grid(row=0, column=2, ipady=3, pady=5, sticky="nw")

    def setup_terminos_frame(self) -> None:
        for widget in self.terminos_frame.winfo_children():
            widget.destroy()

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

        fx = resize_image(FUNCTIONS["f(x)"], (3, 7))
        fx_label = ctkLabel(
            self.terminos_frame,
            width=120,
            corner_radius=10,
            image=fx,
            text="",
            fg_color=self.master_frame.tabview._segmented_button.cget("unselected_color"),
        )

        fx_label.grid(row=0, column=0, columnspan=3, padx=5, ipady=5, pady=5, sticky="n")

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

            signo.grid(row=i + 1, column=0, padx=10, pady=10, sticky="ne")
            dropdown.options_button.grid(
                row=i + 1, column=1, columnspan=2, padx=10, pady=10, sticky="nw"
            )

            self.signos.append(signo)
            self.selectors.append(dropdown)
        leer_func_button = ctkButton(
            self.terminos_frame, text="Leer función", command=self.leer_func
        )

        leer_func_button.grid(row=num_terminos + 1, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.terminos_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def extract_func(self, dropdown: CustomImageDropdown, img: ctkImage) -> None:
        func_key = get_dict_key(dropdown.images, img)
        self.crear_arg_entries(dropdown, func_key)  # type: ignore

    def crear_arg_entries(self, dropdown: CustomImageDropdown, func_key: str) -> None:
        row, column = dropdown.options_button.grid_info()["row"], 2
        arg_entry = ctkEntry(
            self.terminos_frame,
            width=100,
            placeholder_text=generate_placeholders(func_key),
        )

        dropdown.options_button.grid(columnspan=1, sticky="new")
        arg_entry.grid(row=row, column=column, padx=10, pady=10, sticky="nw")
        self.bind_entry_keys(arg_entry, row - 1)
        self.arg_entries.append(arg_entry)

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
        input_func = self.leer_arg_entries()
        if input_func.count("sen") > 0:
            input_func = input_func.replace("sen", "sin")
        if input_func.count("^") > 0:
            input_func = input_func.replace("^", "**")

        parsed_func = parse_expr(input_func, transformations=TRANSFORMS)
        self.mostrar_func(parsed_func)

    def mostrar_func(self, parsed_func) -> None:
        latex_func = latex(parsed_func, ln_notation=True)
        latex_func = r"f(x) = " + latex_func
        img = latex_to_png(latex_func, path.join(ASSET_PATH, "func.png"))

        self.func_frame = ResultadoFrame(self, header="", resultado="", solo_header=True)
        self.func_frame.columnconfigure(0, weight=1)

        func_label = ctkLabel(
            self.func_frame,
            image=img,
            text="",
        )

        self.func_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        func_label.grid(row=0, column=0, sticky="n")
        self.update_idletasks()

    def bind_entry_keys(self, entry: ctkEntry, i: int) -> None:
        entry.bind("<Up>", lambda _: self.entry_move_up(i))
        entry.bind("<Down>", lambda _: self.entry_move_down(i))

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


def generate_placeholders(func_key: str) -> str:
    placeholders: dict[str, str] = {
        "k": f"{randint(-10, 10)}",
        "x^n": f"x^{randint(-10, 10)}",
        "b^x": f"{randint(-10, 10)}^x",
        "e^x": f"e^{randint(-10, 10)}x",
        "ln(x)": f"ln({randint(2, 10)}x)",
        "log-b(x)": f"log_{randint(2, 9)}({randint(2, 9)}x)",
        "sen(x)": f"sen({randint(-9, 9)}x) - {randint(1, 9)}",
        "cos(x)": f"cos({randint(-9, 9)}x + {randint(1, 9)})",
        "tan(x)": f"tan({randint(-9, 9)}x - {randint(1, 9)})",
    }

    return placeholders[func_key]


def latex_to_png(latex_str: str, output_file: str) -> ctkImage:
    rc("text", usetex=True)
    rc("font", family="serif")
    fig, _ = subplots(figsize=(20, 10))

    axis("off")
    text(
        0.5,
        1.0,
        f"${latex_str}$",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=100,
    )

    savefig(
        output_file,
        format="png",
        transparent=True,
        pad_inches=1.0,
        dpi=200,
    )

    close(fig)
    return ctkImage(
        dark_image=open_img(output_file),
        light_image=open_img(output_file),
        size=(300, 150),
    )
