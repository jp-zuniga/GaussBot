"""
Implementación de SistemasFrame,
el frame que resuelve sistemas de ecuaciones lineales.
"""

from typing import (
    TYPE_CHECKING,
    Optional,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkCheckBox as ctkCheckBox,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from gauss_bot import delete_msg_frame
from gauss_bot.models import SistemaEcuaciones
from gauss_bot.managers import MatricesManager
from gauss_bot.gui.custom import (
    CustomDropdown,
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


class SistemasFrame(CustomScrollFrame):
    """
    Frame que permite al usuario seleccionar un sistema
    de ecuaciones ingresado y resolverlo utilizando el
    método Gauss-Jordan o la regla de Cramer.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.mensaje_frame: Optional[ctkFrame] = None

        self.select_sis_mat: CustomDropdown
        self.gauss_jordan_checkbox: ctkCheckBox
        self.cramer_checkbox: ctkCheckBox
        self.sis_mat = ""

        self.gauss_jordan = False
        self.cramer = False

        self.setup_frame()

    def setup_frame(self) -> None:
        if not self.check_matrices():
            return
        delete_msg_frame(self.mensaje_frame)
        self.rowconfigure(0, weight=0)

        instruct_se = ctkLabel(self, text="Seleccione el sistema de ecuaciones a resolver:")
        self.select_sis_mat = CustomDropdown(
            self,
            width=60,
            values=self.nombres_sistemas,
            command=self.update_sis_mat,
        )

        self.gauss_jordan_checkbox = ctkCheckBox(self, text="", command=self.toggle_gj)
        gauss_jordan_label = ctkLabel(self, text="Método Gauss-Jordan")

        self.cramer_checkbox = ctkCheckBox(self, text="", command=self.toggle_cramer)
        cramer_label = ctkLabel(self, text="Regla de Cramer")
        button = ctkButton(self, height=30, text="Resolver", command=self.resolver)

        self.sis_mat = self.select_sis_mat.get()
        self.gauss_jordan = False
        self.cramer = False

        instruct_se.grid(row=0, column=0, columnspan=2, pady=(10, 5), padx=5, sticky="ew")
        self.select_sis_mat.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        self.gauss_jordan_checkbox.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        gauss_jordan_label.grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.cramer_checkbox.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        cramer_label.grid(row=3, column=0, pady=5, padx=5, sticky="e")
        button.grid(row=4, column=0, columnspan=2, pady=5, padx=5)

    def resolver(self) -> None:
        """
        Resuelve el sistema de ecuaciones seleccionado
        por el usuario, utilizando el método indicado.
        """

        delete_msg_frame(self.mensaje_frame)
        self.update_sis_mat(self.select_sis_mat.get())  # type: ignore

        if all([self.gauss_jordan, self.cramer]):
            self.mensaje_frame = ErrorFrame(
                self, "Solamente debe seleccionar un método para resolver el sistema!"
            )
            self.mensaje_frame.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return
        if not any([self.gauss_jordan, self.cramer]):
            self.mensaje_frame = ErrorFrame(
                self, "Debe seleccionar un método para resolver el sistema!"
            )
            self.mensaje_frame.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        sistema: Optional[SistemaEcuaciones] = None
        if self.mats_manager.sis_ingresados[self.sis_mat].es_matriz_cero():
            self.gauss_jordan = True
            self.cramer = False

        if self.gauss_jordan:
            sistema = (
                self.mats_manager.resolver_sistema(self.sis_mat, "gj")
            )
        elif self.cramer:
            try:
                sistema = (
                    self.mats_manager.resolver_sistema(self.sis_mat, "c")
                )
            except (ValueError, ArithmeticError, ZeroDivisionError) as e:
                self.mensaje_frame = ErrorFrame(self, str(e))
                self.mensaje_frame.grid(
                    row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5
                )
                return

        delete_msg_frame(self.mensaje_frame)
        if "!=" in sistema.solucion:  # type: ignore
            self.mensaje_frame = ResultadoFrame(
                self, header=sistema.solucion,  # type: ignore
                resultado="", solo_header=True,
                border_color="#ff3131"
            )
        else:
            self.mensaje_frame = ResultadoFrame(
                self, header=sistema.solucion,  # type: ignore
                resultado="", solo_header=True
            )
        self.mensaje_frame.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)

    def toggle_gj(self) -> None:
        self.gauss_jordan = not self.gauss_jordan

    def toggle_cramer(self) -> None:
        self.cramer = not self.cramer

    def check_matrices(self, mostrar_error=True) -> bool:
        if len(self.nombres_sistemas) == 0:
            if mostrar_error:
                self.display_error()
            return False
        return True

    def display_error(self) -> None:
        self.rowconfigure(0, weight=1)
        self.mensaje_frame = ErrorFrame(self, "No hay sistemas de ecuaciones ingresados!")
        self.mensaje_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    def update_frame(self) -> None:
        # sortear los sistemas para que esten alfabetizados
        self.mats_manager.sis_ingresados = dict(
            sorted(
                self.mats_manager.sis_ingresados.items()
            )
        )

        # actualizar el atributo de nombres despues de cambiar el dict
        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())

        if isinstance(self.mensaje_frame, ErrorFrame):
            for widget in self.winfo_children():
                widget.destroy()  # type: ignore
            self.setup_frame()
        elif not self.check_matrices(mostrar_error=False):
            for widget in self.winfo_children():
                widget.destroy()  # type: ignore
            self.check_matrices(mostrar_error=True)
        else:
            self.select_sis_mat.configure(values=self.nombres_sistemas)
            for widget in self.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore

    def update_sis_mat(self, valor: str) -> None:
        self.sis_mat = valor
