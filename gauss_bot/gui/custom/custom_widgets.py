"""
Implementaciones de widgets personalizadas.
"""

from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Union,
)

from PIL.Image import LANCZOS

from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFont as ctkFont,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot import (
    DROPDOWN_ARROW,
    FUNCTIONS,
)

from gauss_bot.gui.custom.scrollable_dropdown import CustomScrollableDropdown

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI


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
        app: "GaussUI",
        button_text: str,
        width=80,
        height=30,
        **kwargs,
    ) -> None:

        self.app = app
        resizes = {
            name: resize_image(img)
            for name, img in sorted(FUNCTIONS.items())
        }

        self.images: dict[str, ctkImage] = {
            "k": resizes["k"],
            "x^n": resizes["x^n"],
            "b^x": resizes["b^x"],
            "e^x": resizes["e^x"],
            "ln(x)": resizes["ln(x)"],
            "sen(x)": resizes["sen(x)"],
            "cos(x)": resizes["cos(x)"],
            "tan(x)": resizes["tan(x)"],
        }

        imgs = []
        for img in self.images.values():
            img.configure(light_image=img._dark_image)
            imgs.append(img)

        self.options_button = ctkButton(
            master,
            width=width,
            height=height,
            text=button_text,
            image=DROPDOWN_ARROW,
            compound="right",
            **kwargs,
        )

        super().__init__(
            attach=self.options_button,
            width=width * 3,
            height=height * 60,
            values=["" for _ in imgs],
            image_values=imgs,
            command=self._on_select,
            fg_color=self.app.ecuaciones.tabview._segmented_button.cget("unselected_color"),  # type: ignore
            button_color=self.app.ecuaciones.tabview._segmented_button.cget("unselected_color"),  # type: ignore
            **kwargs
        )

        for button in self.widgets.values():
            button.bind(
                "<Button-1>",
                command=lambda _, drop=self, img=button._image:
                self.app.ecuaciones.instances[1].extract_func(drop, img),  # type: ignore
            )

    def _on_select(self, img: ctkImage) -> None:
        self.options_button.configure(
            image=img,
            compound="center",
            text="",
        )

        self.update_idletasks()
