"""
Adapted from:
* https://github.com/Akascape/CTkScrollableDropdown
* Author: Akash Bora

Modified by: Joaquín Zúñiga, on 11/4/2024
Heavily simplified for the purpose of this project.
"""

from typing import (
    Any,
    Callable,
    Optional,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkImage as ctkImage,
    CTkScrollableFrame as ctkScrollFrame,
    CTkToplevel as ctkTop,
    ThemeManager,
)


class CustomScrollableDropdown(ctkTop):
    def __init__(
        self,
        attach: ctkButton,
        height: int = 200,
        width: int = 200,
        x: Optional[int] = None,
        y: Optional[int] = None,

        fg_color: Optional[str] = None,
        hover_color: Optional[str] = None,
        text_color: Optional[str] = None,
        values: list[str] = [],
        image_values: list[ctkImage] = [],
        command: Optional[Callable[[Any], Any]] = None,

        button_height: int = 20,
        button_color: Optional[str] = None,
        scrollbar: bool = True,
        scrollbar_button_color: Optional[str] = None,
        scrollbar_button_hover_color: Optional[str] = None,
        frame_border_width: int = 2,
        frame_corner_radius: int = 20,
        frame_border_color: Optional[str] = None,

        resize: bool = True,
        justify: str = "center",
        **button_kwargs,
    ):

        super().__init__(master=attach.winfo_toplevel(), takefocus=1)
        self.focus()
        self.lift()
        self.attach = attach
        self.corner = frame_corner_radius

        self.hide = True  # type: ignore
        self.withdraw()
        self.update()

        self.after(100, lambda: self.overrideredirect(True))
        self.transparent_color = self._apply_appearance_mode(self._fg_color)
        self.attributes("-transparentcolor", self.transparent_color)

        self.attach.bind(
            "<Button-1>",
            lambda _: self._iconify(),
            add="+"
        )

        self.attach.bind(
            "<Destroy>",
            lambda _: self._withdraw(),
            add="+"
        )

        # self.attach.bind(
        #     "<Configure>",
        #     lambda _: self._withdraw()
        #     if not self.disable
        #     else None,
        #     add="+",
        # )

        # self.attach.winfo_toplevel().bind(
        #     "<Configure>",
        #     lambda _: self._withdraw()
        #     if not self.disable
        #     else None,
        #     add="+",
        # )

        # self.attach.winfo_toplevel().bind(
        #     "<ButtonPress>",
        #     lambda _: self._withdraw()
        #     if not self.disable
        #     else None,
        #     add="+",
        # )

        # self.bind(
        #     "<Escape>",
        #     lambda _: self._withdraw()
        #     if not self.disable
        #     else None,
        #     add="+",
        # )

        self.fg_color = (
            ThemeManager.theme["CTkFrame"]["fg_color"]
            if fg_color is None
            else fg_color
        )

        self.button_color = (
            ThemeManager.theme["CTkFrame"]["top_fg_color"]
            if button_color is None
            else button_color
        )

        self.text_color = (
            ThemeManager.theme["CTkLabel"]["text_color"]
            if text_color is None
            else text_color
        )

        self.hover_color = (
            ThemeManager.theme["CTkButton"]["hover_color"]
            if hover_color is None
            else hover_color
        )

        self.scroll_button_color = (
            ThemeManager.theme["CTkScrollbar"]["button_color"]
            if scrollbar_button_color is None
            else scrollbar_button_color
        )

        self.scroll_hover_color = (
            ThemeManager.theme["CTkScrollbar"]["button_hover_color"]
            if scrollbar_button_hover_color is None
            else scrollbar_button_hover_color
        )

        self.frame_border_color = (
            ThemeManager.theme["CTkFrame"]["border_color"]
            if frame_border_color is None
            else frame_border_color
        )

        if scrollbar is False:
            self.scroll_button_color = self.fg_color
            self.scroll_hover_color = self.fg_color

        self.frame: ctkScrollFrame = ctkScrollFrame(  # type: ignore
            self,
            width=width,
            height=height,
            corner_radius=6,
            fg_color=self.fg_color,
            bg_color=self.transparent_color,
            border_width=frame_border_width,
        )

        self.frame._scrollbar.grid_configure(padx=3)
        self.frame.pack(expand=True, fill="both")

        self.height = height
        self.height_new = height
        self.width = width
        self.command = command  # type: ignore
        self.resize = resize

        if justify.lower() == "left":
            self.justify = "w"
        elif justify.lower() == "right":
            self.justify = "e"
        else:
            self.justify = "c"

        self.values = values
        self.image_values = image_values

        self.button_height = button_height
        self.button_num = len(self.values)

        self._init_buttons(**button_kwargs)
        self.resizable(width=False, height=False)
        self.transient(self.master)  # type: ignore

        self.x = x
        self.y = y
        self.hide = True  # type: ignore
        self.update_idletasks()

    def place_dropdown(self):
        print("placing dropdown")  # debug
        self.x_pos = (
            self.attach.winfo_rootx()
            if self.x is None
            else self.x + self.attach.winfo_rootx()
        )

        self.y_pos = (
            self.attach.winfo_rooty() + self.attach.winfo_reqheight() + 5
            if self.y is None
            else self.y + self.attach.winfo_rooty()
        )

        self.width_new = self.attach.winfo_width() if self.width is None else self.width

        if self.resize:
            if self.button_num <= 5:
                self.height_new = self.button_height * self.button_num + 55
            else:
                self.height_new = self.button_height * self.button_num + 35
            if self.height_new > self.height:
                self.height_new = self.height

        self.geometry(
            f"{self.width_new}x{self.height_new}+{self.x_pos}+{self.y_pos}"
        )

        if hasattr(self.attach, "_text_label") and self.attach._text_label is not None:
            self.attach.focus()
        else:
            self.focus()

    def hide(self):
        self._withdraw()

    def _deiconify(self):
        print("deiconifying")  # debug
        if len(self.values) > 0:
            self.deiconify()

    def _iconify(self):
        print(f"Iconify called, hide state: {self.hide}")  # debug
        if self.attach.cget("state") == "disabled":
            print("cant iconify")  # debug
            return
        if self.hide:
            print("Showing dropdown")  # debug
            self.event_generate("<<Opened>>")
            self.focus()
            self.hide = False
            self.place_dropdown()
            self._deiconify()
        else:
            print("Hiding dropdown")  # debug
            self._withdraw()

    def _withdraw(self):
        if not self.winfo_exists() or not self.winfo_viewable():
            print("cant withdraw")  # debug
            return
        print("withdrawing")  # debug
        self.withdraw()
        self.event_generate("<<Closed>>")
        self.hide = True

    def _attach_key_press(self, k):
        self.event_generate("<<Selected>>")
        if self.command:
            self.command(k)
        self._withdraw()
        self.hide = True

    def _init_buttons(self, **button_kwargs):
        self.i = 0
        self.widgets = {}
        for _ in self.values:
            img = self.image_values[self.i]
            self.widgets[self.i] = ctkButton(
                self.frame,
                text="",
                corner_radius=0,
                height=self.button_height,
                fg_color=self.button_color,
                text_color=self.text_color,
                image=img,
                anchor=self.justify,
                hover_color=self.hover_color,
                command=lambda k=img: self._attach_key_press(k),
                **button_kwargs,
            )

            self.widgets[self.i].pack(fill="x")
            self.i += 1
        self.hide = False

    def configure(self, **kwargs):
        if "height" in kwargs:
            self.height = kwargs.pop("height")
            self.height_new = self.height

        if "alpha" in kwargs:
            self.alpha = kwargs.pop("alpha")

        if "width" in kwargs:
            self.width = kwargs.pop("width")

        if "fg_color" in kwargs:
            self.frame.configure(fg_color=kwargs.pop("fg_color"))

        if "values" in kwargs:
            self.values = kwargs.pop("values")
            self.image_values = None
            self.button_num = len(self.values)
            for key in self.widgets.keys():
                self.widgets[key].destroy()
            self._init_buttons()

        if "image_values" in kwargs:
            self.image_values = kwargs.pop("image_values")
            self.image_values = (
                None
                if len(self.image_values) != len(self.values)
                else self.image_values
            )
            if self.image_values is not None:
                i = 0
                for key in self.widgets.keys():
                    self.widgets[key].configure(image=self.image_values[i])
                    i += 1

        if "button_color" in kwargs:
            button_color = kwargs.pop("button_color")
            for key in self.widgets.keys():
                self.widgets[key].configure(fg_color=button_color)

        if "font" in kwargs:
            font = kwargs.pop("font")
            for key in self.widgets.keys():
                self.widgets[key].configure(font=font)

        if "hover_color" not in kwargs:
            kwargs["hover_color"] = self.hover_color

        for key in self.widgets.keys():
            self.widgets[key].configure(**kwargs)
