"""
Implementación de DerivadasFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

from re import compile as comp
from typing import (
    TYPE_CHECKING,
    Optional,
)

from tkinter import Variable
from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from ....msg_frame_funcs import (
    delete_msg_frame,
    place_msg_frame,
)

from ....util_funcs import generate_sep
from ....models import Func
from ....managers import FuncManager

from ...custom import (
    CustomDropdown,
    CustomScrollFrame,
)

if TYPE_CHECKING:
    from ... import GaussUI
    from .. import AnalisisFrame


class IntegralesFrame(CustomScrollFrame):
    """
    Frame que permite encontrar la integral de una función.
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
            variable=Variable(
                value="Seleccione una función para integrar:",
            ), values=self.nombres_funcs,
            command=self.mostrar_func,
        )

        self.func_select.grid(row=0, column=0, pady=5, sticky="n")

    def mostrar_func(self, nombre_func: str) -> None:
        """
        Muestra la función seleccionada en el dropdown,
        y crea un botón para encontrar la integral.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.winfo_children():  # type: ignore
            if dict(widget.grid_info()).get("row", -1) > 0:  # type: ignore
                widget.destroy()  # type: ignore

        self.func = self.func_manager.funcs_ingresadas[nombre_func]
        ctkLabel(
            self,
            text="",
            image=self.func.get_png(),
        ).grid(row=1, column=0, pady=(10, 5), sticky="n")

        ctkLabel(
            self,
            text="",
            image=generate_sep(False, (250, 5)),
        ).grid(row=2, column=0, sticky="n")

        ctkButton(
            self,
            height=30,
            text=f"Integrar {self.func.nombre}",
            command=self.encontrar_derivada,
        ).grid(row=3, column=0, ipadx=10, pady=5, sticky="n")

    def encontrar_derivada(self) -> None:
        """
        Encuentra y muestra la integral de la función seleccionada.
        """

        integral = self.func.integrar()
        try:
            match = list(comp(r"\^\(-\d+\)").finditer(self.func.nombre))[-1]
            num_ints = int(next(x for x in self.func.nombre if x.isdigit()))
            i_nombre = (
                self.func.nombre[:match.start()] +
                rf"^{{-{num_ints}}}" +
                self.func.nombre[match.end():]
            )
        except IndexError:
            i_nombre = self.func.nombre[0] + r"^{(-1)}" + self.func.nombre[1:]

        int_img = Func.latex_to_png(
            output_file=integral.nombre,
            nombre_expr=i_nombre,
            expr=str(integral.expr) + " + c",
            con_nombre=True,
            order=None,
        )

        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            img=int_img,
            tipo="resultado",
            row=4,
            pady=10,
            sticky="n",
        )

    def update_frame(self):
        """
        Configura todos los backgrounds de los widgets
        por si hubo un cambio de modo de apariencia.
        """

        delete_msg_frame(self.msg_frame)
        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.func_select.configure(values=self.nombres_funcs)

        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore
            if isinstance(widget, ctkFrame):
                for subwidget in widget.winfo_children():  # type: ignore
                    subwidget.configure(bg_color="transparent")  # type: ignore
