"""
Implementación de FuncManager.
Almacena y valida las funciones ingresadas por el usuario.
"""

from gauss_bot.models import Func

class FuncManager:
    """
    Se encarga de almacenar y validar
    las funciones ingresadas por el usuario,
    para su uso en los módulos de análisis numérico.
    """

    def __init__(self, funcs_ingresadas=None):
        """
        * TypeError: Si funcs_ingresadas no es un dict[str, Func]
        """

        if funcs_ingresadas is None:
            self.funcs_ingresadas: dict[str, Func] = {}  # type: ignore

        elif (
            isinstance(funcs_ingresadas, dict)
            and
            all(
                isinstance(k, str) and isinstance(v, Func)
                for k, v in funcs_ingresadas.items()
            )
        ):
            self.funcs_ingresadas = funcs_ingresadas

        else:
            raise TypeError("Argumento inválido para 'funcs_ingresadas'!")
