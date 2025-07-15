"""
Based on CTkPopupKeyboard by Akash Bora (https://github.com/Akascape/CTkPopupKeyboard).
"""

from re import compile as comp, escape
from tkinter import END, INSERT
from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTkImage, CTkToplevel, ThemeManager

from src.utils import NUMPAD_KEYS, resize_image

if TYPE_CHECKING:
    from src.gui.custom import CustomEntry


class CustomNumpad(CTkToplevel):
    """
    Creates a numpad which, instead of regular numbers, has mathematical functions.
    """

    def __init__(self, attach: "CustomEntry") -> None:
        """
        Initialize numpad design.

        Args:
            attach: Widget that numpad is attached to.

        """

        super().__init__()
        self.transient()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(width=False, height=False)

        self.attach = attach
        self.disabled = False
        self.hidden = True

        self.images: dict[str, CTkImage] = {
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
        self.attach.bind("<Control-Tab>", lambda _: self.render())
        self.attach.bind("<Escape>", lambda _: self.hide())
        self.attach.bind("<Unmap>", lambda _: self.hide())
        self.attach.bind("<Configure>", lambda _: self.hide())

        self.unbind("<Escape>")
        self.bind("<Escape>", lambda _: self.hide())

        self.fg_color = ThemeManager.theme["CTkFrame"]["fg_color"]
        self.show_frame = CTkFrame(
            self,
            fg_color=self.fg_color,
            corner_radius=0,
            border_width=3,
        )

        self.show_frame.columnconfigure(0, weight=1)
        self.row1 = CTkFrame(self.show_frame, fg_color=self.fg_color)
        self.row2 = CTkFrame(self.show_frame, fg_color=self.fg_color)
        self.row3 = CTkFrame(self.show_frame, fg_color=self.fg_color)
        self.row4 = CTkFrame(self.show_frame, fg_color=self.fg_color)

        self.show_frame.pack(expand=True, fill="both")
        self.row1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ns")
        self.row2.grid(row=1, column=0, padx=10, sticky="ns")
        self.row3.grid(row=2, column=0, padx=10, sticky="ns")
        self.row4.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ns")

        self.init_keys()
        self.render()

    def init_keys(self) -> None:
        """
        Creates the buttons for each key on the numpad.
        """

        from src.gui.custom import IconButton

        hover_color: str = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        for row, keys in self.key_pad.items():
            match row:
                case "row1":
                    master: CTkFrame = self.row1
                case "row2":
                    master: CTkFrame = self.row2
                case "row3":
                    master: CTkFrame = self.row3
                case "row4":
                    master: CTkFrame = self.row4

            for i, k in enumerate(keys):
                IconButton(
                    master,  # type: ignore[reportPossiblyUnboundVariable]
                    image=self.images[k],
                    width=50,
                    height=50,
                    bg_color=self.fg_color,
                    fg_color=self.fg_color,
                    hover_color=hover_color,
                    command=lambda k=k: self.key_press(k),
                ).grid(row=0, column=i, sticky="nsew")

            self.hidden = False

    def key_press(self, k: str) -> None:  # type: ignore[reportRedeclaration]
        """
        Binding for key press event.

        Args:
            k: Key pressed.

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
                cursor_pos: int | str = INSERT
            else:
                cursor_pos: int | str = last_match.start() + index_adjust

            self.attach.icursor(cursor_pos)
        except IndexError:
            self.attach.icursor(END)
        self.attach.focus_set()

    def destroy(self) -> None:
        """
        Destroy `self` and set `self.disabled` to `True`.
        """

        self.disabled = True
        super().destroy()

    def hide(self) -> str:
        """
        Wrapper for withdraw() to handle custom key-bindings.
        """

        if self.disabled:
            return "break"

        self.hidden = True
        super().withdraw()
        return "break"

    def render(self) -> str:
        """
        Render widget if hidden; otherwise, hide it.
        """

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

    def _adjust_position(self) -> None:
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
            0,
            lambda: self.geometry(f"{numpad_width}x{numpad_height}+{x_pos}+{y_pos}"),
        )
