"""
Implementaciones de widgets personalizadas.
"""

from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
)

from gauss_bot import DROPDOWN_ICON
from gauss_bot.gui.custom import Tooltip

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI


class CustomEntry(ctkEntry):
    def __init__(
        self,
        master: Any,
        width: int = 140,
        height: int = 30,
        placeholder_text: Optional[str] = None,
        justify: str = "center",
        **kwargs
    ) -> None:

        super().__init__(
            master,
            width=width,
            height=height,
            placeholder_text=placeholder_text,
            **kwargs,
        )

        self.configure(justify=justify)
        self.bind("<Tab>", self.autocomplete_placeholder)

    def autocomplete_placeholder(self, event) -> str:
        """
        Inserta el placeholder en el entry si no hay texto
        cuando el usuario presiona la tecla Tab.
        """

        del event
        if self.get() == "" and self.cget("placeholder_text") is not None:
            self.insert(0, self.cget("placeholder_text"))
        return "break"

    def grid(self, **kwargs):
        if "ipadx" not in kwargs:
            kwargs["ipadx"] = 0
        if "ipady" not in kwargs:
            kwargs["ipady"] = 0
        super().grid(**kwargs)


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

        light_dropdown = ctkImage(DROPDOWN_ICON._dark_image)
        self.grid_configure(ipadx=5)
        self.set_dropdown_icon(light_dropdown)

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

    def configure(self, require_redraw=False, **kwargs):
        super().configure(require_redraw, **kwargs)
        try:
            color = self._apply_appearance_mode(self._button_color)
            self.icon_label.configure(fg_color=color, bg_color=color)
        except AttributeError:
            pass

    def _on_enter(self, event: int = 0):
        super()._on_enter(event)
        color = self._apply_appearance_mode(self._button_hover_color)
        self.icon_label.configure(fg_color=color, bg_color=color)

    def _on_leave(self, event: int = 0):
        super()._on_leave(event)
        color = self._apply_appearance_mode(self._button_color)
        self.icon_label.configure(fg_color=color, bg_color=color)


class IconButton(ctkButton):
    def __init__(
        self,
        master: Any,
        app: "GaussUI",
        image: ctkImage,
        tooltip_text: str,
        width: int = 20,
        height: int = 20,
        **kwargs
    ) -> None:

        self.app = app
        super().__init__(
            master,
            width=width,
            height=height,
            image=image,
            text="",
            border_width=0,
            border_spacing=0,
            fg_color="transparent",
            bg_color="transparent",
            hover_color=self.app.theme_config["CTkFrame"]["top_fg_color"],
            **kwargs,
        )

        self.tooltip = Tooltip(self, tooltip_text)

    def destroy(self):
        self.tooltip.destroy()
        super().destroy()

    def configure(self, require_redraw=False, **kwargs):
        if "tooltip_text" in kwargs:
            self.tooltip.configure_tooltip(message=kwargs.pop("tooltip_text"))
        super().configure(require_redraw, **kwargs)
