"""
Funciones de utilidad relacionadas a la interfaz gráfica.
"""

from __future__ import annotations

from platform import system
from typing import TYPE_CHECKING, Literal

from PIL.ImageTk import PhotoImage
from customtkinter import CTkFont, CTkFrame, CTkImage, CTkLabel, CTkToplevel as CTkTop

from .icons import APP_ICON

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.custom.adapted import CustomScrollFrame


def delete_msg_frame(msg_frame: CTkFrame | None) -> None:
    """
    Eliminar un frame de mensaje, si existe.

    Args:
        msg_frame: Frame a eliminar.

    """

    if msg_frame is not None:
        msg_frame.destroy()
        msg_frame = None


def delete_msg_if(
    msg_frame: CTkFrame | None,
    masters: tuple[CTkFrame, CTkFrame],
) -> None:
    """
    Eliminar un frame si está colocado en uno de los frames indicados.

    Args:
        msg_frame: Frame a eliminar.
        masters:   Frames donde buscar msg_frame.master.

    """

    if msg_frame is None:
        return
    if msg_frame.master in masters:
        delete_msg_frame(msg_frame)


def place_msg_frame(
    parent_frame: CTkFrame | CustomScrollFrame,
    msg_frame: CTkFrame | None,
    msg: str | None = None,
    img: CTkImage | None = None,
    tipo: Literal["error", "success", "resultado"] = "error",
    **grid_kwargs,  # noqa: ANN003
) -> CTkFrame:
    """
    Inicializar msg_frame y colocarlo en la interfaz.

    Args:
        parent_frame: Frame que contendrá msg_frame.
        msg_frame:    Frame a colocar.
        msg:          Mensaje a mostrar en el frame.
        img:          Imagen a colocar en el frame.
        tipo:         Tipo de frame a crear.
        grid_kwargs:  Kwargs a pasar a msg_frame.grid().

    Returns:
        CTkFrame: El frame colocado.

    Raises:
        ValueError: Si 'tipo' no es igual a "error", "success", o "resultado".

    """

    # import local para evitar errores de imports circulares
    from src.gui.custom import ErrorFrame, ResultadoFrame, SuccessFrame

    if tipo not in ("error", "success", "resultado"):
        raise ValueError

    if tipo == "error":
        msg_frame = ErrorFrame(parent_frame, msg)
    elif tipo == "success":
        msg_frame = SuccessFrame(parent_frame, msg)
    elif tipo == "resultado":
        bc: str | None = grid_kwargs.pop("border_color", None)
        msg_frame = ResultadoFrame(parent_frame, msg, img, bc)

    # inicializar kwargs por defecto
    if "row" not in grid_kwargs:
        grid_kwargs["row"] = 0
    if "column" not in grid_kwargs:
        grid_kwargs["column"] = 0
    if "padx" not in grid_kwargs:
        grid_kwargs["padx"] = 5
    if "pady" not in grid_kwargs:
        grid_kwargs["pady"] = 5
    if "sticky" not in grid_kwargs:
        grid_kwargs["sticky"] = "n"

    msg_frame.grid(**grid_kwargs)
    return msg_frame


def set_icon(app: GaussUI, window: GaussUI | CTkTop) -> None:
    """
    Establecer el ícono de una ventana según
    la plataforma y el modo actual de la aplicación.

    Args:
        app:    Instancia root de GaussUI.
        window: Ventana a modificar.

    """

    if system() == "Windows":
        window.iconbitmap(bitmap=APP_ICON[0 if app.modo_actual == "dark" else 1])
    else:
        window.iconphoto(
            False,
            PhotoImage(file=APP_ICON[0 if app.modo_actual == "dark" else 1]),  # type: ignore[reportArgumentType]
        )


def toggle_proc(  # noqa: PLR0913
    app: GaussUI,
    parent_frame: CustomScrollFrame,
    window_title: str,
    proc_label: CTkLabel | None,
    label_txt: str,
    proc_hidden: bool,
) -> None:
    """
    Mostrar o esconder la ventana de procedimiento de una operación.

    Args:
        app:          Instancia root de GaussUI.
        parent_frame: Frame donde el usuario lanza la ventana de procedimiento.
        window_title: Título de la ventana a crear.
        proc_label:   Label que contiene el procedimiento.
        label_txt:    Texto del procedimiento.
        proc_hidden:  Bandera para identificar si esta abierta la ventana.

    """

    from src.gui.custom.adapted import CustomNumpad, CustomScrollFrame

    if not proc_hidden or any(
        isinstance(widget, CTkTop) and not isinstance(widget, CustomNumpad)
        for widget in app.winfo_children()
    ):
        return

    new_window = CTkTop(app)
    new_window.title(window_title)
    new_window.geometry("800x800")

    parent_frame.after(100, new_window.focus)
    parent_frame.after(250, lambda: set_icon(app, new_window))

    dummy_frame = CTkFrame(
        new_window,
        fg_color="transparent",
        corner_radius=20,
        border_width=3,
    )

    dummy_frame.pack(expand=True, fill="both", padx=20, pady=20)
    proc_frame = CustomScrollFrame(dummy_frame, fg_color="transparent")

    proc_frame.pack(expand=True, fill="both", padx=10, pady=10)
    proc_label = CTkLabel(proc_frame, text=label_txt.strip(), font=CTkFont(size=14))

    proc_label.pack(expand=True, fill="both", padx=10, pady=10)
    proc_hidden = False

    new_window.protocol("WM_DELETE_WINDOW", lambda: delete_window(new_window))

    def delete_window(new_window: CTkTop) -> None:
        nonlocal proc_hidden, proc_label  # ocupar las variables del alcance exterior

        proc_hidden = True
        new_window.destroy()
        proc_label = None
