from customtkinter import (
    CTkFrame as ctkFrame,
    CTkButton as ctkButton,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
    CTkCheckBox as ctkCheckBox,
)

from gauss_bot.managers.mats_manager import MatricesManager

from gauss_bot.gui.custom_frames import ErrorFrame, ResultadoFrame


class EcuacionesFrame(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
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

        if self.nombres_matrices == []:
            self.rowconfigure(0, weight=1)
            self.mensaje_frame = ErrorFrame(self, "No hay sistemas de ecuaciones ingresados!")
            self.mensaje_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            return

        label = ctkLabel(self, text="Seleccione el sistema de ecuaciones a resolver:")
        label.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

        self.select_sis_mat = ctkOptionMenu(self, width=60, values=self.nombres_matrices, command=self.update_sis_mat)
        self.select_sis_mat.grid(row=1, column=0, columnspan=2, pady=5, padx=5)

        self.sis_mat = self.select_sis_mat.get()

        self.gauss_jordan = False
        self.cramer = False

        self.gauss_jordan_checkbox = ctkCheckBox(self, text="", command=self.toggle_gj)
        self.gauss_jordan_checkbox.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        gauss_jordan_label = ctkLabel(self, text="Método Gauss-Jordan")
        gauss_jordan_label.grid(row=2, column=0, pady=5, padx=5, sticky="e")

        self.cramer_checkbox = ctkCheckBox(self, text="", command=self.toggle_cramer)
        self.cramer_checkbox.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        cramer_label = ctkLabel(self, text="Regla de Cramer")
        cramer_label.grid(row=3, column=0, pady=5, padx=5, sticky="e")

        button = ctkButton(self, text="Resolver", command=self.resolver_sistema)
        button.grid(row=4, column=0, columnspan=2, pady=5, padx=5)

    def toggle_gj(self):
        self.gauss_jordan = not self.gauss_jordan

    def toggle_cramer(self):
        self.cramer = not self.cramer

    def resolver_sistema(self):
        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        if all([self.gauss_jordan, self.cramer]):
            self.mensaje_frame = ErrorFrame(self, "Solamente debe seleccionar un método para resolver el sistema!")
            self.mensaje_frame.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return
        if not any([self.gauss_jordan, self.cramer]):
            self.mensaje_frame = ErrorFrame(self, "Debe seleccionar un método para resolver el sistema!")
            self.mensaje_frame.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        if self.gauss_jordan:
            nombre_sistema, sistema = self.mats_manager.resolver_sistema(nombre_mat=self.sis_mat, metodo="gj")
        elif self.cramer:
            try:
                nombre_sistema, sistema = self.mats_manager.resolver_sistema(nombre_mat=self.sis_mat, metodo="c")
            except (TypeError, ArithmeticError, ValueError) as e:
                self.mensaje_frame = ErrorFrame(self, str(e))
                self.mensaje_frame.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)
                return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(self, header=sistema.solucion, resultado=None, solo_header=True)
        self.mensaje_frame.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)
        if not any(sistema.matriz == mat for mat in self.mats_manager.mats_ingresadas.values()):
            self.mats_manager.mats_ingresadas[nombre_sistema] = sistema.matriz
            self.app.matrices.update_all()

    def update_frame(self):
        self.__init__(self.master, self.app, self.mats_manager)

    def update_sis_mat(self, valor):
        self.sis_mat = valor
