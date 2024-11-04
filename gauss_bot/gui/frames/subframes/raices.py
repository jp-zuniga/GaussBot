"""
Implementación de RaciesFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

from io import BytesIO
from matplotlib.pyplot import (
    axis,
    close,
    rc,
    savefig,
    subplots,
    text,
)

from typing import TYPE_CHECKING

from PIL.Image import (
    LANCZOS,
    open as open_img,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
)

from gauss_bot.gui.custom_frames import (
    CustomImageDropdown,
    CustomScrollFrame,
    ErrorFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI
    from gauss_bot.gui.frames.ecuaciones import EcuacionesFrame


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
        self.columnconfigure(1, weight=1)

        terminos_label = ctkLabel(self, text="¿Cuántos términos tendrá la función?")
        self.terminos_entry = ctkEntry(self, width=60, placeholder_text="3")
        ingresar_button = ctkButton(
            self, text="Ingresar términos", command=self.setup_terminos_frame
        )

        self.terminos_entry.bind("<Return>", lambda _: self.setup_terminos_frame())
        self.option_menus: list[CustomImageDropdown] = []

        self.terminos_frame = ctkFrame(self)
        self.func_output = ctkFrame(self)

        terminos_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.terminos_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ingresar_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.terminos_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="n")

    def setup_terminos_frame(self):
        for widget in self.terminos_frame.winfo_children():
            widget.destroy()

        try:
            num_terminos = int(self.terminos_entry.get())
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos para la cantidad de términos!"
            )
            self.mensaje_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        for i in range(num_terminos):
            label = ctkLabel(self.terminos_frame, text=f"Término {i + 1}:")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            option_menu = CustomImageDropdown(
                self.terminos_frame,
                button_text="",
            )

            option_menu.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            self.option_menus.append(option_menu)

        self.func_output.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="n")

    def latex_to_png(latex_str, output_file):
        rc("text", usetex=True)
        rc("font", family="serif")
        fig, ax = subplots(figsize=(4, 4))

        axis("off")
        text(
            0.5,
            0.5,
            f"${latex_str}$",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=100,
        )

        savefig(
            output_file,
            format="png",
            dpi=300,
            transparent=True,
            bbox_inches="tight",
            pad_inches=0,
        )

        close(fig)

    def render_function(self, function_str: str):
        fig, ax = subplots()
        text(0.5, 0.5, f"${function_str}$", fontsize=20, ha='center', va='center')
        axis('off')

        buf = BytesIO()
        savefig(buf, format='png')
        buf.seek(0)

        close(fig)
        self.display_function_image(buf)

    def display_function_image(self, buf: BytesIO):
        image = open_img(buf)
        image = image.resize((400, 300), LANCZOS)
        photo = ctkImage(image)

        label = ctkLabel(self.func_output, image=photo)
        label._image = photo
        label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

    def update_function(self) -> None: ...
    #     terms = [var.get() for var in self.option_menus]
    #     function_str = "f(x) = " + " + ".join(terms)
    #     self.render_function(function_str)

    def update_frame(self):
        self.update_scrollbar_visibility()
        self.update_idletasks()
