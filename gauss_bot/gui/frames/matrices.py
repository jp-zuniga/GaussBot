from fractions import Fraction
from random import randint

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkScrollableFrame as ctkScrollFrame,
    CTkTabview as ctkTabview,
    CTkButton as ctkButton,
    CTkLabel as ctkLabel,
    CTkEntry as ctkEntry,
    CTkCheckBox as ctkCheckBox,
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot.models.matriz import Matriz
from gauss_bot.managers.mats_manager import MatricesManager

from gauss_bot.gui.custom_frames import ErrorFrame, SuccessFrame


class MatricesFrame(ctkFrame):
    def __init__(self, master_tab, app, mats_manager: MatricesManager):
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.nombres_vectores = list(self.app.vecs_manager.vecs_ingresados.keys())
        self.crear_tabview()

    def crear_tabview(self):
        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill='both')

        self.instances = []
        self.tabs = [
            ("Mostrar matrices", MostrarTab),
            ("Agregar matriz", AgregarTab),
            ("Suma y resta", SumaRestaTab),
            ("Multiplicación", MultiplicacionTab),
            ("Transposición", TransposicionTab),
            ("Calcular determinante", DeterminanteTab),
            ("Encontrar inversa", InversaTab),
        ]

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance = cls(self, tab, self.app, self.mats_manager)
            tab_instance.pack(expand=True, fill='both')
            self.instances.append(tab_instance)

    def update_all(self):
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.nombres_vectores = list(self.app.vecs_manager.vecs_ingresados.keys())
        for tab in self.instances:
            tab.update()


class MostrarTab(ctkScrollFrame):
    def __init__(self, master_frame, master_tab, app, mats_manager: MatricesManager):
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.mats_manager = mats_manager
        self.label = ctkLabel(self, text=mats_manager.get_matrices())
        self.label.pack(pady=5, padx=5, expand=True, fill='both')

    def update(self):
        self.label.configure(text=self.mats_manager.get_matrices())
        self.update_idletasks()


class AgregarTab(ctkScrollFrame):
    def __init__(self, master_frame, master_tab, app, mats_manager: MatricesManager):
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.mats_manager = mats_manager
        self.message_frame = None

        self.aumentada = False
        self.input_entries: list[list[ctkEntry]] = []

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        checkbox_label = ctkLabel(self, text="¿Es aumentada?")
        checkbox_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.check_aumentada = ctkCheckBox(self, text="", command=self.toggle_aumentada)
        self.check_aumentada.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        label_filas = ctkLabel(self, text="Número de filas:")
        label_filas.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_filas = ctkEntry(self, width=50, placeholder_text="2")
        self.entry_filas.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        label_columnas = ctkLabel(self, text="Número de columnas:")
        label_columnas.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_columnas = ctkEntry(self, width=50, placeholder_text="2")
        self.entry_columnas.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ingresar_button = ctkButton(self, height=30, text="Ingresar datos", command=self.generar_casillas)
        ingresar_button.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        aleatoria_button = ctkButton(self, height=30, text="Generar matriz aleatoria", command=self.generar_aleatoria)
        aleatoria_button.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.matriz_frame = ctkFrame(self)
        self.matriz_frame.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="n")

    def toggle_aumentada(self):
        self.aumentada = not self.aumentada

    def generar_casillas(self):
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()

        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())
        except ValueError:
            self.message_frame = ErrorFrame(self, "Debe ingresar números enteros positivos como filas y columnas!")
            self.message_frame.configure(height=30)
            self.message_frame.grid(row=4, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        if self.message_frame is not None:
            self.message_frame.destroy()
            self.message_frame = None

        if self.aumentada:
            columnas += 1

        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                input_entry = ctkEntry(self.matriz_frame, width=50)
                input_entry.grid(row=i, column=j, padx=5, pady=5)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        nombre_label = ctkLabel(self, text="Nombre de la matriz:")
        nombre_label.grid(row=11, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = ctkEntry(self, width=50, placeholder_text="A")
        self.nombre_entry.grid(row=11, column=1, padx=5, pady=5, sticky="w")
        self.agregar_button = ctkButton(self, text="Agregar", command=self.agregar_matriz)
        self.agregar_button.grid(row=12, column=0, padx=5, pady=5, sticky="e")
        self.limpiar_button = ctkButton(self, text="Limpiar casillas", command=self.generar_casillas)
        self.limpiar_button.grid(row=12, column=1, padx=5, pady=5, sticky="w")

    def generar_aleatoria(self):
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()

        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())
        except ValueError:
            self.message_frame = ErrorFrame(self, "Debe ingresar números enteros positivos como filas y columnas!")
            self.message_frame.configure(height=30)
            self.message_frame.grid(row=4, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        if self.message_frame is not None:
            self.message_frame.destroy()
            self.message_frame = None

        if self.aumentada:
            columnas += 1

        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                numerador = randint(1, 20)
                denominador = randint(1, 20)
                valor_random = Fraction(numerador, denominador)
                input_entry = ctkEntry(self.matriz_frame, width=50)
                input_entry.insert(0, str(valor_random))
                input_entry.grid(row=i, column=j, padx=5, pady=5)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        nombre_label = ctkLabel(self, text="Nombre de la matriz:")
        nombre_label.grid(row=11, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = ctkEntry(self, width=50, placeholder_text="A")
        self.nombre_entry.grid(row=11, column=1, padx=5, pady=5, sticky="w")
        self.agregar_button = ctkButton(self, text="Agregar", command=self.agregar_matriz)
        self.agregar_button.grid(row=12, column=0, padx=5, pady=5, sticky="e")
        self.limpiar_button = ctkButton(self, text="Limpiar casillas", command=self.generar_casillas)
        self.limpiar_button.grid(row=12, column=1, padx=5, pady=5, sticky="w")

    def agregar_matriz(self):
        filas = len(self.input_entries)
        columnas = len(self.input_entries[0])

        valores = []
        for fila_entries in self.input_entries:
            fila_valores = []
            for entry in fila_entries:
                try:
                    valor = Fraction(entry.get())
                except ValueError:
                    self.message_frame = ErrorFrame(self, "Todos los valores deben ser números reales!")
                    self.message_frame.configure(height=30)
                    self.message_frame.grid(row=13, column=0, columnspan=2, sticky="n", padx=5, pady=5)
                    return
                except ZeroDivisionError:
                    self.message_frame = ErrorFrame(self, "El denominador no puede ser 0!")
                    self.message_frame.configure(height=30)
                    self.message_frame.grid(row=13, column=0, columnspan=2, sticky="n", padx=5, pady=5)
                    return
                fila_valores.append(valor)
            valores.append(fila_valores)

        if self.message_frame is not None:
            self.message_frame.destroy()
            self.message_frame = None

        nueva_matriz = Matriz(aumentada=self.aumentada, filas=filas, columnas=columnas, valores=valores)
        nombre_nueva_matriz = self.nombre_entry.get()
        if not nombre_nueva_matriz.isalpha() or not nombre_nueva_matriz.isupper() or len(nombre_nueva_matriz) != 1:
            self.message_frame = ErrorFrame(self, "El nombre de la matriz debe ser una letra mayúscula!")
            self.message_frame.configure(height=30)
            self.message_frame.grid(row=13, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return
        elif nombre_nueva_matriz in self.mats_manager.mats_ingresadas:
            self.message_frame = ErrorFrame(self, f"Ya existe una matriz llamada '{nombre_nueva_matriz}'!")
            self.message_frame.configure(height=30)
            self.message_frame.grid(row=13, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        self.mats_manager.mats_ingresadas[nombre_nueva_matriz] = nueva_matriz
        self.master_frame.update_all()
        self.message_frame = SuccessFrame(self, "La matriz se ha agregado exitosamente!")
        self.message_frame.configure(height=30)
        self.message_frame.grid(row=13, column=0, columnspan=2, sticky="n", padx=5, pady=5)

    def update(self):
        self.update_idletasks()


class SumaRestaTab(ctkFrame):
    def __init__(self, master_frame, master_tab, app, mats_manager: MatricesManager):
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.mats_manager = mats_manager

        self.tabview = ctkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        self.tab_sumar = self.tabview.add("Sumar")
        self.tab_restar = self.tabview.add("Restar")

        self.setup_tab(self.tab_sumar, "Sumar")
        self.setup_tab(self.tab_restar, "Restar")

    def setup_tab(self, tab, operacion: str):
        label = ctkLabel(tab, text=f"Seleccione las matrices para {operacion.lower()}:")
        label.pack(pady=5, padx=5)

        self.mat1 = ctkOptionMenu(tab, values=self.master_frame.nombres_matrices)
        self.mat1.pack(pady=5, padx=5)

        self.mat2 = ctkOptionMenu(tab, values=self.master_frame.nombres_matrices)
        self.mat2.pack(pady=5, padx=5)

        button = ctkButton(tab, text=operacion, command=lambda: self.ejecutar_operacion(operacion, self.mat1, self.mat2))
        button.pack(pady=5, padx=5)

    def ejecutar_operacion(self, operacion, mat1, mat2):
        pass

    def sumar_matrices(self, matriz1, matriz2):
        pass

    def restar_matrices(self, matriz1, matriz2):
        pass

    def update(self):
        self.mat1.configure(values=self.master_frame.nombres_matrices)
        self.mat2.configure(values=self.master_frame.nombres_matrices)
        self.update_idletasks()


class MultiplicacionTab(ctkFrame):
    def __init__(self, master_frame, master_tab, app, mats_manager: MatricesManager):
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.mats_manager = mats_manager

        tabview = ctkTabview(self)
        tabview.pack(expand=True, fill='both')

        self.tab_escalar = tabview.add("Escalar por Matriz")
        self.tab_matriz = tabview.add("Multiplicación Matricial")
        self.tab_matriz_vector = tabview.add("Producto Matriz-Vector")
        self.setup_tabs()

    def setup_tabs(self):
        self.setup_escalar_tab(self.tab_escalar)
        self.setup_mult_matrices_tab(self.tab_matriz)
        self.setup_matriz_vector_tab(self.tab_matriz_vector)

    def setup_escalar_tab(self, tab):
        label_escalar = ctkLabel(tab, text="Seleccione la matriz e ingrese el escalar:")
        label_escalar.pack(pady=5, padx=5)

        self.mat_seleccionada = ctkOptionMenu(tab, values=self.master_frame.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        self.entry_escalar = ctkEntry(tab)
        self.entry_escalar.pack(pady=5, padx=5)

        button_multiplicar = ctkButton(tab, text="Multiplicar", command=self.mult_por_escalar)
        button_multiplicar.pack(pady=5, padx=5)

    def setup_mult_matrices_tab(self, tab):
        label_matriz = ctkLabel(tab, text="Seleccione las matrices para multiplicar:")
        label_matriz.pack(pady=5, padx=5)

        self.mat1 = ctkOptionMenu(tab, values=self.master_frame.nombres_matrices)
        self.mat1.pack(pady=5, padx=5)

        self.mat2 = ctkOptionMenu(tab, values=self.master_frame.nombres_matrices)
        self.mat2.pack(pady=5, padx=5)

        button_multiplicar = ctkButton(tab, text="Multiplicar", command=self.mult_matrices)
        button_multiplicar.pack(pady=5, padx=5)

    def setup_matriz_vector_tab(self, tab):
        label_matriz_vector = ctkLabel(tab, text="Seleccione la matriz y el vector para multiplicar:")
        label_matriz_vector.pack(pady=5, padx=5)

        self.mat_seleccionada = ctkOptionMenu(tab, values=self.master_frame.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        self.vec_seleccionado = ctkOptionMenu(tab, values=self.master_frame.nombres_vectores)
        self.vec_seleccionado.pack(pady=5, padx=5)

        button_multiplicar = ctkButton(tab, text="Multiplicar", command=self.matriz_vector)
        button_multiplicar.pack(pady=5, padx=5)

    def mult_por_escalar(self):
        pass

    def mult_matrices(self):
        pass

    def matriz_vector(self):
        pass

    def update(self):
        self.mat_seleccionada.configure(values=self.master_frame.nombres_matrices)
        self.mat1.configure(values=self.master_frame.nombres_matrices)
        self.mat2.configure(values=self.master_frame.nombres_matrices)
        self.vec_seleccionado.configure(values=self.master_frame.nombres_vectores)
        self.update_idletasks()


class TransposicionTab(ctkFrame):
    def __init__(self, master_frame, master_tab, app, mats_manager: MatricesManager):
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.mats_manager = mats_manager

        label = ctkLabel(self, text="Seleccione la matriz para transponer:")
        label.pack(pady=5, padx=5)

        self.mat_seleccionada = ctkOptionMenu(self, values=self.master_frame.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        button = ctkButton(self, text="Transponer", command=self.encontrar_transpuesta)
        button.pack(pady=5, padx=5)

    def encontrar_transpuesta(self):
        pass

    def update(self):
        self.mat_seleccionada.configure(values=self.master_frame.nombres_matrices)
        self.update_idletasks()


class DeterminanteTab(ctkFrame):
    def __init__(self, master_frame, master_tab, app, mats_manager: MatricesManager):
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.mats_manager = mats_manager

        label = ctkLabel(self, text="Seleccione la matriz para calcular el determinante:")
        label.pack(pady=5, padx=5)

        self.mat_seleccionada = ctkOptionMenu(self, values=self.master_frame.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        button = ctkButton(self, text="Calcular", command=self.calcular_determinante)
        button.pack(pady=5, padx=5)

    def calcular_determinante(self):
        pass

    def update(self):
        self.mat_seleccionada.configure(values=self.master_frame.nombres_matrices)
        self.update_idletasks()

class InversaTab(ctkFrame):
    def __init__(self, master_frame, master_tab, app, mats_manager: MatricesManager):
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.mats_manager = mats_manager

        label = ctkLabel(self, text="Seleccione la matriz para encontrar la inversa:")
        label.pack(pady=5, padx=5)

        self.mat_seleccionada = ctkOptionMenu(self, values=self.master_frame.nombres_matrices)
        self.mat_seleccionada.pack(pady=5, padx=5)

        button = ctkButton(self, text="Encontrar", command=self.encontrar_inversa)
        button.pack(pady=5, padx=5)

    def encontrar_inversa(self):
        pass

    def update(self):
        self.mat_seleccionada.configure(values=self.master_frame.nombres_matrices)
        self.update_idletasks()