# from fractions import Fraction

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

# from gauss_bot.clases.matriz import Matriz
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
        pass


class SumaRestaTab(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        self.tabview = ctkTabview(self, width=250)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)

        self.tab_sumar = self.tabview.add("Sumar")
        self.tab_restar = self.tabview.add("Restar")

        self.setup_tab(self.tab_sumar, "Sumar")
        self.setup_tab(self.tab_restar, "Restar")

    def setup_tab(self, tab, operacion):
        label = ctkLabel(tab, text=f"Seleccione las matrices para {operacion.lower()}:")
        label.pack(pady=5, padx=5)

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        mat1 = ctkOptionMenu(tab, values=self.nombres_matrices)
        mat1.pack(pady=5, padx=5)

        mat2 = ctkOptionMenu(tab, values=self.nombres_matrices)
        mat2.pack(pady=5, padx=5)

        button = ctkButton(tab, text=operacion, command=lambda: self.ejecutar_operacion(operacion, mat1, mat2))
        button.pack(pady=5, padx=5)

    def update_nombres_matrices(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        for tab in [self.tab_sumar, self.tab_restar]:
            for widget in tab.winfo_children():
                if isinstance(widget, ctkOptionMenu):
                    widget.configure(values=self.nombres_matrices)

    def ejecutar_operacion(self, operacion, mat1, mat2):
        pass

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
        self.nombres_vectores = list(self.app.vecs_manager.vecs_ingresados.keys())

        tabview = ctkTabview(self)
        tabview.pack(expand=True, fill='both')

        tab_escalar = tabview.add("Multiplicación Escalar")
        tab_matriz = tabview.add("Multiplicación de Matrices")
        tab_matriz_vector = tabview.add("Producto Matriz-Vector")
        self.setup_escalar_tab(tab_escalar)
        self.setup_mult_matrices_tab(tab_matriz)
        self.setup_matriz_vector_tab(tab_matriz_vector)

    def setup_escalar_tab(self, tab):
        label_escalar = ctkLabel(tab, text="Seleccione la matriz e ingrese el escalar:")
        label_escalar.pack(pady=5, padx=5)

        self.mat_seleccionada = ctkOptionMenu(tab, values=self.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        self.entry_escalar = ctkEntry(tab)
        self.entry_escalar.pack(pady=5, padx=5)

        button_matriz = ctkButton(tab, text="Multiplicar", command=self.multiplicar_matrices)
        button_matriz.pack(pady=5, padx=5)

    def setup_mult_matrices_tab(self, tab):
        label_matriz = ctkLabel(tab, text="Seleccione las matrices para multiplicar:")
        label_matriz.pack(pady=5, padx=5)

        self.mat1 = ctkOptionMenu(tab, values=self.nombres_matrices)
        self.mat1.pack(pady=5, padx=5)

        self.mat2 = ctkOptionMenu(tab, values=self.nombres_matrices)
        self.mat2.pack(pady=5, padx=5)

        button_matriz = ctkButton(tab, text="Multiplicar", command=self.multiplicar_matrices)
        button_matriz.pack(pady=5, padx=5)

    def setup_matriz_vector_tab(self, tab):
        label_matriz_vector = ctkLabel(tab, text="Seleccione la matriz y el vector para multiplicar:")
        label_matriz_vector.pack(pady=5, padx=5)

        self.mat_seleccionada = ctkOptionMenu(tab, values=self.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        self.entry_vector = ctkOptionMenu(tab, values=self.nombres_vectores)
        self.entry_vector.pack(pady=5, padx=5)

        button_matriz_vector = ctkButton(tab, text="Multiplicar", command=self.multiplicar_por_escalar)
        button_matriz_vector.pack(pady=5, padx=5)

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