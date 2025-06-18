"""
Implementaciones de frames personalizados.
"""

from typing import Any, Optional, Union

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkScrollableFrame as ctkScrollFrame,
)

from ...utils import CHECK_ICON, ERROR_ICON


class CustomScrollFrame(ctkScrollFrame):
    """
    Subclass de CTkScrollableFrame
    con la scrollbar escondida.
    """

    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._scrollbar.grid_forget()


class ErrorFrame(ctkFrame):
    """
    Frame personalizado para mostrar mensajes de error.
    """

    def __init__(
        self, master: Union[ctkFrame, CustomScrollFrame], msg: Optional[str]
    ) -> None:
        super().__init__(
            master,
            corner_radius=8,
            border_width=2,
            border_color="#ff3131",
            fg_color="transparent",
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.error_icon_label = ctkLabel(self, text="", image=ERROR_ICON)
        self.error_icon_label.grid(
            row=0, column=0, padx=(15, 10), pady=10, sticky="nse"
        )

        if msg is not None:
            self.mensaje_error = ctkLabel(self, text=msg)
            self.mensaje_error.grid(
                row=0, column=1, padx=(10, 15), pady=10, sticky="nsw"
            )

    def destroy(self) -> None:
        self.forget()
        super().destroy()


class SuccessFrame(ctkFrame):
    """
    Frame personalizado para mostrar mensajes de éxito.
    """

    def __init__(
        self, master: Union[ctkFrame, CustomScrollFrame], msg: Optional[str]
    ) -> None:
        super().__init__(
            master,
            corner_radius=8,
            border_width=2,
            border_color="#18c026",
            fg_color="transparent",
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.check_icon_label = ctkLabel(self, text="", image=CHECK_ICON)
        self.check_icon_label.grid(
            row=0, column=0, padx=(15, 10), pady=10, sticky="nse"
        )

        if msg is not None:
            self.mensaje_exito = ctkLabel(self, text=msg)
            self.mensaje_exito.grid(
                row=0, column=1, padx=(10, 15), pady=10, sticky="nsw"
            )

    def destroy(self) -> None:
        self.forget()
        super().destroy()


class ResultadoFrame(ctkFrame):
    """
    Frame personalizado para mostrar resultados de operaciones.
    """

    def __init__(
        self,
        master: Union[ctkFrame, CustomScrollFrame],
        msg: Optional[str] = None,
        img: Optional[ctkImage] = None,
        border_color: Optional[str] = None,
    ) -> None:
        if border_color is None:
            border_color = "#18c026"

        super().__init__(
            master,
            corner_radius=8,
            border_width=2,
            border_color=border_color,
            fg_color="transparent",
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.msg_label: Optional[ctkLabel] = None
        self.img_label: Optional[ctkLabel] = None

        if msg is not None and img is not None:
            raise ValueError("No se pueden mostrar mensaje e imagen al mismo tiempo!")

        if msg is not None:
            self.msg_label = ctkLabel(self, text=msg)
            self.msg_label.grid(row=0, column=0, padx=20, pady=10)  # type: ignore
        elif img is not None:
            self.img_label = ctkLabel(self, text="", image=img)
            self.img_label.grid(row=0, column=0, padx=10, pady=10)  # type: ignore
        else:
            raise ValueError(
                "Se necesita un mensaje o una imagen para mostrar en el frame!"
            )

    def destroy(self) -> None:
        self.forget()
        super().destroy()
