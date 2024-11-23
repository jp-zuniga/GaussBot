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
        delay: float = 0.1,
        x_offset: int = 30,
        y_offset: int = 30,
        padding: tuple[int, int] = (10, 2),
        **message_kwargs,
    ) -> None:

        super().__init__()
        self.widget = widget
        self.transient()
        self.withdraw()
        self.overrideredirect(True)  # disable title bar
        self.resizable(width=True, height=True)

        self.message = message
        self.msg_var = StringVar(value=self.message)

        self.delay = delay
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.padding = padding
        self.bg_color = ThemeManager.theme["CTkFrame"]["fg_color"]


        self.last_moved: float = 0.0
        self.status = "outside"
        self.disable = False

        self.transparent_frame = Frame(self)
        self.transparent_frame.pack(padx=0, pady=0, fill="both", expand=True)

        self.frame: ctkFrame = ctkFrame(  # type: ignore
            self.transparent_frame,
            bg_color=self.bg_color,
            corner_radius=10,
            border_width=2,
            fg_color=self.bg_color,
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
            padx=self.padding[0] + 2,
            pady=self.padding[1] + 2,
            expand=True,
        )

        if (
            self.widget.winfo_name() != "tk"
            and self.frame.cget("fg_color") == self.widget.cget("bg_color")
        ):
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
        x_offset: Optional[int] = None,
        y_offset: Optional[int] = None,
        delay: Optional[float] = None,
        message: Optional[str] = None,
        bg_color: Optional[str] = None,
        **kwargs,
    ) -> None:

        if x_offset:
            self.x_offset = x_offset
        if y_offset:
            self.y_offset = y_offset
        if delay:
            self.delay = delay
        if bg_color:
            self.frame.configure(fg_color=bg_color)
        if message:
            self.msg_var.set(message)  # type: ignore
        self.message_label.configure(**kwargs)
