import os

def limpiar_pantalla() -> None:
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)
    return None

def match_input(pregunta: str) -> int:
        opciones = ("s", "n")
        input_usuario = input(pregunta).strip().lower()
        if input_usuario not in opciones:
            return -1
        return 1 if input_usuario == "s" else 0
