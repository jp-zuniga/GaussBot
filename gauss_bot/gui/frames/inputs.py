"""
Implementación de las clases ManejarMats y ManejarVecs,
los frames que contienen subframes para
agregar, mostrar, editar y eliminar matrices y vectores.
"""

from typing import Union

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager

from gauss_bot.gui.custom_frames import CustomScrollFrame

from gauss_bot.gui.frames.subframes.input_mats import (
    AgregarMats,
    MostrarMats,
    EliminarMats,
)

from gauss_bot.gui.frames.subframes.input_vecs import (
    AgregarVecs,
    MostrarVecs,
    EliminarVecs,
)


class InputsFrame(ctkFrame):
    def __init__(self, master, app, mats_manager: MatricesManager, vecs_manager: VectoresManager) -> None:
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        self.vecs_manager = vecs_manager
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada frame de inputs.
        """

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances: list[Union[ctkFrame, CustomScrollFrame]] = []

        matrices_tab = self.tabview.add("Matrices")
        self.instances.append(ManejarMats(self, matrices_tab, self.app, self.mats_manager))
        vectores_tab = self.tabview.add("Vectores")
        self.instances.append(ManejarVecs(self, vectores_tab, self.app, self.vecs_manager))
        
        for tab in self.instances:
            tab.pack(expand=True, fill="both")

    def update_all(self):
        for tab in self.instances:
            tab.update_frame()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()


class ManejarMats(ctkFrame):
    def __init__(self, master_frame: InputsFrame, master_tab,
                 app, mats_manager: MatricesManager) -> None:

        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.setup_tabview()

    def setup_tabview(self) -> None:
        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances: list[Union[ctkFrame, CustomScrollFrame]] = []
        self.tabs = [
            ("Agregar", AgregarMats),
            ("Mostrar", MostrarMats),
            # ("Editar", EditarMats),
            ("Eliminar", EliminarMats)
        ]

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: Union[ctkFrame, CustomScrollFrame] = (
                cls(self, tab, self.app, self.mats_manager)
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)   # type: ignore

    def update_frame(self):
        for tab in self.instances:
            tab.update_frame()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()


class ManejarVecs(ctkFrame):
    def __init__(self, master_frame: InputsFrame, master_tab,
                 app, vecs_manager: VectoresManager) -> None:

        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)
        self.setup_tabview()

    def setup_tabview(self) -> None:
        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances: list[Union[ctkFrame, CustomScrollFrame]] = []
        self.tabs = [
            ("Agregar", AgregarVecs),
            ("Mostrar", MostrarVecs),
            # ("Editar", EditarVecs),
            ("Eliminar", EliminarVecs)
        ]

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: Union[ctkFrame, CustomScrollFrame] = (
                cls(self, tab, self.app, self.vecs_manager)
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)   # type: ignore

    def update_frame(self):
        for tab in self.instances:
            tab.update_frame()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()
