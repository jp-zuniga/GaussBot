"""
Adapted from:
* https://github.com/Akascape/CTkScrollableDropdown
* Author: Akash Bora
Modified by: Joaquín Zúñiga, on 11/4/2024
"""

from difflib import SequenceMatcher
from time import sleep
from typing import (
    Callable,
    Optional,
)

from tkinter import StringVar
from customtkinter import (
    CTkBaseClass as ctkBase,
    CTkButton as ctkButton,
    CTkComboBox as ctkCombo,
    CTkEntry as ctkEntry,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkScrollableFrame as ctkScrollFrame,
    CTkToplevel as ctkTop,
    CTkOptionMenu as ctkOptionMenu,
    ThemeManager,
)


class CustomScrollableDropdown(ctkTop):
    def __init__(
        self,
        attach: ctkBase,
        height: int = 200,
        width: int = 200,
        x: Optional[int] = None,
        y: Optional[int] = None,

        fg_color: Optional[str] = None,
        hover_color: Optional[str] = None,
        text_color: Optional[str] = None,
        values: list[str] = [],
        image_values: list[ctkImage] = [],
        command: Optional[Callable[[Optional[str]], str]] = None,

        button_height: int = 20,
        button_color: Optional[str] = None,
        scrollbar: bool = True,
        scrollbar_button_color: Optional[str] = None,
        scrollbar_button_hover_color: Optional[str] = None,
        frame_border_width: int = 2,
        frame_corner_radius: int = 20,
        frame_border_color: Optional[str] = None,

        resize: bool = True,
        double_click: bool = False,
        autocomplete: bool = False,
        alpha: float = 0.97,
        justify: str = "center",
        **button_kwargs,
    ):

        super().__init__(master=attach.winfo_toplevel(), takefocus=1)
        self.focus()
        self.lift()
        self.alpha = alpha
        self.attach = attach
        self.corner = frame_corner_radius
        self.padding = 0
        self.focus_something = False
        self.disable = True
        self.disable = False

        self.hide = True  # type: ignore
        self.update()

        self.after(100, lambda: self.overrideredirect(True))
        self.transparent_color = self._apply_appearance_mode(self._fg_color)
        self.attributes("-transparentcolor", self.transparent_color)
        self.attributes("-alpha", 0)

        self.attach.bind(
            "<Configure>",
            lambda _: self._withdraw() if not self.disable else None,
            add="+",
        )

        self.attach.winfo_toplevel().bind(
            "<Configure>",
            lambda _: self._withdraw() if not self.disable else None,
            add="+",
        )

        self.attach.winfo_toplevel().bind(
            "<ButtonPress>",
            lambda _: self._withdraw() if not self.disable else None,
            add="+",
        )

        self.bind(
            "<Escape>",
            lambda _: self._withdraw() if not self.disable else None,
            add="+",
        )

        self.fg_color = (
            ThemeManager.theme["CTkFrame"]["fg_color"] if fg_color is None else fg_color
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
            corner_radius=self.corner,
            fg_color=self.fg_color,
            bg_color=self.transparent_color,
            border_width=frame_border_width,
            border_color=self.frame_border_color,
            scrollbar_button_color=self.scroll_button_color,
            scrollbar_button_hover_color=self.scroll_hover_color,
        )

        self.frame._scrollbar.grid_configure(padx=3)
        self.frame.pack(expand=True, fill="both")
        self.dummy_entry = ctkEntry(
            self.frame,
            fg_color="transparent",
            border_width=0,
            height=1,
            width=1
        )

        self.no_match = ctkLabel(self.frame, text="No Match")
        self.height = height
        self.height_new = height
        self.width = width
        self.command = command  # type: ignore
        self.fade = False
        self.resize = resize
        self.autocomplete = autocomplete
        self.var_update = StringVar()
        self.appear = False

        if justify.lower() == "left":
            self.justify = "w"
        elif justify.lower() == "right":
            self.justify = "e"
        else:
            self.justify = "c"

        self.button_height = button_height
        self.values = values
        self.button_num = len(self.values)
        self.image_values = (
            None if len(image_values) != len(self.values) else image_values
        )

        self.resizable(width=False, height=False)
        self._init_buttons(**button_kwargs)
        self.transient(self.master)  # type: ignore

        if (double_click or
            isinstance(self.attach, ctkEntry) or
            isinstance(self.attach, ctkCombo)):
            self.attach.bind("<Double-Button-1>", lambda _: self._iconify(), add="+")
        else:
            self.attach.bind("<Button-1>", lambda _: self._iconify(), add="+")

        if isinstance(self.attach, ctkCombo):
            self.attach._canvas.tag_bind(
                "right_parts", "<Button-1>", lambda _: self._iconify()
            )

            self.attach._canvas.tag_bind(
                "dropdown_arrow", "<Button-1>", lambda _: self._iconify()
            )

            if self.command is None:
                self.command = self.attach.set

        if isinstance(self.attach, ctkOptionMenu):
            self.attach._canvas.bind("<Button-1>", lambda _: self._iconify())
            self.attach._text_label.bind("<Button-1>", lambda _: self._iconify())
            if self.command is None:
                self.command = self.attach.set

        self.attach.bind("<Destroy>", lambda _: self._destroy(), add="+")

        self.update_idletasks()
        self.x = x
        self.y = y

        if self.autocomplete:
            self.bind_autocomplete()

        self.withdraw()
        self.attributes("-alpha", self.alpha)

    def hide(self):
        self._withdraw()

    def popup(self, x=None, y=None):
        self.x = x
        self.y = y
        self.hide = True
        self._iconify()

    def place_dropdown(self):
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

        self.fade_in()
        self.attributes("-alpha", self.alpha)
        self.attach.focus()

    def live_update(self, string=None):
        if not self.appear:
            return
        if self.disable:
            return
        if self.fade:
            return
        if string:
            string = string.lower()
            self._deiconify()
            i = 1
            for key in self.widgets.keys():
                s = self.widgets[key].cget("text").lower()
                text_similarity = SequenceMatcher(
                    None, s[0 : len(string)], string
                ).ratio()
                similar = s.startswith(string) or text_similarity > 0.75
                if not similar:
                    self.widgets[key].pack_forget()
                else:
                    self.widgets[key].pack(fill="x", pady=2, padx=(self.padding, 0))
                    i += 1

            if i == 1:
                self.no_match.pack(fill="x", pady=2, padx=(self.padding, 0))
            else:
                self.no_match.pack_forget()
            self.button_num = i
            self.place_dropdown()

        else:
            self.no_match.pack_forget()
            self.button_num = len(self.values)
            for key in self.widgets.keys():
                self.widgets[key].destroy()
            self._init_buttons()
            self.place_dropdown()

        self.frame._parent_canvas.yview_moveto(0.0)
        self.appear = False

    def insert(self, value, **kwargs):
        self.widgets[self.i] = ctkButton(
            self.frame,
            text=value,
            height=self.button_height,
            fg_color=self.button_color,
            text_color=self.text_color,
            hover_color=self.hover_color,
            anchor=self.justify,
            command=lambda k=value: self._attach_key_press(k),
            **kwargs,
        )

        self.widgets[self.i].pack(fill="x", pady=2, padx=(self.padding, 0))
        self.i += 1
        self.values.append(value)

    def bind_autocomplete(self):
        def appear(x):
            self.appear = True

        if isinstance(self.attach, ctkCombo):
            self.attach._entry.configure(textvariable=self.var_update)
            self.attach._entry.bind("<Key>", appear)
            self.attach.set(self.values[0])
            self.var_update.trace_add("write", self._update)

        if isinstance(self.attach, ctkEntry):
            self.attach.configure(textvariable=self.var_update)
            self.attach.bind("<Key>", appear)
            self.var_update.trace_add("write", self._update)

    def fade_out(self):
        for i in range(100, 0, -10):
            if not self.winfo_exists():
                break
            self.attributes("-alpha", i / 100)
            self.update()
            sleep(1 / 100)

    def fade_in(self):
        for i in range(0, 100, 10):
            if not self.winfo_exists():
                break
            self.attributes("-alpha", i / 100)
            self.update()
            sleep(1 / 100)

    def destroy_popup(self):
        self.destroy()
        self.disable = True

    def _destroy(self):
        self.after(500, self.destroy_popup)

    def _update(self, a, b, c):
        self.live_update(self.attach._entry.get())

    def _withdraw(self):
        if not self.winfo_exists():
            return
        if self.winfo_viewable() and self.hide:
            self.withdraw()

        self.event_generate("<<Closed>>")
        self.hide = True

    def _init_buttons(self, **button_kwargs):
        self.i = 0
        self.widgets = {}
        for row in self.values:
            self.widgets[self.i] = ctkButton(
                self.frame,
                text=row,
                height=self.button_height,
                fg_color=self.button_color,
                text_color=self.text_color,
                image=self.image_values[self.i]
                if self.image_values is not None
                else None,
                anchor=self.justify,
                hover_color=self.hover_color,
                command=lambda k=row: self._attach_key_press(k),
                **button_kwargs,
            )

            self.widgets[self.i].pack(fill="x", pady=2, padx=(self.padding, 0))
            self.i += 1
        self.hide = False

    def _iconify(self):
        if self.attach.cget("state") == "disabled":
            return
        if self.disable:
            return
        if self.winfo_ismapped():
            self.hide = False
        if self.hide:
            self.event_generate("<<Opened>>")
            self.focus()
            self.hide = False
            self.place_dropdown()
            self._deiconify()
            if self.focus_something:
                self.dummy_entry.pack()
                self.dummy_entry.focus_set()
                self.after(100, self.dummy_entry.pack_forget)
        else:
            self.withdraw()
            self.hide = True

    def _deiconify(self):
        if len(self.values) > 0:
            self.deiconify()

    def _attach_key_press(self, k):
        self.event_generate("<<Selected>>")
        self.fade = True
        if self.command:
            self.command(k)
        self.fade = False
        self.fade_out()
        self.withdraw()
        self.hide = True

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
