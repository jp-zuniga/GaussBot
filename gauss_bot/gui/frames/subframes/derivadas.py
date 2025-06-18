"""
Implementación de DerivadasFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

from tkinter import Variable
from typing import TYPE_CHECKING, Optional

from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from ...custom import CustomDropdown, CustomScrollFrame
from ....managers import FuncManager
from ....models import Func
from ....utils import delete_msg_frame, generate_sep, place_msg_frame

if TYPE_CHECKING:
    from .. import AnalisisFrame
    from ... import GaussUI


class DerivadasFrame(CustomScrollFrame):
    """
    Frame que permite encontrar la derivada de una función.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "AnalisisFrame",
        func_manager: FuncManager,
    ) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.msg_frame: Optional[ctkFrame] = None

        self.func: Func
        self.func_select = CustomDropdown(
            self,
            width=40,
            variable=Variable(value="Seleccione una función para derivar:"),
            values=self.nombres_funcs,
            command=self.mostrar_func,
        )

        self.func_select.grid(row=0, column=0, pady=5, sticky="n")

    def mostrar_func(self, nombre_func: str) -> None:
        """
        Muestra la función seleccionada en el dropdown,
        y crea un botón para encontrar la derivada.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.winfo_children():  # type: ignore
            if dict(widget.grid_info()).get("row", -1) > 0:  # type: ignore
                widget.destroy()  # type: ignore

        self.func = self.func_manager.funcs_ingresadas[nombre_func]
        ctkLabel(self, text="", image=self.func.get_png()).grid(
            row=1, column=0, pady=(10, 5), sticky="n"
        )

        ctkLabel(self, text="", image=generate_sep(False, (250, 5))).grid(
            row=2, column=0, sticky="n"
        )

        ctkButton(
            self,
            height=30,
            text=f"Derivar {self.func.nombre}",
            command=self.encontrar_derivada,
        ).grid(row=3, column=0, ipadx=10, pady=5, sticky="n")

    def encontrar_derivada(self) -> None:
        """
        Encuentra y muestra la derivada de
        la función seleccionada.
        """

        derivada = self.func.derivar()
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            img=Func.latex_to_png(
                output_file=derivada.nombre,
                nombre_expr=derivada.get_di_nombre(diffr=True),
                expr=str(derivada.expr),
                con_nombre=True,
            ),
            tipo="resultado",
            row=4,
            pady=10,
        )

    def update_frame(self):
        """
        Configura todos los backgrounds de los widgets
        por si hubo un cambio de modo de apariencia.
        """

        delete_msg_frame(self.msg_frame)
        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.func_select.configure(
            values=self.nombres_funcs,
            variable=Variable(value="Seleccione una función para derivar:"),
        )

        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore
            if dict(widget.grid_info()).get("row", -1) > 0:
                widget.destroy()
