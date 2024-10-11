from fractions import Fraction
from typing import Union, Tuple, List, Dict, overload

from gauss_bot.clases.vector import Vector
from gauss_bot.utils import limpiar_pantalla, match_input

class VectoresManager:
    def __init__(self, parent=None, vecs_ingresados: Dict[str, Vector] = {}) -> None:
        self.parent = parent
        self.vecs_ingresados = vecs_ingresados

    def menu_vectores(self) -> None:
        while True:
            limpiar_pantalla()
            print("\n###############################")
            print("### Operaciones de Vectores ###")
            print("###############################")
            print("\n1. Agregar un vector")
            print("2. Mostrar vectores\n")
            print("3. Sumar vectores")
            print("4. Restar vectores")
            print("5. Multiplicar vector por escalar")
            print("6. Multiplicar vectores")
            print("7. Multiplicar matriz por vector\n")
            print("8. Regresar al menú principal")
            try:
                option = int(input("\n=> Seleccione una opción: ").strip())
                if option < 1 or option > 8:
                    raise ValueError
            except ValueError:
                input("=> Error: Ingrese una opción válida!")
                continue
            if option == 8:
                input("=> Regresando a menú principal...")
                break
            self.procesar_menu(option)
        return None

    def procesar_menu(self, opcion: int) -> None:
        match opcion:
            case 1:
                self.agregar_vector()
                return None
            case 2:
                self._mostrar_vectores()
            case 3:
                resultado = self.procesar_operacion("s")
                if resultado is not None:
                    self.mostrar_resultado("s", resultado)
                    return None
            case 4:
                resultado = self.procesar_operacion("r")
                if resultado is not None:
                    self.mostrar_resultado("r", resultado)
                    return None
            case 5:
                resultado = self.procesar_operacion("ve")
                if resultado is not None:
                    self.mostrar_resultado("ve", resultado)
                    return None
            case 6:
                resultado = self.procesar_operacion("m")
                if resultado is not None:
                    self.mostrar_resultado("m", resultado)
                    return None
            case 7:
                self.parent.producto_matriz_vector()
        input("Presione cualquier tecla para regresar al menú de vectores...")
        return None

    def agregar_vector(self) -> None:
        try:
            limpiar_pantalla()
            nombre = input("\nIngrese el nombre del vector (una letra minúscula): ").strip().lower()
            if not nombre.isalpha() or len(nombre) != 1:
                raise NameError("Error: Ingrese solamente una letra minúscula!")
            if nombre in self.vecs_ingresados:
                raise KeyError(f"Error: Ya hay un vector con el nombre '{nombre}'!")

            longitud = int(input(f"¿Cuántas dimensiones tendrá el vector '{nombre}'? ").strip())
            if longitud <= 0:
                raise ArithmeticError("Error: La longitud del vector debe ser un número entero positivo!")

        except NameError as n:
            input(n)
            return self.agregar_vector()
        except KeyError as k:
            input(k)
            return self.agregar_vector()
        except ValueError:
            input("Error: Ingrese un número entero!")
            return self.agregar_vector()
        except ArithmeticError as a:
            input(a)
            return self.agregar_vector()

        self.vecs_ingresados[nombre] = self.pedir_vector(nombre, longitud)
        print("\nVector agregado exitosamente!")
        ingresar_otro = match_input("\n¿Desea ingresar otro vector? (s/n) ")
        if ingresar_otro == 1:
            return self.agregar_vector()
        elif ingresar_otro == 0:
            input("Presione cualquier tecla para regresar al menú de vectores...")
        else:
            input("Opción inválida!\nPresione cualquier tecla para regresar al menú de vectores...")
        return None

    def pedir_vector(self, nombre: str, longitud: int) -> Vector:
        try:
            componentes = [
                Fraction(x).limit_denominator(100)
                for x in input(f"Ingrese los componentes del vector '{nombre}' (separados por comas): ")
                .strip()
                .split(",")
            ]

            if len(componentes) != longitud:
                raise TypeError("Error: El vector no tiene las dimensiones correctas!")

        except TypeError as t:
            input(t)
            return self.pedir_vector(nombre, longitud)
        except ValueError:
            input("Error: Ingrese un número real!")
            return self.pedir_vector(nombre, longitud)
        except ZeroDivisionError:
            input("Error: El denominador no puede ser cero!")
            return self.pedir_vector(nombre, longitud)

        return Vector(componentes)

    def procesar_operacion(self, operacion: str) -> Tuple:
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

        limpiar_pantalla()
        if operacion not in ("s", "r", "ve", "m") or not self._validar_vecs_ingresados():
            return ()

        if operacion in ("s", "r", "m"):
            nombres_vecs = self.seleccionar(None)
            if nombres_vecs == []:
                return ()

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
            if nombre_vec == "":
                return ()

            vec_seleccionado = self.vecs_ingresados[nombre_vec]
            try:
                escalar = Fraction(input("Ingrese el escalar: ").strip()).limit_denominator(100)
            except ValueError:
                input("Error: Ingrese un número real!")
                return ()
            except ZeroDivisionError:
                input("Error: El denominador no puede ser cero!")
                return ()
            return (nombre_vec, escalar, vec_seleccionado * escalar)
        return ()

    def mostrar_resultado(self, operacion: str, resultado: Tuple) -> None:
        """
        * operacion: el codigo de operacion usada en .procesar_operacion()
        * resultado: la tupla retornada por .procesar_operacion()

        codigos validos de operacion:
        * "s": sumar vectores
        * "r": restar vectores
        * "ve": multiplicar vector por escalar
        * "m": multiplicar vectores
        """

        limpiar_pantalla()
        if operacion not in ("s", "r", "ve", "m") or resultado == ():
            return None

        match operacion:
            case "s":   # ? sumar vectores
                vecs_seleccionados, vec_sumado = resultado
                vec1, vec2 = self.vecs_ingresados[vecs_seleccionados[0]], self.vecs_ingresados[vecs_seleccionados[1]]

                limpiar_pantalla()
                print("\nVectores seleccionados:")
                print("---------------------------------------------")
                print(f"{vecs_seleccionados[0]} = {vec1}")
                print(f"{vecs_seleccionados[1]} = {vec2}")
                print("---------------------------------------------")
                print(f"\n{vecs_seleccionados[0]} + {vecs_seleccionados[1]} = {vec_sumado}")

                input("\nPresione cualquier tecla para continuar...")
                return None

            case "r":   # ? restar vectore
                vecs_seleccionados, vec_restado = resultado
                vec1, vec2 = self.vecs_ingresados[vecs_seleccionados[0]], self.vecs_ingresados[vecs_seleccionados[1]]

                limpiar_pantalla()
                print("\nVectores seleccionados:")
                print("---------------------------------------------")
                print(f"{vecs_seleccionados[0]} = {vec1}")
                print(f"{vecs_seleccionados[1]} = {vec2}")
                print("---------------------------------------------")
                print(f"\n{vecs_seleccionados[0]} - {vecs_seleccionados[1]} = {vec_restado}")

                input("\nPresione cualquier tecla para continuar...")
                return None

            case "ve":  # ? multiplicar vector por escalar
                vec_seleccionado, escalar, vec_multiplicado = resultado
                vec = self.vecs_ingresados[vec_seleccionado]
                if escalar in (1, -1):
                    imprimir_escalar = ""
                elif Fraction(escalar).is_integer():
                    imprimir_escalar = str(escalar)
                else:
                    imprimir_escalar = f"({escalar}) * "

                limpiar_pantalla()
                print(f"\n{vec_seleccionado} = {vec}")
                print(f"\n{imprimir_escalar}{vec_seleccionado} = {vec_multiplicado}")

                input("\nPresione cualquier tecla para continuar...")
                return None

            case "m":   # ? multiplicar vectores
                vecs_seleccionados, vec_multiplicado = resultado
                vec1, vec2 = self.vecs_ingresados[vecs_seleccionados[0]], self.vecs_ingresados[vecs_seleccionados[1]]

                limpiar_pantalla()
                print("\nVectores seleccionados:")
                print("---------------------------------------------")
                print(f"{vecs_seleccionados[0]} = {vec1}")
                print(f"{vecs_seleccionados[1]} = {vec2}")
                print("---------------------------------------------")
                print(f"\n{vecs_seleccionados[0]}.{vecs_seleccionados[1]} = {vec_multiplicado}")

                input("\nPresione cualquier tecla para continuar...")
                return None
        return None

    @overload
    def seleccionar(self, operacion: str) -> str: ...

    @overload
    def seleccionar(self, operacion: None) -> List[str]: ...

    def seleccionar(self, operacion: Union[str, None]) -> Union[str, List[str]]:
        if operacion not in ("ve", "mv", None):
            return "" if operacion is not None else []

        elif not self._validar_vecs_ingresados():
            return "" if operacion is not None else []

        mensaje = self._get_mensaje(operacion)
        if operacion in ("ve", "mv"):
            input_vec = self._get_input(mensaje, operacion)
            try:
                self._validar_input_vec(input_vec)
            except KeyError as k:
                input(k)
                return ""
            return input_vec
        elif operacion is None:
            input_vecs = self._get_input(mensaje, operacion).split(",")
            try:
                self._validar_input_vecs(input_vecs)
            except (KeyError, ValueError, ArithmeticError) as e:
                input(e)
                return []
            return input_vecs
        return ""

    def _get_input(self, mensaje: str, operacion: Union[str, None]) -> str:
        limpiar_pantalla()
        self._mostrar_vectores()
        return input(mensaje).strip()

    def _get_mensaje(self, operacion: Union[str, None]) -> str:
        match operacion:
            case "ve":
                return "\n¿Cuál vector desea multiplicar por un escalar? "
            case "mv":
                return "\n¿Cuál vector desea multiplicar por una matriz? "
            case None:
                return "\n¿Cuáles vectores desea seleccionar? (separados por comas) "
            case _:
                return ""

    def _validar_input_vec(self, input_vec: str) -> None:
        if input_vec not in self.vecs_ingresados:
            raise KeyError(f"Error: El vector '{input_vec}' no existe!")

    def _validar_input_vecs(self, input_vecs: List[str]) -> None:
        vec = next((vec for vec in input_vecs if vec not in self.vecs_ingresados), None)
        if vec is not None:
            raise KeyError(f"Error: El vector '{vec}' no existe!")
        elif len(input_vecs) != 2:
            raise ValueError("Error: Debe seleccionar exactamente dos vectores!")
        vec1, vec2 = input_vecs
        if len(vec1) != len(vec2):
            raise ArithmeticError("Error: Los vectores deben tener la misma longitud!")

    def _validar_vecs_ingresados(self) -> bool:
        if self.vecs_ingresados == {}:
            print("\nNo hay vectores ingresados!")
            return False
        return True

    def _mostrar_vectores(self) -> None:
        limpiar_pantalla()
        if not self._validar_vecs_ingresados():
            return None

        print("\nVectores ingresados:")
        print("---------------------------------------------")
        for nombre, vec in self.vecs_ingresados.items():
            print(f"{nombre}: {vec}")
        print("---------------------------------------------")
        return None
