"""
Implementación de ConfigFrame, encargado de mostrar
y editar las configuraciones de la aplicación.
"""

from os import path
from typing import Optional, Union

from tkinter import StringVar
from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    set_appearance_mode,
    set_widget_scaling,
    set_default_color_theme,
)

from gauss_bot import THEMES_PATH
from gauss_bot.gui.custom_frames import (
    CustomDropdown,
    SuccessFrame,
)


class ConfigFrame(ctkFrame):
    """
    Frame personalizado para mostrar y editar la configuración.
    """

    def __init__(self, master, app) -> None:
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mensaje_frame: Optional[SuccessFrame] = None

        self.escalas_dict = {
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

        self.modos_dict = {
            "Claro": "light",
            "Oscuro": "dark",
        }

        self.temas_dict = {
            "Autumn": "autumn.json",
            "Breeze": "breeze.json",
            "Cherry": "cherry.json",
            "Carrot": "carrot.json",
            "Coffee": "coffee.json",
            "Lavender": "lavender.json",
            "Marsh": "marsh.json",
            "Metal": "metal.json",
            "Midnight": "midnight.json",
            "Orange": "orange.json",
            "Patina": "patina.json",
            "Pink": "pink.json",
            "Red": "red.json",
            "Rime": "rime.json",
            "Rose": "rose.json",
            "Sky": "sky.json",
            "Violet": "violet.json",
            "Yellow": "yellow.json",
        }

        self.escalas = list(self.escalas_dict.keys())
        self.modos = list(self.modos_dict.keys())
        self.temas = list(self.temas_dict.keys())

        self.escala_actual_key = self._get_dict_key(self.escalas_dict, self.app.escala_actual)
        self.modo_actual_key = self._get_dict_key(self.modos_dict, self.app.modo_actual)
        self.tema_actual_key = self._get_dict_key(self.temas_dict, self.app.tema_actual)

        try:
            self.first_escala = StringVar(value=self.escala_actual_key)
            self.first_modo = StringVar(value=self.modo_actual_key)
            self.first_tema = StringVar(value=self.tema_actual_key)
        except AttributeError:
            self.first_escala = StringVar(value="100%")
            self.first_modo = StringVar(value="Oscuro")
            self.first_tema = StringVar(value="Metal")

        self.escala_label = ctkLabel(self, text="Escala:")
        self.modos_label = ctkLabel(self, text="Modo:")
        self.temas_label = ctkLabel(self, text="Tema:")

        self.desplegar_escalas = CustomDropdown(
            self, width=105, variable=self.first_escala,
            values=self.escalas, command=self.cambiar_escala,
        )

        self.desplegar_modos = CustomDropdown(
            self, width=105, variable=self.first_modo,
            values=self.modos, command=self.cambiar_modo
        )

        self.desplegar_temas = CustomDropdown(
            self, width=105, variable=self.first_tema,
            values=self.temas, command=self.cambiar_tema
        )

        self.escala_label.grid(row=0, column=0, padx=(30, 10), pady=(20, 10), sticky="nw")
        self.desplegar_escalas.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="nw")
        self.modos_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="nw")
        self.desplegar_modos.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        self.temas_label.grid(row=2, column=0, padx=(30, 10), pady=10, sticky="nw")
        self.desplegar_temas.grid(row=2, column=1, padx=10, pady=10, sticky="nw")

    def cambiar_escala(self, escala_seleccionada: str) -> None:
        """
        Cambia la escala actual de la aplicación a la indicado.
        """

        if self.escalas_dict[escala_seleccionada] == self.app.escala_actual:
            return

        self.app.escala_actual = self.escalas_dict[escala_seleccionada]
        set_widget_scaling(self.app.escala_actual)
        self.app.inputs_frame.update_frame()
        self.app.matrices.update_all()
        self.app.vectores.update_all()
        self.app.update_idletasks()

    def cambiar_modo(self, modo_seleccionado: str) -> None:
        """
        Cambia el modo actual de apariencia de la aplicación al indicado.
        """

        if self.modos_dict[modo_seleccionado] == self.app.modo_actual:
            return
            
        self.app.modo_actual = self.modos_dict[modo_seleccionado]
        set_appearance_mode(self.app.modo_actual)
        self.app.set_icon(self.app.modo_actual)
        self.app.inputs_frame.update_all()
        self.app.matrices.update_all()
        self.app.vectores.update_all()
        self.app.config_frame.update_frame()
        self.app.update_idletasks()

    def cambiar_tema(self, tema_seleccionado: str) -> None:
        """
        Cambia el tema actual de la aplicación al indicado.
        """

        if self.temas_dict[tema_seleccionado] == self.app.tema_actual:
            return

        self.app.tema_actual = self.temas_dict[tema_seleccionado]
        self.mensaje_frame = SuccessFrame(
            self,
            message="Tema cambiado exitosamente! " +
                    "Cambios tomarán efecto al reiniciar la aplicación."
        )
        self.mensaje_frame.grid(row=3, column=1, pady=30)
        set_default_color_theme(path.join(THEMES_PATH, self.app.tema_actual))
        self.app.update_idletasks()

    def _get_dict_key(self, dict_lookup: dict, buscando: str) -> Union[str, None]:
        """
        Busca un valor en un diccionario y retorna su llave.
        """

        for key, value in dict_lookup.items():
            if value == buscando:
                return key
        return None

    def update_frame(self) -> None:
        self.update_idletasks()
        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None
        self.modo_actual_key = self._get_dict_key(self.modos_dict, self.app.modo_actual)
        self.escala_actual_key = self._get_dict_key(self.escalas_dict, self.app.escala_actual)
        self.tema_actual_key = self._get_dict_key(self.temas_dict, self.app.tema_actual)
        self.first_modo.set(self.modo_actual_key)  # type: ignore
        self.first_escala.set(self.escala_actual_key)  # type: ignore
        self.first_tema.set(self.tema_actual_key)  # type: ignore
        self.desplegar_escalas.configure(variable=self.first_escala)
        self.desplegar_modos.configure(variable=self.first_modo)
        self.desplegar_temas.configure(variable=self.first_tema)
        self.update_idletasks()
