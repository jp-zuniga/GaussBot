"""
Based on CTkTooltip by Akash Bora (https://github.com/Akascape/CTkToolTip).
"""

from time import time
from tkinter import Event, Frame, Toplevel

from customtkinter import CTkBaseClass, CTkFont, CTkFrame, CTkLabel, ThemeManager


class Tooltip(Toplevel):
    """
    Mouse-over tooltip with modern design.
    """

    def __init__(  # noqa: PLR0913
        self,
        widget: CTkBaseClass,
        message: str,
        delay: int = 50,
        padx: int = 15,
        pady: int = 5,
        x_offset: int = 20,
        y_offset: int = 20,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Initialize design mouse-over functionality.

        Args:
            widget:   Widget tooltip is attached to.
            message:  Message to place in tooltip label.
            delay:    Millisecond delay for tooltip movement.
            padx:     Horizontal padding for tooltip label.
            pady:     Vertical padding for tooltip label.
            x_offset: Horizontal offset from parent widget.
            y_offset: Vertical offset from parent widget.
            kwargs:   Configuration arguments for widget color and label initialization.

        """

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

        self.frame: CTkFrame = CTkFrame(
            self.transparent_frame,
            border_width=2,
            bg_color=bg,
            fg_color=bg,
        )

        self.message_label = CTkLabel(
            self.frame,
            font=CTkFont(size=10),
            text=message,
            **kwargs,
        )

        self.frame.pack(expand=True, fill="both")
        self.message_label.pack(fill="both", padx=padx, pady=pady, expand=True)

        self.widget.bind("<Enter>", self._on_enter, add="+")
        self.widget.bind("<Leave>", lambda _: self._on_leave(), add="+")
        self.widget.bind("<Motion>", self._on_enter, add="+")
        self.widget.bind("<B1-Motion>", self._on_enter, add="+")
        self.widget.bind("<Destroy>", lambda _: self.hide(), add="+")

    def configure_tooltip(self, **kwargs) -> None:  # noqa: ANN003
        """
        Configure `self`.

        Args:
            kwargs: Config options for Tooltip attributes and `self.message_label`.

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

    def show(self) -> None:
        """
        Render tooltip.
        """

        if not self.widget.winfo_exists():
            self.hide()
            self.destroy()

        if self.status == "inside" and (time() - self.last_moved >= self.delay):
            self.status = "visible"
            self.deiconify()

    def hide(self) -> None:
        """
        Hide tooltip.
        """

        if not self.winfo_exists():
            return
        self.withdraw()
        self.disable = True

    def _on_enter(self, event: Event) -> None:
        """
        Handle tooltip movement.
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
        self.after(self.delay, self.show)

    def _on_leave(self) -> None:
        """
        Hide tooltip when mouse leaves `self.widget`.
        """

        if self.disable:
            return
        self.status = "outside"
        self.withdraw()
