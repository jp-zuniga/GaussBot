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
    THEMES_PATH,
)

from gauss_bot.managers import OpsManager
from gauss_bot.gui.frames import (
    HomeFrame,
    InputsFrame,
    MatricesFrame,
    VectoresFrame,
    ConfigFrame,
    EcuacionesFrame,
    NavFrame,
)


class GaussUI(ctk):
    """
    Ventana principal del GUI.
    """

    def __init__(self) -> None:
        super().__init__()

        self.load_config()
        self.set_icon(self.modo_actual)

        self.title("GaussBot")
        self.geometry("1280x720")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ops_manager = OpsManager()
        self.mats_manager = self.ops_manager.mats_manager
        self.vecs_manager = self.ops_manager.vecs_manager

        self.home_frame = HomeFrame(master=self, app=self)
        self.inputs_frame = InputsFrame(
            master=self,
            app=self,
            mats_manager=self.mats_manager,
            vecs_manager=self.vecs_manager,
        )

        self.matrices = MatricesFrame(
            master=self,
            app=self,
            mats_manager=self.mats_manager,
            vecs_manager=self.vecs_manager,
        )

        self.vectores = VectoresFrame(
            master=self,
            app=self,
            vecs_manager=self.vecs_manager,
            mats_manager=self.mats_manager,
        )

        self.ecuaciones = EcuacionesFrame(
            master=self, app=self, mats_manager=self.mats_manager
        )

        self.config_frame = ConfigFrame(master=self, app=self)
        self.nav_frame = NavFrame(master=self, app=self)
        self.nav_frame.seleccionar_frame("home")
        self.update_idletasks()

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
                "escala": 1.0,
                "modo": "light",
                "tema": "sky.json"
            }

        self.escala_actual = self.config_options["escala"]
        self.modo_actual = self.config_options["modo"]
        self.tema_actual = self.config_options["tema"]
        self.theme_config = self._load_theme_config()
        self.configure(fg_color=self.theme_config["CTkFrame"]["fg_color"])

        set_appearance_mode(self.modo_actual)
        set_widget_scaling(self.escala_actual)
        set_default_color_theme(path.join(THEMES_PATH, self.tema_actual))

    def save_config(self) -> None:
        """
        Guarda la configuración actual en config.json.
        """

        self.config_options["escala"] = self.escala_actual
        self.config_options["modo"] = self.modo_actual
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

    def _load_theme_config(self) -> dict:
        """
        Carga el archivo de configuración del tema actual.
        """

        with open(
            path.join(THEMES_PATH, self.tema_actual), mode="r", encoding="utf-8"
        ) as theme_file:
            return load(theme_file)
