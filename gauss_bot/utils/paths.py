"""
Direcciones de los archivos utilizados por la aplicación.
"""

from os import path

# assets y temas
ASSET_PATH = path.join(path.dirname(path.dirname(path.realpath(__file__))), "assets")
THEMES_PATH = path.join(ASSET_PATH, "themes")
NUMPAD_ICON_PATH = path.join(ASSET_PATH, "numpad_icons")

# root folder de todos los datos
DATA_PATH = path.join(path.expanduser("~"), "GaussBot", "data")

# archivos de datos especificos
CONFIG_PATH = path.join(DATA_PATH, "config.json")
FUNCIONES_PATH = path.join(DATA_PATH, "funciones.json")
LOG_PATH = path.join(DATA_PATH, "log.txt")
MATRICES_PATH = path.join(DATA_PATH, "matrices.json")
SAVED_FUNCS_PATH = path.join(DATA_PATH, "saved_funcs")
SISTEMAS_PATH = path.join(DATA_PATH, "sistemas.json")
VECTORES_PATH = path.join(DATA_PATH, "vectores.json")
