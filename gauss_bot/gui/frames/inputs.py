"""
Implementación de las clases ManejarMats y ManejarVecs,
los frames que contienen subframes para
agregar, mostrar, editar y eliminar matrices y vectores.
"""

from typing import (
    TYPE_CHECKING,
    Union,
)

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager

from gauss_bot.gui.custom.custom_frames import CustomScrollFrame

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

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI


class InputsFrame(ctkFrame):
    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        mats_manager: MatricesManager,
        vecs_manager: VectoresManager,
    ) -> None:

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

        self.instances: list[Union[ManejarMats, ManejarVecs]] = []

        matrices_tab = self.tabview.add("Matrices")
        vectores_tab = self.tabview.add("Vectores")
        self.instances.append(ManejarMats(self.app, matrices_tab, self, self.mats_manager))
        self.instances.append(ManejarVecs(self.app, vectores_tab, self, self.vecs_manager))

        for tab in self.instances:
            tab.pack(expand=True, fill="both")

    def update_all(self):
        self.update_idletasks()
        for tab in self.instances:
            tab.update_all()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()


class ManejarMats(ctkFrame):
    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: InputsFrame,
        mats_manager: MatricesManager,
    ) -> None:

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
                cls(self.app, tab, self, self.mats_manager)
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)   # type: ignore

    def update_all(self):
        for tab in self.instances:
            tab.update_frame()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()


class ManejarVecs(ctkFrame):
    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: InputsFrame,
        vecs_manager: VectoresManager,
    ) -> None:

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
                cls(self.app, tab, self, self.vecs_manager)
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)   # type: ignore

    def update_all(self):
        self.update_idletasks()
        for tab in self.instances:
            tab.update_frame()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()
