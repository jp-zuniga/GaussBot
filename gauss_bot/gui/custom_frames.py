"""
Implementación de frames personalizados para
mostrar diferentes tipos de mensajes al usuario.
"""

from os import path
from typing import (
    Any,
    Callable,
    Optional,
    Union
)

from PIL.Image import open as open_img
from tkinter import (
    Variable,
    NORMAL
)

from customtkinter import (
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkScrollableFrame as ctkScrollFrame,
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot import (
    ASSET_PATH,
    dropdown_icon
)


class CustomDropdown(ctkOptionMenu):
    def __init__(
        self,
        master: Any,
        width: int = 140,
        height: int = 28,
        corner_radius: Optional[Union[int]] = None,
        bg_color: Union[str, tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, tuple[str, str]]] = None,
        button_color: Optional[Union[str, tuple[str, str]]] = None,
        button_hover_color: Optional[Union[str, tuple[str, str]]] = None,
        text_color: Optional[Union[str, tuple[str, str]]] = None,
        text_color_disabled: Optional[Union[str, tuple[str, str]]] = None,
        dropdown_fg_color: Optional[Union[str, tuple[str, str]]] = None,
        dropdown_hover_color: Optional[Union[str, tuple[str, str]]] = None,
        dropdown_text_color: Optional[Union[str, tuple[str, str]]] = None,
        font: Optional[Union[tuple, ctkFont]] = None,
        dropdown_font: Optional[Union[tuple, ctkFont]] = None,
        values: Optional[list] = None,
        variable: Union[Variable, None] = None,
        state: str = NORMAL,
        hover: bool = True,
        command: Union[Callable[[str], Any], None] = None,
        dynamic_resizing: bool = True,
        anchor: str = "w",
        **kwargs
    ):

        super().__init__(
            master,
            width,
            height,
            corner_radius,
            bg_color,
            fg_color,
            button_color,
            button_hover_color,
            text_color,
            text_color_disabled,
            dropdown_fg_color,
            dropdown_hover_color,
            dropdown_text_color,
            font,
            dropdown_font,
            values,
            variable,
            state,
            hover,
            command,
            dynamic_resizing,
            anchor,
            **kwargs,
        )

        self.image_label: ctkLabel
        self.set_dropdown_icon(dropdown_icon)

    def set_dropdown_icon(self, image: ctkImage, right_distance: int = 5):
        self.image_label = ctkLabel(self, text="", image=image)
        self._canvas.delete("dropdown_arrow")

        color = self._canvas.itemcget("inner_parts_right", "fill")
        self.image_label.configure(fg_color=color, bg_color=color)

        grid_info = self._text_label.grid_info()
        grid_info["padx"], grid_info["sticky"] = right_distance, "e"
        self.image_label.grid(**grid_info)

        self.image_label.bind("<Button-1>", self._clicked)
        self.image_label.bind("<Enter>", self._on_enter)
        self.image_label.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        super()._on_enter(event)
        if self.image_label:
            color = self._apply_appearance_mode(self._button_hover_color)
            self.image_label.configure(fg_color=color, bg_color=color)

    def _on_leave(self, event):
        super()._on_leave(event)
        if self.image_label:
            color = self._apply_appearance_mode(self._button_color)
            self.image_label.configure(fg_color=color, bg_color=color)


class CustomScrollFrame(ctkScrollFrame):
    def __init__(self, app, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.app = app
        self.bind("<Configure>", self._on_frame_configure)
    
    def _on_frame_configure(self, event) -> None:
        self.update_idletasks()
        self._fit_frame_dimensions_to_canvas(event)
        self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all"))
        self.update_scrollbar_visibility()

    def update_scrollbar_visibility(self) -> None:
        self.update_idletasks()
        content_height, frame_height = self._calculate_heights()
        if content_height > frame_height:
            self._scrollbar.grid()
        else:
            self._scrollbar.grid_remove()

    def _calculate_heights(self) -> tuple[int, int]:
        total_padding = 0
        for widget in self.winfo_children():
            total_padding += 10
            if isinstance(widget, ctkFrame):
                for _ in widget.winfo_children():
                    total_padding += 10

        frame_height = self.app._current_height
        content_height = 0

        for widget in self.winfo_children():
            content_height += widget.winfo_reqheight()
            if isinstance(widget, ctkFrame):
                content_height += sum(
                    subwidget.winfo_reqheight()
                    for subwidget in widget.winfo_children()
                )
        content_height -= total_padding
        return (content_height, frame_height)


class ErrorFrame(ctkFrame):
    """
    Frame personalizado para mostrar mensajes de error.
    """

    def __init__(self, parent: Union[ctkFrame, CustomScrollFrame], message: str) -> None:
        super().__init__(parent, corner_radius=8, border_width=2, border_color="#ff3131")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.error_icon = ctkImage(open_img(path.join(ASSET_PATH, "error_icon.png")))
        self.error_icon_label = ctkLabel(self, text="", image=self.error_icon)
        self.mensaje_error = ctkLabel(self, text=message)

        self.error_icon_label.grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")
        self.mensaje_error.grid(row=0, column=1, padx=(5, 15), pady=10, sticky="e")

    def destroy(self) -> None:
        self.forget()
        super().destroy()


class SuccessFrame(ctkFrame):
    """
    Frame personalizado para mostrar mensajes de éxito.
    """

    def __init__(self, parent: Union[ctkFrame, CustomScrollFrame], message: str) -> None:
        super().__init__(parent, corner_radius=8, border_width=2, border_color="#18c026")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.check_icon = ctkImage(open_img(path.join(ASSET_PATH, "check_icon.png")))
        self.check_icon_label = ctkLabel(self, text="", image=self.check_icon)
        self.mensaje_exito = ctkLabel(self, text=message)

        self.check_icon_label.grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")
        self.mensaje_exito.grid(row=0, column=1, padx=(5, 15), pady=10, sticky="e")

    def destroy(self) -> None:
        self.forget()
        super().destroy()


class ResultadoFrame(ctkFrame):
    """
    Frame personalizado para mostrar resultados de operaciones.
    """

    def __init__(self, parent: Union[ctkFrame, CustomScrollFrame],
                 header: str, resultado: str, solo_header=False,
                 border_color="#18c026") -> None:

        super().__init__(parent, corner_radius=8, border_width=2, border_color=border_color)

        pady_tuple = (10, 10) if solo_header else (10, 3)
        self.header = ctkLabel(self, text=header)
        self.header.grid(row=0, column=0, padx=20, pady=pady_tuple, sticky="n")

        if not solo_header:
            self.resultado = ctkLabel(self, text=resultado)
            self.resultado.grid(row=1, column=0, padx=20, pady=(3, 10), sticky="n")

    def destroy(self) -> None:
        self.forget()
        super().destroy()
