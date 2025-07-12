"""
Implementación de barra de navegación.
"""

from tkinter import Event
from typing import TYPE_CHECKING

from bidict import bidict
from customtkinter import CTkFont, CTkFrame, CTkLabel, ThemeManager

from src.gui.custom import IconButton
from src.gui.custom.adapted import CustomMessageBox
from src.utils import (
    ANALISIS_ICON,
    CONFIG_ICON,
    DROPLEFT_ICON,
    DROPRIGHT_ICON,
    ECUACIONES_ICON,
    INPUTS_ICON,
    LOGO,
    MATRIZ_ICON,
    QUIT_ICON,
    VECTOR_ICON,
)

if TYPE_CHECKING:
    from src.gui import GaussUI


class NavFrame(CTkFrame):
    """
    Barra de navigación que contiene botones
    para navegar entre los distintos frames de la aplicación.
    """

    def __init__(self, app: "GaussUI", master: "GaussUI") -> None:
        """
        Inicializar diseño de barra de navegación.
        """

        super().__init__(master, corner_radius=0)

        self.app = app
        self.msg_box: CustomMessageBox | None = None

        self.configure(fg_color=ThemeManager.theme["CTk"]["fg_color"])
        self.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(7, weight=1)  # para tener un espacio entre los botones
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.hidden = False
        self.button_texts: dict[str, str] = {
            "home": "Inicio",
            "inputs": "Datos",
            "matrices": "Matrices",
            "vectores": "Vectores",
            "analisis": "Análisis Númerico",
            "sistemas": "Sistemas de Ecuaciones",
            "config": "Configuración",
            "quit": "Cerrar",
        }

        # label y logo de la barra de navegacion
        self.app_name = CTkLabel(
            self,
            text="GaussBot",
            font=CTkFont(size=16, weight="bold"),
        )

        self.hide_button = IconButton(
            self,
            tooltip_x_offset=75,
            tooltip_y_offset=-15,
            tooltip_text="Esconder barra de navegación",
            image=DROPLEFT_ICON,
            command=self.toggle_nav,
        )

        # crear botones de navegacion
        self.home_button = IconButton(
            self,
            corner_radius=0,
            border_spacing=10,
            anchor="w",
            text="Inicio",
            image=LOGO,
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            command=lambda: self.seleccionar_frame("home"),
        )

        self.inputs_button = IconButton(
            self,
            corner_radius=0,
            border_spacing=10,
            anchor="w",
            text="Datos",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            image=INPUTS_ICON,
            command=lambda: self.seleccionar_frame("inputs"),
        )

        self.matrices_button = IconButton(
            self,
            corner_radius=0,
            border_spacing=10,
            anchor="w",
            text="Matrices",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            image=MATRIZ_ICON,
            command=lambda: self.seleccionar_frame("matrices"),
        )

        self.vectores_button = IconButton(
            self,
            corner_radius=0,
            border_spacing=10,
            anchor="w",
            text="Vectores",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            image=VECTOR_ICON,
            command=lambda: self.seleccionar_frame("vectores"),
        )

        self.analisis_button = IconButton(
            self,
            corner_radius=0,
            border_spacing=10,
            anchor="w",
            text="Análisis Númerico",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            image=ANALISIS_ICON,
            command=lambda: self.seleccionar_frame("analisis"),
        )

        self.sistemas_button = IconButton(
            self,
            corner_radius=0,
            border_spacing=10,
            anchor="w",
            text="Sistemas de Ecuaciones",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            image=ECUACIONES_ICON,
            command=lambda: self.seleccionar_frame("sistemas"),
        )

        self.config_button = IconButton(
            self,
            corner_radius=0,
            border_spacing=10,
            anchor="w",
            text="Configuración",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            image=CONFIG_ICON,
            command=lambda: self.seleccionar_frame("config"),
        )

        self.quit_button = IconButton(
            self,
            corner_radius=0,
            border_spacing=10,
            anchor="w",
            text="Cerrar",
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            image=QUIT_ICON,
            command=self.quit_event,
        )

        self.frames: dict[str, CTkFrame] = {
            "home": self.app.home_frame,
            "inputs": self.app.inputs_frame,
            "matrices": self.app.matrices,
            "vectores": self.app.vectores,
            "analisis": self.app.analisis,
            "sistemas": self.app.sistemas,
            "config": self.app.config_frame,
        }

        self.buttons: bidict[str, IconButton] = bidict(
            {
                "home": self.home_button,
                "inputs": self.inputs_button,
                "matrices": self.matrices_button,
                "vectores": self.vectores_button,
                "analisis": self.analisis_button,
                "sistemas": self.sistemas_button,
                "config": self.config_button,
                "quit": self.quit_button,
            },
        )

        # colocar widgets en la barra de navegacion
        self.app_name.grid(row=0, column=0, padx=0, pady=(20, 10), sticky="nse")
        self.hide_button.grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=(20, 10),
            sticky="nse",
        )

        i = 1
        for j, widget in enumerate(self.buttons.values()):
            if i == 7:
                i += 1

            widget.grid(
                row=i,
                column=0,
                columnspan=2,
                padx=15,
                pady=(0, 10) if j == len(self.buttons.values()) - 1 else 0,
                sticky="ew",
            )

            i += 1

    def seleccionar_frame(self, nombre: str) -> None:
        """
        Mostrar el frame seleccionado por el usuario.
        """

        # resaltar el boton seleccionado
        for nombre_frame, button in self.buttons.items():
            button.configure(
                fg_color=ThemeManager.theme["CTkFrame"]["top_fg_color"]
                if nombre == nombre_frame
                else "transparent",
            )

        # mostrar el frame seleccionado y ocultar el resto
        for nombre_frame, frame in self.frames.items():
            if nombre == nombre_frame:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def toggle_nav(self) -> None:
        """
        Mostrar/ocultar barra de navegación.
        """

        if self.hidden:
            for widget in self.winfo_children():
                if widget is self.hide_button:
                    continue
                if widget is self.app_name:
                    widget.grid()
                elif isinstance(widget, IconButton):
                    widget.configure(
                        text=self.button_texts[self.buttons.inverse[widget]],
                    )

                    widget._image_label.grid_configure(columnspan=1, sticky="e")  # type: ignore[reportOptionalMemberAccess]  # noqa: SLF001

            self.hidden = False
            self.hide_button.configure(
                image=DROPLEFT_ICON,
                tooltip_text="Esconder barra de navegación",
            )

            self.hide_button.grid_configure(column=1, columnspan=1, sticky="nse")

        else:
            for widget in self.winfo_children():
                if widget is self.hide_button:
                    continue
                if widget is self.app_name:
                    widget.grid_remove()
                elif isinstance(widget, IconButton):
                    widget.configure(text="")
                    widget._image_label.grid_configure(columnspan=3, sticky="nsew")  # type: ignore[reportOptionalMemberAccess]  # noqa: SLF001

            self.hidden = True
            self.hide_button.configure(
                image=DROPRIGHT_ICON,
                tooltip_text="Mostrar barra de navegación",
            )

            self.hide_button.grid_configure(column=0, columnspan=2, sticky="nse")

    def quit_event(self, event: Event | None = None) -> None:
        """
        Guardar datos y cerrar aplicación.
        """

        del event

        if self.msg_box is not None:
            self.msg_box.focus()
            return

        self.msg_box = CustomMessageBox(
            self.app,
            name="Cerrar aplicación",
            msg="¿Está seguro que desea cerrar GaussBot?"
            "\n(sus cambios serán guardados)",
            button_options=("Sí", "No", None),
            icon="warning",
        )

        seleccion: str = self.msg_box.get()
        self.msg_box.destroy()
        del self.msg_box

        if seleccion == "Sí":
            self.app.func_manager.save_funciones()
            self.app.ops_manager.save_sistemas()
            self.app.ops_manager.save_matrices()
            self.app.ops_manager.save_vectores()
            self.app.save_config()
            self.app.quit()
