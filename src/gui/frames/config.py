"""
Implementación de ConfigFrame, encargado de mostrar
y editar las configuraciones de la aplicación.
"""

from decimal import getcontext
from tkinter import StringVar
from typing import TYPE_CHECKING, Optional

from bidict import bidict
from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    set_appearance_mode as set_mode,
)

from ..custom import CustomDropdown, SuccessFrame
from ... import FRAC_PREC
from ...utils import delete_msg_frame, place_msg_frame, set_icon

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

        self.escalas_dict: bidict[str, float] = bidict(
            {
                "80%": 0.8,
                "90%": 0.9,
                "100%": 1.0,
                "110%": 1.1,
                "120%": 1.2,
                "130%": 1.3,
                "140%": 1.4,
                "150%": 1.5,
                "160%": 1.6,
                "170%": 1.7,
                "180%": 1.8,
            }
        )

        self.modos_dict: bidict[str, str] = bidict({"Claro": "light", "Oscuro": "dark"})
        self.temas_dict: bidict[str, str] = bidict(
            {
                "Primavera": "primavera.json",
                "Verano": "verano.json",
                "Otoño": "otono.json",
                "Invierno": "invierno.json",
            }
        )

        self.frac_prec_dict: bidict[str, int] = bidict(
            {
                "Denominador máximo de 100": 100,
                "Denominador máximo de 500": 500,
                "Denominador máximo de 1000": 1000,
            }
        )

        self.dec_prec_dict: bidict[str, int] = bidict(
            {"3 decimales": 3, "6 decimales": 6, "9 decimales": 9}
        )

        self.escalas = list(self.escalas_dict.keys())
        self.modos = list(self.modos_dict.keys())
        self.temas = list(self.temas_dict.keys())
        self.frac_precs = list(self.frac_prec_dict.keys())
        self.dec_precs = list(self.dec_prec_dict.keys())

        first_escala = StringVar(
            value=self.escalas_dict.inverse[self.app.escala_actual]
        )

        first_modo = StringVar(value=self.modos_dict.inverse[self.app.modo_actual])
        first_tema = StringVar(value=self.temas_dict.inverse[self.app.tema_actual])
        first_frac_prec = StringVar(
            value=self.frac_prec_dict.inverse[self.app.frac_prec_actual]
        )

        first_dec_prec = StringVar(
            value=self.dec_prec_dict.inverse[self.app.dec_prec_actual]
        )

        # crear labels
        self.escala_label = ctkLabel(self, text="Escala:")
        self.modos_label = ctkLabel(self, text="Modo:")
        self.temas_label = ctkLabel(self, text="Tema:")
        self.frac_precs_label = ctkLabel(self, text="Precisión fraccional:")
        self.dec_precs_label = ctkLabel(self, text="Precisión decimal:")

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

        self.desplegar_frac_precs = CustomDropdown(
            self,
            width=105,
            values=self.frac_precs,
            variable=first_frac_prec,
            command=self.cambiar_frac_prec,
        )

        self.desplegar_dec_precs = CustomDropdown(
            self,
            width=105,
            values=self.dec_precs,
            variable=first_dec_prec,
            command=self.cambiar_dec_prec,
        )

        # colocar widgets
        self.frac_precs_label.grid(
            row=0, column=0, padx=(30, 5), pady=(20, 5), sticky="nw"
        )
        self.desplegar_frac_precs.grid(
            row=0, column=1, padx=5, pady=(20, 5), sticky="nw"
        )
        self.dec_precs_label.grid(row=1, column=0, padx=(30, 5), pady=5, sticky="nw")
        self.desplegar_dec_precs.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
        self.escala_label.grid(row=2, column=0, padx=(30, 5), pady=5, sticky="nw")
        self.desplegar_escalas.grid(row=2, column=1, padx=5, pady=5, sticky="nw")
        self.modos_label.grid(row=3, column=0, padx=(30, 5), pady=5, sticky="nw")
        self.desplegar_modos.grid(row=3, column=1, padx=5, pady=5, sticky="nw")
        self.temas_label.grid(row=4, column=0, padx=(30, 5), pady=5, sticky="nw")
        self.desplegar_temas.grid(row=4, column=1, padx=5, pady=5, sticky="nw")

    def cambiar_escala(self, escala_seleccionada: str) -> None:
        """
        Cambia la escala actual de la aplicación a la indicado.
        """

        if self.escalas_dict[escala_seleccionada] == self.app.escala_actual:
            # si selecciono la misma escala, no cambiar nada
            return

        delete_msg_frame(self.msg_frame)
        self.app.escala_actual = self.escalas_dict[escala_seleccionada]

        # explicar que se necesita reiniciar la app
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg="¡Escala actualizada exitosamente!\n"
            + "Sus cambios tomarán efecto al reiniciar la aplicación.",
            tipo="success",
            row=5,
            column=1,
            padx=5,
            pady=10,
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
        set_icon(self.app, self.app)
        self.app.home_frame.update_frame()  # type: ignore
        self.app.inputs_frame.update_all()  # type: ignore
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore
        self.app.analisis.update_all()  # type: ignore
        self.app.sistemas.update_all()  # type: ignore
        self.update_frame()

        delete_msg_frame(self.msg_frame)
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg="¡Modo actualizado exitosamente!",
            tipo="success",
            row=5,
            column=1,
            padx=5,
            pady=10,
        )

    def cambiar_tema(self, tema_seleccionado: str) -> None:
        """
        Cambia el tema actual de la aplicación al indicado.
        """

        if self.temas_dict[tema_seleccionado] == self.app.tema_actual:
            # si se selecciono el mismo tema, no cambiar nada
            return

        delete_msg_frame(self.msg_frame)
        self.app.tema_actual = self.temas_dict[tema_seleccionado]

        # explicar que se necesita reiniciar la app
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg="¡Tema actualizado exitosamente!\n"
            + "Sus cambios tomarán efecto al reiniciar la aplicación.",
            tipo="success",
            row=5,
            column=1,
            padx=5,
            pady=10,
        )

    def cambiar_frac_prec(self, prec_seleccionada: str) -> None:
        """
        Cambia la precisión fraccional de la aplicación.
        """

        if self.frac_prec_dict[prec_seleccionada] == self.app.frac_prec_actual:
            # si se selecciono la misma precision, no cambiar nada
            return

        delete_msg_frame(self.msg_frame)

        FRAC_PREC["prec"] = self.app.frac_prec_actual = self.frac_prec_dict[
            prec_seleccionada
        ]

        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg="¡Precisión fraccional actualizada exitosamente!",
            tipo="success",
            row=5,
            column=1,
            padx=5,
            pady=10,
        )

    def cambiar_dec_prec(self, prec_seleccionada: str) -> None:
        """
        Cambia la precisión decimal de la aplicación.
        """

        if self.dec_prec_dict[prec_seleccionada] == self.app.dec_prec_actual:
            # si se selecciono la misma precision, no cambiar nada
            return

        delete_msg_frame(self.msg_frame)
        getcontext().prec = self.app.dec_prec_actual = self.dec_prec_dict[
            prec_seleccionada
        ]

        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg="¡Precisión decimal actualizada exitosamente!",
            tipo="success",
            row=5,
            column=1,
            padx=5,
            pady=10,
        )

    def update_frame(self) -> None:
        """
        Configura los backgrounds de los widgets,
        por si hubo un cambio de tema.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
