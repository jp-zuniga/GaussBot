"""
Implementación de ventana principal, que contiene
todos los frames y managers necesarios para el GUI.
"""

from json import dump, load
from os import makedirs, path
from typing import Union

from customtkinter import (
    CTk as ctk,
    ThemeManager,
    set_appearance_mode as set_mode,
    set_default_color_theme as set_theme,
    set_widget_scaling as set_scaling,
)

from .frames import (
    AnalisisFrame,
    ConfigFrame,
    HomeFrame,
    InputsFrame,
    MatricesFrame,
    NavFrame,
    SistemasFrame,
    VectoresFrame,
)
from ..managers import FuncManager, OpsManager
from ..utils import CONFIG_PATH, LOGGER, THEMES_PATH, set_icon


class GaussUI(ctk):
    """
    Ventana principal del GUI.
    """

    def __init__(self) -> None:
        super().__init__()

        self.config_options: dict[str, Union[float, str]] = {}
        self.escala_actual: float
        self.modo_actual: str
        self.tema_actual: str

        self._load_config()
        set_icon(self, self)

        self.theme_config = ThemeManager.theme
        self.configure(fg_color=self.theme_config["CTkFrame"]["fg_color"])

        self.geometry("1200x600")
        self.title("GaussBot")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # inicializar managers
        self.func_manager = FuncManager()
        self.ops_manager = OpsManager()
        self.mats_manager = self.ops_manager.mats_manager
        self.vecs_manager = self.ops_manager.vecs_manager

        # inicializar frames
        self.home_frame = HomeFrame(app=self, master=self)
        self.inputs_frame = InputsFrame(
            app=self,
            master=self,
            managers=(self.func_manager, self.mats_manager, self.vecs_manager),
        )

        self.matrices = MatricesFrame(
            app=self,
            master=self,
            mats_manager=self.mats_manager,
            vecs_manager=self.vecs_manager,
        )

        self.vectores = VectoresFrame(
            app=self,
            master=self,
            vecs_manager=self.vecs_manager,
            mats_manager=self.mats_manager,
        )

        self.analisis = AnalisisFrame(
            app=self, master=self, func_manager=self.func_manager
        )

        self.sistemas = SistemasFrame(
            app=self, master=self, mats_manager=self.mats_manager
        )

        self.config_frame = ConfigFrame(app=self, master=self)
        self.nav_frame = NavFrame(app=self, master=self)

        # seleccionar frame por defecto
        self.nav_frame.seleccionar_frame("home")

        # configurar evento de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.nav_frame.quit_event)

    def save_config(self) -> None:
        """
        Guarda la configuración actual en config.json.
        """

        # extraer configuracion actual
        self.config_options["escala"] = self.escala_actual
        self.config_options["modo"] = self.modo_actual
        self.config_options["tema"] = self.tema_actual

        if not path.exists(CONFIG_PATH):
            makedirs(path.dirname(CONFIG_PATH), exist_ok=True)
            LOGGER.info("Creando archivo 'config.json'...")

        with open(CONFIG_PATH, mode="w", encoding="utf-8") as config_file:
            dump(self.config_options, config_file, indent=4, sort_keys=True)
            LOGGER.info("Configuración guardada!")

    def _load_config(self) -> None:
        """
        Carga la configuración guardada en config.json.
        Si config.json no existe, utiliza valores por defecto.
        """

        if path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, mode="r", encoding="utf-8") as config_file:
                self.config_options = load(config_file)
                LOGGER.info("Configuración cargada!")
        else:
            LOGGER.info(
                "Archivo 'config.json' no existe, "
                + "inicializando con valores por defecto..."
            )

            self.config_options = {
                "escala": 1.0,
                "modo": "light",
                "tema": "ceruleo.json",
            }

        # extraer configs individuales del diccionario
        self.escala_actual = self.config_options["escala"]
        self.modo_actual = self.config_options["modo"]
        self.tema_actual = self.config_options["tema"]

        # aplicar configs
        set_mode(self.modo_actual)
        set_scaling(self.escala_actual)
        set_theme(path.join(THEMES_PATH, self.tema_actual))
        LOGGER.info("Configuración aplicada!")
