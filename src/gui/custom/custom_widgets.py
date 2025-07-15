"""
Implementaciones de widgets personalizadas.
"""

from typing import TYPE_CHECKING

from customtkinter import (
    CTkButton,
    CTkEntry,
    CTkImage,
    CTkLabel,
    CTkOptionMenu,
    ThemeManager,
)

from src.utils import DROPDOWN_ICON

from .adapted.tooltip import Tooltip

if TYPE_CHECKING:
    from customtkinter import CTkBaseClass


class CustomEntry(CTkEntry):
    """
    Entry personalizado con texto centrado y custom bindings.
    """

    def __init__(
        self,
        master: "CTkBaseClass",
        placeholder_text: str | None = None,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar con justificación centrada y `Tab` binding.

        Args:
            master:           Widget a la cual este entry pertenece.
            placeholder_text: Texto marcador de posición.
            kwargs:           Argumentos a pasar a CTkEntry.__init__().

        """

        super().__init__(
            master,
            width=kwargs.pop("width", 140),
            height=kwargs.pop("height", 36),
            justify=kwargs.pop("justify", "center"),
            placeholder_text=placeholder_text,
            **kwargs,
        )

        self.bind("<Tab>", lambda _: self.autocomplete_placeholder())

    def autocomplete_placeholder(self) -> str:
        """
        Insertar placeholder text si no se ha ingresado texto.
        """

        if self.get() == "" and self.cget("placeholder_text") is not None:
            self.insert(0, self.cget("placeholder_text"))
        return "break"

    def grid(self, **kwargs) -> None:  # noqa: ANN003, D102
        if "ipadx" not in kwargs:
            kwargs["ipadx"] = 0
        if "ipady" not in kwargs:
            kwargs["ipady"] = 0
        super().grid(**kwargs)


class CustomDropdown(CTkOptionMenu):
    """
    CTkOptionMenu personalizado con otro ícono.
    """

    def __init__(self, master: "CTkBaseClass", **kwargs) -> None:  # noqa: ANN003
        """
        Configurar ícono de dropdown.

        Args:
            master: Widget a la cual este entry pertenece.
            kwargs: Argumentos a pasar a CTkOptionMenu.__init__().

        """

        anchor = kwargs.pop("text_anchor", "center")

        super().__init__(
            master,
            width=kwargs.pop("width", 140),
            height=kwargs.pop("height", 30),
            **kwargs,
        )

        self.icon_label: CTkLabel
        self._text_label.configure(anchor=anchor)

        self.grid_configure(ipadx=5)
        self.set_dropdown_icon(CTkImage(DROPDOWN_ICON._dark_image))  # noqa: SLF001
        self.update_idletasks()

    def set_dropdown_icon(self, image: CTkImage, right_distance: int = 5) -> None:
        """
        Cambiar ícono de dropdown.

        Args:
            image:          Ícono de dropdown a utilizar.
            right_distance: Valor de padx.

        """

        self.icon_label = CTkLabel(self, text="", image=image)
        self._canvas.delete("dropdown_arrow")
        self.icon_label.configure(
            fg_color=self._canvas.itemcget("inner_parts_right", "fill"),
        )

        grid_info = self._text_label.grid_info()
        grid_info["padx"], grid_info["sticky"] = right_distance, "e"
        self.icon_label.grid(**grid_info)

        self.icon_label.bind("<Button-1>", self._clicked)
        self.icon_label.bind("<Enter>", self._on_enter)
        self.icon_label.bind("<Leave>", self._on_leave)

    def configure(self, require_redraw: bool = False, **kwargs) -> None:  # noqa: ANN003, D102
        super().configure(require_redraw, **kwargs)
        try:
            color = self._apply_appearance_mode(self._button_color)
            self.icon_label.configure(fg_color=color, bg_color=color)
        except AttributeError:
            pass

    def _on_enter(self, event: int = 0) -> None:
        super()._on_enter(event)
        color: str = ThemeManager.theme["CTkOptionMenu"]["button_color"]
        self.icon_label.configure(fg_color=color, bg_color=color)

    def _on_leave(self, event: int = 0) -> None:
        super()._on_leave(event)
        color: str = ThemeManager.theme["CTkOptionMenu"]["button_color"]
        self.icon_label.configure(fg_color=color, bg_color=color)


class IconButton(CTkButton):
    """
    CTkButton personalizado con ícono y tooltip.
    """

    def __init__(
        self,
        master: "CTkBaseClass",
        image: CTkImage | None = None,
        tooltip_text: str | None = None,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar botón con configuración personalizada y crear tooltip si se desea.

        Args:
            master:       Widget a la cual este entry pertenece.
            image:        Imagen a colocar en el frame.
            tooltip_text: Texto a colocar en tooltip.
            kwargs:       Argumentos a pasar a CTkButton.__init__().

        """

        text: str = kwargs.pop("text", "")
        width: int = kwargs.pop("width", 30)
        height: int = kwargs.pop("height", 30)
        border_width: int = kwargs.pop("border_width", 0)
        border_spacing: int = kwargs.pop("border_spacing", 0)
        fg_color: str = kwargs.pop("fg_color", "transparent")
        hover_color: str = kwargs.pop(
            "hover_color",
            ThemeManager.theme["CTkFrame"]["top_fg_color"],
        )

        tt_padx: int = kwargs.pop("tooltip_padx", 15)
        tt_pady: int = kwargs.pop("tooltip_pady", 5)
        tt_x_offset: int = kwargs.pop("tooltip_x_offset", 20)
        tt_y_offset: int = kwargs.pop("tooltip_y_offset", 20)
        swap_tt_colors: bool = kwargs.pop("swap_tooltip_colors", False)

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

        if text == "" and image is not None:
            self._image_label.grid_configure(  # type: ignore[reportOptionalMemberAccess]
                columnspan=3,
                sticky="nsew",
            )

        if tooltip_text is None:
            self.tooltip = None
        else:
            bg: list[str] = (
                ThemeManager.theme["CTk"]["fg_color"]
                if swap_tt_colors
                else ThemeManager.theme["CTkFrame"]["fg_color"]
            )

            self.tooltip: Tooltip | None = Tooltip(
                self,
                tooltip_text,
                padx=tt_padx,
                pady=tt_pady,
                x_offset=tt_x_offset,
                y_offset=tt_y_offset,
                bg_color=bg,
            )

    def destroy(self) -> None:  # noqa: D102
        if self.tooltip is not None:
            self.tooltip.destroy()
        super().destroy()

    def configure(self, require_redraw: bool = False, **kwargs) -> None:  # noqa: ANN003, D102
        if "tooltip_text" in kwargs:
            tt_text = kwargs.pop("tooltip_text", None)
            if self.tooltip is None and tt_text is not None:
                self.tooltip = Tooltip(self, tt_text)
            elif self.tooltip is not None and tt_text is None:
                self.tooltip.destroy()
                self.tooltip = None
            elif self.tooltip is not None and tt_text is not None:
                self.tooltip.configure_tooltip(message=tt_text)

        super().configure(require_redraw, **kwargs)
