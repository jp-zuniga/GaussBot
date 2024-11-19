from typing import (
    Literal,
    Optional,
    Union,
)

from customtkinter import CTkFrame as ctkFrame
from .adapted import (
    CustomMessagebox,
    # CustomScrollFrame,
    CustomNumpad,
    Tooltip,
    ScrollableDropdown,
)

from .custom_frames import (
    CustomScrollFrame,
    ErrorFrame,
    SuccessFrame,
    ResultadoFrame,
)

from .custom_widgets import (
    CustomEntry,
    CustomDropdown,
    FuncDropdown,
    IconButton,
)

__all__ = [
    "CustomEntry",
    "CustomDropdown",
    "CustomMessagebox",
    "CustomScrollFrame",
    "FuncDropdown",
    "IconButton",
    "ErrorFrame",
    "SuccessFrame",
    "ResultadoFrame",
    "CustomNumpad",
    "Tooltip",
    "ScrollableDropdown",
    "place_msg_frame",
]


def place_msg_frame(
    parent_frame: Union[ctkFrame, CustomScrollFrame],  # noqa
    msg_frame: Optional[ctkFrame],
    msg: Optional[str] = None,
    tipo: Literal["error", "success", "resultado"] = "error",
    **grid_kwargs,
) -> ctkFrame:

    """
    Inicializa msg_frame y lo coloca en la interfaz con grid_kwargs.
    * parent_frame: frame que contendrá msg_frame
    * msg_frame: frame a colocar
    * msg: mensaje a mostrar en el frame
    * tipo: tipo de frame a crear
    * grid_kwargs: kwargs a pasar a msg_frame.grid()
    """

    # esta funcion esta aqui pq el hecho que tiene que inicializar un
    # ErrorFrame/SuccessFrame/ResultadoFrame causa errores si esta en otro modulo :/
    # haria mas sentido en el __init__ de gauss_bot, pero ni modo

    if tipo == "error":
        msg_frame = ErrorFrame(parent_frame, msg)  # noqa
    elif tipo == "success":
        msg_frame = SuccessFrame(parent_frame, msg)  # noqa
    elif tipo == "resultado":
        msg_frame = ResultadoFrame(parent_frame, msg)  # noqa
    else:
        raise ValueError("Valor inválido para argumento 'tipo'!")

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
