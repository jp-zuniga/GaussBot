"""
Implementación de todos los frames relacionados con vectores.
"""

from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from gauss_bot import INPUTS_ICON
from gauss_bot.managers import (
    MatricesManager,
    VectoresManager,
)

from gauss_bot.gui.custom import (
    CustomScrollFrame,
    ErrorFrame,
)

from gauss_bot.gui.frames.subframes import (
    VSumaRestaTab,
    VMultiplicacionTab,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


class VectoresFrame(ctkFrame):
    """
    Frame que contiene un ctkTabview para todas
    las funcionalidades de vectores, donde cada
    una tiene su propia tab.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        vecs_manager: VectoresManager,
        mats_manager: MatricesManager,
    ) -> None:

        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.vecs_manager = vecs_manager
        self.mats_manager = mats_manager

        self.dummy_frame: ctkFrame
        self.mensaje_frame: Optional[ctkFrame] = None
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        self.instances: list[
            Union[
                VSumaRestaTab,
                VMultiplicacionTab,
            ]
        ] = []

        self.tabs: list[
            tuple[
                str,
                Union[
                    type[VSumaRestaTab],
                    type[VMultiplicacionTab],
                ]
            ]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un ctkTabview con pestañas para cada funcionalidad.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if len(self.nombres_vectores) == 0:
            self.dummy_frame = ctkFrame(self, fg_color="transparent")
            self.mensaje_frame = ErrorFrame(self.dummy_frame, message="No hay vectores ingresados!")
            agregar_button = ctkButton(
                self.dummy_frame,
                height=30,
                text="Agregar vectores",
                image=INPUTS_ICON,
                command=lambda: self.app.home_frame.ir_a_vector(mostrar=False),  # type: ignore
            )

            self.dummy_frame.pack(expand=True, anchor="center")
            self.mensaje_frame.pack(pady=5, anchor="center")
            agregar_button.pack(pady=5, anchor="center")
            return

        if self.mensaje_frame is not None:
            for widget in self.winfo_children():
                widget.destroy()
            self.mensaje_frame = None

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        self.tabs = [
            ("Suma y Resta", VSumaRestaTab),
            ("Multiplicación", VMultiplicacionTab),
        ]

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = cls(
                self.app, tab, self, self.vecs_manager
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self) -> None:
        """
        Actualiza los datos de todos los frames del tabview.
        """

        self.mats_manager.mats_ingresadas = {
            nombre: mat
            for nombre, mat in sorted(self.mats_manager.mats_ingresadas.items())
        }

        self.vecs_manager.vecs_ingresados = {
            nombre: vec
            for nombre, vec in sorted(self.vecs_manager.vecs_ingresados.items())
        }

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        if (self.mensaje_frame is not None
            or len(self.nombres_vectores) == 0
            or self.instances == []):
            self.setup_tabview()
            return

        for tab in self.instances:
            tab.update_frame()  # type: ignore
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
