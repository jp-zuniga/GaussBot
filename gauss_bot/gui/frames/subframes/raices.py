"""
Implementación de RaciesFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

# from io import BytesIO
from matplotlib.pyplot import (
    axis,
    close,
    rc,
    savefig,
    subplots,
    text,
)

from typing import (
    TYPE_CHECKING,
    Optional,
)

from os import path
from PIL.Image import (
    # LANCZOS,
    open as open_img,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
)

from gauss_bot import (
    ASSET_PATH,
    FUNCTIONS,
)

from gauss_bot.gui.custom.custom_widgets import (
    CustomImageDropdown,
    resize_image,
)

from gauss_bot.gui.custom.custom_frames import (
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
        self.columnconfigure(2, weight=1)
        theme_config = app.theme_config

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
            hover_color=theme_config["CTkFrame"]["top_fg_color"],
            text="",
            command=self.setup_terminos_frame,
        )

        self.selectors: list[CustomImageDropdown] = []
        self.mensaje_frame: Optional[ctkFrame] = None

        self.terminos_frame = ctkFrame(self)
        self.func_output = ctkFrame(self)
        self.terminos_frame.columnconfigure(0, weight=1)
        self.terminos_frame.columnconfigure(2, weight=1)

        self.terminos_entry.bind("<Return>", lambda _: self.setup_terminos_frame())

        terminos_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.terminos_entry.grid(row=0, column=1, padx=5, pady=5, sticky="n")
        ingresar_button.grid(row=0, column=2, ipadx=0, ipady=0, padx=0, pady=0, sticky="w")

    def setup_terminos_frame(self):
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

        fx = resize_image(img=FUNCTIONS["f(x)"], divisors=(3, 7))
        fx_label = ctkLabel(self.terminos_frame, width=120, text="", image=fx)
        fx_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")

        for i in range(num_terminos):
            dropdown = CustomImageDropdown(
                self.terminos_frame,
                button_text="Seleccione una familia de funciones:",
            )

            dropdown.options_button.grid(row=i + 1, column=0, columnspan=3, padx=10, pady=10, sticky="n")
            self.selectors.append(dropdown)
        self.terminos_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.func_output.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="n")

    def update_frame(self):
        self.update_scrollbar_visibility()
        self.update_idletasks()


def latex_to_png(latex_str: str, output_file: str) -> None:
    rc("text", usetex=True)
    rc("font", family="serif")
    fig, _ = subplots(figsize=(4, 4))

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
        pad_inches=0.05,
    )

    close(fig)
