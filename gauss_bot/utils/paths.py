"""
Direcciones de los archivos utilizados por la aplicación.
"""

from pathlib import Path
from platform import system

# assets y temas
ASSET_PATH: Path = Path(__file__).parent.parent / "assets"
THEMES_PATH: Path = ASSET_PATH / "themes"
NUMPAD_ICON_PATH: Path = ASSET_PATH / "numpad_icons"

# root folder de todos los datos
if system() == "Windows":
    DATA_PATH: Path = Path.home() / "AppData" / "Roaming" / "GaussBot"
else:
    DATA_PATH: Path = Path.home() / ".config" / "GaussBot"

# archivos de datos especificos
CONFIG_PATH: Path = DATA_PATH / "config.json"
FUNCIONES_PATH: Path = DATA_PATH / "funciones.json"
LOG_PATH: Path = DATA_PATH / "log.txt"
MATRICES_PATH: Path = DATA_PATH / "matrices.json"
SAVED_FUNCS_PATH: Path = DATA_PATH / "saved_funcs"
SISTEMAS_PATH: Path = DATA_PATH / "sistemas.json"
VECTORES_PATH: Path = DATA_PATH / "vectores.json"
