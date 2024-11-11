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

from gauss_bot.managers import (
    MatricesManager,
    VectoresManager,
)

from gauss_bot.gui.custom import CustomScrollFrame
from gauss_bot.gui.frames.subframes import (
    AgregarSistemas,
    MostrarSistemas,
    EliminarSistemas,
    AgregarMats,
    MostrarMats,
    EliminarMats,
    AgregarVecs,
    MostrarVecs,
    EliminarVecs,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


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
        self.tabview: ctkTabview
        self.instances: list[Union[ManejarSistemas, ManejarMats, ManejarVecs]]

        self.setup_tabview()
        self.tabview.set("Matrices")

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada frame de inputs.
        """

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances = []

        sistemas_tab = self.tabview.add("Sistemas de Ecuaciones")
        matrices_tab = self.tabview.add("Matrices")
        vectores_tab = self.tabview.add("Vectores")
        self.instances.append(ManejarSistemas(self.app, sistemas_tab, self, self.mats_manager))
        self.instances.append(ManejarMats(self.app, matrices_tab, self, self.mats_manager))
        self.instances.append(ManejarVecs(self.app, vectores_tab, self, self.vecs_manager))

        for tab in self.instances:
            tab.pack(expand=True, fill="both")

    def update_all(self):
        for tab in self.instances:
            tab.update_all()
        self.tabview.configure(fg_color="transparent")


class ManejarSistemas(ctkFrame):
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
        self.tabview: ctkTabview
        self.instances: list[
            Union[
                AgregarSistemas,
                MostrarSistemas,
                # EditarSistemas,
                EliminarSistemas,
            ]
        ] = []

        self.tabs: list[
            tuple[
                str,
                Union[
                    type[AgregarSistemas],
                    type[MostrarSistemas],
                    # type[EditarSistemas],
                    type[EliminarSistemas],
                ]
            ]
        ]

        self.setup_tabview()

    def setup_tabview(self) -> None:
        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        tabs = [
            ("Agregar", AgregarSistemas),
            ("Mostrar", MostrarSistemas),
            # ("Editar", EditarSistemas),
            ("Eliminar", EliminarSistemas)
        ]

        for nombre, cls in tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = (
                cls(self.app, tab, self, self.mats_manager)
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)   # type: ignore

    def update_all(self):
        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")


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
        self.instances: list[
            Union[
                AgregarMats,
                MostrarMats,
                # EditarMats,
                EliminarMats,
            ]
        ] = []

        self.tabs: list[
            tuple[
                str,
                Union[
                    type[AgregarMats],
                    type[MostrarMats],
                    # type[EditarMats],
                    type[EliminarMats],
                ]
            ]
        ]

        self.setup_tabview()

    def setup_tabview(self) -> None:
        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        tabs = [
            ("Agregar", AgregarMats),
            ("Mostrar", MostrarMats),
            # ("Editar", EditarMats),
            ("Eliminar", EliminarMats)
        ]

        for nombre, cls in tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = (
                cls(self.app, tab, self, self.mats_manager)
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)   # type: ignore

    def update_all(self):
        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")


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
        self.instances: list[
            Union[
                AgregarVecs,
                MostrarVecs,
                # EditarVecs,
                EliminarVecs,
            ]
        ] = []

        self.tabs: list[
            tuple[
                str,
                Union[
                    type[AgregarVecs],
                    type[MostrarVecs],
                    # type[EditarVecs],
                    type[EliminarVecs],
                ]
            ]
        ]

        self.setup_tabview()

    def setup_tabview(self) -> None:
        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        tabs = [
            ("Agregar", AgregarVecs),
            ("Mostrar", MostrarVecs),
            # ("Editar", EditarVecs),
            ("Eliminar", EliminarVecs)
        ]

        for nombre, cls in tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = (
                cls(self.app, tab, self, self.vecs_manager)
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)   # type: ignore

    def update_all(self):
        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")
