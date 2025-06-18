"""
Implementación de ConfigFrame, encargado de mostrar
y editar las configuraciones de la aplicación.
"""

from tkinter import StringVar
from typing import (
    TYPE_CHECKING,
    Optional,
)

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    set_appearance_mode as set_mode,
    set_widget_scaling as set_scaling,
)

from ..custom import (
    CustomDropdown,
    SuccessFrame,
)
from ...utils import get_dict_key

if TYPE_CHECKING:
    from .. import GaussUI


class ConfigFrame(ctkFrame):
    """
    Frame personalizado para mostrar y editar la configuración.
    """

    def __init__(self, app: "GaussUI", master: "GaussUI") -> None:
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.msg_frame: Optional[SuccessFrame] = None

        self.escalas_dict = {
            "100%": 1.0,
            "110%": 1.1,
            "120%": 1.2,
            "130%": 1.3,
            "140%": 1.4,
            "150%": 1.5,
            "160%": 1.6,
            "170%": 1.7,
            "180%": 1.8,
            "190%": 1.9,
            "200%": 2.0,
        }

        self.modos_dict = {
            "Claro": "light",
            "Oscuro": "dark",
        }

        self.temas_dict = {
            "Cerúleo": "ceruleo.json",
            "Verdeante": "verdeante.json",
            "Viento": "viento.json",
        }

        self.escalas = list(self.escalas_dict.keys())
        self.modos = list(self.modos_dict.keys())
        self.temas = list(self.temas_dict.keys())

        self.tema_anterior: Optional[str] = None

        # buscar las llaves de la configuracion actual
        escala_actual_key = get_dict_key(self.escalas_dict, self.app.escala_actual)
        modo_actual_key = get_dict_key(self.modos_dict, self.app.modo_actual)
        tema_actual_key = get_dict_key(self.temas_dict, self.app.tema_actual)

        try:
            # inicializar variables de config actual
            first_escala = StringVar(value=escala_actual_key)
            first_modo = StringVar(value=modo_actual_key)
            first_tema = StringVar(value=tema_actual_key)
        except AttributeError:
            # si get_dict_key() retorna None, StringVar va a tirar error,
            # entonces se inicializan con valores por defecto
            first_escala = StringVar(value="100%")
            first_modo = StringVar(value="Claro")
            first_tema = StringVar(value="Sky")

        # crear labels
        self.escala_label = ctkLabel(self, text="Escala:")
        self.modos_label = ctkLabel(self, text="Modo:")
        self.temas_label = ctkLabel(self, text="Tema:")

        # crear dropdowns
        self.desplegar_escalas = CustomDropdown(
            self,
            width=105,
            values=self.escalas,
            variable=first_escala,
            command=self.cambiar_escala,
        )

        self.desplegar_modos = CustomDropdown(
            self,
            width=105,
            values=self.modos,
            variable=first_modo,
            command=self.cambiar_modo,
        )

        self.desplegar_temas = CustomDropdown(
            self,
            width=105,
            values=self.temas,
            variable=first_tema,
            command=self.cambiar_tema,
        )

        # colocar widgets
        self.escala_label.grid(
            row=0, column=0, padx=(30, 10), pady=(20, 10), sticky="nw"
        )

        self.desplegar_escalas.grid(
            row=0, column=1, padx=10, pady=(20, 10), sticky="nw"
        )

        self.modos_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="nw")
        self.desplegar_modos.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        self.temas_label.grid(row=2, column=0, padx=(30, 10), pady=10, sticky="nw")
        self.desplegar_temas.grid(row=2, column=1, padx=10, pady=10, sticky="nw")

    def cambiar_escala(self, escala_seleccionada: str) -> None:
        """
        Cambia la escala actual de la aplicación a la indicado.
        """

        if self.escalas_dict[escala_seleccionada] == self.app.escala_actual:
            # si selecciono la misma escala, no cambiar nada
            return

        self.app.escala_actual = self.escalas_dict[escala_seleccionada]
        set_scaling(self.app.escala_actual)

        if self.app.nav_frame.hidden:
            self.app.nav_frame.app_name.grid_remove()
            self.app.nav_frame.hide_button.grid_configure(
                column=1,
                columnspan=1,
                sticky="e",
            )

        else:
            self.app.nav_frame.app_name.grid()
            self.app.nav_frame.hide_button.grid_configure(
                column=0,
                columnspan=2,
                sticky="n",
            )

    def cambiar_modo(self, modo_seleccionado: str) -> None:
        """
        Cambia el modo actual de apariencia de la aplicación al indicado.
        """

        if self.modos_dict[modo_seleccionado] == self.app.modo_actual:
            # si se selecciono el mismo, no cambiar nada
            return

        self.app.modo_actual = self.modos_dict[modo_seleccionado]
        set_mode(self.app.modo_actual)

        # mandar a actualizar todo
        self.app.set_icon(self.app.modo_actual)
        self.app.home_frame.update_frame()  # type: ignore
        self.app.inputs_frame.update_all()  # type: ignore
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore
        self.app.analisis.update_all()  # type: ignore
        self.app.sistemas.update_all()  # type: ignore
        self.update_frame()

    def cambiar_tema(self, tema_seleccionado: str) -> None:
        """
        Cambia el tema actual de la aplicación al indicado.
        """

        if self.temas_dict[tema_seleccionado] == self.app.tema_actual:
            # si se selecciono el mismo tema, no cambiar nada
            return

        self.tema_anterior, self.app.tema_actual = (
            self.app.tema_actual,
            self.temas_dict[tema_seleccionado],
        )

        # explicar que se necesita reiniciar la app
        self.msg_frame = SuccessFrame(
            self,
            msg="Tema cambiado exitosamente!\n"
            + "El cambio tomará efecto al reiniciar la aplicación.",
        )

        self.msg_frame.grid(row=3, column=1, padx=10, pady=20)

    def update_frame(self) -> None:
        """
        Configura los backgrounds de los widgets,
        por si hubo un cambio de tema.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
