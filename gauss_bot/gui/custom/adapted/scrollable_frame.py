"""
Adapted from:
* https://github.com/Akascape/CTkXYFrame
* By: Akash Bora

Modified by: Joaquín Zúñiga, on 11/8/2024.
Formatted file and added type annotations for personal use.
"""

from typing import Optional

from tkinter import Canvas
from customtkinter import (
    CTkFrame as ctkFrame,
    CTkScrollableFrame as ctkScrollFrame,
    CTkScrollbar as ctkScrollbar,
)


class CustomScrollFrame(ctkFrame):
    def __init__(
        self,
        master: ctkFrame,
        width: int = 800,
        height: int = 400,
        scrollbar_width: int = 16,
        scrollbar_fg_color: Optional[str] = None,
        scrollbar_button_color: Optional[str] = None,
        scrollbar_button_hover_color: Optional[str] = None,
        **kwargs,
    ):

        self.parent_frame = ctkFrame(master=master, **kwargs)
        self.bg_color = self.parent_frame.cget("bg_color")

        self.xy_canvas = Canvas(
            self.parent_frame,
            width=width,
            height=height,
            bg=self.parent_frame._apply_appearance_mode(self.bg_color),
            borderwidth=0,
            highlightthickness=0,
        )

        self.xy_canvas.rowconfigure(0, weight=1)
        self.xy_canvas.columnconfigure(0, weight=1)
        self.parent_frame.rowconfigure(0, weight=1)
        self.parent_frame.columnconfigure(0, weight=1)

        ctkFrame.__init__(
            self,
            master=self.xy_canvas,
            fg_color=self.parent_frame.cget("fg_color"),
            bg_color=self.parent_frame.cget("fg_color"),
        )

        self.window_id = self.xy_canvas.create_window((0, 0), window=self, anchor="center")

        self.v_scrollbar = ctkScrollbar(
            self.parent_frame,
            orientation="vertical",
            command=self.xy_canvas.yview,
            fg_color=scrollbar_fg_color,
            button_color=scrollbar_button_color,
            button_hover_color=scrollbar_button_hover_color,
            width=scrollbar_width,
        )

        self.h_scrollbar = ctkScrollbar(
            self.parent_frame,
            orientation="horizontal",
            command=self.xy_canvas.xview,
            fg_color=scrollbar_fg_color,
            button_color=scrollbar_button_color,
            button_hover_color=scrollbar_button_hover_color,
            height=scrollbar_width,
        )

        self.xy_canvas.configure(
            yscrollcommand=lambda x, y: self.dynamic_v_scrollbar(x, y),
            xscrollcommand=lambda x, y: self.dynamic_h_scrollbar(x, y),
        )

        self.xy_canvas.grid(row=0, column=0, sticky="nsew", padx=(7,0), pady=(7,0))

        self.bind(
            "<Configure>",
            lambda _, canvas=self.xy_canvas: self.on_frame_config(canvas),
        )

        self.xy_canvas.bind_all(
            "<MouseWheel>", lambda e: self._on_mousewheel(e.delta, e.widget), add="+"
        )

        self.xy_canvas.bind_all(
            "<Shift-MouseWheel>",
            lambda e: self._on_mousewheel_shift(e.delta, e.widget),
            add="+",
        )

        self.xy_canvas.bind_all(
            "<Button-4>", lambda e: self._on_mousewheel(120, e.widget), add="+"
        )

        self.xy_canvas.bind_all(
            "<Button-5>", lambda e: self._on_mousewheel(-120, e.widget), add="+"
        )

        self.xy_canvas.bind_all(
            "<Shift-Button-4>",
            lambda e: self._on_mousewheel_shift(120, e.widget),
            add="+",
        )

        self.xy_canvas.bind_all(
            "<Shift-Button-5>",
            lambda e: self._on_mousewheel_shift(-120, e.widget),
            add="+",
        )

        if isinstance(master, ctkScrollFrame):
            master.check_if_master_is_canvas = self.disable_contentscroll

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        self.xy_canvas.config(
            bg=self.parent_frame._apply_appearance_mode(self.bg_color)
        )

    def destroy(self):
        ctkFrame.destroy(self)
        self.parent_frame.destroy()

    def check_if_master_is_canvas(self, widget):
        if widget == self.xy_canvas:
            return True
        elif widget.master is not None:
            return self.check_if_master_is_canvas(widget.master)
        else:
            return False

    def disable_contentscroll(self, widget):
        if widget == self.xy_canvas:
            return True
        else:
            return False

    def dynamic_v_scrollbar(self, x, y):
        if float(x) == 0.0 and float(y) == 1.0:
            self.v_scrollbar.grid_forget()
        else:
            self.v_scrollbar.grid(row=0, column=1, rowspan=2, sticky="ne", pady=5)
        self.v_scrollbar.set(x, y)

    def dynamic_h_scrollbar(self, x, y):
        if float(x) == 0.0 and float(y) == 1.0:
            self.h_scrollbar.grid_forget()
        else:
            self.h_scrollbar.grid(row=1, column=0, sticky="se", padx=(5, 0))
        self.h_scrollbar.set(x, y)

    def on_frame_config(self, canvas: Canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_mousewheel(self, event, widget):
        if self.check_if_master_is_canvas(widget):
            self.xy_canvas.yview_scroll(int(-1 * (event / 120)), "units")

    def _on_mousewheel_shift(self, event, widget):
        if self.check_if_master_is_canvas(widget):
            self.xy_canvas.xview_scroll(int(-1 * (event / 120)), "units")

    def pack(self, **kwargs):
        self.parent_frame.pack(**kwargs)

    def place(self, **kwargs):
        self.parent_frame.place(**kwargs)

    def grid(self, **kwargs):
        self.parent_frame.grid(**kwargs)

    def pack_forget(self):
        self.parent_frame.pack_forget()

    def place_forget(self, **kwargs):
        self.parent_frame.place_forget()

    def grid_forget(self, **kwargs):
        self.parent_frame.grid_forget()

    def grid_remove(self, **kwargs):
        self.parent_frame.grid_remove()

    def grid_propagate(self, **kwargs):
        self.parent_frame.grid_propagate()

    def grid_info(self, **kwargs):
        return self.parent_frame.grid_info()

    def lift(self, aboveThis=None):
        self.parent_frame.lift(aboveThis)

    def lower(self, belowThis=None):
        self.parent_frame.lower(belowThis)

    def configure(self, **kwargs):
        if "fg_color" in kwargs:
            self.bg_color = kwargs["fg_color"]
            self.xy_canvas.config(bg=self.bg_color)
            self.configure(fg_color=self.bg_color)
        if "width" in kwargs:
            self.xy_canvas.config(width=kwargs["width"])
        if "height" in kwargs:
            self.xy_canvas.config(height=kwargs["height"])
        self.parent_frame.configure(**kwargs)
