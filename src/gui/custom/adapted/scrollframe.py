"""
Based on CTkXYFrame by Akash Bora (https://github.com/Akascape/CTkXYFrame).
"""

from __future__ import annotations

from tkinter import Canvas
from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTkScrollableFrame, CTkScrollbar

if TYPE_CHECKING:
    from tkinter import Misc, _GridInfo

    from customtkinter import CTk, CTkBaseClass, CTkToplevel

    from src.gui import GaussUI


class CustomScrollFrame(CTkFrame):
    """
    Scrollable frame with support for dynamic scrollbars
    and simultaenous vertical and horizontal scrolling.
    """

    def __init__(
        self,
        master: CTk | CTkFrame | CTkToplevel | GaussUI,
        width: int = 100,
        height: int = 100,
        scrollbar_width: int = 16,
        scrollbar_padding: tuple[tuple[int, int], int] = ((0, 5), 8),
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Initialize frame with scrolling functionality.

        Args:
            master:            Widget within which this frame is in.
            width:             Width of frame in pixels.
            height:            Height of frame in pixels.
            scrollbar_width:   Scrollbar width in pixels.
            scrollbar_padding: Padding around scrollbar.
            kwargs:            Inner frame initialization configuration.

        """

        self.parent_frame = CTkFrame(master=master, **kwargs)
        self.xy_canvas = Canvas(
            self.parent_frame,
            width=width,
            height=height,
            bg=self.parent_frame._apply_appearance_mode(  # noqa :SLF001
                self.parent_frame.cget("bg_color"),
            ),
            borderwidth=0,
            highlightthickness=0,
        )

        self.parent_frame.rowconfigure(0, weight=1)
        self.parent_frame.columnconfigure(0, weight=1)

        super().__init__(
            master=self.xy_canvas,
            fg_color=self.parent_frame.cget("fg_color"),
            bg_color=self.parent_frame.cget("fg_color"),
        )

        self.padx, self.pady = scrollbar_padding
        self.window_id = self.xy_canvas.create_window((0, 0), window=self, anchor="nw")

        self.vsb = CTkScrollbar(
            self.parent_frame,
            orientation="vertical",
            command=self.xy_canvas.yview,
            width=scrollbar_width,
        )

        self.hsb = CTkScrollbar(
            self.parent_frame,
            orientation="horizontal",
            command=self.xy_canvas.xview,
            height=scrollbar_width,
        )

        self.xy_canvas.configure(
            xscrollcommand=self._dynamic_scrollbar_hsb,
            yscrollcommand=self._dynamic_scrollbar_vsb,
        )

        self.xy_canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.bind("<Configure>", lambda _: self._update_scrollregion())
        self.xy_canvas.bind("<Configure>", lambda _: self._update_scrollregion())
        self.xy_canvas.bind_all(
            "<MouseWheel>",
            lambda e: self._on_mousewheel(e.delta, e.widget),
            add="+",
        )

        self.xy_canvas.bind_all(
            "<Shift-MouseWheel>",
            lambda e: self._on_mousewheel_shift(e.delta, e.widget),
            add="+",
        )

        self.xy_canvas.bind_all(
            "<Button-4>",
            lambda e: self._on_mousewheel(120, e.widget),
            add="+",
        )

        self.xy_canvas.bind_all(
            "<Button-5>",
            lambda e: self._on_mousewheel(-120, e.widget),
            add="+",
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

        if isinstance(master, CTkScrollableFrame):
            master.check_if_master_is_canvas = self.disable_contentscroll

    def configure(self, require_redraw: bool = False, **kwargs) -> None:  # noqa: ANN003
        """
        Configure inner frame and canvas with kwargs.

        Args:
            require_redraw: Passed to `CTkFrame.configure()`.
            kwargs:         New frame configuration.

        """

        if "fg_color" in kwargs or "bg_color" in kwargs:
            new_fg: str = kwargs.pop("fg_color", self.cget("fg_color"))
            new_bg: str = kwargs.pop("bg_color", self.cget("bg_color"))

            self.xy_canvas.config(bg=new_bg)
            self.parent_frame.configure(fg_color=new_fg, bg_color=new_bg)

            super().configure(fg_color=new_fg, bg_color=new_bg)
            self._update_child_colors(self)

        if "width" in kwargs:
            self.xy_canvas.config(width=kwargs.pop("width"))
        if "height" in kwargs:
            self.xy_canvas.config(height=kwargs.pop("height"))

        self.parent_frame.configure(require_redraw, **kwargs)

    def destroy(self) -> None:
        """
        Destroy `self.parent_frame` before destroying `self`.
        """

        self.parent_frame.destroy()
        super().destroy()

    def disable_contentscroll(self, widget: Canvas | CTkBaseClass) -> bool:
        """
        Override for `CTkScrollableFrame.check_if_master_is_canvas()`.

        Args:
            widget: Widget whose master will be checked.

        """

        return widget is self.xy_canvas

    def check_if_master_is_canvas(self, widget: Canvas | CTkBaseClass | Misc) -> bool:
        """
        Checks if a widget's master is an instance of `tkinter.Canvas`.

        Args:
            widget: Widget whose master will be checked.

        """

        if widget is self.xy_canvas:
            return True
        if widget.master is not None:
            return self.check_if_master_is_canvas(widget.master)
        return False

    def grid(self, **kwargs) -> None:  # noqa: ANN003
        """
        Position widget in parent widget's grid.
        """

        self.parent_frame.grid(**kwargs)

    def grid_forget(self, **kwargs) -> None:  # noqa: ANN003
        """
        Unmap widget.
        """

        self.parent_frame.grid_forget(**kwargs)

    def grid_remove(self, **kwargs) -> None:  # noqa: ANN003
        """
        Unmap widget, but remember its grid options.
        """

        self.parent_frame.grid_remove(**kwargs)

    def grid_propagate(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        flag: bool | None = None,
    ) -> bool | None:
        """
        Set/get status of propagation of geometry information.
        """

        if flag is None:
            return self.parent_frame.grid_propagate()
        return self.parent_frame.grid_propagate(flag)

    def grid_info(self, **kwargs) -> _GridInfo:  # noqa: ANN003
        """
        Return information about the options for positioning this widget in a grid.
        """

        return self.parent_frame.grid_info(**kwargs)

    def pack(self, **kwargs) -> None:  # noqa: ANN003
        """
        Pack widget in parent widget.
        For details, see CTkFrame.place().
        """

        self.parent_frame.pack(**kwargs)

    def pack_forget(self) -> None:
        """
        Unmap widget and do not use it for packing order.
        """

        self.parent_frame.pack_forget()

    def place(self, **kwargs) -> None:  # noqa: ANN003
        """
        Place widget in parent widget.
        For details, see CTkFrame.place().
        """

        self.parent_frame.place(**kwargs)

    def place_forget(self, **kwargs) -> None:  # noqa: ANN003
        """
        Unmap widget.
        """

        self.parent_frame.place_forget(**kwargs)

    def lift(self, aboveThis: CTkBaseClass | Misc | None = None) -> None:  # noqa: N803
        """
        Raise widget in stacking order.
        """

        self.parent_frame.lift(aboveThis)

    def lower(self, belowThis: CTkBaseClass | Misc | None = None) -> None:  # noqa: N803
        """
        Lower widget in stacking order.
        """

        self.parent_frame.lower(belowThis)

    def _update_scrollregion(self) -> None:
        """
        Set scrollregion of `self.xy_canvas` according to content size.
        """

        inner_width = self.winfo_reqwidth()
        inner_height = self.winfo_reqheight()

        canvas_width = self.xy_canvas.winfo_width()
        canvas_height = self.xy_canvas.winfo_height()

        if inner_width < canvas_width:
            self.xy_canvas.itemconfig(self.window_id, width=canvas_width)
        else:
            self.xy_canvas.itemconfig(self.window_id, width=0)

        self.xy_canvas.configure(
            scrollregion=(
                0,
                0,
                max(inner_width, canvas_width),
                max(inner_height, canvas_height),
            ),
        )
        self._dynamic_scrollbar_hsb(*self.xy_canvas.xview())
        self._dynamic_scrollbar_vsb(*self.xy_canvas.yview())

    def _dynamic_scrollbar_vsb(self, x: float, y: float) -> None:
        """
        Set vertical scrollbar location, and show/hide it as needed.

        Args:
            x: Horizontal position of scrollregion.
            y: Vertical position of scrollregion.

        """

        x, y = float(x), float(y)

        if x == 0.0 and y == 1.0:
            self.vsb.grid_forget()
        else:
            self.vsb.grid(row=0, column=1, sticky="nse", padx=self.padx, pady=self.pady)
        self.vsb.set(x, y)

    def _dynamic_scrollbar_hsb(self, x: float, y: float) -> None:
        """
        Set horizontal scrollbar location, and show/hide it as needed.

        Args:
            x: Horizontal position of scrollregion.
            y: Vertical position of scrollregion.

        """

        x, y = float(x), float(y)

        if x == 0.0 and y == 1.0:
            self.hsb.grid_forget()
        else:
            self.hsb.grid(row=1, column=0, sticky="swe", padx=self.pady, pady=self.padx)
        self.hsb.set(x, y)

    def _on_mousewheel(self, delta: int, widget: CTkBaseClass | Misc) -> None:
        """
        Handle vertical scrolling.

        Args:
            delta:  Scroll amount.
            widget: Widget within which the user scrolled.

        """

        if self.check_if_master_is_canvas(widget):
            content_height = self.winfo_reqheight()
            viewport_height = self.xy_canvas.winfo_height()
            if content_height > viewport_height:
                self.xy_canvas.yview_scroll(int(-1 * (delta / 120)), "units")

    def _on_mousewheel_shift(self, delta: int, widget: CTkBaseClass | Misc) -> None:
        """
        Handle horizontal scrolling.

        Args:
            delta:  Scroll amount.
            widget: Widget within which the user scrolled.

        """

        if self.check_if_master_is_canvas(widget):
            content_width = self.winfo_reqwidth()
            viewport_width = self.xy_canvas.winfo_width()
            if content_width > viewport_width:
                self.xy_canvas.xview_scroll(int(-1 * (delta / 120)), "units")

    def _set_appearance_mode(self, mode_string: str) -> None:
        super()._set_appearance_mode(mode_string)

        bg: str = self.parent_frame.cget("bg_color")
        fg: str = self.parent_frame.cget("fg_color")
        themed_bg = self._apply_appearance_mode(bg)

        self.xy_canvas.config(bg=themed_bg)
        self.parent_frame.configure(fg_color=fg, bg_color=bg)
        super().configure(fg_color=fg, bg_color=bg)

        self._update_child_colors(self)

    def _update_child_colors(self, widget: CustomScrollFrame) -> None:
        for child in widget.winfo_children():
            if hasattr(child, "_set_appearance_mode"):
                child._set_appearance_mode(self.__appearance_mode)  # noqa: SLF001

            self._update_child_colors(child)
