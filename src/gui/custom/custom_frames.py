"""
Implementaciones de frames personalizados.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTkImage, CTkLabel

from src.utils import CHECK_ICON, ERROR_ICON

if TYPE_CHECKING:
    from .adapted import CustomScrollFrame


class ErrorFrame(CTkFrame):
    """
    Frame personalizado para mostrar mensajes de error.
    """

    def __init__(
        self,
        master: CTkFrame | CustomScrollFrame,
        msg: str | None,
    ) -> None:
        """
        Personalizar diseño de frame, inicializar widget con mensaje.

        Args:
            master: Widget que contiene este frame.
            msg:    Mensaje a colocar en frame.

        """

        super().__init__(
            master,
            border_width=2,
            border_color="#ff3131",
            fg_color="transparent",
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.error_icon_label = CTkLabel(self, text="", image=ERROR_ICON)
        self.error_icon_label.grid(
            row=0,
            column=0,
            padx=(15, 10),
            pady=10,
            sticky="nse",
        )

        if msg is not None:
            self.mensaje_error = CTkLabel(self, text=msg)
            self.mensaje_error.grid(
                row=0,
                column=1,
                padx=(10, 15),
                pady=10,
                sticky="nsw",
            )


class SuccessFrame(CTkFrame):
    """
    Frame personalizado para mostrar mensajes de éxito.
    """

    def __init__(
        self,
        master: CTkFrame | CustomScrollFrame,
        msg: str | None,
    ) -> None:
        """
        Personalizar diseño de frame, inicializar widget con mensaje.

        Args:
            master: Widget que contiene este frame.
            msg:    Mensaje a colocar en frame.

        """

        super().__init__(
            master,
            border_width=2,
            border_color="#18c026",
            fg_color="transparent",
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.check_icon_label = CTkLabel(self, text="", image=CHECK_ICON)
        self.check_icon_label.grid(
            row=0,
            column=0,
            padx=(15, 10),
            pady=10,
            sticky="nse",
        )

        if msg is not None:
            self.mensaje_exito = CTkLabel(self, text=msg)
            self.mensaje_exito.grid(
                row=0,
                column=1,
                padx=(10, 15),
                pady=10,
                sticky="nsw",
            )


class ResultadoFrame(CTkFrame):
    """
    Frame personalizado para mostrar resultados de operaciones.
    """

    def __init__(
        self,
        master: CTkFrame | CustomScrollFrame,
        msg: str | None = None,
        img: CTkImage | None = None,
        border_color: str | None = None,
    ) -> None:
        """
        Personalizar diseño de frame, inicializar widget con mensaje o imagen.

        Args:
            master:       Widget que contiene este frame.
            msg:          Mensaje a colocar en frame.
            img:          Imagen a colocar en frame.
            border_color: Color de borde del frame.

        Raises:
            ValueError: Si `msg is not None and img is not None` es `True`.

        """

        if border_color is None:
            border_color = "#18c026"

        super().__init__(
            master,
            border_width=2,
            border_color=border_color,
            fg_color="transparent",
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.msg_label: CTkLabel | None = None
        self.img_label: CTkLabel | None = None

        if msg is not None and img is not None:
            raise ValueError(
                "No se puede mostrar un mensaje e una imagen al mismo tiempo.",
            )

        if msg is not None:
            self.msg_label = CTkLabel(self, text=msg)
            self.msg_label.grid(row=0, column=0, padx=20, pady=10)
        elif img is not None:
            self.img_label = CTkLabel(self, text="", image=img)
            self.img_label.grid(row=0, column=0, padx=10, pady=10)
