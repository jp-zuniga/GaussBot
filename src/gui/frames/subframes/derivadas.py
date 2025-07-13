"""
Implementación de frame de derivadas de funciones.
"""

from tkinter import Variable
from typing import TYPE_CHECKING

from customtkinter import CTkButton, CTkFrame, CTkLabel

from src.gui.custom import CustomDropdown
from src.gui.custom.adapted import CustomScrollFrame
from src.managers import FuncManager
from src.models import Func
from src.utils import delete_msg_frame, generate_sep, place_msg_frame

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.frames import AnalisisFrame


class DerivadasFrame(CustomScrollFrame):
    """
    Frame para derivar funciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "AnalisisFrame",
        func_manager: FuncManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de derivadas.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.msg_frame: CTkFrame | None = None

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
        Mostrar función seleccionada y crear botón para derivar.

        Args:
            nombre_func: Función seleccionada.

        """

        delete_msg_frame(self.msg_frame)
        for widget in self.winfo_children():
            if dict(widget.grid_info()).get("row", -1) > 0:
                widget.destroy()

        self.func = self.func_manager.funcs_ingresadas[nombre_func]
        CTkLabel(self, text="", image=self.func.get_png()).grid(
            row=1,
            column=0,
            pady=(10, 5),
            sticky="n",
        )

        CTkLabel(self, text="", image=generate_sep(False, (250, 5))).grid(
            row=2,
            column=0,
            sticky="n",
        )

        CTkButton(
            self,
            height=30,
            text=f"Derivar {self.func.nombre}",
            command=self.encontrar_derivada,
        ).grid(row=3, column=0, ipadx=10, pady=5, sticky="n")

    def encontrar_derivada(self) -> None:
        """
        Derivar la función seleccionada y mostrar el resultado.
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
            row=4,  # type: ignore[reportArgumentType]
            pady=10,  # type: ignore[reportArgumentType]
        )

    def update_frame(self) -> None:
        """
        Actualizar colores de widgets.
        """

        delete_msg_frame(self.msg_frame)
        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.func_select.configure(
            values=self.nombres_funcs,
            variable=Variable(value="Seleccione una función para derivar:"),
        )

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
            if dict(widget.grid_info()).get("row", -1) > 0:
                widget.destroy()
