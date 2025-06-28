"""
Adapted from:
* https://github.com/Akascape/CTkXYFrame
* Author: Akash Bora

Modified by: Joaquín Zúñiga, on 6/23/2025.
"""

from tkinter import Canvas
from typing import TYPE_CHECKING, Union

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkScrollableFrame as ctkScrollFrame,
    CTkScrollbar as ctkScrollbar,
)

if TYPE_CHECKING:
    from ...gui import GaussUI


class CustomScrollFrame(ctkFrame):
    def __init__(
        self,
        master: Union["GaussUI", ctkFrame],
        width: int = 100,
        height: int = 100,
        scrollbar_width: int = 16,
        scrollbar_padding: tuple[int, int] = (5, 8),
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

        self.parent_frame.rowconfigure(0, weight=1)
        self.parent_frame.columnconfigure(0, weight=1)

        ctkFrame.__init__(
            self,
            master=self.xy_canvas,
            fg_color=self.parent_frame.cget("fg_color"),
            bg_color=self.parent_frame.cget("fg_color"),
        )

        self.window_id = self.xy_canvas.create_window((0, 0), window=self, anchor="nw")
        self.padx, self.pady = scrollbar_padding

        self.vsb = ctkScrollbar(
            self.parent_frame,
            orientation="vertical",
            command=self.xy_canvas.yview,
            width=scrollbar_width,
        )

        self.hsb = ctkScrollbar(
            self.parent_frame,
            orientation="horizontal",
            command=self.xy_canvas.xview,
            height=scrollbar_width,
        )

        self.xy_canvas.configure(
            yscrollcommand=self.dynamic_scrollbar_vsb,
            xscrollcommand=self.dynamic_scrollbar_hsb,
        )

        self.xy_canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.bind("<Configure>", self.on_inner_frame_configure)
        self.xy_canvas.bind("<Configure>", self.on_canvas_resize)
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

    def destroy(self):
        ctkFrame.destroy(self)
        self.parent_frame.destroy()

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        self.xy_canvas.config(
            bg=self.parent_frame._apply_appearance_mode(self.bg_color)
        )

    def check_if_master_is_canvas(self, widget):
        if widget == self.xy_canvas:
            return True
        if widget.master is not None:
            return self.check_if_master_is_canvas(widget.master)
        return False

    def disable_contentscroll(self, widget):
        return widget == self.xy_canvas

    def dynamic_scrollbar_vsb(self, x, y):
        if float(x) == 0.0 and float(y) == 1.0:
            self.vsb.grid_forget()
        else:
            self.vsb.grid(row=0, column=1, sticky="nse", padx=self.padx, pady=self.pady)
        self.vsb.set(x, y)

    def dynamic_scrollbar_hsb(self, x, y):
        if float(x) == 0.0 and float(y) == 1.0:
            self.hsb.grid_forget()
        else:
            self.hsb.grid(row=1, column=0, sticky="swe", padx=self.padx, pady=self.pady)
        self.hsb.set(x, y)

    def on_canvas_resize(self, event):
        self.xy_canvas.itemconfig(self.window_id, width=event.width)

    def on_inner_frame_configure(self, event=None):
        del event
        self.xy_canvas.configure(scrollregion=self.xy_canvas.bbox("all"))
        self.xy_canvas.xview_moveto(0)
        self.xy_canvas.yview_moveto(0)

    def _on_mousewheel(self, event, widget):
        if self.check_if_master_is_canvas(widget):
            content_height = self.winfo_reqheight()
            viewport_height = self.xy_canvas.winfo_height()
            if content_height > viewport_height:
                self.xy_canvas.yview_scroll(int(-1 * (event / 120)), "units")

    def _on_mousewheel_shift(self, event, widget):
        if self.check_if_master_is_canvas(widget):
            content_width = self.winfo_reqwidth()
            viewport_width = self.xy_canvas.winfo_width()
            if content_width > viewport_width:
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
        self.parent_frame.place_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.parent_frame.grid_forget(**kwargs)

    def grid_remove(self, **kwargs):
        self.parent_frame.grid_remove(**kwargs)

    def grid_propagate(self, **kwargs):
        self.parent_frame.grid_propagate(**kwargs)

    def grid_info(self, **kwargs):
        return self.parent_frame.grid_info(**kwargs)

    def lift(self, aboveThis=None):
        self.parent_frame.lift(aboveThis)

    def lower(self, belowThis=None):
        self.parent_frame.lower(belowThis)

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)

        bg_color = self.parent_frame.cget("bg_color")
        fg_color = self.parent_frame.cget("fg_color")
        actual_bg_color = self.parent_frame._apply_appearance_mode(bg_color)

        self.xy_canvas.config(bg=actual_bg_color)
        self.parent_frame.configure(fg_color=fg_color, bg_color=bg_color)
        super().configure(fg_color=fg_color, bg_color=bg_color)

        self._update_child_colors(self)

    def _update_child_colors(self, widget):
        for child in widget.winfo_children():
            if hasattr(child, "_set_appearance_mode"):
                child._set_appearance_mode(self._appearance_mode)

            self._update_child_colors(child)

    def configure(self, **kwargs):
        if "fg_color" in kwargs or "bg_color" in kwargs:
            new_fg = kwargs.pop("fg_color", self.cget("fg_color"))
            new_bg = kwargs.pop("bg_color", self.cget("bg_color"))

            self.xy_canvas.config(bg=new_bg)
            self.parent_frame.configure(fg_color=new_fg, bg_color=new_bg)
            super().configure(fg_color=new_fg, bg_color=new_bg)
            self._update_child_colors(self)

        if "width" in kwargs:
            self.xy_canvas.config(width=kwargs.pop("width"))
        if "height" in kwargs:
            self.xy_canvas.config(height=kwargs.pop("height"))
        self.parent_frame.configure(**kwargs)
