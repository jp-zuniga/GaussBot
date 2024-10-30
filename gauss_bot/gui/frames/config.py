"""
Implementación de ConfigFrame, encargado de mostrar
y editar las configuraciones de la aplicación.
"""

from os import path
from typing import Union

from tkinter import StringVar
from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
    set_appearance_mode,
    set_widget_scaling,
    set_default_color_theme,
)

from gauss_bot import THEMES_PATH


class ConfigFrame(ctkFrame):
    """
    Frame personalizado para mostrar y editar la configuración.
    """

    def __init__(self, master, app) -> None:
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app

        self.modos_dict = {
            "Claro": "light",
            "Oscuro": "dark",
        }

        self.escalas_dict = {
            "80%": 0.8,
            "90%": 0.9,
            "100%": 1.0,
            "110%": 1.1,
            "120%": 1.2,
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

        self.modos = list(self.modos_dict.keys())
        self.escalas = list(self.escalas_dict.keys())
        self.temas = list(self.temas_dict.keys())

        self.modo_actual_key = self._get_dict_key(self.modos_dict, self.app.modo_actual)
        self.escala_actual_key = self._get_dict_key(self.escalas_dict, self.app.escala_actual)
        self.tema_actual_key = self._get_dict_key(self.temas_dict, self.app.tema_actual)

        try:
            self.first_tema = StringVar(value=self.tema_actual_key)
            self.first_modo = StringVar(value=self.modo_actual_key)
            self.first_escala = StringVar(value=self.escala_actual_key)
        except AttributeError:
            self.first_tema = StringVar(value="Metal")
            self.first_modo = StringVar(value="Oscuro")
            self.first_escala = StringVar(value="100%")

        self.temas_label = ctkLabel(self, text="Tema:")
        self.escala_label = ctkLabel(self, text="Escala:")
        self.modos_label = ctkLabel(self, text="Modo:")

        self.desplegar_temas = ctkOptionMenu(
            self, variable=self.first_tema,
            values=self.temas, command=self.cambiar_tema
        )

        self.desplegar_modos = ctkOptionMenu(
            self, variable=self.first_modo,
            values=self.modos, command=self.cambiar_modo
        )

        self.desplegar_escalas = ctkOptionMenu(
            self, variable=self.first_escala,
            values=self.escalas, command=self.cambiar_escala,
        )

        self.temas_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        self.desplegar_temas.grid(row=0, column=1, padx=(20, 10), pady=10)
        self.modos_label.grid(row=1, column=0, padx=(20, 10), pady=10)
        self.desplegar_modos.grid(row=1, column=1, padx=(20, 10), pady=10)
        self.escala_label.grid(row=2, column=0, padx=(20, 10), pady=10)
        self.desplegar_escalas.grid(row=2, column=1, padx=(20, 10), pady=10)

    def cambiar_modo(self, modo_seleccionado: str) -> None:
        """
        Cambia el modo actual de apariencia de la aplicación al indicado.
        """

        self.app.modo_actual = self.modos_dict[modo_seleccionado]
        set_appearance_mode(self.app.modo_actual)
        self.app.set_icon(self.app.modo_actual)
        self.app.matrices.update_all()
        self.app.vectores.update_all()

    def cambiar_escala(self, escala_seleccionada: str) -> None:
        """
        Cambia la escala actual de la aplicación a la indicado.
        """

        self.app.escala_actual = self.escalas_dict[escala_seleccionada]
        set_widget_scaling(self.app.escala_actual)
        self.app.matrices.update_all()
        self.app.vectores.update_all()

    def cambiar_tema(self, tema_seleccionado: str) -> None:
        """
        Cambia el tema actual de la aplicación al indicado.
        """

        self.app.tema_actual = path.join(THEMES_PATH, (self.temas_dict[tema_seleccionado]))
        set_default_color_theme(self.app.tema_actual)
        self.app.matrices.update_all()
        self.app.vectores.update_all()


    def _get_dict_key(self, dict_lookup: dict, buscando: str) -> Union[str, None]:
        """
        Busca un valor en un diccionario y retorna su llave.
        """

        for key, value in dict_lookup.items():
            if value == buscando:
                return key
        return None
