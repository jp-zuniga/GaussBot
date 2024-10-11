from fractions import Fraction
from copy import deepcopy
from typing import List, Any, overload

from gauss_bot.clases.vector import Vector, DictVectores
from gauss_bot.utils import limpiar_pantalla, match_input

class VectoresManager:
    def __init__(self, vecs_ingresados: DictVectores = {}) -> None:
        self.vecs_ingresados = vecs_ingresados

    def menu_vectores(self) -> None:
        while True:
            limpiar_pantalla()
            print("\n###############################")
            print("### Operaciones de Vectores ###")
            print("###############################")
            print("\n1. Agregar un vector")
            print("2. Mostrar vectores")
            print("3. Sumar vectores")
            print("4. Restar vectores")
            print("5. Multiplicar vector por escalar")
            print("6. Multiplicar vectores")
            print("7. Multiplicar matriz por vector")
            print("8. Regresar al menú principal")
            try:
                option = int(input("\nSeleccione una opción: ").strip())
                if option < 1 or option > 8:
                    raise ValueError
            except ValueError:
                input("\nError: Ingrese una opción válida!")
                continue
            if option == 8:
                input("Regresando a menú principal...")
                break
            self.procesar_menu(option)
        return None

    def procesar_menu(self, opcion: int) -> None:
        match opcion:
            case 1:
                self.agregar_vector()
            case 2:
                self._mostrar_vectores()
            case 3:
                self.mostrar_resultado("s", self.procesar_operacion("s"))
            case 4:
                self.mostrar_resultado("r", self.procesar_operacion("r"))
            case 5:
                self.mostrar_resultado("ve", self.procesar_operacion("ve"))
            case 6:
                self.mostrar_resultado("m", self.procesar_operacion("m"))
            case 7:
                ...  # TODO: producto matriz-vector
        return None

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
        print("\nMatriz agregada exitosamente!")
        ingresar_otro = match_input("¿Desea ingresar otro vector? (s/n) ")
        if ingresar_otro:
            return self.agregar_vector()
        elif not ingresar_otro:
            input("Regresando al menú de vectores...")
        else:
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
        except ZeroDivisionError:
            input("Error: El denominador no puede ser cero!")
            return self.pedir_vector(longitud)

        return Vector(componentes)

    def procesar_operacion(self, operacion: str):
        """
        * toma un codigo de operacion
        * selecciona los vectores necesarios
        * retorna una tupla con lo que selecciono el usuario y los resultados de la operacion

        codigos validos de operacion:
        * "s": sumar vectores
        * "r": restar vectores
        * "ve": multiplicar vector por escalar
        * "m": multiplicar vectores
        """

        if operacion not in ("s", "r", "ve", "m"):
            return None

        if operacion in ("s", "r", "m"):
            nombres_vecs = self.seleccionar(None)
            vec1, vec2 = self.vecs_ingresados[nombres_vecs[0]], self.vecs_ingresados[nombres_vecs[1]]
            match operacion:
                case "s":
                    return (nombres_vecs, vec1 + vec2)
                case "r":
                    return (nombres_vecs, vec1 - vec2)
                case "m":
                    return (nombres_vecs, vec1 * vec2)

        elif operacion == "ve":
            nombre_vec = self.seleccionar(operacion)
            vec_copia = deepcopy(self.vecs_ingresados[nombre_vec])
            escalar = Fraction(input("Ingrese el escalar: ").strip())
            return (nombre_vec, vec_copia * escalar)

    def mostrar_resultado(self, operacion: str, resultado: Any) -> None:
        """
        * operacion: el codigo de operacion usada en .procesar_operacion()
        * resultado: la tupla retornada por .procesar_operacion()

        codigos validos de operacion:
        * "s": sumar vectores
        * "r": restar vectores
        * "ve": multiplicar vector por escalar
        * "m": multiplicar vectores
        """

        if operacion not in ("s", "r", "ve", "m"):
            return None

        match operacion:
            case "s":   # ? sumar vectores
                vecs_seleccionados, vec_sumado = self.procesar_operacion("s")
                vec1, vec2 = self.vecs_ingresados[vecs_seleccionados[0]], self.vecs_ingresados[vecs_seleccionados[1]]

                limpiar_pantalla()
                print(f"\n{vecs_seleccionados[0]} = {vec1}")
                print(f"\n{vecs_seleccionados[1]} = {vec2}")
                print(f"\n{vecs_seleccionados[0]} + {vecs_seleccionados[1]} = {vec_sumado}")

                input("\nPresione cualquier tecla para continuar...")
                return None
            case "r":   # ? restar vectores
                vecs_seleccionados, vec_restado = self.procesar_operacion("r")
                vec1, vec2 = self.vecs_ingresados[vecs_seleccionados[0]], self.vecs_ingresados[vecs_seleccionados[1]]

                limpiar_pantalla()
                print(f"\n{vecs_seleccionados[0]} = {vec1}")
                print(f"\n{vecs_seleccionados[1]} = {vec2}")
                print(f"\n{vecs_seleccionados[0]} - {vecs_seleccionados[1]} = {vec_restado}")

                input("\nPresione cualquier tecla para continuar...")
                return None
            case "me":  # ? multiplicar vectores por escalar
                vec_seleccionado, escalar, vec_multiplicado = self.procesar_operacion("me")
                vec = self.vecs_ingresados[vec_seleccionado]

                limpiar_pantalla()
                print(f"\n{vec_seleccionado} = {vec}")
                print(f"\n{vec_seleccionado} * {escalar} = {vec_multiplicado}")

                input("\nPresione cualquier tecla para continuar...")
                return None
            case "m":   # ? multiplicar vectores
                vecs_seleccionados, vec_multiplicado = self.procesar_operacion("m")
                vec1, vec2 = self.vecs_ingresados[vecs_seleccionados[0]], self.vecs_ingresados[vecs_seleccionados[1]]

                limpiar_pantalla()
                print(f"\n{vecs_seleccionados[0]} = {vec1}")
                print(f"\n{vecs_seleccionados[1]} = {vec2}")
                print(f"\n{vecs_seleccionados[0]}.{vecs_seleccionados[1]} = {vec_multiplicado}")

                input("\nPresione cualquier tecla para continuar...")
                return None
        return None

    @overload
    def seleccionar(self, operacion: str) -> str: ...

    @overload
    def seleccionar(self, operacion: None) -> List[str]: ...

    def seleccionar(self, operacion: str | None) -> str | List[str]:
        if operacion not in ("ve", "mv", None):
            return "" if operacion else []

        if not self._validar_vecs_ingresados():
            return "" if operacion else []

        if operacion is not None:
            mensaje = self._get_mensaje(operacion)
            input_vec = self._get_input(mensaje, operacion)
            self._validate_input_vec(input_vec, operacion)
            return input_vec
        else:
            mensaje = "\n¿Cuáles vectores desea seleccionar? (separados por comas) "
            input_vecs = self._get_input(mensaje, operacion).split(",")
            self._validate_input_vecs(input_vecs)
            return input_vecs

    def _get_mensaje(self, operacion: str) -> str:
        match operacion:
            case "ve":
                return "\n¿Cuál vector desea multiplicar por un escalar? "
            case "mv":
                return "\n¿Cuál vector desea multiplicar por una matriz? "
            case _:
                return ""

    def _get_input(self, mensaje: str, operacion: str | None) -> str:
        limpiar_pantalla()
        self._mostrar_vectores()
        return input(mensaje).strip()

    def _validate_input_vec(self, input_vec: str, operacion: str) -> None:
        if input_vec not in self.vecs_ingresados:
            raise KeyError("Error: El vector no existe.")

    def _validate_input_vecs(self, input_vecs: List[str]) -> None:
        vec = next((vec for vec in input_vecs if vec not in self.vecs_ingresados), None)
        if vec is not None:
            raise KeyError(f"Error: El vector {vec} no existe.")
        elif len(input_vecs) != 2:
            raise ValueError("Error: Debe seleccionar exactamente dos vectores.")

    def _validar_vecs_ingresados(self) -> bool:
        if self.vecs_ingresados == {}:
            input("\nNo hay vectores ingresados!")
            return False
        return True

    def _mostrar_vectores(self) -> None:
        if not self._validar_vecs_ingresados():
            return None

        print("\nVectores ingresados:")
        print("---------------------------------------------")
        for nombre, vec in self.vecs_ingresados.items():
            print(f"{nombre}: {vec}")
        print("---------------------------------------------")

        input("\nPresione cualquier tecla para regresar al menú de vectores...")
        return None
