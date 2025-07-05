"""
Implementación de ventana principal, que contiene
todos los frames y managers necesarios para el GUI.
"""

from decimal import getcontext
from importlib.resources import as_file
from json import dump, load
from pathlib import Path
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
from .. import FRAC_PREC
from ..managers import FuncManager, OpsManager
from ..utils import CONFIG_PATH, LOGGER, THEMES, set_icon


class GaussUI(ctk):
    """
    Ventana principal del GUI.
    """

    def __init__(self) -> None:
        super().__init__()

        self.config_options: dict[str, Union[float, str, int]] = {}
        self.escala_inicial: float
        self.escala_actual: float
        self.modo_actual: str
        self.tema_actual: str
        self.frac_prec_actual: int
        self.dec_prec_actual: int

        self.load_config()
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

        self.unbind_all("<Escape>")
        self.bind("<Escape>", self.nav_frame.quit_event)

    def save_config(self) -> None:
        """
        Guarda la configuración actual en config.json.
        """

        # extraer configuracion actual
        self.config_options["escala"] = self.escala_actual
        self.config_options["modo"] = self.modo_actual
        self.config_options["tema"] = self.tema_actual
        self.config_options["frac_prec"] = self.frac_prec_actual
        self.config_options["dec_prec"] = self.dec_prec_actual

        if not CONFIG_PATH.exists():
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            LOGGER.info("Creando archivo '%s'...", CONFIG_PATH)

        with open(CONFIG_PATH, mode="w", encoding="utf-8") as config_file:
            dump(self.config_options, config_file, indent=4, sort_keys=True)
            LOGGER.info("Configuración guardada exitosamente")

    def load_config(self) -> None:
        """
        Carga la configuración guardada en config.json.
        Si config.json no existe, utiliza valores por defecto.
        """

        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, mode="r", encoding="utf-8") as config_file:
                self.config_options = load(config_file)
                LOGGER.info("Configuración cargada exitosamente")
        else:
            LOGGER.info(
                "Archivo '%s' no existe, inicializando con valores por defecto...",
                CONFIG_PATH,
            )

            self.config_options = {
                "escala": 1.0,
                "modo": "light",
                "tema": "primavera.json",
                "frac_prec": 100,
                "dec_prec": 3,
            }

        # extraer configs individuales del diccionario
        self.escala_inicial = self.escala_actual = self.config_options["escala"]
        self.modo_actual = self.config_options["modo"]
        self.tema_actual = self.config_options["tema"]
        FRAC_PREC["prec"] = self.frac_prec_actual = self.config_options["frac_prec"]
        getcontext().prec = self.dec_prec_actual = self.config_options["dec_prec"]

        # aplicar configs
        set_mode(self.modo_actual)
        set_scaling(self.escala_actual)

        with as_file(THEMES) as themes_path:
            set_theme(str(Path(str(themes_path), self.tema_actual)))

        LOGGER.info("Configuración aplicada")
