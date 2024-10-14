from customtkinter import (
    CTkFrame as ctkFrame,
    CTkScrollableFrame as ctkScrollFrame,
    CTkButton as ctkButton,
    CTkTabview as ctkTabview,
    CTkLabel as ctkLabel,
    CTkEntry as ctkEntry,
    # CTkCheckBox as ctkCheckBox,
    # CTkOptionMenu as ctkOptionMenu,
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
