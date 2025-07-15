"""
Customized UI elements for customtkinter.
"""

from . import adapted
from .custom_frames import ErrorFrame, ResultadoFrame, SuccessFrame
from .custom_widgets import CustomDropdown, CustomEntry, IconButton

__all__: list[str] = [
    "CustomDropdown",
    "CustomEntry",
    "ErrorFrame",
    "IconButton",
    "ResultadoFrame",
    "SuccessFrame",
    "adapted",
]
