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
    CTkFont as ctkFont,
    CTkLabel as ctkLabel,
    CTkToplevel as ctkTop,
)

from ....icons import APP_ICON
from ....util_funcs import generate_sep
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
        }

        # definir atributos, se inicializan en setup_frame
        self.select_sis_mat: CustomDropdown
        self.select_modo: CustomDropdown
        self.sis_mat = ""
        self.met = ""

        self.proc_label: ctkLabel
        self.proc_hidden = True

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
            values=self.master_frame.nombres_sistemas,
            variable=Variable(
                value="Seleccione el sistema de ecuaciones a resolver:"
            ),
            command=self.update_sis_mat,
        )

        self.select_metodo = CustomDropdown(
            self,
            width=40,
            variable=Variable(value="Seleccione el método a utilizar:"),
            values=list(self.metodos.keys()),
            command=self.update_metodo,
        )

        self.select_sis_mat.grid(row=0, column=0, pady=(20, 10), sticky="n")
        self.select_metodo.grid(row=1, column=0, pady=10, sticky="n")

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
                    pady=10,
                )

                return

        delete_msg_frame(self.msg_frame)
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=sistema.solucion,  # type: ignore
            tipo="error" if "!=" in sistema.solucion else "resultado",
            row=5,
            pady=10,
        )

        lambda_proc = (
            sistema.procedimiento
            if met == "gj"
            else sistema.procedimiento + sistema.solucion
        )

        ctkButton(
            self,
            text="Mostrar procedimiento",
            command=lambda: self.toggle_proc(lambda_proc),
        ).grid(row=6, column=0, pady=5, sticky="n")

    def toggle_proc(self, procedimiento: str) -> None:
        """
        Muestra o esconde la ventana de procedimiento.
        """

        if not self.proc_hidden:
            return

        new_window = ctkTop(self.app)
        new_window.title(
            "GaussBot: Procedimiento para resolver " +
           f"el sistema de ecuaciones '{self.sis_mat}' mediante " +
           f"{"el método" if "−" in self.met else "la"} {self.met}"
        )

        new_window.geometry("400x800")
        self.after(100, new_window.focus)  # type: ignore

        if self.app.modo_actual == "dark":
            i = 0
        elif self.app.modo_actual == "light":
            i = 1

        self.after(
            250,
            lambda: new_window.iconbitmap(APP_ICON[i]),  # pylint: disable=E0606
        )

        new_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: delete_window(new_window),
        )

        dummy_frame = ctkFrame(
            new_window,
            fg_color="transparent",
            corner_radius=20,
            border_width=3,
        )

        dummy_frame.pack(expand=True, fill="both", padx=20, pady=20)
        proc_frame = CustomScrollFrame(
            dummy_frame,
            fg_color="transparent",
        )

        proc_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.proc_label = ctkLabel(
            proc_frame,
            text=procedimiento.strip(),
            font=ctkFont(size=14),
        )

        self.proc_label.pack(expand=True, fill="both", padx=10, pady=10)
        self.proc_hidden = False

        def delete_window(new_window: ctkTop) -> None:
            self.proc_hidden = True
            new_window.destroy()

    def update_frame(self) -> None:
        """
        Actualizar el frame y sus datos.
        """

        self.select_sis_mat.configure(
            values=self.master_frame.nombres_sistemas,
            variable=Variable(
                value="Seleccione el sistema de ecuaciones a resolver:"
            ),
        )

        self.select_metodo.configure(
            values=list(self.metodos.keys()),
            variable=Variable(
                value="Seleccione el método a utilizar:"
            ),
        )

        if not self.proc_hidden:
            if self.app.modo_actual == "dark":
                self.after(
                    250,
                    lambda: self.proc_label.master.master.iconbitmap(APP_ICON[1]),  # type: ignore
                )
            elif self.app.modo_actual == "light":
                self.after(
                    250,
                    lambda: self.proc_label.master.master.iconbitmap(APP_ICON[0]),  # type: ignore
                )

        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore
            if widget not in (self.select_metodo, self.select_sis_mat):
                widget.destroy()  # type: ignore

    def update_sis_mat(self, valor: str) -> None:
        """
        Actualiza self.sis_mat con la opción
        seleccionada en el dropdown.
        """

        self.sis_mat = valor
        delete_msg_frame(self.msg_frame)

        for widget in self.winfo_children():  # type: ignore
            if (
                widget.grid_info()["row"] > 0
                and
                widget not in (self.select_sis_mat, self.select_metodo)
            ):
                widget.destroy()  # type: ignore

        ctkLabel(
            self,
            text=str(self.mats_manager.sis_ingresados[self.sis_mat]),
        ).grid(row=1, column=0, pady=10, sticky="n")

        ctkLabel(
            self,
            text="",
            image=generate_sep(False, (300, 3)),
        ).grid(row=2, column=0, sticky="n")

        self.select_metodo.grid_configure(row=3)
        if "" not in (self.sis_mat, self.met):
            ctkButton(
                self,
                height=30,
                text="Resolver",
                command=self.resolver,
            ).grid(row=4, column=0, pady=5, sticky="n")

    def update_metodo(self, valor: str) -> None:
        """
        Actualiza self.met con la opción
        seleccionada en el dropdown.
        """

        self.met = valor
        for widget in self.winfo_children():  # type: ignore
            if widget.grid_info()["row"] > 4:
                widget.destroy()  # type: ignore

        if "" not in (self.sis_mat, self.met):
            ctkButton(
                self,
                height=30,
                text="Resolver",
                command=self.resolver,
            ).grid(row=4, column=0, pady=5, sticky="n")
