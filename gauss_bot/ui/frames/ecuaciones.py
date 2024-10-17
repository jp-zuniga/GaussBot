from tkinter import BooleanVar as BoolVar
from customtkinter import (
    CTkFrame as ctkFrame,
    CTkButton as ctkButton,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
    CTkCheckBox as ctkCheckBox,
)

from gauss_bot.managers.mats_manager import MatricesManager

class EcuacionesFrame(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        label = ctkLabel(self, text="Seleccione la matriz a resolver:")
        label.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada = ctkOptionMenu(self, values=self.nombres_matrices)
        self.mat_seleccionada.grid(row=1, column=0, columnspan=2, pady=5, padx=5)

        self.gauss_jordan_var = BoolVar()
        self.cramer_var = BoolVar()

        self.gauss_jordan_checkbox = ctkCheckBox(self, text="", variable=self.gauss_jordan_var)
        self.gauss_jordan_checkbox.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        self.gauss_jordan_label = ctkLabel(self, text="Método Gauss-Jordan")
        self.gauss_jordan_label.grid(row=2, column=0, pady=5, padx=5, sticky="e")

        self.cramer_checkbox = ctkCheckBox(self, text="", variable=self.cramer_var)
        self.cramer_checkbox.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        self.cramer_label = ctkLabel(self, text="Regla de Cramer")
        self.cramer_label.grid(row=3, column=0, pady=5, padx=5, sticky="e")

        button = ctkButton(self, text="Resolver", command=self.resolver_sistema)
        button.grid(row=4, column=0, columnspan=2, pady=5, padx=5)

    def update_nombres(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada.configure(values=self.nombres_matrices)

    def resolver_sistema(self):
        pass