import os


def limpiar_pantalla() -> None:
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)
    return None


def match_input(pregunta: str) -> int:
    opciones = {"s": 1, "n": 0}
    input_usuario = input(pregunta).strip().lower()
    if input_usuario in opciones:
        return opciones[input_usuario]
    else:
        return -1
