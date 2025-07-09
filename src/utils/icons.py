"""
Definiciones de todos los íconos e imágenes de la aplicación.
"""

from platform import system

from customtkinter import CTkImage

from .paths import ICONS
from .util_funcs import load_mode_icon, load_numpad_icons, load_single_icon

APP_ICON = (
    (str(ICONS / "light" / "logo.ico"), str(ICONS / "dark" / "logo.ico"))
    if system() == "Windows"
    else (str(ICONS / "light" / "logo.png"), str(ICONS / "dark" / "logo.png"))
)

################################################################################
############################   Íconos de NavFrame   ############################
################################################################################

LOGO = load_mode_icon("logo.png")
INPUTS_ICON = load_mode_icon("input_icon.png")
MATRIZ_ICON = load_mode_icon("matriz_icon.png")
VECTOR_ICON = load_mode_icon("vector_icon.png")
ANALISIS_ICON = load_mode_icon("analisis_icon.png")
ECUACIONES_ICON = load_mode_icon("ecuaciones_icon.png")
CONFIG_ICON = load_mode_icon("config_icon.png")
QUIT_ICON = load_mode_icon("quit_icon.png")

################################################################################
########################   Íconos de CustomMessagebox   ########################
################################################################################

CHECK_ICON = load_single_icon("check_icon.png")
ERROR_ICON = load_single_icon("error_icon.png")
INFO_ICON = load_mode_icon("info_icon.png")
QUESTION_ICON = load_mode_icon("question_icon.png")
WARNING_ICON = load_single_icon("warning_icon.png")

MSGBOX_ICONS: dict[str, CTkImage] = {
    "check": CHECK_ICON,
    "error": ERROR_ICON,
    "info": INFO_ICON,
    "question": QUESTION_ICON,
    "warning": WARNING_ICON,
}

################################################################################
############################   Íconos de botones   #############################
################################################################################

ACEPTAR_ICON = load_mode_icon("aceptar_icon.png")
DROPDOWN_ICON = load_mode_icon("dropdown_icon.png")
DROPLEFT_ICON = load_mode_icon("dropleft_icon.png")
DROPRIGHT_ICON = load_mode_icon("dropright_icon.png")
DROPUP_ICON = load_mode_icon("dropup_icon.png")
ELIMINAR_ICON = load_mode_icon("eliminar_icon.png")
ENTER_ICON = load_mode_icon("enter_icon.png")
LIMPIAR_ICON = load_mode_icon("limpiar_icon.png", size=(30, 20))
MOSTRAR_ICON = load_mode_icon("mostrar_icon.png")
SAVE_ICON = load_mode_icon("save_icon.png")
SHUFFLE_ICON = load_mode_icon("shuffle_icon.png")

################################################################################
##########################   Íconos de CustomNumpad   ##########################
################################################################################

NUMPAD_KEYS: dict[str, CTkImage] = load_numpad_icons()
