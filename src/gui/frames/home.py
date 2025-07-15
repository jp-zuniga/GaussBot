"""
Implementación de pantalla de inicio.
"""

from typing import TYPE_CHECKING
from webbrowser import open as open_link

from customtkinter import CTkFont, CTkFrame, CTkLabel, ThemeManager

from src.gui.custom import IconButton
from src.utils import (
    ANALISIS_ICON,
    ECUACIONES_ICON,
    INFO_ICON,
    MATRIZ_ICON,
    VECTOR_ICON,
    generate_sep,
)

if TYPE_CHECKING:
    from src.gui import GaussUI


class HomeFrame(CTkFrame):
    """
    Pantalla de inicio de la aplicación.
    """

    def __init__(self, app: "GaussUI", master: "GaussUI") -> None:
        """
        Inicializar diseño de pantalla de inicio.
        """

        from src import __version__

        super().__init__(master, corner_radius=0)

        self.app = app

        # centrar widgets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)

        CTkLabel(
            self,
            text="¡Bienvenido a GaussBot!",
            font=CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="s")

        CTkLabel(
            self,
            text="GaussBot es una aplicación para realizar cálculos matemáticos como:\n"
            "− Operaciones con matrices y vectores\n"
            "− Resolución de sistemas de ecuaciones\n"
            "− Análisis númerico",
        ).grid(row=1, column=0, columnspan=2, pady=0, sticky="s")

        CTkLabel(self, text="", image=generate_sep(False, (600, 8))).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10,
            sticky="s",
        )

        IconButton(
            self,
            height=40,
            image=MATRIZ_ICON,
            text="Operaciones de Matrices",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            tooltip_text="Suma, resta, multiplicación,"
            "\ntransposición, calcular determinante,"
            "\nencontrar inversa.",
            tooltip_pady=10,
            command=lambda: self.ir_a_frame("matrices"),
        ).grid(row=3, column=0, padx=(10, 5), pady=(10, 3), sticky="se")

        IconButton(
            self,
            height=40,
            image=VECTOR_ICON,
            text="Operaciones de Vectores",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            tooltip_text="Magnitud, suma, resta,"
            "\nmultiplicación escalar,"
            "\nproducto punto, producto cruz.",
            tooltip_pady=10,
            command=lambda: self.ir_a_frame("vectores"),
        ).grid(row=3, column=1, padx=(5, 10), pady=(10, 3), sticky="sw")

        IconButton(
            self,
            height=40,
            image=ANALISIS_ICON,
            text="Análisis Númerico",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            tooltip_text="Raíces de funciones, derivadas, integrales.",
            command=lambda: self.ir_a_frame("analisis"),
        ).grid(row=4, column=0, padx=(10, 5), pady=3, sticky="ne")

        IconButton(
            self,
            height=40,
            image=ECUACIONES_ICON,
            text="Sistemas de Ecuaciones",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            tooltip_text="Resolver sistemas de ecuaciones por los métodos de:"
            "\n− Gauss-Jordan"
            "\n− Regla de Cramer",
            tooltip_pady=10,
            command=lambda: self.ir_a_frame("sistemas"),
        ).grid(row=4, column=1, padx=(5, 10), pady=3, sticky="nw")

        IconButton(
            self,
            image=INFO_ICON,
            tooltip_text="− Desarrollado y diseñado por: Joaquín Zúñiga\n"
            f"− Versión: {__version__}",
            tooltip_pady=10,
            command=lambda: open_link(
                "https://github.com/jp-zuniga/GaussBot",
                autoraise=False,
            ),
        ).grid(row=5, column=0, columnspan=2, padx=10, pady=(3, 10), sticky="n")

    def ir_a_frame(self, frame: str) -> None:
        """
        Seleccionar un frame de la aplicación.
        """

        self.app.nav_frame.seleccionar_frame(frame)

    def update_frame(self) -> None:
        """
        Actualizar colores de widgets.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
            if isinstance(widget, IconButton) and widget.tooltip is not None:
                widget.tooltip.configure_tooltip(
                    bg_color=ThemeManager.theme["CTkFrame"]["fg_color"],
                )
