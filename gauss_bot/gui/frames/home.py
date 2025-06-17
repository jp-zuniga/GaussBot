"""
Home frame de la interfaz.
"""

from typing import TYPE_CHECKING
from webbrowser import open as open_link

from customtkinter import (
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from ..custom import IconButton
from ...icons import (
    ABOUT_US_ICON,
    ANALISIS_ICON,
    ECUACIONES_ICON,
    INFO_ICON,
    MATRIZ_ICON,
    VECTOR_ICON,
)
from ...util_funcs import generate_sep

if TYPE_CHECKING:
    from .. import GaussUI


class HomeFrame(ctkFrame):
    """
    Pantalla de bienvenida de la aplicación.
    """

    def __init__(self, app: "GaussUI", master: "GaussUI") -> None:
        super().__init__(master, corner_radius=0)
        self.app = app

        # para centrar widgets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)

        ctkLabel(
            self,
            text="¡Bienvenido a GaussBot!",
            font=ctkFont(
                size=20,
                weight="bold",
            ),
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="s")

        ctkLabel(
            self,
            text="GaussBot es una aplicación para realizar cálculos matemáticos como:\n"
            + "− Operaciones con matrices y vectores\n"
            + "− Resolución de sistemas de ecuaciones\n"
            + "− Análisis númerico",
        ).grid(row=1, column=0, columnspan=2, pady=0, sticky="s")

        ctkLabel(
            self,
            text="",
            image=generate_sep(False, (600, 8)),
        ).grid(row=2, column=0, columnspan=2, pady=10, sticky="s")

        IconButton(
            self,
            app=self.app,
            height=40,
            image=MATRIZ_ICON,
            text="Operaciones de Matrices",
            text_color=self.app.theme_config["CTkLabel"]["text_color"],
            tooltip_text="\nSuma, resta, multiplicación,"
            + "\ntransposición, calcular determinante,"
            + "\nencontrar inversa.\n",
            command=self.ir_a_mats,
        ).grid(row=3, column=0, padx=(10, 5), pady=(10, 3), sticky="se")

        IconButton(
            self,
            app=self.app,
            height=40,
            image=VECTOR_ICON,
            text="Operaciones de Vectores",
            text_color=self.app.theme_config["CTkLabel"]["text_color"],
            tooltip_text="\nMagnitud, suma, resta,"
            + "\nmultiplicación escalar,"
            + "\nproducto punto, producto cruz.\n",
            command=self.ir_a_vecs,
        ).grid(row=3, column=1, padx=(5, 10), pady=(10, 3), sticky="sw")

        IconButton(
            self,
            app=self.app,
            height=40,
            image=ANALISIS_ICON,
            text="Análisis Númerico",
            text_color=self.app.theme_config["CTkLabel"]["text_color"],
            tooltip_text="\nRaíces de funciones, derivadas, integrales.\n",
            command=self.ir_a_funcs,
        ).grid(row=4, column=0, padx=(10, 5), pady=3, sticky="ne")

        IconButton(
            self,
            app=self.app,
            height=40,
            image=ECUACIONES_ICON,
            text="Sistemas de Ecuaciones",
            text_color=self.app.theme_config["CTkLabel"]["text_color"],
            tooltip_text="\nResolver sistemas de ecuaciones por los métodos de:"
            + "\n− Gauss−Jordan"
            + "\n− Regla de Cramer\n",
            command=self.ir_a_sis,
        ).grid(row=4, column=1, padx=(5, 10), pady=3, sticky="nw")

        IconButton(
            self,
            app=self.app,
            height=30,
            image=ABOUT_US_ICON,
            tooltip_text="\n− Desarrollado por: Joaquín Zúñiga"
            + "\n− Versión: 1.0"
            + "\n− Licencia: MIT License"
            + "\n(puede hacer click para ir al repositorio de Github)\n",
            command=lambda: open_link("https://github.com/jp-zuniga/GaussBot"),
        ).grid(row=5, column=0, padx=(10, 5), pady=(3, 10), sticky="ne")

        IconButton(
            self,
            app=self.app,
            height=30,
            image=INFO_ICON,
            tooltip_text="\nTodos los datos ingresados y resultados calculados"
            + "\n(excepto determinantes, magnitudes de vectores, "
            + "   y raíces de funciones)".strip()
            + "\npueden ser guardados para uso futuro.\n",
        ).grid(row=5, column=1, padx=(5, 10), pady=(3, 10), sticky="nw")

    def ir_a_mats(self) -> None:
        """
        Selecciona el menú de matrices.
        """

        self.app.nav_frame.seleccionar_frame("matrices")

    def ir_a_vecs(self) -> None:
        """
        Selecciona el menú de vectores.
        """

        self.app.nav_frame.seleccionar_frame("vectores")

    def ir_a_funcs(self) -> None:
        """
        Selecciona el frame de análisis númerico.
        """

        self.app.nav_frame.seleccionar_frame("analisis")

    def ir_a_sis(self) -> None:
        """
        Selecciona el frame de sistemas de ecuaciones.
        """

        self.app.nav_frame.seleccionar_frame("sistemas")

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
