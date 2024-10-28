"""
Implementación de ventana principal, que contiene
todos los frames y managers necesarios para el GUI.
"""

from json import dump, load
from os import path, makedirs

from customtkinter import (
    CTk as ctk,
    set_appearance_mode,
    set_widget_scaling,
    set_default_color_theme,
)

from gauss_bot import (
    ASSET_PATH,
    CONFIG_PATH,
    THEMES_PATH
)

from gauss_bot.managers.ops_manager import OpsManager

from gauss_bot.gui.frames.ecuaciones import EcuacionesFrame
from gauss_bot.gui.frames.matrices import MatricesFrame
from gauss_bot.gui.frames.vectores import VectoresFrame
from gauss_bot.gui.frames.config import ConfigFrame
from gauss_bot.gui.frames.nav import NavFrame


class GaussUI(ctk):
    """
    Ventana principal del GUI.
    """

    def __init__(self) -> None:
        super().__init__()

        self.load_config()
        self.set_icon(self.modo_actual)

        self.title("GaussBot")
        self.geometry("1200x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ops_manager = OpsManager()
        self.mats_manager = self.ops_manager.mats_manager
        self.vecs_manager = self.ops_manager.vecs_manager

        self.ecuaciones = EcuacionesFrame(master=self, app=self, mats_manager=self.mats_manager)
        self.matrices = MatricesFrame(master=self, app=self, mats_manager=self.mats_manager)
        self.vectores = VectoresFrame(master=self, app=self, vecs_manager=self.vecs_manager)
        self.config_frame = ConfigFrame(master=self, app=self)
        self.nav_frame = NavFrame(master=self, app=self)

    def load_config(self) -> None:
        """
        Carga la configuración guardada en config.json.
        Si config.json no existe, setea la configuración
        con valores por defecto.
        """

        if path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, mode="r", encoding="utf-8") as config_file:
                self.config_options = load(config_file)
        else:
            self.config_options = {
                "modo": "dark",
                "escala": 1.0,
                "tema": "metal.json"
            }

        self.modo_actual = self.config_options["modo"]
        self.escala_actual = self.config_options["escala"]
        self.tema_actual = self.config_options["tema"]

        set_appearance_mode(self.modo_actual)
        set_widget_scaling(self.escala_actual)
        set_default_color_theme(path.join(THEMES_PATH, self.tema_actual))

    def save_config(self) -> None:
        """
        Guarda la configuración actual en config.json.
        """

        self.config_options["modo"] = self.modo_actual
        self.config_options["escala"] = self.escala_actual
        self.config_options["tema"] = self.tema_actual

        if not path.exists(CONFIG_PATH):
            makedirs(path.dirname(CONFIG_PATH), exist_ok=True)

        with open(CONFIG_PATH, mode="w", encoding="utf-8") as config_file:
            dump(self.config_options, config_file, indent=4, sort_keys=True)

    def set_icon(self, modo: str) -> None:
        """
        Setea el ícono de la ventana según el modo de apariencia.
        * ValueError: si el input no es "light" o "dark"
        """

        if modo == "light":
            self.iconbitmap(path.join(ASSET_PATH, "dark_logo.ico"))
        elif modo == "dark":
            self.iconbitmap(path.join(ASSET_PATH, "light_logo.ico"))
        else:
            raise ValueError("Input inválido!")
