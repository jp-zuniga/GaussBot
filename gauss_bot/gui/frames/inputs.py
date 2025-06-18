"""
Implementación de las clases ManejarSistemas,
ManejarMats, y ManejarVecs, los frames que contienen
subframes para agregar, mostrar, y eliminar los datos.
"""

from typing import TYPE_CHECKING, Union

from customtkinter import CTkFrame as ctkFrame, CTkTabview as ctkTabview

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
from ..custom import CustomScrollFrame
from ...managers import FuncManager, MatricesManager, VectoresManager

if TYPE_CHECKING:
    from .. import GaussUI


class InputsFrame(ctkFrame):
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
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.func_manager, self.mats_manager, self.vecs_manager = managers

        self.instances: list[
            Union[ManejarFuncs, ManejarSistemas, ManejarMats, ManejarVecs]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()
        self.tabview.set("Matrices")

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada frame de inputs.
        """

        self.tabview = ctkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")
        self.instances = []

        # crear tabs en tabview
        matrices_tab = self.tabview.add("Matrices")
        vectores_tab = self.tabview.add("Vectores")
        funcs_tab = self.tabview.add("Funciones")
        sistemas_tab = self.tabview.add("Sistemas de Ecuaciones")

        # inicializar frames y append a lista de instancias:
        self.instances.append(
            ManejarMats(self.app, matrices_tab, self, self.mats_manager)
        )

        self.instances.append(
            ManejarVecs(self.app, vectores_tab, self, self.vecs_manager)
        )

        self.instances.append(
            ManejarFuncs(self.app, funcs_tab, self, self.func_manager)
        )

        self.instances.append(
            ManejarSistemas(self.app, sistemas_tab, self, self.mats_manager)
        )

        # pack frames para mostrarlos
        for tab in self.instances:
            tab.pack(expand=True, fill="both")

    def ir_a_input_mats(self, mostrar: bool):
        """
        Mostrar frame 'ManejarMats'.
        * mostrar: si se quiere seleccionar la tab de mostrar o no
        """

        self.app.nav_frame.seleccionar_frame("inputs")  # type: ignore
        self.app.inputs_frame.tabview.set("Matrices")  # type: ignore
        if mostrar:
            self.instances[0].tabview.set("Mostrar")  # type: ignore
        else:
            self.instances[0].tabview.set("Agregar")  # type: ignore

    def ir_a_input_vecs(self, mostrar: bool):
        """
        Mostrar frame 'ManejarVecs'.
        * mostrar: si se quiere seleccionar la tab de mostrar o no
        """

        self.app.nav_frame.seleccionar_frame("inputs")  # type: ignore
        self.app.inputs_frame.tabview.set("Vectores")  # type: ignore
        if mostrar:
            self.instances[1].tabview.set("Mostrar")  # type: ignore
        else:
            self.instances[1].tabview.set("Agregar")  # type: ignore

    def ir_a_input_funcs(self, mostrar: bool):
        """
        Mostrar frame 'ManejarFuncs'.
        * mostrar: si se quiere seleccionar la tab de mostrar o no
        """

        self.app.nav_frame.seleccionar_frame("inputs")  # type: ignore
        self.app.inputs_frame.tabview.set("Funciones")  # type: ignore
        if mostrar:
            self.instances[2].tabview.set("Mostrar")  # type: ignore
        else:
            self.instances[2].tabview.set("Agregar")  # type: ignore

    def ir_a_input_sis(self, mostrar: bool):
        """
        Mostrar frame 'ManejarSistemas'.
        * mostrar: si se quiere seleccionar la tab de mostrar o no
        """

        self.app.nav_frame.seleccionar_frame("inputs")  # type: ignore
        self.app.inputs_frame.tabview.set("Sistemas de Ecuaciones")  # type: ignore
        if mostrar:
            self.instances[3].tabview.set("Mostrar")  # type: ignore
        else:
            self.instances[3].tabview.set("Agregar")  # type: ignore

    def update_all(self):
        """
        Llama al método update_all de cada instancia
        para que se encarguen de actualizar sus subframes.
        """

        for tab in self.instances:
            tab.update_all()
        self.tabview.configure(fg_color="transparent")


class ManejarMats(ctkFrame):
    """
    Frame que permite agregar, mostrar, y eliminar matrices.
    """

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

        self.instances: list[Union[AgregarMats, MostrarMats, EliminarMats]]

        self.tabs: list[
            tuple[str, Union[type[AgregarMats], type[MostrarMats], type[EliminarMats]]]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview para todos los
        subframes de inputs de matrices.
        """

        self.tabview = ctkTabview(self, fg_color="transparent")
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
                self.app, tab, self, self.mats_manager
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self):
        """
        Mandar a actualizar todos los subframes.
        """

        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")


class ManejarVecs(ctkFrame):
    """
    Frame que permite agregar, mostrar, y eliminar vectores.
    """

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

        self.instances: list[Union[AgregarVecs, MostrarVecs, EliminarVecs]]

        self.tabs: list[
            tuple[str, Union[type[AgregarVecs], type[MostrarVecs], type[EliminarVecs]]]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview para todos los
        subframes de inputs de vectores.
        """

        self.tabview = ctkTabview(self, fg_color="transparent")
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
                self.app, tab, self, self.vecs_manager
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self):
        """
        Mandar a actualizar todos los subframes.
        """

        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")


class ManejarFuncs(ctkFrame):
    """
    Frame que permite agregar, mostrar,
    y eliminar sistemas de ecuaciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: InputsFrame,
        func_manager: FuncManager,
    ) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager

        self.instances: list[Union[AgregarFuncs, MostrarFuncs, EliminarFuncs]]

        self.tabs: list[
            tuple[
                str, Union[type[AgregarFuncs], type[MostrarFuncs], type[EliminarFuncs]]
            ]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada subframe.
        """

        self.tabview = ctkTabview(self, fg_color="transparent")
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
                self.app, tab, self, self.func_manager
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self):
        """
        Manda a actualizar todos los subframes.
        """

        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")


class ManejarSistemas(ctkFrame):
    """
    Frame que permite agregar, mostrar,
    y eliminar sistemas de ecuaciones.
    """

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

        self.instances: list[Union[AgregarSistemas, MostrarSistemas, EliminarSistemas]]

        self.tabs: list[
            tuple[
                str,
                Union[
                    type[AgregarSistemas], type[MostrarSistemas], type[EliminarSistemas]
                ],
            ]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada subframe.
        """

        self.tabview = ctkTabview(self, fg_color="transparent")
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
                self.app, tab, self, self.mats_manager
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self):
        """
        Manda a actualizar todos los subframes.
        """

        for tab in self.instances:
            tab.update_frame()
        self.tabview.configure(fg_color="transparent")
