"""
Implementación de frames personalizados para
mostrar diferentes tipos de mensajes al usuario.
"""

from os import path
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Union,
)

from PIL.Image import (
    LANCZOS,
    open as open_img,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkScrollableFrame as ctkScrollFrame,
    CTkToplevel as ctkTop,
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot import (
    ASSET_PATH,
    DROPDOWN_ARROW,
    FUNCTIONS
)

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI


class CustomEntry(ctkEntry):
    def __init__(
        self,
        master: Any,
        width: int = 140,
        height: int = 28,
        corner_radius: Optional[Union[int]] = None,
        bg_color: Union[str, tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, tuple[str, str]]] = None,
        text_color: Optional[Union[str, tuple[str, str]]] = None,
        font: Optional[Union[tuple, ctkFont]] = None,
        justify: str = "center",
        **kwargs
    ) -> None:

        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=corner_radius,
            bg_color=bg_color,
            fg_color=fg_color,
            text_color=text_color,
            font=font,
            **kwargs,
        )

        self.configure(justify=justify)


class CustomImageDropdown(ctkButton):
    def __init__(
        self,
        master: Any,
        button_text: str,
        **kwargs,
    ) -> None:

        super().__init__(
            master,
            width=100,
            height=30,
            text=button_text,
            image=DROPDOWN_ARROW,
            command=self._show_menu,
            **kwargs
        )

        self.options_window: ctkTop
        self.images: dict[str, ctkImage] = {
            name: self._resize_image(img)
            for name, img in sorted(FUNCTIONS.items())
        }

    def _show_menu(self):
        self.options_window = ctkTop(self)
        self.options_window.overrideredirect(True)
        self.options_window.attributes("-topmost", True)
        for img in self.images.values():
            ctkButton(
                self.options_window,
                width=100,
                height=30,
                text="",
                image=img,
                fg_color="transparent",
                command=lambda: self._on_select(img),
            ).pack(fill="both", padx=5, pady=5)
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.options_window.geometry(f"+{x}+{y}")

    def _resize_image(self, img: ctkImage) -> ctkImage:
        dark = img._dark_image
        light = img._light_image

        width, height = img._size
        new_width = width // 4
        new_height = height // 4

        dark_img = dark.resize((new_width, new_height), LANCZOS)
        light_img = light.resize((new_width, new_height), LANCZOS)
        return ctkImage(
            dark_image=dark_img,
            light_image=light_img,
            size=(new_width // 8, new_height // 8),
        )

    def _on_select(self, img_selected: ctkImage) -> None:
        self.options_window.destroy()
        self.configure(image=img_selected)


class CustomDropdown(ctkOptionMenu):
    def __init__(
        self,
        master: Any,
        width: int = 140,
        height: int = 30,
        text_anchor = "center",
        **kwargs
    ) -> None:

        super().__init__(
            master,
            width,
            height,
            **kwargs
        )

        self.icon_label: ctkLabel
        self._text_label.configure(anchor=text_anchor)

        self.grid_configure(ipadx=5)
        self.set_dropdown_icon(DROPDOWN_ARROW)

    def set_dropdown_icon(self, image: ctkImage, right_distance: int = 5) -> None:
        self.icon_label = ctkLabel(
            self,
            text="",
            image=image,
        )

        self._canvas.delete("dropdown_arrow")
        color = self._canvas.itemcget("inner_parts_right", "fill")
        self.icon_label.configure(fg_color=color)

        grid_info = self._text_label.grid_info()
        grid_info["padx"], grid_info["sticky"] = right_distance, "e"
        self.icon_label.grid(**grid_info)

        self.icon_label.bind("<Button-1>", self._clicked)
        self.icon_label.bind("<Enter>", self._on_enter)
        self.icon_label.bind("<Leave>", self._on_leave)

    def configure(self, **kwargs):
        super().configure(**kwargs)
        try:
            color = self._apply_appearance_mode(self._button_color)
            self.icon_label.configure(fg_color=color, bg_color=color)
        except AttributeError:
            pass

    def _on_enter(self, event):
        super()._on_enter(event)
        color = self._apply_appearance_mode(self._button_hover_color)
        self.icon_label.configure(fg_color=color, bg_color=color)

    def _on_leave(self, event):
        super()._on_leave(event)
        color = self._apply_appearance_mode(self._button_color)
        self.icon_label.configure(fg_color=color, bg_color=color)


class CustomScrollFrame(ctkScrollFrame):
    def __init__(
        self,
        app: "GaussUI",
        master: Any,
        **kwargs
    ) -> None:

        super().__init__(
            master,
            **kwargs
        )

        self.app = app
        self.bind("<Configure>", self._on_frame_configure)

    def update_scrollbar_visibility(self) -> None:
        self.update_idletasks()
        content_height, frame_height = self._calculate_heights()
        if content_height > frame_height:
            self._scrollbar.grid()
        else:
            self._scrollbar.grid_remove()

    def _on_frame_configure(self, event) -> None:
        self.update_idletasks()
        self._fit_frame_dimensions_to_canvas(event)
        self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all"))
        self.update_scrollbar_visibility()

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

    def __init__(
        self,
        parent: Union[ctkFrame, CustomScrollFrame],
        header: str,
        resultado: str,
        solo_header: bool =False,
        border_color: str = "#18c026",
    ) -> None:

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
