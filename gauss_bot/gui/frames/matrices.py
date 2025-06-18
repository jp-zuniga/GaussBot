"""
Implementación de MatricesFrame, el parent frame
de todos los subframes relacionados con matrices.
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

from .subframes import (
    DeterminanteTab,
    InversaTab,
    MultiplicacionTab,
    SumaRestaTab,
    TransposicionTab,
)
from ..custom import (
    CustomScrollFrame,
    ErrorFrame,
)
from ...managers import (
    MatricesManager,
    VectoresManager,
)
from ...utils import INPUTS_ICON

if TYPE_CHECKING:
    from .. import GaussUI


class MatricesFrame(ctkFrame):
    """
    Frame principal para la sección de matrices.
    Contiene un tabview con todas las operaciones disponibles.
    """

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

        self.dummy_frame: ctkFrame  # para pack mensaje de error inicial
        self.msg_frame: Optional[ctkFrame] = None
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        self.instances: list[
            Union[
                SumaRestaTab,
                MultiplicacionTab,
                DeterminanteTab,
                TransposicionTab,
                InversaTab,
            ]
        ]

        self.tabs: list[
            tuple[
                str,
                Union[
                    type[SumaRestaTab],
                    type[MultiplicacionTab],
                    type[DeterminanteTab],
                    type[TransposicionTab],
                    type[InversaTab],
                ],
            ]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada operación con matrices.
        Se encarga de validar si hay matrices ingresadas para que
        los setups de los frames individuales no lo tengan que hacer.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if len(self.nombres_matrices) == 0:
            # si no hay matrices guardadas, mostrar mensaje de error y
            # agregar boton para dirigir al usuario adonde se agregan
            self.dummy_frame = ctkFrame(self, fg_color="transparent")
            self.msg_frame = ErrorFrame(
                self.dummy_frame,
                msg="No se ha guardado ninguna matriz!",
            )

            agregar_button = ctkButton(
                self.dummy_frame,
                height=30,
                text="Agregar matrices",
                image=INPUTS_ICON,
                command=lambda: (
                    self.app.inputs_frame.ir_a_input_mats(mostrar=False)  # type: ignore
                ),
            )

            self.dummy_frame.pack(expand=True, anchor="center")
            self.msg_frame.pack(pady=5, anchor="center")
            agregar_button.pack(pady=5, anchor="center")
            return

        # cleanup mensaje de error si todavia existe
        if self.msg_frame is not None:
            for widget in self.winfo_children():
                widget.destroy()
            self.msg_frame = None

        self.tabview = ctkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        self.tabs = [
            ("Suma y Resta", SumaRestaTab),
            ("Multiplicación", MultiplicacionTab),
            ("Calcular Determinante", DeterminanteTab),
            ("Transposición", TransposicionTab),
            ("Encontrar Inversa", InversaTab),
        ]

        # iterar sobre self.tabs para:
        # * agregar tabs al tabview
        # * inicializar los frames de cada tab
        # * añadir los frames a self.instances
        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = cls(
                self.app, tab, self, self.mats_manager
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self) -> None:
        """
        Actualiza todos los frames del tabview.
        """

        # sortear los diccionarios de datos para que esten alfabetizados
        self.mats_manager.mats_ingresadas = dict(
            sorted(self.mats_manager.mats_ingresadas.items())
        )

        self.vecs_manager.vecs_ingresados = dict(
            sorted(self.vecs_manager.vecs_ingresados.items())
        )

        # actualizar los atributos de nombres despues que cambiaron los dicts
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        if (
            self.msg_frame is not None
            or len(self.nombres_matrices) == 0
            or self.instances == []
        ):
            # si hay un mensaje de error,
            # o no hay matrices ingresadas,
            # o no se han inicializado los frames,
            # correr el setup
            self.setup_tabview()
            return

        # si no, actualizar todos los subframes
        for tab in self.instances:
            tab.update_frame()
