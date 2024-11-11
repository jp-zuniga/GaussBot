"""
Adapted from:
* https://github.com/Akascape/CTkToolTip
* By: Akash Bora

Modified by: Joaquín Zúñiga, on 11/8/2024.
Formatted file and added type annotations for personal use.
"""

from time import time
from typing import Optional

from tkinter import (
    Event,
    Frame,
    Toplevel,
)

from customtkinter import (
    CTkBaseClass as ctkBase,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    StringVar,
    ThemeManager,
)


class Tooltip(Toplevel):
    def __init__(
        self,
        widget: ctkBase,
        message: str,
        alpha: float = 1.0,
        delay: float = 0.1,
        follow: bool = True,
        x_offset: int = 20,
        y_offset: int = 20,
        padding: tuple[int, int] = (10, 2),
        corner_radius: int = 10,
        border_width: int = 2,
        border_color: Optional[str] = None,
        bg_color: Optional[str] = None,
        **message_kwargs,
    ) -> None:

        super().__init__()
        self.widget = widget
        self.withdraw()
        self.overrideredirect(True)  # disable title bar
        self.resizable(width=True, height=True)
        self.transient()

        self.message = message
        self.msg_var = StringVar(value=self.message)

        self.delay = delay
        self.follow = follow
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.corner_radius = corner_radius
        self.alpha = alpha
        self.border_width = border_width
        self.padding = padding
        self.bg_color = (
            ThemeManager.theme["CTkFrame"]["fg_color"]
            if bg_color is None else bg_color
        )

        self.border_color = border_color
        self.disable = False

        self.status = "outside"
        self.last_moved: float = 0.0

        self.transparent_frame = Frame(self)
        self.transparent_frame.pack(padx=0, pady=0, fill="both", expand=True)

        self.frame: ctkFrame = ctkFrame(  # type: ignore
            self.transparent_frame,
            bg_color=self.bg_color,
            corner_radius=self.corner_radius,
            border_width=self.border_width,
            fg_color=self.bg_color,
            border_color=self.border_color,
        )

        self.frame.pack(padx=0, pady=0, fill="both", expand=True)

        self.message_label = ctkLabel(
            self.frame,
            font=("Roboto", 12),
            textvariable=self.msg_var,
            **message_kwargs
        )

        self.message_label.pack(
            fill="both",
            padx=self.padding[0] + self.border_width,
            pady=self.padding[1] + self.border_width,
            expand=True,
        )

        if (self.widget.winfo_name() != "tk"
            and self.frame.cget("fg_color") == self.widget.cget("bg_color")
            and not bg_color):

            self._top_fg_color = self.frame._apply_appearance_mode(
                ThemeManager.theme["CTkFrame"]["fg_color"]
            )

            if self._top_fg_color != self.frame._fg_color:
                self.frame.configure(fg_color=self._top_fg_color)

        self.widget.bind("<Enter>", self.on_enter, add="+")
        self.widget.bind("<Leave>", lambda _: self.on_leave(), add="+")
        self.widget.bind("<Motion>", self.on_enter, add="+")
        self.widget.bind("<B1-Motion>", self.on_enter, add="+")
        self.widget.bind("<Destroy>", lambda _: self.hide(), add="+")

    def show(self) -> None:
        self.disable = False

    def on_enter(self, event: Event) -> None:
        if self.disable:
            return
        self.last_moved = time()

        # Set the status as inside for the very first time
        if self.status == "outside":
            self.status = "inside"

        # If the follow flag is not set, motion within the widget will make the tooltip disappear
        if not self.follow:
            self.status = "inside"
            self.withdraw()

        # Calculate available space on the right side of the widget relative to the screen
        root_width = self.winfo_screenwidth()
        widget_x = event.x_root
        space_on_right = root_width - widget_x

        # Calculate the width of the tooltip's text based on the length of the message string
        text_width = self.message_label.winfo_reqwidth()

        # Calculate the offset based on available space and
        # text width to avoid going off-screen on the right side
        offset_x = self.x_offset
        if space_on_right < text_width + 20:  # Adjust the threshold as needed
            offset_x = (
                -text_width
                - 20  # Negative offset when space is limited on the right side
            )

        # Offsets the Tooltip using the coordinates of an event as an origin
        self.geometry(f"+{event.x_root + offset_x}+{event.y_root + self.y_offset}")
        self.after(int(self.delay * 1000), self._show)

    def on_leave(self) -> None:
        if self.disable:
            return
        self.status = "outside"
        self.withdraw()

    def _show(self) -> None:
        if not self.widget.winfo_exists():
            self.hide()
            self.destroy()

        if self.status == "inside" and (time() - self.last_moved >= self.delay):
            self.status = "visible"
            self.deiconify()

    def hide(self) -> None:
        if not self.winfo_exists():
            return
        self.withdraw()
        self.disable = True

    def is_disabled(self) -> bool:
        return self.disable

    def get(self) -> str:
        return self.msg_var.get()

    def configure_tooltip(
        self,
        message: Optional[str] = None,
        delay: Optional[float] = None,
        bg_color: Optional[str] = None,
        **kwargs,
    ) -> None:

        if delay:
            self.delay = delay
        if bg_color:
            self.frame.configure(fg_color=bg_color)

        self.msg_var.set(message)  # type: ignore
        self.message_label.configure(**kwargs)
