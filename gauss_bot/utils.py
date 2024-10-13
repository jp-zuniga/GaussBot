import os


def limpiar_pantalla() -> None:
    """
    Llama os.system() con el comando necesario para limpiar la pantalla.
    """

    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def match_input(pregunta: str) -> int:
    """
    Recibe una pregunta de sí o no, y retorna el input.
    * return 1: si el input es "s"
    * return 0: si el input es "n"
    * return -1: si el input no es válido
    """

    opciones = {"s": 1, "n": 0}
    input_usuario = input(pregunta).strip().lower()
    if input_usuario in opciones:
        return opciones[input_usuario]
    return -1
