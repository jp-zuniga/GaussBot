"""
Home frame de la interfaz.
"""

from typing import TYPE_CHECKING
from webbrowser import open as open_link

from customtkinter import CTkFont as ctkFont, CTkFrame as ctkFrame, CTkLabel as ctkLabel

from ..custom import IconButton
from ...utils import (
    ANALISIS_ICON,
    ECUACIONES_ICON,
    INFO_ICON,
    MATRIZ_ICON,
    VECTOR_ICON,
    generate_sep,
)

if TYPE_CHECKING:
    from .. import GaussUI


class HomeFrame(ctkFrame):
    """
    Pantalla de bienvenida de la aplicación.
    """

    def __init__(self, app: "GaussUI", master: "GaussUI") -> None:
        from ... import __version__

        super().__init__(master, corner_radius=0)
        self.app = app

        # centrar widgets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)

        ctkLabel(
            self, text="¡Bienvenido a GaussBot!", font=ctkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="s")

        ctkLabel(
            self,
            text="GaussBot es una aplicación para realizar cálculos matemáticos como:\n"
            + "− Operaciones con matrices y vectores\n"
            + "− Resolución de sistemas de ecuaciones\n"
            + "− Análisis númerico",
        ).grid(row=1, column=0, columnspan=2, pady=0, sticky="s")

        ctkLabel(self, text="", image=generate_sep(False, (600, 8))).grid(
            row=2, column=0, columnspan=2, pady=10, sticky="s"
        )

        IconButton(
            self,
            app=self.app,
            height=40,
            image=MATRIZ_ICON,
            text="Operaciones de Matrices",
            text_color=self.app.theme_config["CTkLabel"]["text_color"],
            tooltip_text="Suma, resta, multiplicación,"
            + "\ntransposición, calcular determinante,"
            + "\nencontrar inversa.",
            command=lambda: self.ir_a_frame("matrices"),
        ).grid(row=3, column=0, padx=(10, 5), pady=(10, 3), sticky="se")

        IconButton(
            self,
            app=self.app,
            height=40,
            image=VECTOR_ICON,
            text="Operaciones de Vectores",
            text_color=self.app.theme_config["CTkLabel"]["text_color"],
            tooltip_text="Magnitud, suma, resta,"
            + "\nmultiplicación escalar,"
            + "\nproducto punto, producto cruz.",
            command=lambda: self.ir_a_frame("vectores"),
        ).grid(row=3, column=1, padx=(5, 10), pady=(10, 3), sticky="sw")

        IconButton(
            self,
            app=self.app,
            height=40,
            image=ANALISIS_ICON,
            text="Análisis Númerico",
            text_color=self.app.theme_config["CTkLabel"]["text_color"],
            tooltip_text="Raíces de funciones, derivadas, integrales.",
            command=lambda: self.ir_a_frame("analisis"),
        ).grid(row=4, column=0, padx=(10, 5), pady=3, sticky="ne")

        IconButton(
            self,
            app=self.app,
            height=40,
            image=ECUACIONES_ICON,
            text="Sistemas de Ecuaciones",
            text_color=self.app.theme_config["CTkLabel"]["text_color"],
            tooltip_text="Resolver sistemas de ecuaciones por los métodos de:"
            + "\n− Gauss-Jordan"
            + "\n− Regla de Cramer",
            command=lambda: self.ir_a_frame("sistemas"),
        ).grid(row=4, column=1, padx=(5, 10), pady=3, sticky="nw")

        IconButton(
            self,
            app=self.app,
            height=30,
            image=INFO_ICON,
            tooltip_text="− Desarrollado y diseñado por: Joaquín Zúñiga\n"
            + f"− Versión: {__version__}",
            command=lambda: open_link(
                "https://github.com/jp-zuniga/GaussBot", autoraise=False
            ),
        ).grid(row=5, column=0, columnspan=2, padx=10, pady=(3, 10), sticky="n")

    def ir_a_frame(self, frame: str) -> None:
        """
        Selecciona un frame de la aplicación.
        """

        self.app.nav_frame.seleccionar_frame(frame)

    def update_frame(self) -> None:
        """
        Configura los backgrounds de los widgets,
        por si hubo un cambio de tema.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
            if isinstance(widget, IconButton) and widget.tooltip is not None:
                widget.tooltip.configure_tooltip(
                    bg_color=self.app.theme_config["CTkFrame"]["fg_color"]
                )
