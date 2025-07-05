"""
Adapted from:
* https://github.com/Akascape/CTkToolTip
* By: Akash Bora

Modified by: Joaquín Zúñiga, on 11/8/2024.
Formatted file and added type annotations for personal use.
"""

from time import time
from tkinter import Event, Frame, Toplevel

from customtkinter import (
    CTkBaseClass as ctkBase,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    ThemeManager,
)


class Tooltip(Toplevel):
    """
    Tooltip with modern design that appears
    when the mouse hovers over a widget.
    """

    def __init__(
        self,
        widget: ctkBase,
        message: str,
        delay: float = 0.05,
        padx: int = 15,
        pady: int = 5,
        x_offset: int = 20,
        y_offset: int = 20,
        **kwargs,
    ) -> None:
        super().__init__()
        self.resizable(width=True, height=True)
        self.overrideredirect(True)
        self.transient()
        self.withdraw()

        self.widget = widget
        self.disable = False
        self.status = "outside"
        self.delay = delay
        self.last_moved = 0.0
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.transparent_frame = Frame(self)
        self.transparent_frame.pack(expand=True, fill="both")

        bg: str = kwargs.pop("bg_color", ThemeManager.theme["CTkFrame"]["fg_color"])

        self.frame: ctkFrame = ctkFrame(
            self.transparent_frame, border_width=2, bg_color=bg, fg_color=bg
        )

        self.message_label = ctkLabel(
            self.frame, font=ctkFont(size=10), text=message, **kwargs
        )

        self.frame.pack(expand=True, fill="both")
        self.message_label.pack(fill="both", padx=padx, pady=pady, expand=True)

        self.widget.bind("<Enter>", self.on_enter, add="+")
        self.widget.bind("<Leave>", lambda _: self.on_leave(), add="+")
        self.widget.bind("<Motion>", self.on_enter, add="+")
        self.widget.bind("<B1-Motion>", self.on_enter, add="+")
        self.widget.bind("<Destroy>", lambda _: self.hide(), add="+")

    def on_enter(self, event: Event) -> None:
        """
        Handles tooltip movement.
        """

        if self.disable:
            return
        self.last_moved = time()

        if self.status == "outside":
            self.status = "inside"

        offset_x: int = self.x_offset
        text_width: int = self.message_label.winfo_reqwidth()
        space_on_right: int = self.winfo_screenwidth() - event.x_root - text_width

        if space_on_right < text_width + 20:
            offset_x: int = -text_width - 20

        self.geometry(f"+{event.x_root + offset_x}+{event.y_root + self.y_offset}")
        self.after(int(self.delay * 1000), self.show)

    def on_leave(self) -> None:
        """
        Hides the widget when the mouse leaves the widget.
        """

        if self.disable:
            return
        self.status = "outside"
        self.withdraw()

    def show(self) -> None:
        if not self.widget.winfo_exists():
            self.hide()
            self.destroy()

        if self.status == "inside" and (time() - self.last_moved >= self.delay):
            self.status = "visible"
            self.deiconify()

    def hide(self) -> None:
        """
        Hides the tooltip.
        """

        if not self.winfo_exists():
            return
        self.withdraw()
        self.disable = True

    def configure_tooltip(self, **kwargs) -> None:
        """
        Configures the tooltip with new values.
        """

        if "x_offset" in kwargs:
            self.x_offset = kwargs.pop("x_offset")
        if "y_offset" in kwargs:
            self.y_offset = kwargs.pop("y_offset")
        if "delay" in kwargs:
            self.delay = kwargs.pop("delay")
        if "bg_color" in kwargs:
            self.frame.configure(fg_color=kwargs.pop("bg_color"))
        if "message" in kwargs:
            self.message_label.configure(text=kwargs.pop("message"))

        self.message_label.configure(**kwargs)
