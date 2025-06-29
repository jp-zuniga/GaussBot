"""
Direcciones de los archivos utilizados por la aplicación.
"""

from importlib.resources import files
from pathlib import Path
from platform import system

PKG: str = "src"

ASSETS = files(f"{PKG}.assets")
ICONS = files(f"{PKG}.assets.icons")
DARK_ICONS = files(f"{PKG}.assets.icons.dark")
LIGHT_ICONS = files(f"{PKG}.assets.icons.light")
DARK_NUMPAD_ICONS = files(f"{PKG}.assets.icons.numpad_dark")
LIGHT_NUMPAD_ICONS = files(f"{PKG}.assets.icons.numpad_light")
THEMES = files(f"{PKG}.assets.themes")

# root folder de datos
DATA_PATH: Path = (
    Path.home()
    / ("AppData/Roaming" if system() == "Windows" else ".config")
    / "GaussBot"
)

# archivos de datos especificos
CONFIG_PATH: Path = DATA_PATH / "config.json"
FUNCIONES_PATH: Path = DATA_PATH / "funciones.json"
LOG_PATH: Path = DATA_PATH / "log.txt"
MATRICES_PATH: Path = DATA_PATH / "matrices.json"
SAVED_FUNCS_PATH: Path = DATA_PATH / "saved_funcs"
SISTEMAS_PATH: Path = DATA_PATH / "sistemas.json"
VECTORES_PATH: Path = DATA_PATH / "vectores.json"
