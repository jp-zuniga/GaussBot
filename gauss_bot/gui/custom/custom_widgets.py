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

from .adapted.tooltip import Tooltip
from ...icons import DROPDOWN_ICON

if TYPE_CHECKING:
    from ..gui import GaussUI


class CustomEntry(ctkEntry):
    """
    Entry personalizado con texto centrado y autocomplete bindings.
    """

    def __init__(
        self, master: Any, placeholder_text: Optional[str] = None, **kwargs
    ) -> None:
        justify = kwargs.pop("justify", "center")
        super().__init__(
            master,
            width=kwargs.pop("width", 140),
            height=kwargs.pop("height", 30),
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
    """
    OptionMenu personalizado con un ícono mejor.
    """

    def __init__(self, master: Any, **kwargs) -> None:
        anchor = kwargs.pop("text_anchor", "center")
        super().__init__(
            master,
            width=kwargs.pop("width", 140),
            height=kwargs.pop("height", 30),
            **kwargs,
        )

        self.icon_label: ctkLabel
        self._text_label.configure(anchor=anchor)

        light_dropdown = ctkImage(DROPDOWN_ICON._dark_image)
        self.grid_configure(ipadx=5)
        self.set_dropdown_icon(light_dropdown)
        self.update_idletasks()

    def set_dropdown_icon(self, image: ctkImage, right_distance: int = 5) -> None:
        """
        Cambia el ícono del dropdown
        """

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
    """
    CTkButton personalizado para tener
    botones con íconos y tooltips.
    """

    def __init__(
        self,
        master: Any,
        app: "GaussUI",
        image: Optional[ctkImage] = None,
        tooltip_text: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.app = app

        text = kwargs.pop("text", "")
        width = kwargs.pop("width", 20)
        height = kwargs.pop("height", 20)
        border_width = kwargs.pop("border_width", 0)
        border_spacing = kwargs.pop("border_spacing", 0)
        fg_color = kwargs.pop("fg_color", "transparent")
        hover_color = kwargs.pop(
            "hover_color",
            self.app.theme_config["CTkFrame"]["top_fg_color"],
        )

        super().__init__(
            master,
            width=width,
            height=height,
            image=image,
            text=text,
            border_width=border_width,
            border_spacing=border_spacing,
            fg_color=fg_color,
            hover_color=hover_color,
            **kwargs,
        )

        if tooltip_text is not None:
            self.tooltip: Optional[Tooltip] = Tooltip(self, tooltip_text)
        else:
            self.tooltip = None

    def destroy(self):
        if self.tooltip is not None:
            self.tooltip.destroy()
        super().destroy()

    def configure(self, require_redraw=False, **kwargs):
        if "tooltip_text" in kwargs:
            tt_text = kwargs.pop("tooltip_text")
            if self.tooltip is None and tt_text is not None:
                self.tooltip = Tooltip(self, tt_text)
            elif self.tooltip is not None and tt_text is None:
                self.tooltip.destroy()
                self.tooltip = None
            else:
                self.tooltip.configure_tooltip(message=tt_text)

        super().configure(require_redraw, **kwargs)
