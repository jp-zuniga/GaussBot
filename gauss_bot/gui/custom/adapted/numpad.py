"""
Adapted from:
* https://github.com/Akascape/CTkPopupKeyboard
* Author: Akash Bora

Modified by: Joaquín Zúñiga, on 11/18/2024
Formatted, type-annotated, and simplified.
Transformed for use as a calculator-like numpad,
with mathematical functions for use in this project.
"""
from re import (
    compile as comp,
    escape,
)

from typing import TYPE_CHECKING

from tkinter import END
from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkToplevel as ctkTop,
    ThemeManager,
)

from gauss_bot import (
    FUNCTIONS,
    resize_image,
)

if TYPE_CHECKING:
    from gauss_bot.gui.custom import CustomEntry


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

        resizes = {
            name: resize_image(
                img,
                (4, 8)
                if name not in ("x", "abs(x)", "x^n", "b^x", "e^x")
                else (3, 7)
            )

            for name, img in FUNCTIONS.items()
            if name not in ("f(x)", "log-b(x)", "k")
        }

        self.images: dict[str, ctkImage] = {
            "x": resizes["x"],
            "abs(x)": resizes["abs(x)"],
            "x^n": resizes["x^n"],
            "b^x": resizes["b^x"],
            "e^x": resizes["e^x"],
            "ln(x)": resizes["ln(x)"],
            "sen(x)": resizes["sen(x)"],
            "cos(x)": resizes["cos(x)"],
            "tan(x)": resizes["tan(x)"],
        }

        self.key_pad = {
            "row1": ["x", "abs(x)", "x^n"],
            "row2": ["b^x", "e^x", "ln(x)"],
            "row3": ["sen(x)", "cos(x)", "tan(x)"],
            "row4": ["⯇"],
        }

        self.attach.unbind("<Alt_L>")
        self.attach.unbind("<Escape>")
        self.attach.bind("<Alt_L>", self.render)
        self.attach.bind("<Escape>", self.hide)
        self.unbind("<Escape>")
        self.bind("<Escape>", self.hide)

        self.fg_color = ThemeManager.theme["CTkFrame"]["fg_color"]
        self.show_frame = ctkFrame(
            self,
            fg_color=self.fg_color,
            corner_radius=0,
            border_width=3,
        )

        self.row1 = ctkFrame(self.show_frame, fg_color=self.fg_color)
        self.row2 = ctkFrame(self.show_frame, fg_color=self.fg_color)
        self.row3 = ctkFrame(self.show_frame, fg_color=self.fg_color)
        self.row4 = ctkFrame(self.show_frame, fg_color=self.fg_color)

        self.show_frame.pack(expand=True, fill="both")
        self.row1.grid(row=1, column=0, pady=(10, 0))
        self.row2.grid(row=2, column=0, padx=10)
        self.row3.grid(row=3, column=0, padx=10)
        self.row4.grid(row=4, column=0, pady=(0, 10))

        self.init_keys()
        self.render()

    def init_keys(self):
        """
        Initializes self.keypad and creates the
        buttons for each key on the numpad.
        """

        hover_color = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        for row, keys in self.key_pad.items():
            if row == "row1":
                for i, k in enumerate(keys):
                    ctkButton(
                        self.row1,
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

            elif row == "row2":
                for i, k in enumerate(keys):
                    ctkButton(
                        self.row2,
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

            elif row == "row3":
                for i, k in enumerate(keys):
                    ctkButton(
                        self.row3,
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

            elif row == "row4":
                ctkButton(
                    self.row4,
                    text=self.key_pad["row4"][0],
                    width=150,
                    height=50,
                    border_spacing=0,
                    border_width=0,
                    bg_color=self.fg_color,
                    fg_color=self.fg_color,
                    hover_color=hover_color,
                    command=lambda: self.key_press("⯇"),
                ).grid(row=0, column=i, sticky="nsew")

            self.hidden = False

    def key_press(self, k: str) -> None:
        """
        Binding for key press event.
        Handles deleting if backspace is pressed,
        else just inserts the pressed key into self.attach
        """

        end_pattern = comp(r"(\s*[\+\-]\s*|\s+)$")
        func_pattern = comp(
            r"|".join(
                escape(func)
                .replace(r"\(x\)", r"\([^)]*\)")
                .replace(r"\^n", r"\^\([^)]*\)")
                for func in self.images
            ) + r"|x"
        )

        if k == "⯇":
            text = self.attach.get()
            matches = list(func_pattern.finditer(text))
            if matches:
                last_match = matches[-1]
                text = text[:last_match.start()]
            elif end_pattern.search(text):
                text = end_pattern.sub("", text)

            self.attach.delete(0, END)
            self.attach.insert(0, text)
            return

        if "^n" in k:
            k = k.replace("^n", "^()")
        elif "^x" in k:
            k = k.replace("^x", "^()")
        elif "(x)" in k:
            k = k.replace("(x)", "()")

        self.attach.insert(END, k)
        if not k.endswith("()"):
            return

        cursor_pos = self.attach.index(END) - 1
        self.attach.icursor(cursor_pos)
        self.attach.focus_set()

    def destroy(self):
        """
        Destroys self and sets self.disabled to True.
        """

        self.disabled = True
        super().destroy()

    def hide(self, event=None) -> str:
        """
        Reskin of withdraw() to handle custom key-bindings.
        """

        del event
        if self.disabled:
            return "break"

        self.hidden = True
        super().withdraw()
        return "break"

    def render(self, event=None) -> str:
        """
        Reskin of iconify() to handle custom key-bindings.
        """

        del event
        if self.disabled:
            return "break"

        if self.hidden:
            self.deiconify()
            self.focus()
            self.hidden = False
            x_pos = self.attach.winfo_rootx()
            y_pos = self.attach.winfo_rooty() + self.attach.winfo_reqheight() + 5

            self.geometry(
                f"{self.show_frame.winfo_reqwidth()}x" +
                f"{self.show_frame.winfo_reqheight()}" +
                f"+{x_pos}+{y_pos}"
            )

        else:
            self.hide()
            self.hidden = True
        return "break"
