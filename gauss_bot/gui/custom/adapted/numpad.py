"""
Adapted from:
* https://github.com/Akascape/CTkPopupKeyboard
* Author: Akash Bora

Modified by: Joaquín Zúñiga, on 11/18/2024
Formatted, type-annotated, and simplified.
Transformed for use as a calculator-like numpad
with mathematical functions for use in this project.
"""

from re import compile as comp, escape
from tkinter import END, INSERT, Event
from typing import TYPE_CHECKING, Optional

from customtkinter import (
    CTkButton as ctkButton,
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
        self.focus()
        self.transient()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(width=False, height=False)

        self.attach = attach
        self.disabled = False
        self.hidden = True

        self.images: dict[str, ctkImage] = {
            "pi": resize_image(NUMPAD_KEYS["pi"], (3, 6.4)),
            "x": resize_image(NUMPAD_KEYS["x"], (3, 6.4)),
            "x^n": resize_image(NUMPAD_KEYS["x^n"], (3, 7.2)),
            "b^x": resize_image(NUMPAD_KEYS["b^x"], (3.5, 7.5)),
            "e^x": resize_image(NUMPAD_KEYS["e^x"], (3.5, 7.5)),
            "ln(x)": resize_image(NUMPAD_KEYS["ln(x)"]),
            "sin(x)": resize_image(NUMPAD_KEYS["sin(x)"], (3.8, 7.8)),
            "cos(x)": resize_image(NUMPAD_KEYS["cos(x)"]),
            "tan(x)": resize_image(NUMPAD_KEYS["tan(x)"]),
            "+": resize_image(NUMPAD_KEYS["plus"], (3, 7)),
            "-": resize_image(NUMPAD_KEYS["minus"], (3, 7)),
            "*": resize_image(NUMPAD_KEYS["times"], (3, 7)),
            "/": resize_image(NUMPAD_KEYS["divide"], (3, 7)),
        }

        self.key_pad = {
            "row1": ["pi", "x", "x^n"],
            "row2": ["b^x", "e^x", "ln(x)"],
            "row3": ["sin(x)", "cos(x)", "tan(x)"],
            "row4": ["+", "-", "*", "/"],
        }

        self.attach.unbind("<Escape>")
        self.attach.unbind("<Control-Tab>")
        self.attach.unbind("<Unmap>")
        self.attach.bind("<Control-Tab>", self.render)
        self.attach.bind("<Escape>", self.hide)
        self.attach.bind("<Configure>", self.hide)
        self.attach.bind("<Unmap>", self.hide)

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

        hover_color = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        for row, keys in self.key_pad.items():
            match row:
                case "row1":
                    master = self.row1
                case "row2":
                    master = self.row2
                case "row3":
                    master = self.row3
                case "row4":
                    master = self.row4

            for i, k in enumerate(keys):
                ctkButton(
                    master,
                    text="",
                    image=self.images[k],
                    width=50,
                    height=50,
                    border_spacing=0,
                    border_width=0,
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

        set_from_end = False
        index_adjust: int = 1
        re_pattern = r"\(([^()]*)\)"

        if k == "b^x":
            k = "^()"
            re_pattern = escape("^()")
            index_adjust = 0
        elif "^n" in k:
            k = k.replace("^n", "^()")
        elif "^x" in k:
            k = k.replace("^x", "^()")
        elif "(x)" in k:
            k = k.replace("(x)", "()")
        elif k in ("+", "-", "/"):
            k = f" {k} "
            set_from_end = True
        else:
            set_from_end = True

        self.attach.insert(INSERT, k)
        try:
            text = self.attach.get()
            last_match = list(comp(re_pattern).finditer(text))[-1]

            if set_from_end:
                cursor_pos = INSERT
            else:
                cursor_pos = last_match.start() + index_adjust  # type: ignore

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
        """
        Wrapper for iconify() to handle custom key-bindings.
        """

        del event
        if self.disabled:
            return "break"

        if self.hidden:
            self.deiconify()
            self.focus()
            self.lift()
            self.hidden = False

            attach_width = self.attach.winfo_reqwidth()
            numpad_width = self.show_frame.winfo_reqwidth()
            x_pos = self.attach.winfo_rootx() + (attach_width - numpad_width) // 2
            y_pos = self.attach.winfo_rooty() + self.attach.winfo_reqheight() + 10

            self.geometry(
                f"{numpad_width}x{self.show_frame.winfo_reqheight()}"
                + f"+{x_pos}+{y_pos}"
            )

        else:
            self.hide()
            self.hidden = True
        return "break"
