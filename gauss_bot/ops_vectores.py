from fractions import Fraction
from typing import List, Dict

from gauss_bot.clases.vector import Vector
from gauss_bot.utils import limpiar_pantalla

DictVectores = Dict[str, Vector]

class OperacionesVectores:
    def __init__(self, default_vecs: DictVectores = {}) -> None:
        self.vecs_ingresados = default_vecs

    """ def main_vectores(self) -> None:
        option = self.menu_vectores()
        while option != 7:
            match option:
                case 1:
                    limpiar_pantalla()
                    self.agregar_vector()
                    option = self.menu_vectores()
                    continue
                case 2:
                    limpiar_pantalla()
                    self.suma_resta_vectores()
                    option = self.menu_vectores()
                    continue
                case 3:
                    limpiar_pantalla()
                    self.mult_escalar()
                    option = self.menu_vectores()
                    continue
                case 4:
                    limpiar_pantalla()
                    self.mult_vectorial()
                    option = self.menu_vectores()
                    continue
                case 5:
                    limpiar_pantalla()
                    self.mult_matriz_vector()
                    option = self.menu_vectores()
                    continue
                case 6:
                    input("Regresando al menú principal...")
                    break
                case _:
                    input("Opción inválida! Por favor, intente de nuevo...")
                    continue
        return None """

    """ def menu_vectores(self) -> int:
        limpiar_pantalla()
        print("\n###############################")
        print("### Operaciones Vectoriales ###")
        print("###############################")
        self._imprimir_vectores()
        print("\n1. Agregar un vector")
        print("2. Suma y resta de vectores")
        print("3. Multiplicación escalar")
        print("4. Producto punto")
        print("5. Producto matriz-vector")
        print("6. Regresar al menú principal")

        try:
            option = int(input("\nSeleccione una opción: "))
            if option < 1 or option > 6:
                raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.menu_vectores()

        return option """

    def agregar_vector(self) -> None:
        try:
            limpiar_pantalla()
            nombre = input("\nIngrese el nombre del vector (una letra minúscula): ").strip().lower()
            if not nombre.isalpha() or len(nombre) != 1:
                raise NameError("Error: Ingrese solamente una letra minúscula!")
            if nombre in self.vecs_ingresados:
                raise KeyError(f"Error: Ya hay un vector con el nombre {nombre}!")

            longitud = int(input("¿Cuántas dimensiones tendrá el vector? ").strip())

        except NameError as n:
            input(n)
            return self.agregar_vector()
        except KeyError as k:
            input(k)
            return self.agregar_vector()
        except ValueError:
            input("Error: Ingrese un número entero!")
            return self.agregar_vector()

        self.vecs_ingresados[nombre] = self.pedir_vector(longitud)
        print("\nVector agregado exitosamente!")

        match input("¿Desea agregar otro vector? (s/n) ").strip().lower():
            case "s":
                return self.agregar_vector()
            case "n":
                input("Regresando al menú de vectores...")
            case _:
                input("Opción inválida! Regresando al menú de vectores...")

        return None

    def pedir_vector(self, longitud: int) -> Vector:
        try:
            componentes = [
                Fraction(x).limit_denominator(100)
                for x in input("Ingrese los componentes (separados por comas): ")
                .strip()
                .split(",")
            ]

            if len(componentes) != longitud:
                raise TypeError("Error: El vector no tiene las dimensiones correctas!")

        except TypeError as t:
            input(t)
            return self.pedir_vector(longitud)
        except ValueError:
            input("Error: Ingrese un número real!")
            return self.pedir_vector(longitud)

        return Vector(componentes)

    def seleccionar_vector(self, operacion: str) -> str:
        if operacion not in ("e", "mv"):
            return ""
        if not self._validar_vecs_ingresados():
            return ""

        match operacion:
            case "e":
                mensaje = "multiplicar escalarmente"
            case "mv":
                mensaje = "multiplicar por la matriz"

        mensaje = f"\n¿Cuál vector desea {mensaje}? "
        try:
            limpiar_pantalla()
            self._imprimir_vectores()
            input_vec = input(mensaje).strip()
            if input_vec not in self.vecs_ingresados:
                raise KeyError(f"Error: El vector '{input_vec}' no existe!")

        except KeyError as k:
            input(k)
            return self.seleccionar_vector(operacion)

        return input_vec

    def seleccionar_vectores(self) -> List[str]:
        if not self._validar_vecs_ingresados():
            return []

        mensaje = "\n¿Cuáles vectores desea seleccionar? (separados por comas)"
        try:
            limpiar_pantalla()
            self._imprimir_vectores()
            input_vecs = input(mensaje).strip().split(",")
            vec_existe = next((vec for vec in input_vecs if vec not in self.vecs_ingresados), None)

            if vec_existe is not None:
                raise KeyError(f"Error: El vector '{vec_existe}' no existe!")
            if len(input_vecs) != 2:
                raise ValueError("Error: Solamente debe ingresar dos vectores!")

        except KeyError as k:
            input(k)
            return self.seleccionar_vectores()
        except ValueError as v:
            input(v)
            return self.seleccionar_vectores()

        return input_vecs

    def _validar_vecs_ingresados(self) -> bool:
        if self.vecs_ingresados == {}:
            input("\nNo hay vectores ingresados!")
            return False
        return True

    def _imprimir_vectores(self, es_matricial=False) -> None:
        if not self._validar_vecs_ingresados():
            return None

        mensaje = "seleccionados" if es_matricial else "ingresados"
        print(f"\nVectores {mensaje}:")
        print("---------------------------------------------")
        for nombre, vector in self.vecs_ingresados.items():
            """ vec = [str(num.limit_denominator(100)) for num in vector]
            print(f"{nombre}: {vec}") """
        print("---------------------------------------------")

        return None
