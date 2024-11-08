"""
Home frame de la interfaz.
"""

from typing import TYPE_CHECKING

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


class HomeFrame(ctkFrame):
    def __init__(self, app: "GaussUI", master: "GaussUI") -> None:
        super().__init__(master, corner_radius=0)
        self.app = app
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        welcome = ctkLabel(
            self,
            text="¡Bienvenido a GaussBot!",
            font=ctkFont(
                size=26,
                weight="bold",
            )
        )

        agregar_matrices = ctkButton(
            self,
            width=180,
            height=40,
            text="Agregar matrices",
            font=ctkFont(size=16),
            command=lambda: self.ir_a_matriz(mostrar=False)
        )

        agregar_vectores = ctkButton(
            self,
            width=180,
            height=40,
            text="Agregar vectores",
            font=ctkFont(size=16),
            command=lambda: self.ir_a_vector(mostrar=False)
        )

        mostrar_matrices = ctkButton(
            self,
            width=180,
            height=40,
            text="Mostrar matrices",
            font=ctkFont(size=16),
            command=lambda: self.ir_a_matriz(mostrar=True)
        )

        mostrar_vectores = ctkButton(
            self,
            width=180,
            height=40,
            text="Mostrar vectores",
            font=ctkFont(size=16),
            command=lambda: self.ir_a_vector(mostrar=True)
        )

        welcome.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="s")
        agregar_matrices.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="ne")
        agregar_vectores.grid(row=1, column=1, padx=20, pady=(20, 10), sticky="nw")
        mostrar_matrices.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ne")
        mostrar_vectores.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="nw")
    
    def ir_a_matriz(self, mostrar: bool):
        self.app.nav_frame.seleccionar_frame("inputs")  # type: ignore
        self.app.inputs_frame.tabview.set("Matrices")  # type: ignore
        if mostrar:
            self.app.inputs_frame.instances[0].tabview.set("Mostrar")  # type: ignore
    
    def ir_a_vector(self, mostrar: bool):
        self.app.nav_frame.seleccionar_frame("inputs")  # type: ignore
        self.app.inputs_frame.tabview.set("Vectores")  # type: ignore
        if mostrar:
            self.app.inputs_frame.instances[1].tabview.set("Mostrar")  # type: ignore
