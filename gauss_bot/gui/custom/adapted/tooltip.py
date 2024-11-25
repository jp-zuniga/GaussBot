"""
Adapted from:
* https://github.com/Akascape/CTkToolTip
* By: Akash Bora

Modified by: Joaquín Zúñiga, on 11/8/2024.
Formatted file and added type annotations for personal use.
"""

from time import time
from tkinter import (
    Event,
    Frame,
    Toplevel,
)

from customtkinter import (
    CTkBaseClass as ctkBase,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    StringVar,
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
        delay: float = 0.1,
        x_offset: int = 20,
        y_offset: int = 30,
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
        self.bg_color = ThemeManager.theme["CTkFrame"]["fg_color"]

        self.last_moved: float = 0.0
        self.status = "outside"
        self.disable = False

        self.transparent_frame = Frame(self)
        self.transparent_frame.pack(expand=True, fill="both")

        self.frame: ctkFrame = ctkFrame(  # type: ignore
            self.transparent_frame,
            corner_radius=10,
            border_width=2,
            bg_color=self.bg_color,
            fg_color=self.bg_color,
        )

        self.frame.pack(expand=True, fill="both")
        self.message_label = ctkLabel(
            self.frame,
            font=ctkFont(size=12),
            textvariable=self.msg_var,
            **message_kwargs
        )

        self.message_label.pack(
            fill="both",
            padx=10,
            pady=5,
            expand=True,
        )

        if (
            self.widget.winfo_name() != "tk"
            and
            self.frame.cget("fg_color") == self.widget.cget("bg_color")
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

    def on_enter(self, event: Event) -> None:
        """
        Handles tooltip movement.
        """

        if self.disable:
            return
        self.last_moved = time()

        # Set the status as inside for the very first time
        if self.status == "outside":
            self.status = "inside"

        # Calculate available space on the right side
        # of the widget relative to the screen
        root_width = self.winfo_screenwidth()
        widget_x = event.x_root
        space_on_right = root_width - widget_x

        # Calculate the width of the tooltip's text
        # based on the length of the message string
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
        """
        Hides the widget when the mouse leaves the widget.
        """

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
            self.msg_var.set(kwargs.pop("message"))

        self.message_label.configure(**kwargs)
