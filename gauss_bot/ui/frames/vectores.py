from customtkinter import (
    CTkFrame as ctkFrame,
    CTkScrollableFrame as ctkScrollFrame,
    CTkButton as ctkButton,
    CTkTabview as ctkTabview,
    CTkLabel as ctkLabel,
    CTkEntry as ctkEntry,
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot.clases.vector import Vector
from gauss_bot.managers.vecs_manager import VectoresManager

class VectoresFrame(ctkFrame):
    def __init__(self, master, app, vecs_manager: VectoresManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.vecs_manager = vecs_manager
        self.crear_tabview()

    def crear_tabview(self):
        tabview = ctkTabview(self)
        tabview.pack(expand=True, fill='both')
        tabs = [
            ("Mostrar vectores", MostrarTab),
            ("Agregar vector", AgregarTab),
            ("Sumar y restar vectores", SumaRestaTab),
            ("Multiplicación", MultiplicacionTab),
        ]

        for nombre, clase in tabs:
            tab = tabview.add(nombre)
            clase(tab, self.app, self.vecs_manager).pack(expand=True, fill='both')


class MostrarTab(ctkScrollFrame):
    def __init__(self, master, app, vecs_manager: VectoresManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.vecs_manager = vecs_manager
        label = ctkLabel(self, text=vecs_manager.mostrar_vectores())
        label.pack(pady=5, padx=5, expand=True, fill='both')


class AgregarTab(ctkFrame):
    def __init__(self, master, app, vecs_manager: VectoresManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.vecs_manager = vecs_manager
        self.input_entries: list[ctkEntry] = []

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        label_nombre = ctkLabel(self, text="Nombre del vector:")
        label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = ctkEntry(self)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        label_dim = ctkLabel(self, text="Dimensión del vector:")
        label_dim.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_dim = ctkEntry(self)
        self.entry_dim.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        generar_button = ctkButton(self, text="Generar vector", command=self.generar_vector)
        generar_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.vector_frame = ctkFrame(self)
        self.vector_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ns")

    def generar_vector(self):
        for widget in self.vector_frame.winfo_children():
            widget.destroy()

        dim = int(self.entry_dim.get())
        for i in range(dim):
            input_entry = ctkEntry(self.vector_frame)
            input_entry.grid(row=i, column=0, padx=5, pady=5)
            self.input_entries.append(input_entry)

        agregar_button = ctkButton(self, text="Agregar", command=self.agregar_vector)
        agregar_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def agregar_vector(self):
        nombre = self.entry_nombre.get()
        dim = int(self.entry_dim.get())
        valores = [float(entry.get()) for entry in self.input_entries]

        vector = Vector(nombre, dim, valores)
        self.vecs_manager.vectores_ingresados[nombre] = vector


class SumaRestaTab(ctkFrame):
    def __init__(self, master, app, vecs_manager: VectoresManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.vecs_manager = vecs_manager

        self.tabview = ctkTabview(self, width=250)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)

        self.tab_sumar = self.tabview.add("Sumar")
        self.tab_restar = self.tabview.add("Restar")

        self.setup_tab(self.tab_sumar, "Sumar")
        self.setup_tab(self.tab_restar, "Restar")

    def setup_tab(self, tab, operacion):
        label = ctkLabel(tab, text=f"Seleccione los vectores para {operacion.lower()}:")
        label.pack(pady=5, padx=5)

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        vec1 = ctkOptionMenu(tab, values=self.nombres_vectores)
        vec1.pack(pady=5, padx=5)

        vec2 = ctkOptionMenu(tab, values=self.nombres_vectores)
        vec2.pack(pady=5, padx=5)

        button = ctkButton(tab, text=operacion, command=lambda: self.ejecutar_operacion(operacion, vec1, vec2))
        button.pack(pady=5, padx=5)

    def update_nombres_vectores(self):
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        for tab in [self.tab_sumar, self.tab_restar]:
            for widget in tab.winfo_children():
                if isinstance(widget, ctkOptionMenu):
                    widget.configure(values=self.nombres_vectores)
    
    def ejecutar_operacion(self):
        pass


class MultiplicacionTab(ctkFrame):
    def __init__(self, master, app, vecs_manager: VectoresManager):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.vecs_manager = vecs_manager
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())

        tabview = ctkTabview(self)
        tabview.pack(expand=True, fill='both')

        tab_escalar = tabview.add("Multiplicación Escalar")
        label_escalar = ctkLabel(tab_escalar, text="Seleccione el vector e ingrese el escalar:")
        label_escalar.pack(pady=5, padx=5)

        self.vec_seleccionado = ctkOptionMenu(tab_escalar, values=self.nombres_vectores)
        self.vec_seleccionado.pack(pady=5, padx=5)

        self.entry_escalar = ctkEntry(tab_escalar)
        self.entry_escalar.pack(pady=5, padx=5)

        button_escalar = ctkButton(tab_escalar, text="Multiplicar", command=self.multiplicar_por_escalar)
        button_escalar.pack(pady=5, padx=5)

        tab_vector = tabview.add("Multiplicación de Vectores")
        label_vector = ctkLabel(tab_vector, text="Seleccione los vectores para multiplicar:")
        label_vector.pack(pady=5, padx=5)

        self.vec1 = ctkOptionMenu(tab_vector, values=self.nombres_vectores)
        self.vec1.pack(pady=5, padx=5)

        self.vec2 = ctkOptionMenu(tab_vector, values=self.nombres_vectores)
        self.vec2.pack(pady=5, padx=5)

        button_vector = ctkButton(tab_vector, text="Multiplicar", command=self.multiplicar_vectores)
        button_vector.pack(pady=5, padx=5)

    def update_nombres_vectores(self):
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.vec_seleccionado.configure(values=self.nombres_vectores)
        self.vec1.configure(values=self.nombres_vectores)
        self.vec2.configure(values=self.nombres_vectores)

    def multiplicar_por_escalar(self):
        pass

    def multiplicar_vectores(self):
        pass
