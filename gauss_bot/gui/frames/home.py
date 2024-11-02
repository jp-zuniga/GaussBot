"""
Home frame de la interfaz.
"""

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)


class HomeFrame(ctkFrame):
    def __init__(self, master, app) -> None:
        super().__init__(master, corner_radius=0)
        self.app = app
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        welcome = ctkLabel(
            self,
            text="¡Bienvenido a GaussBot!",
            font=ctkFont(
                size=30,
                weight="bold",
            )
        )

        matrices = ctkButton(
            self,
            width=200,
            height=50,
            text="Agregar matrices",
            font=ctkFont(size=18),
            command=self.ir_a_matriz
        )

        vectores = ctkButton(
            self,
            width=200,
            height=50,
            text="Agregar vectores",
            font=ctkFont(size=18),
            command=self.ir_a_vector
        )

        welcome.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="s")
        matrices.grid(row=1, column=0, padx=20, pady=20, sticky="ne")
        vectores.grid(row=1, column=1, padx=20, pady=20, sticky="nw")
    
    def ir_a_matriz(self):
        self.app.nav_frame.seleccionar_frame("inputs")
        self.app.inputs_frame.tabview.set("Matrices")
    
    def ir_a_vector(self):
        self.app.nav_frame.seleccionar_frame("inputs")
        self.app.inputs_frame.tabview.set("Vectores")
