"""
Based on CTkMessagebox by Akash Bora (https://github.com/Akascape/CTkMessagebox).
"""

from typing import TYPE_CHECKING, Literal

from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkToplevel, ThemeManager

from src.gui.custom.custom_widgets import IconButton
from src.utils import MSGBOX_ICONS, QUIT_ICON

if TYPE_CHECKING:
    from tkinter import Event

    from src.gui import GaussUI


class CustomMessageBox(CTkToplevel):
    """
    Personalized MessageBox with modern UI elements.
    """

    def __init__(
        self,
        master: "GaussUI",
        name: str,
        msg: str,
        button_options: tuple[str, str | None, str | None],
        icon: Literal["check", "error", "info", "question", "warning"] = "info",
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Initialize button and window dragging functionality.

        Args:
            master:         Root application instance.
            name:           Window title.
            msg:            Message to place in window.
            button_options: Possible interactions (1 minimum, 3 maximum).
            icon:           Window icon.
            kwargs:         Frame initialization arguments.

        Raises:
            ValueError: If width or height are less than 250 or 125, respectively.

        """

        super().__init__()

        self.title(name)
        self.overrideredirect(True)
        self.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.button_event(""),
        )

        self.resizable(width=False, height=False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.master_window = master
        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.offset_x = 0
        self.offset_y = 0
        self.option1, self.option2, self.option3 = button_options
        self.clicked_button: str = ""

        bg_color: str = kwargs.pop(
            "bg_color",
            ThemeManager.theme["CTkFrame"]["fg_color"],
        )

        width = kwargs.pop("width", 360)
        height = kwargs.pop("height", 160)
        spawn_x = int(
            self.master_window.winfo_width() * 0.5
            + self.master_window.winfo_x()
            - 0.5 * width,
        )

        spawn_y = int(
            self.master_window.winfo_height() * 0.5
            + self.master_window.winfo_y()
            - 0.5 * height,
        )

        self.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")
        self.lift()

        self.frame_top = CTkFrame(
            self,
            width=width,
            corner_radius=24,
            border_width=3,
            bg_color=bg_color,
            fg_color=kwargs.pop(
                "fg_color",
                ThemeManager.theme["CTkFrame"]["top_fg_color"],
            ),
        )

        self.frame_top.grid(sticky="nsew")
        self.frame_top.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_top.grid_rowconfigure((0, 1, 2), weight=1)

        self.icon_label = CTkLabel(self.frame_top, image=MSGBOX_ICONS[icon], text="")
        self.icon_label.grid(row=0, column=0, padx=(20, 5), pady=(10, 8), sticky="nsw")

        self.title_label = CTkLabel(self.frame_top, text=name)
        self.title_label.grid(row=0, column=1, pady=(10, 8), sticky="nsw")

        for widget in (self.icon_label, self.title_label, self.frame_top):
            widget.bind("<B1-Motion>", self.move_window)
            widget.bind("<ButtonPress-1>", self.set_old_xy)

        IconButton(
            self.frame_top,
            image=QUIT_ICON,
            hover_color=bg_color,
            command=lambda: self.button_event(""),
        ).grid(row=0, column=2, padx=(0, 10), pady=(10, 8), sticky="nse")

        CTkLabel(
            self.frame_top,
            fg_color=bg_color,
            text=msg,
            justify="center",
            wraplength=width - 30,
        ).grid(row=1, column=0, columnspan=3, padx=3, ipady=10, sticky="nsew")

        self.button_1 = CTkButton(
            self.frame_top,
            height=30,
            text=self.option1,
            command=lambda: self.button_event(self.option1),
        )

        if self.option2:
            self.button_2 = CTkButton(
                self.frame_top,
                height=30,
                text=self.option2,
                command=lambda: self.button_event(self.option2),  # type: ignore[reportArgumentType]
            )
        if self.option3:
            self.button_3 = CTkButton(
                self.frame_top,
                height=30,
                text=self.option3,
                command=lambda: self.button_event(self.option3),  # type: ignore[reportArgumentType]
            )

        if all(button_options):
            self.button_1.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="nsew")
            self.button_2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
            self.button_3.grid(row=2, column=2, padx=(0, 10), pady=10, sticky="nsew")
        elif self.option2:
            self.button_1.grid(row=2, column=1, padx=(10, 0), pady=10, sticky="nsew")
            self.button_2.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        else:
            self.button_1.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self._set_scaling(
            self.master_window.escala_inicial,
            self.master_window.escala_inicial,
        )

        self.grab_set()

    def button_event(self, selection: str) -> None:
        """
        Destroy self and set the event attribute to `selection`.

        Args:
            selection: Button that triggered event.

        """

        self.grab_release()
        self.destroy()

        if selection != "":
            self.clicked_button = selection
            self.master_window.focus_force()

    def get(self) -> str:
        """
        Wait for window to be destroyed, before returning `self.clicked_button`.
        """

        if self.winfo_exists():
            self.master.wait_window(self)
        return self.clicked_button

    def set_old_xy(self, event: "Event") -> None:
        """
        Save current x and y coordinates of window.
        """

        self.offset_x = event.x_root - self.winfo_x()
        self.offset_y = event.y_root - self.winfo_y()

    def move_window(self, event: "Event") -> None:
        """
        Move window according to the event received.
        """

        new_x = int(event.x_root - self.offset_x)
        new_y = int(event.y_root - self.offset_y)
        self.geometry(f"+{new_x}+{new_y}")
