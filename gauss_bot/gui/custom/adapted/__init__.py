"""
Custom widgets based on the work of Akash Bora.
* https://github.com/Akascape/

Most of them have been heavily simplified for use in GaussBot,
having sacrificed some of the original functionality
and cross-platform compatibility.

These widgets are built to work only on Windows.
"""

from .messagebox import CustomMessageBox
from .numpad import CustomNumpad
from .table import CustomTable
from .tooltip import Tooltip

__all__ = ["CustomMessageBox", "CustomNumpad", "CustomTable", "Tooltip"]
