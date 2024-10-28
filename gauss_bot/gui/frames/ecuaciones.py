"""
Implementación de EcuacionesFrame,
el frame que resuelve sistemas de ecuaciones lineales.
"""

from customtkinter import (
    CTkButton as ctkButton,
    CTkCheckBox as ctkCheckBox,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot.gui.custom_frames import (
    ErrorFrame,
    ResultadoFrame
)

from gauss_bot.managers.mats_manager import MatricesManager


class EcuacionesFrame(ctkFrame):
    """
    Frame que permite al usuario seleccionar un sistema
    de ecuaciones ingresado y resolverlo utilizando el
    método Gauss-Jordan o la regla de Cramer.
    """

    def __init__(self, master, app, mats_manager: MatricesManager) -> None:
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.mensaje_frame = None

        self.nombres_matrices = []
        for nombre, mat in self.mats_manager.mats_ingresadas.items():
            if mat.aumentada:
                self.nombres_matrices.append(nombre)

        if not self.nombres_matrices:
            self.rowconfigure(0, weight=1)
            self.mensaje_frame = ErrorFrame(self, "No hay sistemas de ecuaciones ingresados!")
            self.mensaje_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            return

        instruct_se = ctkLabel(self, text="Seleccione el sistema de ecuaciones a resolver:")
        self.select_sis_mat = ctkOptionMenu(
            self, width=60, values=self.nombres_matrices, command=self.update_sis_mat
        )

        self.gauss_jordan_checkbox = ctkCheckBox(self, text="", command=self.toggle_gj)
        gauss_jordan_label = ctkLabel(self, text="Método Gauss-Jordan")

        self.cramer_checkbox = ctkCheckBox(self, text="", command=self.toggle_cramer)
        cramer_label = ctkLabel(self, text="Regla de Cramer")
        button = ctkButton(self, text="Resolver", command=self.resolver_sistema)

        self.sis_mat = self.select_sis_mat.get()
        self.gauss_jordan = False
        self.cramer = False

        instruct_se.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="ew")
        self.select_sis_mat.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        self.gauss_jordan_checkbox.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        gauss_jordan_label.grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.cramer_checkbox.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        cramer_label.grid(row=3, column=0, pady=5, padx=5, sticky="e")
        button.grid(row=4, column=0, columnspan=2, pady=5, padx=5)

    def resolver_sistema(self) -> None:
        """
        Resuelve el sistema de ecuaciones seleccionado
        por el usuario, utilizando el método indicado.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        if all([self.gauss_jordan, self.cramer]):
            self.mensaje_frame = ErrorFrame(
                self, "Solamente debe seleccionar un método para resolver el sistema!"
            ).grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return
        if not any([self.gauss_jordan, self.cramer]):
            self.mensaje_frame = ErrorFrame(
                self, "Debe seleccionar un método para resolver el sistema!"
            ).grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        nombre_sistema = ""
        if self.gauss_jordan:
            nombre_sistema, sistema = (
                self.mats_manager.resolver_sistema(nombre_mat=self.sis_mat, metodo="gj")
            )

        elif self.cramer:
            try:
                nombre_sistema, sistema = (
                    self.mats_manager.resolver_sistema(nombre_mat=self.sis_mat, metodo="c")
                )

            except (TypeError, ArithmeticError, ZeroDivisionError) as e:
                self.mensaje_frame = ErrorFrame(self, str(e)).grid(
                    row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5
                )

                return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        if not any(sistema.matriz == mat for mat in self.mats_manager.mats_ingresadas.values()):
            self.mats_manager.mats_ingresadas[nombre_sistema] = sistema.matriz
            self.app.matrices.update_all()

        self.mensaje_frame = ResultadoFrame(
            self, header=sistema.solucion, resultado="", solo_header=True
        ).grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)

    def toggle_gj(self) -> None:
        self.gauss_jordan = not self.gauss_jordan

    def toggle_cramer(self) -> None:
        self.cramer = not self.cramer

    def update_frame(self) -> None:
        self.__init__(self.master, self.app, self.mats_manager)

    def update_sis_mat(self, valor: str) -> None:
        self.sis_mat = valor
