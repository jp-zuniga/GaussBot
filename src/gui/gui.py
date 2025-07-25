"""
Implementación de ventana principal, que contiene
todos los frames y managers necesarios para el GUI.
"""

from decimal import getcontext
from importlib.resources import as_file
from json import dump, load
from pathlib import Path

from customtkinter import (
    CTk,
    ThemeManager,
    set_appearance_mode as set_mode,
    set_default_color_theme as set_theme,
    set_widget_scaling as set_scaling,
)

from src import FRAC_PREC
from src.managers import FuncManager, OpsManager
from src.utils import CONFIG_PATH, LOGGER, THEMES, set_icon

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


class GaussUI(CTk):
    """
    Ventana principal del GUI.
    """

    def __init__(self) -> None:
        """
        Configurar ventana principal e inicializar subframes.
        """

        super().__init__()

        self.config_options: dict[str, str | float] = {}
        self.escala_inicial: float
        self.escala_actual: float
        self.modo_actual: str
        self.tema_actual: str
        self.frac_prec_actual: int
        self.dec_prec_actual: int

        self.load_config()
        set_icon(self, self)

        self.geometry("1200x600")
        self.title("GaussBot")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.configure(fg_color=ThemeManager.theme["CTkFrame"]["fg_color"])

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
            app=self,
            master=self,
            func_manager=self.func_manager,
        )

        self.sistemas = SistemasFrame(
            app=self,
            master=self,
            mats_manager=self.mats_manager,
        )

        self.config_frame = ConfigFrame(app=self, master=self)
        self.nav_frame = NavFrame(app=self, master=self)

        # seleccionar frame por defecto
        self.nav_frame.seleccionar_frame("home")

        # configurar evento de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.nav_frame.quit_event)

        self.unbind_all("<Escape>")
        self.bind("<Escape>", lambda _: self.nav_frame.quit_event())

    def save_config(self) -> None:
        """
        Guardar configuración actual.
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

        with CONFIG_PATH.open(mode="w") as config_file:
            dump(self.config_options, config_file, indent=4, sort_keys=True)
            LOGGER.info("Configuración guardada exitosamente")

    def load_config(self) -> None:
        """
        Cargar configuración almacenada.
        """

        if CONFIG_PATH.exists():
            with CONFIG_PATH.open() as config_file:
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
        self.escala_inicial = self.escala_actual = float(self.config_options["escala"])
        self.modo_actual = self.config_options["modo"]  # type: ignore[reportAttributeAccessIssue]
        self.tema_actual = self.config_options["tema"]  # type: ignore[reportAttributeAccessIssue]

        getcontext().prec = self.dec_prec_actual = int(self.config_options["dec_prec"])
        FRAC_PREC["prec"] = self.frac_prec_actual = int(
            self.config_options["frac_prec"],
        )

        # aplicar configs
        set_mode(self.modo_actual)
        set_scaling(self.escala_actual)

        with as_file(THEMES) as themes_path:
            set_theme(str(Path(str(themes_path), self.tema_actual)))

        LOGGER.info("Configuración aplicada")
