"""
Implementación de frame para resolver sistemas de ecuaciones lineales.
"""

from tkinter import Variable
from typing import TYPE_CHECKING

from customtkinter import CTkButton, CTkFrame, CTkLabel

from src.gui.custom import CustomDropdown
from src.gui.custom.adapted import CustomScrollFrame
from src.managers import MatricesManager
from src.utils import (
    delete_msg_frame,
    generate_sep,
    place_msg_frame,
    set_icon,
    toggle_proc,
)

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.frames import SistemasFrame
    from src.models import SistemaEcuaciones


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
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de sistemas de ecuaciones.
        """

        super().__init__(master_frame, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.msg_frame: CTkFrame | None = None
        self.metodos: dict[str, str] = {"Gauss-Jordan": "gj", "Regla de Cramer": "c"}

        # definir atributos, se inicializan en setup_frame
        self.select_sis_mat: CustomDropdown
        self.select_modo: CustomDropdown
        self.sis_mat: str = ""
        self.met: str = ""

        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar widgets del frame.
        """

        for widget in self.winfo_children():
            widget.destroy()

        self.select_sis_mat = CustomDropdown(
            self,
            width=40,
            values=self.master_frame.nombres_sistemas,
            variable=Variable(value="Seleccione sistema de ecuaciones a resolver:"),
            command=self.update_sis_mat,
        )

        self.select_metodo = CustomDropdown(
            self,
            width=40,
            variable=Variable(value="Seleccione método a utilizar:"),
            values=list(self.metodos.keys()),
            command=self.update_metodo,
        )

        self.select_sis_mat.grid(row=0, column=0, pady=(20, 10), sticky="n")
        self.select_metodo.grid(row=1, column=0, pady=10, sticky="n")

    def resolver(self) -> None:
        """
        Resolver sistema de ecuaciones seleccionado utilizando método seleccionado.
        """

        delete_msg_frame(self.msg_frame)
        self.update_sis_mat(self.select_sis_mat.get())

        sistema: SistemaEcuaciones
        met = self.metodos[self.met]

        # si es matriz cero, cambiar a gauss_jordan
        # para mostrar la explicacion del resultado
        if self.mats_manager.sis_ingresados[self.sis_mat].es_matriz_cero():
            met = "gj"

        try:
            sistema = self.mats_manager.resolver_sistema(self.sis_mat, met)
        except (ValueError, ArithmeticError, ZeroDivisionError) as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
                row=5,
                pady=10,
            )

            return

        delete_msg_frame(self.msg_frame)
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=sistema.solucion,
            tipo="error" if "!=" in sistema.solucion else "resultado",
            row=5,
            pady=10,
        )

        proc_text = (
            sistema.procedimiento
            if met == "gj"
            else sistema.procedimiento + sistema.solucion
        )

        CTkButton(
            self,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento para resolver "
                f"el sistema de ecuaciones {self.sis_mat} mediante "
                f"{'el método' if '−' in self.met else 'la'} {self.met}",
                proc_label=self.proc_label,
                label_txt=proc_text,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=6, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Actualizar frame y datos.
        """

        self.select_sis_mat.configure(
            values=self.master_frame.nombres_sistemas,
            variable=Variable(value="Seleccione el sistema de ecuaciones a resolver:"),
        )

        self.select_metodo.configure(
            values=list(self.metodos.keys()),
            variable=Variable(value="Seleccione el método a utilizar:"),
        )

        if not self.proc_hidden:
            set_icon(self.app, self.proc_label.master.master)  # type: ignore[reportArgumentType]

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
            if widget not in (self.select_metodo, self.select_sis_mat):
                widget.destroy()

    def update_sis_mat(self, valor: str) -> None:
        """
        Actualizar sistema de ecuaciones seleccionado.

        Args:
            valor: Sistema seleccionado.

        """

        self.sis_mat = valor
        delete_msg_frame(self.msg_frame)

        for widget in self.winfo_children():
            if widget.grid_info()["row"] > 0 and widget not in (
                self.select_sis_mat,
                self.select_metodo,
            ):
                widget.destroy()

        CTkLabel(self, text=str(self.mats_manager.sis_ingresados[self.sis_mat])).grid(
            row=1,
            column=0,
            pady=10,
            sticky="n",
        )

        CTkLabel(self, text="", image=generate_sep(False, (300, 3))).grid(
            row=2,
            column=0,
            sticky="n",
        )

        self.select_metodo.grid_configure(row=3)
        if "" not in (self.sis_mat, self.met):
            CTkButton(self, height=30, text="Resolver", command=self.resolver).grid(
                row=4,
                column=0,
                pady=5,
                sticky="n",
            )

    def update_metodo(self, valor: str) -> None:
        """
        Actualizar método seleccionado.

        Args:
            valor: Método seleccionado.

        """

        self.met = valor
        for widget in self.winfo_children():
            if widget.grid_info()["row"] > 4:
                widget.destroy()

        if "" not in (self.sis_mat, self.met):
            CTkButton(self, height=30, text="Resolver", command=self.resolver).grid(
                row=4,
                column=0,
                pady=5,
                sticky="n",
            )
