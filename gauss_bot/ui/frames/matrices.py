from fractions import Fraction

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkScrollableFrame as ctkScrollFrame,
    CTkButton as ctkButton,
    CTkTabview as ctkTabview,
    CTkLabel as ctkLabel,
    CTkEntry as ctkEntry,
    CTkCheckBox as ctkCheckBox,
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot.clases.matriz import Matriz
from gauss_bot.managers.mats_manager import MatricesManager


class MatricesFrame(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        self.crear_tabview()

    def crear_tabview(self):
        tabview = ctkTabview(self)
        tabview.pack(expand=True, fill='both')
        tabs = [
            ("Mostrar matrices", MostrarTab),
            ("Agregar matriz", AgregarTab),
            ("Resolver sistema", ResolverTab),
            ("Suma y resta", SumaRestaTab),
            ("Multiplicación", MultiplicacionTab),
            ("Transposición", TransposicionTab),
            ("Calcular determinante", DeterminanteTab),
            ("Encontrar inversa", InversaTab),
        ]

        for nombre, clase in tabs:
            tab = tabview.add(nombre)
            clase(tab, self.app, self.mats_manager).pack(expand=True, fill='both')


class MostrarTab(ctkScrollFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        label = ctkLabel(self, text=mats_manager.mostrar_matrices(necesita_aumentada=-1))
        label.pack(pady=5, padx=5, expand=True, fill='both')


class AgregarTab(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        self.aumentada = False
        self.input_entries: list[list[ctkEntry]] = []

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.checkbox_label = ctkLabel(self, text="¿Es aumentada?")
        self.checkbox_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.check_aumentada = ctkCheckBox(self, text="", command=self.toggle_aumentada)
        self.check_aumentada.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        label_filas = ctkLabel(self, text="Número de filas:")
        label_filas.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_filas = ctkEntry(self)
        self.entry_filas.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        label_columnas = ctkLabel(self, text="Número de columnas:")
        label_columnas.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_columnas = ctkEntry(self)
        self.entry_columnas.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        generar_button = ctkButton(self, text="Generar matriz", command=self.generar_matriz)
        generar_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.matriz_frame = ctkFrame(self)
        self.matriz_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ns")

    def toggle_aumentada(self):
        self.aumentada = not self.aumentada

    def generar_matriz(self):
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()

        filas = int(self.entry_filas.get())
        columnas = int(self.entry_columnas.get())
        if self.aumentada:
            columnas += 1

        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                input_entry = ctkEntry(self.matriz_frame)
                input_entry.grid(row=i, column=j, padx=5, pady=5)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        agregar_button = ctkButton(self, text="Agregar", command=self.agregar_matriz)
        agregar_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def agregar_matriz(self):
        nombre = self.entry_nombre.get()
        filas = int(self.entry_filas.get())
        columnas = int(self.entry_columnas.get())
        if self.aumentada:
            columnas += 1

        valores = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                valor = Fraction(self.input_entries[i][j].get())
                fila.append(valor)
            valores.append(fila)

        matriz = Matriz(self.aumentada, filas, columnas, valores)
        self.mats_manager.mats_ingresadas[nombre] = matriz


class ResolverTab(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        label = ctkLabel(self, text="Seleccione la matriz a resolver:")
        label.pack(pady=5, padx=5)

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada = ctkOptionMenu(self, values=self.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        button = ctkButton(self, text="Resolver", command=self.resolver_sistema)
        button.pack(pady=5, padx=5)

    def update_nombres(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada.configure(values=self.nombres_matrices)

    def resolver_sistema(self):
        selected_matrix_name = self.mat_seleccionada.get()
        if selected_matrix_name:
            pass


class SumaRestaTab(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        label = ctkLabel(self, text="Seleccione las matrices para sumar o restar:")
        label.pack(pady=5, padx=5)

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat1 = ctkOptionMenu(self, values=self.nombres_matrices)
        self.mat1.pack(pady=5, padx=5)

        self.mat2 = ctkOptionMenu(self, values=self.nombres_matrices)
        self.mat2.pack(pady=5, padx=5)

        self.checkbox_sumar = ctkCheckBox(self, text="Sumar")
        self.checkbox_sumar.pack(pady=5, padx=5)

        self.checkbox_restar = ctkCheckBox(self, text="Restar")
        self.checkbox_restar.pack(pady=5, padx=5)

        button = ctkButton(self, text="Ejecutar", command=self.ejecutar_operacion)
        button.pack(pady=5, padx=5)

    def update_nombres_matrices(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat1.configure(values=self.nombres_matrices)
        self.mat2.configure(values=self.nombres_matrices)

    def ejecutar_operacion(self):
        nombre_mat1 = self.mat1.get()
        nombre_mat2 = self.mat2.get()
        if nombre_mat1 and nombre_mat2:
            matriz1 = self.mats_manager.mats_ingresadas[nombre_mat1]
            matriz2 = self.mats_manager.mats_ingresadas[nombre_mat2]
            if self.checkbox_sumar.get():
                self.sumar_matrices(matriz1, matriz2)
            if self.checkbox_restar.get():
                self.restar_matrices(matriz1, matriz2)

    def sumar_matrices(self, matriz1, matriz2):
        pass

    def restar_matrices(self, matriz1, matriz2):
        pass


class MultiplicacionTab(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        tabview = ctkTabview(self)
        tabview.pack(expand=True, fill='both')

        tab_escalar = tabview.add("Multiplicación Escalar")
        label_escalar = ctkLabel(tab_escalar, text="Seleccione la matriz e ingrese el escalar:")
        label_escalar.pack(pady=5, padx=5)

        self.mat_seleccionada = ctkOptionMenu(tab_escalar, values=self.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        self.entry_escalar = ctkEntry(tab_escalar)
        self.entry_escalar.pack(pady=5, padx=5)

        button_escalar = ctkButton(tab_escalar, text="Multiplicar", command=self.multiplicar_por_escalar)
        button_escalar.pack(pady=5, padx=5)

        tab_matrix = tabview.add("Multiplicación de Matrices")
        label_matrix = ctkLabel(tab_matrix, text="Seleccione las matrices para multiplicar:")
        label_matrix.pack(pady=5, padx=5)

        self.mat1 = ctkOptionMenu(tab_matrix, values=self.nombres_matrices)
        self.mat1.pack(pady=5, padx=5)

        self.mat2 = ctkOptionMenu(tab_matrix, values=self.nombres_matrices)
        self.mat2.pack(pady=5, padx=5)

        button_matrix = ctkButton(tab_matrix, text="Multiplicar", command=self.multiplicar_matrices)
        button_matrix.pack(pady=5, padx=5)

    def update_nombres_matrices(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada.configure(values=self.nombres_matrices)
        self.mat1.configure(values=self.nombres_matrices)
        self.mat2.configure(values=self.nombres_matrices)

    def multiplicar_por_escalar(self):
        pass

    def multiplicar_matrices(self):
        pass


class TransposicionTab(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        label = ctkLabel(self, text="Seleccione la matriz para transponer:")
        label.pack(pady=5, padx=5)

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada = ctkOptionMenu(self, values=self.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        button = ctkButton(self, text="Transponer", command=self.transponer)
        button.pack(pady=5, padx=5)

    def update_nombres_matrices(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada.configure(values=self.nombres_matrices)

    def transponer(self):
        selected_matrix_name = self.mat_seleccionada.get()
        if selected_matrix_name:
            # matriz = self.mats_manager.mats_ingresadas[selected_matrix_name]
            pass


class DeterminanteTab(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        label = ctkLabel(self, text="Seleccione la matriz para calcular el determinante:")
        label.pack(pady=5, padx=5)

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada = ctkOptionMenu(self, values=self.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        button = ctkButton(self, text="Calcular", command=self.calcular_determinante)
        button.pack(pady=5, padx=5)

    def update_nombres_matrices(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada.configure(values=self.nombres_matrices)

    def calcular_determinante(self):
        pass


class InversaTab(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        label = ctkLabel(self, text="Seleccione la matriz para encontrar la inversa:")
        label.pack(pady=5, padx=5)

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada = ctkOptionMenu(self, values=self.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        button = ctkButton(self, text="Encontrar", command=self.encontrar_inversa)
        button.pack(pady=5, padx=5)

    def update_nombres_matrices(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mat_seleccionada.configure(values=self.nombres_matrices)

    def encontrar_inversa(self):
        pass