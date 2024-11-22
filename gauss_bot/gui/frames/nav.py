"""
Implementación de la clase NavFrame,
la barra de navegación de la aplicación.
"""

from typing import TYPE_CHECKING

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from ...icons import (
    LOGO,
    HOME_ICON,
    INPUTS_ICON,
    MATRIZ_ICON,
    VECTOR_ICON,
    ANALISIS_ICON,
    ECUACIONES_ICON,
    CONFIG_ICON,
    QUIT_ICON,
)

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

        self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(7, weight=1)  # para tener un espacio entre los botones
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.configure(fg_color=self.app.theme_config["CTk"]["fg_color"])

        # label y logo de la barra de navegacion
        self.logo_label = ctkLabel(self, image=LOGO, text="")
        self.logo_text = ctkLabel(
            self, text="GaussBot",
            font=ctkFont(size=18, weight="bold"),
        )

        # crear botones de navegacion
        self.home_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Inicio", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=HOME_ICON, anchor="w",
            command=self.home_button_event,
        )

        self.inputs_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Datos", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=INPUTS_ICON, anchor="w",
            command=self.inputs_button_event,
        )

        self.matrices_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Matrices", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=MATRIZ_ICON, anchor="w",
            command=self.matrices_button_event,
        )

        self.vectores_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Vectores", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=VECTOR_ICON, anchor="w",
            command=self.vectores_button_event,
        )

        self.analisis_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Análisis Númerico", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=ANALISIS_ICON, anchor="w",
            command=self.analisis_button_event,
        )

        self.sistemas_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Sistemas de Ecuaciones", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=ECUACIONES_ICON, anchor="w",
            command=self.sistemas_button_event,
        )

        self.config_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Configuración", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=CONFIG_ICON, anchor="w",
            command=self.config_button_event,
        )

        self.quit_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Cerrar", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=QUIT_ICON, anchor="w",
            command=self.quit_event,
        )

        # colocar widgets en la barra de navegacion
        self.logo_label.grid(row=0, column=0, padx=5, pady=20, sticky="e")
        self.logo_text.grid(row=0, column=1, padx=5, pady=20, sticky="w")
        self.home_button.grid(row=1, column=0, columnspan=2, padx=10, sticky="ew")
        self.inputs_button.grid(row=2, column=0, columnspan=2, padx=10, sticky="ew")
        self.matrices_button.grid(row=3, column=0, columnspan=2, padx=10, sticky="ew")
        self.vectores_button.grid(row=4, column=0, columnspan=2, padx=10, sticky="ew")
        self.analisis_button.grid(row=5, column=0, columnspan=2, padx=10, sticky="ew")
        self.sistemas_button.grid(row=6, column=0, columnspan=2, padx=10, sticky="ew")
        self.config_button.grid(row=8, column=0, columnspan=2, padx=10, sticky="ew")
        self.quit_button.grid(
            row=9, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew"
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

        self.buttons: dict[str, ctkButton] = {
            "home": self.home_button,
            "inputs": self.inputs_button,
            "matrices": self.matrices_button,
            "vectores": self.vectores_button,
            "analisis": self.analisis_button,
            "sistemas": self.sistemas_button,
            "config": self.config_button
        }

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
