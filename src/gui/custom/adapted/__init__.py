"""
Custom widgets based on the work of Akash Bora (https://github.com/Akascape/).
"""

from .messagebox import CustomMessageBox
from .numpad import CustomNumpad
from .scrollframe import CustomScrollFrame
from .table import CustomTable
from .tooltip import Tooltip

__all__: list[str] = [
    "CustomMessageBox",
    "CustomNumpad",
    "CustomScrollFrame",
    "CustomTable",
    "Tooltip",
]
