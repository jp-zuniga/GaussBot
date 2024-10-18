from os import path
from PIL import Image

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkImage as ctkImage,
)

from gauss_bot.gui.frames.nav import ASSET_PATH

class ErrorFrame(ctkFrame):
    def __init__(self, parent, message):
        super().__init__(parent, corner_radius=6, border_width=2, border_color="#ff3131")

        self.error_icon = ctkImage(Image.open(path.join(ASSET_PATH, "error_icon.png")))
        self.error_icon_label = ctkLabel(self, text="", image=self.error_icon)
        self.error_icon_label.grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")

        self.mensaje_error = ctkLabel(self, text=message)
        self.mensaje_error.grid(row=0, column=1, padx=(5, 15), pady=10, sticky="e")
    
    def destroy(self):
        self.pack_forget()
        super().destroy()
