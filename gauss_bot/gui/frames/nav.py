# pylint: disable=protected-access

"""
Implementación de la clase NavFrame,
la barra de navegación de la aplicación.
"""

from typing import TYPE_CHECKING

from customtkinter import (
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from ...util_funcs import get_dict_key
from ...icons import (
    LOGO,
    DROPLEFT_ICON,
    DROPRIGHT_ICON,
    HOME_ICON,
    INPUTS_ICON,
    MATRIZ_ICON,
    VECTOR_ICON,
    ANALISIS_ICON,
    ECUACIONES_ICON,
    CONFIG_ICON,
    QUIT_ICON,
)

from ..custom import IconButton

if TYPE_CHECKING:
    from .. import GaussUI


class NavFrame(ctkFrame):
    """
    Barra de navigación que contiene botones
    para navegar entre los distintos frames de la aplicación.
    """

    def __init__(self, app: "GaussUI", master: "GaussUI") -> None:
        super().__init__(master, corner_radius=0)
        self.app = app

        self.configure(fg_color=self.app.theme_config["CTk"]["fg_color"])
        self.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(8, weight=1)  # para tener un espacio entre los botones
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.hidden = False
        self.button_texts: dict[str, str] = {
            "home": "Inicio",
            "inputs": "Menú de Datos",
            "matrices": "Menú de Matrices",
            "vectores": "Menú de Vectores",
            "analisis": "Análisis Númerico",
            "sistemas": "Sistemas de Ecuaciones",
            "config": "Configuración",
            "quit": "Cerrar",
        }

        # label y logo de la barra de navegacion
        self.logo_label = ctkLabel(self, image=LOGO, text="")
        self.app_name = ctkLabel(
            self,
            text="GaussBot",
            font=ctkFont(size=16, weight="bold"),
        )

        self.hide_button = IconButton(
            self,
            app=self.app,
            width=30,
            height=30,
            image=DROPLEFT_ICON,
            command=self.toggle_nav,
        )

        # crear botones de navegacion
        self.home_button = IconButton(
            self,
            app=self.app,
            height=30,
            corner_radius=0,
            border_width=0,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            text="Inicio",
            image=HOME_ICON,
            anchor="w",
            command=self.home_button_event,
        )

        self.inputs_button = IconButton(
            self,
            app=self.app,
            height=30,
            corner_radius=0,
            border_width=0,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            text="Menú de Datos",
            image=INPUTS_ICON,
            anchor="w",
            command=self.inputs_button_event,
        )

        self.matrices_button = IconButton(
            self,
            app=self.app,
            height=30,
            corner_radius=0,
            border_width=0,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            text="Menú de Matrices",
            image=MATRIZ_ICON,
            anchor="w",
            command=self.matrices_button_event,
        )

        self.vectores_button = IconButton(
            self,
            app=self.app,
            height=30,
            corner_radius=0,
            border_width=0,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            text="Menú de Vectores",
            image=VECTOR_ICON,
            anchor="w",
            command=self.vectores_button_event,
        )

        self.analisis_button = IconButton(
            self,
            app=self.app,
            height=30,
            corner_radius=0,
            border_width=0,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            text="Análisis Númerico",
            image=ANALISIS_ICON,
            anchor="w",
            command=self.analisis_button_event,
        )

        self.sistemas_button = IconButton(
            self,
            app=self.app,
            height=30,
            corner_radius=0,
            border_width=0,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            text="Sistemas de Ecuaciones",
            image=ECUACIONES_ICON,
            anchor="w",
            command=self.sistemas_button_event,
        )

        self.config_button = IconButton(
            self,
            app=self.app,
            height=30,
            corner_radius=0,
            border_width=0,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            text="Configuración",
            image=CONFIG_ICON,
            anchor="w",
            command=self.config_button_event,
        )

        self.quit_button = IconButton(
            self,
            app=self.app,
            height=30,
            corner_radius=0,
            border_width=0,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            text="Cerrar",
            image=QUIT_ICON,
            anchor="w",
            command=self.quit_event,
        )

        self.frames: dict[str, ctkFrame] = {
            "home": self.app.home_frame,  # type: ignore
            "inputs": self.app.inputs_frame,  # type: ignore
            "matrices": self.app.matrices,  # type: ignore
            "vectores": self.app.vectores,  # type: ignore
            "analisis": self.app.analisis,  # type: ignore
            "sistemas": self.app.sistemas,  # type: ignore
            "config": self.app.config_frame  # type: ignore
        }

        self.buttons: dict[str, IconButton] = {
            "home": self.home_button,
            "inputs": self.inputs_button,
            "matrices": self.matrices_button,
            "vectores": self.vectores_button,
            "analisis": self.analisis_button,
            "sistemas": self.sistemas_button,
            "config": self.config_button,
            "quit": self.quit_button,
        }

        # colocar widgets en la barra de navegacion
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 3))
        self.app_name.grid(row=1, column=0, padx=0, pady=(3, 10), sticky="nse")
        self.hide_button.grid(row=1, column=1, padx=10, pady=(3, 10), sticky="e")

        i = 2
        for j, widget in enumerate(self.buttons.values()):
            if i == 8:
                i += 1

            if j == len(self.buttons.values()) - 1:
                pady = (0, 10)
            else:
                pady = 0  # type: ignore

            widget.grid(row=i, column=0, columnspan=3, padx=10, pady=pady, sticky="ew")
            i += 1

    def seleccionar_frame(self, nombre: str) -> None:
        """
        Muestra el frame correspondiente al nombre ingresado,
        y oculta los demás. Cambia el color del botón presionado.
        """

        # resaltar el boton seleccionado
        for nombre_frame, button in self.buttons.items():
            button.configure(
                fg_color=("gray75", "gray25")
                if nombre == nombre_frame
                else "transparent"
            )

        # mostrar el frame seleccionado y ocultar el resto
        for nombre_frame, frame in self.frames.items():
            if nombre == nombre_frame:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def toggle_nav(self) -> None:
        """
        Muestra u oculta la barra de navegación.
        """

        if self.hidden:
            for widget in self.winfo_children():
                if widget in (self.logo_label, self.hide_button):
                    continue
                if isinstance(widget, ctkLabel):
                    widget.grid()
                elif isinstance(widget, IconButton):
                    widget.configure(
                        width=140,
                        text=self.button_texts[
                            get_dict_key(self.buttons, widget)  # type: ignore
                        ],
                    )

                    widget._image_label.grid_configure(  # type: ignore
                        columnspan=1, sticky="e",
                    )

            self.hidden = False
            self.hide_button.grid_configure(column=1, columnspan=1, sticky="e")
            self.hide_button.configure(image=DROPLEFT_ICON)

        else:
            for widget in self.winfo_children():
                if widget in (self.logo_label, self.hide_button):
                    continue
                if widget is self.app_name:
                    widget.grid_remove()
                elif isinstance(widget, IconButton):
                    widget.configure(width=20, text="")
                    widget._image_label.grid_configure(  # type: ignore
                        columnspan=3, sticky="nsew",
                    )

            self.hidden = True
            self.hide_button.grid_configure(column=0, columnspan=2, sticky="nsew")
            self.hide_button.configure(image=DROPRIGHT_ICON)

    def home_button_event(self) -> None:
        """
        Muestra HomeFrame cuando el evento de su botón ocurre.
        """

        self.seleccionar_frame("home")

    def inputs_button_event(self) -> None:
        """
        Muestra InputsFrame cuando el evento de su botón ocurre.
        """

        self.seleccionar_frame("inputs")

    def matrices_button_event(self) -> None:
        """
        Muestra MatricesFrame cuando el evento de su botón ocurre.
        """

        self.seleccionar_frame("matrices")

    def vectores_button_event(self) -> None:
        """
        Muestra VectoresFrame cuando el evento de su botón ocurre.
        """

        self.seleccionar_frame("vectores")

    def analisis_button_event(self) -> None:
        """
        Muestra AnalisisFrame cuando el evento de su botón ocurre.
        """

        self.seleccionar_frame("analisis")

    def sistemas_button_event(self) -> None:
        """
        Muestra EcuacionesFrame cuando el evento de su botón ocurre.
        """

        self.seleccionar_frame("sistemas")


    def config_button_event(self) -> None:
        """
        Muestra ConfigFrame cuando el evento de su botón ocurre.
        """

        self.seleccionar_frame("config")

    def quit_event(self) -> None:
        """
        Evento de cierre de aplicación.
        Se encarga de llamar los métodos para guardar los datos.
        """

        self.app.func_manager.save_funciones()  # type: ignore
        self.app.ops_manager.save_sistemas()  # type: ignore
        self.app.ops_manager.save_matrices()  # type: ignore
        self.app.ops_manager.save_vectores()  # type: ignore
        self.app.save_config()
        self.app.quit()
