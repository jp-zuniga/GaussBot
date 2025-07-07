"""
Implementación de frames de manejo de entradas de datos.
"""

from typing import TYPE_CHECKING, Literal

from customtkinter import CTkFrame, CTkTabview

from src.managers import FuncManager, MatricesManager, VectoresManager

from .subframes import (
    AgregarFuncs,
    AgregarMats,
    AgregarSistemas,
    AgregarVecs,
    EliminarFuncs,
    EliminarMats,
    EliminarSistemas,
    EliminarVecs,
    MostrarFuncs,
    MostrarMats,
    MostrarSistemas,
    MostrarVecs,
)

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.custom.adapted import CustomScrollFrame


class InputsFrame(CTkFrame):
    """
    Frame que contiene a todos los subframes
    que se encargan de manejar los inputs de la aplicación.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        managers: tuple[FuncManager, MatricesManager, VectoresManager],
    ) -> None:
        """
        Inicializar diseño de frame principal de entrada de datos.
        """

        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.func_manager, self.mats_manager, self.vecs_manager = managers

        self.instances: list[ManejarFuncs | ManejarSistemas | ManejarMats | ManejarVecs]

        self.tabview: CTkTabview
        self.setup_tabview()
        self.tabview.set("Matrices")

    def setup_tabview(self) -> None:
        """
        Crear un tabview con pestañas para cada frame de inputs.
        """

        self.tabview = CTkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        # crear tabs en tabview
        matrices_tab = self.tabview.add("Matrices")
        vectores_tab = self.tabview.add("Vectores")
        funcs_tab = self.tabview.add("Funciones")
        sistemas_tab = self.tabview.add("Sistemas de Ecuaciones")

        # inicializar frames:
        self.instances = [
            ManejarMats(self.app, matrices_tab, self, self.mats_manager),
            ManejarVecs(self.app, vectores_tab, self, self.vecs_manager),
            ManejarFuncs(self.app, funcs_tab, self, self.func_manager),
            ManejarSistemas(self.app, sistemas_tab, self, self.mats_manager),
        ]

        # pack frames para mostrarlos
        for tab in self.instances:
            tab.configure(border_width=3)
            tab.pack(expand=True, fill="both")

    def ir_a_input_frame(
        self,
        tab_name: Literal[
            "Matrices",
            "Vectores",
            "Funciones",
            "Sistemas de Ecuaciones",
        ],
        sub_tab_name: Literal["Agregar", "Mostrar"] = "Agregar",
    ) -> None:
        """
        Seleccionar un frame del tabview.

        Args:
            tab_name:     Nombre de tab a seleccionar.
            sub_tab_name: Nombre de tab a seleccionar dentro de 'tab_name'.

        """

        self.app.nav_frame.seleccionar_frame("inputs")
        self.app.inputs_frame.tabview.set(tab_name)
        self.instances[0].tabview.set(sub_tab_name)

    def update_all(self) -> None:
        """
        Actualizar todos los tabs del tabview.
        """

        for tab in self.instances:
            tab.update_all()
        self.tabview.configure(fg_color="transparent")


class ManejarMats(CTkFrame):
    """
    Frame que permite agregar, mostrar, y eliminar matrices.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: InputsFrame,
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de manejo de entradas de matrices.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager

        self.instances: list[AgregarMats | MostrarMats | EliminarMats]

        self.tabs: list[tuple[str, type[AgregarMats | MostrarMats | EliminarMats]]]

        self.tabview: CTkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview para todos los
        subframes de inputs de matrices.
        """

        self.tabview = CTkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        tabs = [
            ("Agregar", AgregarMats),
            ("Mostrar", MostrarMats),
            ("Eliminar", EliminarMats),
        ]

        # crear tab, inicializar y almacenar instancias
        for nombre, cls in tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = cls(
                self.app,
                tab,
                self,
                self.mats_manager,
                border_width=3,
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)

    def update_all(self) -> None:
        """
        Actualizar todos los tabs del tabview.
        """

        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")


class ManejarVecs(CTkFrame):
    """
    Frame que permite agregar, mostrar, y eliminar vectores.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: InputsFrame,
        vecs_manager: VectoresManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de manejo de entradas de vectores.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.app = app
        self.master_frame = master_frame
        self.vecs_manager = vecs_manager

        self.instances: list[AgregarVecs | MostrarVecs | EliminarVecs]

        self.tabs: list[tuple[str, type[AgregarVecs | MostrarVecs | EliminarVecs]]]

        self.tabview: CTkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview para todos los
        subframes de inputs de vectores.
        """

        self.tabview = CTkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        tabs = [
            ("Agregar", AgregarVecs),
            ("Mostrar", MostrarVecs),
            ("Eliminar", EliminarVecs),
        ]

        # crear tabs, inicializar y almacenar instancias
        for nombre, cls in tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = cls(
                self.app,
                tab,
                self,
                self.vecs_manager,
                border_width=3,
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)

    def update_all(self) -> None:
        """
        Actualizar todos los tabs del tabview.
        """

        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")


class ManejarFuncs(CTkFrame):
    """
    Frame que permite agregar, mostrar,
    y eliminar sistemas de ecuaciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: InputsFrame,
        func_manager: FuncManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de manejo de entradas de .
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager

        self.instances: list[AgregarFuncs | MostrarFuncs | EliminarFuncs]

        self.tabs: list[
            tuple[
                str,
                type[AgregarFuncs | MostrarFuncs | EliminarFuncs],
            ]
        ]

        self.tabview: CTkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada subframe.
        """

        self.tabview = CTkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        tabs = [
            ("Agregar", AgregarFuncs),
            ("Mostrar", MostrarFuncs),
            ("Eliminar", EliminarFuncs),
        ]

        # crear tabs, inicializar y almacenar instancias
        for nombre, cls in tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = cls(
                self.app,
                tab,
                self,
                self.func_manager,
                border_width=3,
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)

    def update_all(self) -> None:
        """
        Actualizar todos los tabs del tabview.
        """

        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")


class ManejarSistemas(CTkFrame):
    """
    Frame que permite agregar, mostrar,
    y eliminar sistemas de ecuaciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: InputsFrame,
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de manejo de entradas de .
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager

        self.instances: list[AgregarSistemas | MostrarSistemas | EliminarSistemas]

        self.tabs: list[
            tuple[
                str,
                type[AgregarSistemas | MostrarSistemas | EliminarSistemas],
            ]
        ]

        self.tabview: CTkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada subframe.
        """

        self.tabview = CTkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        tabs = [
            ("Agregar", AgregarSistemas),
            ("Mostrar", MostrarSistemas),
            ("Eliminar", EliminarSistemas),
        ]

        # crear tab, inicializar y almacenar instancias
        for nombre, cls in tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = cls(
                self.app,
                tab,
                self,
                self.mats_manager,
                border_width=3,
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)

    def update_all(self) -> None:
        """
        Actualizar todos los tabs del tabview.
        """

        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")
