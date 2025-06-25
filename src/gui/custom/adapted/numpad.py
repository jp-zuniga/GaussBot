"""
Adapted from:
* https://github.com/Akascape/CTkPopupKeyboard
* Author: Akash Bora

Modified by: Joaquín Zúñiga, on 11/24/2024
Formatted, type-annotated, and simplified.
Transformed for use as a calculator-like numpad
with mathematical functions for use in this project.
"""

from re import compile as comp, escape
from tkinter import END, INSERT, Event
from typing import TYPE_CHECKING, Optional, Union

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkToplevel as ctkTop,
    ThemeManager,
)

from ....utils import NUMPAD_KEYS, resize_image

if TYPE_CHECKING:
    from ..custom_widgets import CustomEntry


class CustomNumpad(ctkTop):
    """
    Creates a numpad attached to the specified widget.
    Instead of regular numbers, it has mathematical functions as keys.
    """

    def __init__(self, attach: "CustomEntry"):
        super().__init__()
        self.transient()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(width=False, height=False)

        self.attach = attach
        self.disabled = False
        self.hidden = True

        self.images: dict[str, ctkImage] = {
            "pi": resize_image(NUMPAD_KEYS["pi"], 0.04),
            "x": resize_image(NUMPAD_KEYS["x"], 0.04),
            "x^n": resize_image(NUMPAD_KEYS["x^n"], 0.04),
            "b^x": resize_image(NUMPAD_KEYS["b^x"], 0.04),
            "e^x": resize_image(NUMPAD_KEYS["e^x"], 0.04),
            "ln(x)": resize_image(NUMPAD_KEYS["ln(x)"], 0.07),
            "sin(x)": resize_image(NUMPAD_KEYS["sin(x)"], 0.07),
            "cos(x)": resize_image(NUMPAD_KEYS["cos(x)"], 0.07),
            "tan(x)": resize_image(NUMPAD_KEYS["tan(x)"], 0.07),
            "+": resize_image(NUMPAD_KEYS["plus"], 0.02),
            "-": resize_image(NUMPAD_KEYS["minus"], 0.02),
            "*": resize_image(NUMPAD_KEYS["times"], 0.02),
            "/": resize_image(NUMPAD_KEYS["divide"], 0.02),
        }

        self.key_pad = {
            "row1": ["pi", "x"],
            "row2": ["x^n", "b^x", "e^x"],
            "row3": ["ln(x)", "sin(x)", "cos(x)", "tan(x)"],
            "row4": ["+", "-", "*", "/"],
        }

        self.attach.unbind("<Escape>")
        self.attach.unbind("<Control-Tab>")
        self.attach.unbind("<Unmap>")
        self.attach.bind("<Control-Tab>", self.render)
        self.attach.bind("<Escape>", self.hide)
        self.attach.bind("<Unmap>", self.hide)
        self.attach.bind("<Configure>", self.hide)

        self.unbind("<Escape>")
        self.bind("<Escape>", self.hide)

        self.fg_color = ThemeManager.theme["CTkFrame"]["fg_color"]
        self.show_frame = ctkFrame(
            self, fg_color=self.fg_color, corner_radius=0, border_width=3
        )

        self.show_frame.columnconfigure(0, weight=1)
        self.row1 = ctkFrame(self.show_frame, fg_color=self.fg_color)
        self.row2 = ctkFrame(self.show_frame, fg_color=self.fg_color)
        self.row3 = ctkFrame(self.show_frame, fg_color=self.fg_color)
        self.row4 = ctkFrame(self.show_frame, fg_color=self.fg_color)

        self.show_frame.pack(expand=True, fill="both")
        self.row1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ns")
        self.row2.grid(row=1, column=0, padx=10, sticky="ns")
        self.row3.grid(row=2, column=0, padx=10, sticky="ns")
        self.row4.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ns")

        self.init_keys()
        self.render()

    def init_keys(self):
        """
        Creates the buttons for each key on the numpad.
        """

        from ..custom_widgets import IconButton

        hover_color: str = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        for row, keys in self.key_pad.items():
            match row:
                case "row1":
                    master: ctkFrame = self.row1
                case "row2":
                    master: ctkFrame = self.row2
                case "row3":
                    master: ctkFrame = self.row3
                case "row4":
                    master: ctkFrame = self.row4

            for i, k in enumerate(keys):
                IconButton(
                    master,
                    app=self.attach.winfo_toplevel(),
                    image=self.images[k],
                    width=50,
                    height=50,
                    bg_color=self.fg_color,
                    fg_color=self.fg_color,
                    hover_color=hover_color,
                    command=lambda k=k: self.key_press(k),
                ).grid(row=0, column=i, sticky="nsew")

            self.hidden = False

    def key_press(self, k: str) -> None:
        """
        Binding for key press event.
        Handles deleting if backspace is pressed,
        else just inserts the pressed key into self.attach
        """

        set_from_end: bool = False
        index_adjust: int = 1
        re_pattern: str = r"\(([^()]*)\)"

        if k == "b^x":
            k: str = "^()"
            re_pattern = escape("^()")
            index_adjust: int = 0
        elif "^n" in k:
            k: str = k.replace("^n", "^()")
        elif "^x" in k:
            k: str = k.replace("^x", "^()")
        elif "(x)" in k:
            k: str = k.replace("(x)", "()")
        elif k in ("+", "-", "/"):
            k = f" {k} "
            set_from_end: bool = True
        else:
            set_from_end: bool = True

        self.attach.insert(INSERT, k)
        try:
            text: str = self.attach.get()
            last_match = list(comp(re_pattern).finditer(text))[-1]

            if set_from_end:
                cursor_pos: Union[int, str] = INSERT
            else:
                cursor_pos: Union[int, str] = last_match.start() + index_adjust  # type: ignore

            self.attach.icursor(cursor_pos)
        except IndexError:
            self.attach.icursor(END)
        self.attach.focus_set()

    def destroy(self):
        """
        Destroys self and sets self.disabled to True.
        """

        self.disabled = True
        super().destroy()

    def hide(self, event: Optional[Event] = None) -> str:
        """
        Wrapper for withdraw() to handle custom key-bindings.
        """

        del event
        if self.disabled:
            return "break"

        self.hidden = True
        super().withdraw()
        return "break"

    def render(self, event: Optional[Event] = None) -> str:
        if self.disabled:
            return "break"

        if self.hidden:
            self.update_idletasks()
            self.deiconify()
            self.focus()
            self.lift()
            self._adjust_position()
            self.hidden = False
        else:
            self.hide()
            self.hidden = True
        return "break"

    def _adjust_position(self):
        """
        Adjust widget position.
        """

        numpad_width = self.winfo_width()
        numpad_height = self.winfo_height()

        attach_x = self.attach.winfo_rootx()
        attach_y = self.attach.winfo_rooty()
        attach_width = self.attach.winfo_width()
        attach_height = self.attach.winfo_height()

        x_pos = attach_x + (attach_width - numpad_width) // 2
        y_pos = attach_y + attach_height + 10

        self.after(
            0, lambda: self.geometry(f"{numpad_width}x{numpad_height}+{x_pos}+{y_pos}")
        )
