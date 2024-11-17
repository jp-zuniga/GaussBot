"""
Implementaciones de frames personalizados.
"""

from typing import (
    TYPE_CHECKING,
    Any,
    Union,
)

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkScrollableFrame as ctkScrollFrame,
)

from gauss_bot import (
    CHECK_ICON,
    ERROR_ICON,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


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
        super().__init__(
            parent,
            corner_radius=8,
            border_width=2,
            border_color="#ff3131",
            fg_color="transparent",
        )

        self.parent = parent
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.error_icon_label = ctkLabel(self, text="", image=ERROR_ICON)
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
        super().__init__(
            parent,
            corner_radius=8,
            border_width=2,
            border_color="#18c026",
            fg_color="transparent",
        )

        self.parent = parent
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.check_icon_label = ctkLabel(self, text="", image=CHECK_ICON)
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
        msj: str,
        border_color: str = "#18c026",
    ) -> None:

        super().__init__(
            parent,
            corner_radius=8,
            border_width=2,
            border_color=border_color,
            fg_color="transparent",
        )

        self.parent = parent
        self.msj_label = ctkLabel(self, text=msj)
        self.msj_label.grid(row=0, column=0, padx=10, pady=10)

    def destroy(self) -> None:
        self.forget()
        super().destroy()
