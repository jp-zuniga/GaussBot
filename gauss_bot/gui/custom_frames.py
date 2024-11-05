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
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot import (
    ASSET_PATH,
    DROPDOWN_ARROW,
    FUNCTIONS,
)

from gauss_bot.gui.scrollable_dropdown import CustomScrollableDropdown

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


class CustomImageDropdown(CustomScrollableDropdown):
    def __init__(
        self,
        master: Any,
        button_text: str,
        width=80,
        height=30,
        **kwargs,
    ) -> None:

        self.images: dict[str, ctkImage] = {
            name: resize_image(img)
            for name, img in sorted(FUNCTIONS.items())
        }

        self.imgs = [img for name, img in self.images.items() if name != "f(x)"]
        values = ["" for _ in self.imgs]

        self.options_button = ctkButton(
            master,
            width=width,
            height=height,
            text=button_text,
            image=DROPDOWN_ARROW,
            compound="right",
            **kwargs
        )

        super().__init__(
            attach=self.options_button,
            width=width * 5,
            height=height * 60,
            values=values,
            image_values=self.imgs,
            command=self._on_select,
            **kwargs
        )

    def _on_select(self, img: ctkImage) -> None:
        self.options_button.configure(
            image=img,
            compound="left",
            text="",
        )

        self.update_idletasks()


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


def resize_image(img: ctkImage, divisors: tuple[int, int] = (4, 8)) -> ctkImage:
    div1, div2 = divisors
    dark = img._dark_image
    light = img._light_image

    width, height = img._size
    new_width = width // div1
    new_height = height // div1

    dark_img = dark.resize((new_width, new_height), LANCZOS)
    light_img = light.resize((new_width, new_height), LANCZOS)
    return ctkImage(
        dark_image=dark_img,
        light_image=light_img,
        size=(new_width // div2, new_height // div2),
    )
