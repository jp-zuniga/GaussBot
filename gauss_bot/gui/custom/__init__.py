from typing import (
    Literal,
    Optional,
    Union,
)

from customtkinter import CTkFrame as ctkFrame

from .adapted import (
    ScrollableDropdown,
    # CustomScrollFrame,
    CustomMessagebox,
    Tooltip,
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
    "ScrollableDropdown",
    "CustomMessagebox",
    "Tooltip",
    "CustomScrollFrame",
    "ErrorFrame",
    "SuccessFrame",
    "ResultadoFrame",
    "CustomEntry",
    "CustomDropdown",
    "FuncDropdown",
    "IconButton",
    "place_msg_frame",
]


def place_msg_frame(
    parent_frame: Union[ctkFrame, CustomScrollFrame],  # noqa
    msj_frame: Optional[ctkFrame],
    msj: str,
    tipo: Literal["error", "success", "resultado"] = "error",
    **grid_kwargs,
) -> None:

    """
    Inicializa self.mensaje_frame y lo coloca en la interfaz.
    * parent_frame: frame que contendrá msj_frame
    * msj_frame: frame a colocar
    * msj: mensaje a mostrar en el frame
    * tipo: tipo de frame a crear
    * grid_kwargs: kwargs a pasar a msj_frame.grid()
    """

    if tipo == "error":
        msj_frame = ErrorFrame(parent_frame, msj)  # noqa
    elif tipo == "success":
        msj_frame = SuccessFrame(parent_frame, msj)  # noqa
    elif tipo == "resultado":
        msj_frame = ResultadoFrame(parent_frame, msj)  # noqa
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

    msj_frame.grid(**grid_kwargs)
