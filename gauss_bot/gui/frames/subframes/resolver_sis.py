"""
Implementación de SistemasFrame, el frame que
resuelve sistemas de ecuaciones lineales.
"""

from typing import (
    TYPE_CHECKING,
    Optional,
)

from tkinter import Variable
from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
)

from ....msg_frame_funcs import (
    delete_msg_frame,
    place_msg_frame,
)

from ....models import SistemaEcuaciones
from ....managers import MatricesManager
from ...custom import (
    CustomDropdown,
    CustomScrollFrame,
)

if TYPE_CHECKING:
    from ... import GaussUI
    from .. import SistemasFrame


class ResolverSisFrame(CustomScrollFrame):
    """
    Frame que permite al usuario seleccionar un sistema
    de ecuaciones ingresado y resolverlo utilizando el
    método Gauss-Jordan o la regla de Cramer.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_frame: "SistemasFrame",
        mats_manager: MatricesManager,
    ) -> None:

        super().__init__(master_frame, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.msg_frame: Optional[ctkFrame] = None
        self.metodos: dict[str, str ] = {
            "Gauss−Jordan": "gj",
            "Regla de Cramer": "c",
            # "Factorización LU": "f",
        }

        # definir atributos, se inicializan en setup_frame
        self.select_sis_mat: CustomDropdown
        self.select_modo: CustomDropdown
        self.sis_mat = ""
        self.met = ""

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializa y configura el frame.
        Se encarga de mostrar mensaje de error si
        no hay sistemas de ecuaciones ingresados.
        """

        for widget in self.winfo_children():
            widget.destroy()  # type: ignore

        self.select_sis_mat = CustomDropdown(
            self,
            width=40,
            variable=Variable(
                value="Seleccione el sistema de ecuaciones a resolver:"
            ), values=self.master_frame.nombres_sistemas,
            command=self.update_sis_mat,
        )

        self.select_metodo = CustomDropdown(
            self,
            width=40,
            variable=Variable(value="Seleccione el método a utilizar:"),
            values=list(self.metodos.keys()),
            command=self.update_metodo,
        )

        self.select_sis_mat.grid(row=0, column=0, padx=5, pady=(40, 5), sticky="n")
        self.select_metodo.grid(row=1, column=0, padx=5, pady=5, sticky="n")

    def resolver(self) -> None:
        """
        Resuelve el sistema de ecuaciones seleccionado
        por el usuario, utilizando el método indicado.
        """

        delete_msg_frame(self.msg_frame)
        self.update_sis_mat(self.select_sis_mat.get())  # type: ignore

        sistema: SistemaEcuaciones
        met = self.metodos[self.met]

        # si es matriz cero, cambiar a gauss_jordan
        # para mostrar la explicacion del resultado
        if self.mats_manager.sis_ingresados[self.sis_mat].es_matriz_cero():
            met = "gj"

        if len(self.sis_mat) > 1:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="Debe seleccionar un sistema de ecuaciones!",
                tipo="error",
                row=5,
            )

        if met == "gj":
            sistema = (
                self.mats_manager.resolver_sistema(self.sis_mat, met)
            )
        elif met == "c":
            try:
                sistema = (
                    self.mats_manager.resolver_sistema(self.sis_mat, met)
                )
            except (ValueError, ArithmeticError, ZeroDivisionError) as e:
                self.msg_frame = place_msg_frame(
                    parent_frame=self,
                    msg_frame=self.msg_frame,
                    msg=str(e),  # type: ignore
                    tipo="error",
                    row=5,
                )

                return

        delete_msg_frame(self.msg_frame)
        if "!=" in sistema.solucion:  # type: ignore
            # si el sistema es inconsistente, habria un != en la solucion
            # entonces se muestra el resultado con un borde rojo
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg=sistema.solucion,  # type: ignore
                tipo="resultado",
                border_color="#ff3131",
                row=5,
            )

            return

        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=sistema.solucion,  # type: ignore
            tipo="resultado",
            row=5,
        )

    def update_frame(self) -> None:
        """
        Actualizar el frame y sus datos.
        """

        self.select_sis_mat.configure(
            variable=Variable(
                value="Seleccione el sistema de ecuaciones a resolver:"
            ), values=self.master_frame.nombres_sistemas,
        )

        self.select_sis_mat.configure(
            variable=Variable(
                value="Seleccione el método a utilizar:"
            ), values=list(self.metodos.keys()),
        )

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore

    def update_sis_mat(self, valor: str) -> None:
        """
        Actualiza self.sis_mat con la opción
        seleccionada en el dropdown.
        """

        self.sis_mat = valor
        if len(self.sis_mat) == 1 and len(self.met) > 1:
            ctkButton(
                self,
                height=30,
                text="Resolver",
                command=self.resolver
            ).grid(row=2, column=0, pady=5, padx=5, sticky="n")

    def update_metodo(self, valor: str) -> None:
        """
        Actualiza self.met con la opción
        seleccionada en el dropdown.
        """

        self.met = valor
        if len(self.sis_mat) == 1 and len(self.met) > 1:
            ctkButton(
                self,
                height=30,
                text="Resolver",
                command=self.resolver
            ).grid(row=2, column=0, pady=5, padx=5, sticky="n")
