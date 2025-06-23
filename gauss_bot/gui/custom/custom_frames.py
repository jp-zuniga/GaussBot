"""
Implementaciones de frames personalizados.
"""

from tkinter import Canvas
from typing import TYPE_CHECKING, Optional, Union

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkScrollbar as ctkScrollbar,
    CTkScrollableFrame as ctkScrollFrame,
)

from ...utils import CHECK_ICON, ERROR_ICON

if TYPE_CHECKING:
    from ..gui import GaussUI


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
            yscrollcommand=lambda x, y: self.dynamic_scrollbar_vsb(x, y),
            xscrollcommand=lambda x, y: self.dynamic_scrollbar_hsb(x, y),
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
        elif widget.master is not None:
            return self.check_if_master_is_canvas(widget.master)
        else:
            return False

    def disable_contentscroll(self, widget):
        if widget == self.xy_canvas:
            return True
        else:
            return False

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
            self.bg_color = kwargs["bg_color"]
            self.xy_canvas.config(bg=self.bg_color)
            self.parent_frame.configure(fg_color=self.bg_color, bg_color=self.bg_color)
            self.configure(fg_color=self.bg_color, bg_color=self.bg_color)
        if "width" in kwargs:
            self.xy_canvas.config(width=kwargs["width"])
        if "height" in kwargs:
            self.xy_canvas.config(height=kwargs["height"])
        self.parent_frame.configure(**kwargs)


class ErrorFrame(ctkFrame):
    """
    Frame personalizado para mostrar mensajes de error.
    """

    def __init__(
        self, master: Union[ctkFrame, CustomScrollFrame], msg: Optional[str]
    ) -> None:
        super().__init__(
            master, border_width=2, border_color="#ff3131", fg_color="transparent"
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.error_icon_label = ctkLabel(self, text="", image=ERROR_ICON)
        self.error_icon_label.grid(
            row=0, column=0, padx=(15, 10), pady=10, sticky="nse"
        )

        if msg is not None:
            self.mensaje_error = ctkLabel(self, text=msg)
            self.mensaje_error.grid(
                row=0, column=1, padx=(10, 15), pady=10, sticky="nsw"
            )

    def destroy(self) -> None:
        self.forget()
        super().destroy()


class SuccessFrame(ctkFrame):
    """
    Frame personalizado para mostrar mensajes de éxito.
    """

    def __init__(
        self, master: Union[ctkFrame, CustomScrollFrame], msg: Optional[str]
    ) -> None:
        super().__init__(
            master, border_width=2, border_color="#18c026", fg_color="transparent"
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.check_icon_label = ctkLabel(self, text="", image=CHECK_ICON)
        self.check_icon_label.grid(
            row=0, column=0, padx=(15, 10), pady=10, sticky="nse"
        )

        if msg is not None:
            self.mensaje_exito = ctkLabel(self, text=msg)
            self.mensaje_exito.grid(
                row=0, column=1, padx=(10, 15), pady=10, sticky="nsw"
            )

    def destroy(self) -> None:
        self.forget()
        super().destroy()


class ResultadoFrame(ctkFrame):
    """
    Frame personalizado para mostrar resultados de operaciones.
    """

    def __init__(
        self,
        master: Union[ctkFrame, CustomScrollFrame],
        msg: Optional[str] = None,
        img: Optional[ctkImage] = None,
        border_color: Optional[str] = None,
    ) -> None:
        if border_color is None:
            border_color = "#18c026"

        super().__init__(
            master, border_width=2, border_color=border_color, fg_color="transparent"
        )

        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.msg_label: Optional[ctkLabel] = None
        self.img_label: Optional[ctkLabel] = None

        if msg is not None and img is not None:
            raise ValueError("No se pueden mostrar mensaje e imagen al mismo tiempo!")

        if msg is not None:
            self.msg_label = ctkLabel(self, text=msg)
            self.msg_label.grid(row=0, column=0, padx=20, pady=10)  # type: ignore
        elif img is not None:
            self.img_label = ctkLabel(self, text="", image=img)
            self.img_label.grid(row=0, column=0, padx=10, pady=10)  # type: ignore
        else:
            raise ValueError(
                "Se necesita un mensaje o una imagen para mostrar en el frame!"
            )

    def destroy(self) -> None:
        self.forget()
        super().destroy()
