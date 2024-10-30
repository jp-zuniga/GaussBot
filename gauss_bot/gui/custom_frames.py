"""
Implementación de frames personalizados para
mostrar diferentes tipos de mensajes al usuario.
"""

from os import path
from typing import Union

from PIL import Image
from customtkinter import (
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkScrollableFrame as ctkScrollFrame,
)

from gauss_bot import ASSET_PATH

class ErrorFrame(ctkFrame):
    """
    Frame personalizado para mostrar mensajes de error.
    """

    def __init__(self, parent: Union[ctkFrame, ctkScrollFrame], message: str) -> None:
        super().__init__(parent, corner_radius=8, border_width=2, border_color="#ff3131")

        self.error_icon = ctkImage(Image.open(path.join(ASSET_PATH, "error_icon.png")))
        self.error_icon_label = ctkLabel(self, text="", image=self.error_icon)
        self.mensaje_error = ctkLabel(self, text=message)

        self.error_icon_label.grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")
        self.mensaje_error.grid(row=0, column=1, padx=(5, 15), pady=10, sticky="e")

    def destroy(self) -> None:
        self.forget()
        super().destroy()


class SuccessFrame(ctkFrame):
    """
    Frame personalizado para mostrar mensajes de éxito.
    """

    def __init__(self, parent: Union[ctkFrame, ctkScrollFrame], message: str) -> None:
        super().__init__(parent, corner_radius=8, border_width=2, border_color="#18c026")

        self.check_icon = ctkImage(Image.open(path.join(ASSET_PATH, "check_icon.png")))
        self.check_icon_label = ctkLabel(self, text="", image=self.check_icon)
        self.mensaje_exito = ctkLabel(self, text=message)

        self.check_icon_label.grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")
        self.mensaje_exito.grid(row=0, column=1, padx=(5, 15), pady=10, sticky="e")

    def destroy(self) -> None:
        self.forget()
        super().destroy()


class ResultadoFrame(ctkFrame):
    """
    Frame personalizado para mostrar resultados de operaciones.
    """

    def __init__(self, parent: Union[ctkFrame, ctkScrollFrame],
                 header: str, resultado: str, solo_header=False) -> None:

        super().__init__(parent, corner_radius=8, border_width=2, border_color="#18c026")

        pady_tuple = (10, 10) if solo_header else (10, 3)
        self.header = ctkLabel(self, text=header)
        self.header.grid(row=0, column=0, padx=20, pady=pady_tuple, sticky="n")

        if not solo_header:
            self.resultado = ctkLabel(self, text=resultado)
            self.resultado.grid(row=1, column=0, padx=20, pady=(3, 10), sticky="n")

    def destroy(self) -> None:
        self.forget()
        super().destroy()
