"""
Adapted from:
* https://github.com/Akascape/CTkMessagebox
* Author: Akash Bora

Modified by: Joaquín Zúñiga, on 11/25/2024
Formatted file and added type annotations for personal use,
and heavily simplified the functionality for use in this project.
"""

from tkinter import Event
from typing import TYPE_CHECKING, Literal, Optional

from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkToplevel as ctkTop,
    ThemeManager,
)

from ..custom_widgets import IconButton
from ....utils import MSGBOX_ICONS, QUIT_ICON

if TYPE_CHECKING:
    from ... import GaussUI


class CustomMessageBox(ctkTop):
    """
    Personalized MessageBox with modern UI elements.
    """

    def __init__(
        self,
        master: "GaussUI",
        name: str,
        msg: str,
        button_options: tuple[str, Optional[str], Optional[str]],
        icon: Literal["check", "error", "info", "question", "warning"] = "info",
        **kwargs,
    ):
        """
        Must receive at least one option, with support for up to 3 buttons.
        * ValueError: if width or height are less than 250 or 125, respectively.
        """

        super().__init__()
        self.master_window = master
        self.title(name)
        self.overrideredirect(True)
        self.protocol("WM_DELETE_WINDOW", lambda _: self.button_event(""))

        self.resizable(width=False, height=False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.width = kwargs.pop("width", 360)
        self.height = kwargs.pop("height", 160)

        self.spawn_x = int(
            self.master_window.winfo_width() * 0.5
            + self.master_window.winfo_x()
            - 0.5 * self.width
        )

        self.spawn_y = int(
            self.master_window.winfo_height() * 0.5
            + self.master_window.winfo_y()
            - 0.5 * self.height
        )

        self.after(
            5,
            self.geometry(f"{self.width}x{self.height}+{self.spawn_x}+{self.spawn_y}"),
        )

        self.lift()
        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.oldx = 0
        self.oldy = 0

        self.msgbox_name = name
        self.msg = msg
        self.clicked_button = ""
        self.option1, self.option2, self.option3 = button_options

        self.bg_color = self._apply_appearance_mode(
            ThemeManager.theme["CTkFrame"]["fg_color"]
        )

        self.fg_color = self._apply_appearance_mode(
            ThemeManager.theme["CTkFrame"]["top_fg_color"]
        )

        self.frame_top = ctkFrame(
            self,
            width=self.width,
            corner_radius=24,
            border_width=3,
            bg_color=self.bg_color,
            fg_color=self.fg_color,
        )

        self.icon: ctkImage
        self.frame_top.grid(sticky="nsew")
        self.frame_top.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_top.grid_rowconfigure((0, 1, 2), weight=1)

        self.load_icon(icon)
        self.icon_label = ctkLabel(self.frame_top, image=self.icon, text="")
        self.icon_label.grid(row=0, column=0, padx=(20, 5), pady=(10, 8), sticky="nsw")

        self.title_label = ctkLabel(self.frame_top, text=self.msgbox_name)
        self.title_label.grid(row=0, column=1, pady=(10, 8), sticky="nsw")

        self.button_close = IconButton(
            self.frame_top,
            app=self.master_window,
            image=QUIT_ICON,
            hover_color=self.bg_color,
            command=lambda: self.button_event(""),
            width=30,
            height=30,
        ).grid(row=0, column=2, padx=(0, 10), pady=(10, 8), sticky="nse")

        for widget in (self.icon_label, self.title_label, self.frame_top):
            widget.bind("<B1-Motion>", self.move_window)
            widget.bind("<ButtonPress-1>", self.set_old_xy)

        ctkLabel(
            self.frame_top,
            fg_color=self.bg_color,
            text=self.msg,
            justify="center",
            wraplength=self.width - 30,
        ).grid(row=1, column=0, columnspan=3, padx=3, sticky="nsew")

        self.button_1 = ctkButton(
            self.frame_top,
            height=30,
            text=self.option1,
            command=lambda: self.button_event(self.option1),
        )

        if self.option2:
            self.button_2 = ctkButton(
                self.frame_top,
                height=30,
                text=self.option2,
                command=lambda: self.button_event(self.option2),
            )
        if self.option3:
            self.button_3 = ctkButton(
                self.frame_top,
                height=30,
                text=self.option3,
                command=lambda: self.button_event(self.option3),
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
            self.master_window.escala_inicial, self.master_window.escala_inicial
        )

        self.grab_set()

    def button_event(self, selection: str) -> None:
        """
        Destroys self and sets the event attribute to the received event.
        """

        self.grab_release()
        self.destroy()

        if selection != "":
            self.clicked_button = selection
            self.master_window.focus_force()

    def get(self):
        """
        Waits for the message box window to be destroyed and then returns the event.
        """

        if self.winfo_exists():
            self.master.wait_window(self)
        return self.clicked_button

    def set_old_xy(self, event: Event) -> None:
        """
        Saves the current x and y coordinates of the window.
        """

        self.oldx = event.x
        self.oldy = event.y

    def move_window(self, event: Event) -> None:
        """
        Moves the window according to the event received.
        """

        self.y = event.y_root - self.oldy
        self.x = event.x_root - self.oldx
        self.geometry(f"+{self.x}+{self.y}")

    def load_icon(self, icon: str) -> None:
        """
        Sets self.icon to the corresponding icon.
        """

        self.icon = MSGBOX_ICONS[icon]
