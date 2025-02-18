"""
Implementación de ventana principal, que contiene
todos los frames y managers necesarios para el GUI.
"""

from json import (
    dump,
    load,
)

from os import (
    makedirs,
    path,
)

from typing import Union
from customtkinter import (
    CTk as ctk,
    ThemeManager,
    set_appearance_mode as set_mode,
    set_widget_scaling as set_scaling,
    set_default_color_theme as set_theme,
)

from .. import (
    CONFIG_PATH,
    THEMES_PATH,
)

from ..icons import APP_ICON
from ..util_funcs import LOGGER
from ..managers import (
    FuncManager,
    OpsManager,
)

from .frames import (
    NavFrame,
    HomeFrame,
    InputsFrame,
    SistemasFrame,
    MatricesFrame,
    VectoresFrame,
    AnalisisFrame,
    ConfigFrame,
)


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
        self.set_icon(self.modo_actual)

        self.theme_config = ThemeManager.theme
        self.configure(fg_color=self.theme_config["CTkFrame"]["fg_color"])

        self.geometry("1280x720")
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
            managers=(
                self.func_manager,
                self.mats_manager,
                self.vecs_manager,
            )
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
            app=self,
            master=self,
            func_manager=self.func_manager,
        )

        self.sistemas = SistemasFrame(
            app=self,
            master=self,
            mats_manager=self.mats_manager
        )

        self.config_frame = ConfigFrame(app=self, master=self)
        self.nav_frame = NavFrame(app=self, master=self)

        # seleccionar frame por defecto
        self.nav_frame.seleccionar_frame("home")

        # configurar evento de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.nav_frame.quit_event)

    def set_icon(self, modo: str) -> None:
        """
        Setea el ícono de la ventana según el modo de apariencia.
        * ValueError: si el input no es "light" o "dark"
        """

        if modo == "light":
            self.iconbitmap(bitmap=APP_ICON[1])
        elif modo == "dark":
            self.iconbitmap(bitmap=APP_ICON[0])
        else:
            raise ValueError("Valor inválido para argumento 'modo'!")

    def save_config(self) -> None:
        """
        Guarda la configuración actual en config.json.
        """

        # extrar configuracion actual
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
        Si config.json no existe, setea la configuración
        con valores por defecto.
        """

        if path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, mode="r", encoding="utf-8") as config_file:
                self.config_options = load(config_file)
                LOGGER.info("Configuración cargada!")
        else:
            LOGGER.info(
                "Archivo 'config.json' no existe, " +
                "inicializando con valores por defecto..."
            )

            self.config_options = {
                "escala": 1.0,
                "modo": "light",
                "tema": "sky.json"
            }

        # extrar configs individuales del diccionario
        self.escala_actual = self.config_options["escala"]  # type: ignore
        self.modo_actual = self.config_options["modo"]  # type: ignore
        self.tema_actual = self.config_options["tema"]  # type: ignore

        # aplicar configs
        set_mode(self.modo_actual)
        set_scaling(self.escala_actual)
        set_theme(path.join(THEMES_PATH, self.tema_actual))
        LOGGER.info("Configuración aplicada!")
