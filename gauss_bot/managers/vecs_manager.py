from fractions import Fraction
from typing import Union, overload

from gauss_bot.clases.vector import Vector
from gauss_bot.utils import limpiar_pantalla, match_input


class VectoresManager:
    """
    Se encarga de realizar pedir y guardar vectores, realizar operaciones y mostrar sus resultados
    """

    def __init__(self, vecs_ingresados: dict[str, Vector], parent=None) -> None:
        """
        * vecs_ingresadas: diccionario con vectores ingresados por el usuario
        * parent: el objeto que contiene a este manager
        """

        self.vecs_ingresados = vecs_ingresados
        self.parent = parent

        """
        codigos validos de operacion:
        * "s": sumar vectores
        * "r": restar vectores
        * "ve": multiplicar vector por escalar
        * "m": multiplicar vectores
        * "mv": multiplicar matriz por vector
        """
        self.ops_validas = ("s", "r", "ve", "m", "mv")
        self.ops_con_una = ("ve", "mv")
        self.ops_con_dos = ("s", "r", "m")

    def menu_vectores(self) -> None:
        """
        Le muestra el menú al usuario y se encarga de procesar y validar las opciones ingresadas.
        """

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

    def procesar_menu(self, opcion: int) -> None:
        """
        Recibe la opción retornada por menu_vectores() y la procesa.
        Se encarga de llamar a los métodos correspondientes para cada opción.
        """

        match opcion:
            case 1:
                self.agregar_vector()
                return
            case 2:
                self._mostrar_vectores()
            case 3:
                resultado = self.procesar_operacion("s")
                if resultado is not None:
                    self.mostrar_resultado("s", resultado)
                    return
            case 4:
                resultado = self.procesar_operacion("r")
                if resultado is not None:
                    self.mostrar_resultado("r", resultado)
                    return
            case 5:
                resultado = self.procesar_operacion("ve")
                if resultado is not None:
                    self.mostrar_resultado("ve", resultado)
                    return
            case 6:
                resultado = self.procesar_operacion("m")
                if resultado is not None:
                    self.mostrar_resultado("m", resultado)
                    return
            case 7:
                self.parent.producto_matriz_vector()
        input("Presione cualquier tecla para regresar al menú de vectores...")

    def agregar_vector(self) -> None:
        """
        Agrega el vector ingresado al diccionario de vectores ingresados.
        Llama a pedir_vector() para obtener los componentes del vector.
        """

        try:
            limpiar_pantalla()
            nombre = (
                input("\nIngrese el nombre del vector (una letra minúscula): ")
                .strip()
                .lower()
            )

            # validar nombre ingresado:
            if not nombre.isalpha() or len(nombre) != 1:
                raise NameError
            if nombre in self.vecs_ingresados:
                raise KeyError
            
            # convertir a int puede tirar ValueError
            longitud = int(input(f"¿Cuántas dimensiones tendrá el vector '{nombre}'? ").strip())
            if longitud <= 0:
                raise ArithmeticError

        except NameError:
            print("\nError: Ingrese solamente una letra minúscula!")
            input("Presione cualquier tecla para regresar al menú de vectores...")
            return
        except KeyError:
            print(f"\nError: Ya hay un vector con el nombre '{nombre}'!")
            input("Presione cualquier inputa para regresar al menú de vectores...")
            return
        except ValueError:
            print("\nError: Ingrese un número entero!")
            input("Presione cualquier tecla para regresar al menú de vectores...")
            return
        except ArithmeticError:
            print("\nError: Las dimensiones del vector deben ser un número entero positivo!")
            input("Presione cualquier tecla para regresar al menú de vectores...")
            return

        self.vecs_ingresados[nombre] = self.pedir_vector(nombre, longitud)
        print("\nVector agregado exitosamente!")

        ingresar_otro = match_input("\n¿Desea ingresar otro vector? (s/n) ")
        if ingresar_otro == 1:
            return self.agregar_vector()
        if ingresar_otro == 0:
            input("Presione cualquier tecla para regresar al menú de vectores...")
        else:
            input("Opción inválida!\nPresione cualquier tecla para regresar al menú de vectores...")

    def pedir_vector(self, nombre: str, longitud: int) -> Vector:
        """
        Se encarga de pedir y validar los componentes del vector.
        """

        try:
            limpiar_pantalla()
            componentes = [
                Fraction(x).limit_denominator(100) for x in
                input(f"Ingrese los componentes del vector '{nombre}' (separados por comas): ")
                .strip().split(",")
            ]

            if len(componentes) != longitud:
                raise TypeError

        except ValueError:
            input("\nError: Ingrese un número real!")
            print()
            return self.pedir_vector(nombre, longitud)
        except ZeroDivisionError:
            input("\nError: El denominador no puede ser cero!")
            print()
            return self.pedir_vector(nombre, longitud)
        except TypeError:
            input("\nError: El vector no tiene las dimensiones correctas!")
            print()
            return self.pedir_vector(nombre, longitud)
        return Vector(componentes)

    def procesar_operacion(self, operacion: str) -> tuple:
        """
        Recibe un código de operación, selecciona los vectores necesarios
        para esa operación, y retorna una tupla con el resultado.

        Códigos válidos de operación:
        * "s": sumar vectores
        * "r": restar vectores
        * "ve": multiplicar vector por escalar
        * "m": multiplicar vectores
        """

        limpiar_pantalla()
        if operacion not in self.ops_validas or not self._validar_vecs_ingresados():
            return ()

        if operacion in self.ops_con_una:
            nombres_vecs = self.seleccionar(None)

            # si hubo un error en seleccionar():
            if nombres_vecs == []:
                return ()

            vec1, vec2 = (
                self.vecs_ingresados[nombres_vecs[0]],
                self.vecs_ingresados[nombres_vecs[1]],
            )

            # retornar vectores seleccionados y resultado de operacion:
            match operacion:
                case "s":  # ? suma
                    return (nombres_vecs, vec1 + vec2)
                case "r":  # ? resta
                    return (nombres_vecs, vec1 - vec2)
                case "m":  # ? multiplicacion
                    return (nombres_vecs, vec1 * vec2)

        elif operacion == "ve":
            nombre_vec = self.seleccionar(operacion)

            # si hubo un error en seleccionar():
            if nombre_vec == "":
                return ()

            # validar input del escalar:
            try:
                escalar = Fraction(
                    input("Ingrese el escalar: ").strip()
                ).limit_denominator(100)
            except ValueError:
                input("Error: Ingrese un número real!")
                return ()
            except ZeroDivisionError:
                input("Error: El denominador no puede ser cero!")
                return ()
            vec_seleccionado = self.vecs_ingresados[nombre_vec]
            return (nombre_vec, escalar, vec_seleccionado * escalar)
        return ()

    def mostrar_resultado(self, operacion: str, resultado: tuple) -> None:
        """
        Recibe el código de operación recibido por procesar_operacion(),
        y la tupla retornada por el.

        Códigos válidos de operación:
        * "s": sumar vectores
        * "r": restar vectores
        * "ve": multiplicar vector por escalar
        * "m": multiplicar vectores
        """

        limpiar_pantalla()
        if operacion not in self.ops_validas or resultado == ():
            return

        # manejar operaciones con dos vectores:
        if operacion in self.ops_con_dos:
            vecs_seleccionados, vec_resultante = resultado
            vec1, vec2 = (
                self.vecs_ingresados[vecs_seleccionados[0]],
                self.vecs_ingresados[vecs_seleccionados[1]],
            )

            limpiar_pantalla()
            print("\nVectores seleccionados:")
            print("---------------------------------------------")
            print(f"{vecs_seleccionados[0]} = {vec1}")
            print(f"{vecs_seleccionados[1]} = {vec2}")
            print("---------------------------------------------")

            match operacion:
                case "s":
                    print(f"\n{vecs_seleccionados[0]} + {vecs_seleccionados[1]} = {vec_resultante}")
                case "r":
                    print(f"\n{vecs_seleccionados[0]} - {vecs_seleccionados[1]} = {vec_resultante}")
                case "m":
                    print(f"\n{vecs_seleccionados[0]}.{vecs_seleccionados[1]} = {vec_resultante}")

        elif operacion == "ve":  # ? multiplicar vector por escalar
            vec_seleccionado, escalar, vec_resultante = resultado
            vec = self.vecs_ingresados[vec_seleccionado]
            if escalar in (1, -1):
                imprimir_escalar = ""
            elif Fraction(escalar).is_integer():
                imprimir_escalar = str(escalar)
            else:
                imprimir_escalar = f"({escalar}) * "

            limpiar_pantalla()
            print(f"\n{vec_seleccionado} = {vec}")
            print(f"\n{imprimir_escalar}{vec_seleccionado} = {vec_resultante}")

        input("\nPresione cualquier tecla para continuar...")

    @overload
    def seleccionar(self, operacion: str) -> str: ...

    @overload
    def seleccionar(self, operacion: None) -> list[str]: ...

    def seleccionar(self, operacion: Union[str, None]) -> Union[str, list[str]]:
        """
        Pide la matriz a seleccionar para realizar la operación dada.
        Overloads para seleccionar uno o dos vectores. Usa _validar_input_vec()
        y _validar_input_vecs() para validar si los vectores seleccionados son
        válidos para la operación a realizar.
        """

        if operacion not in ("ve", "mv", None):
            return "" if operacion is not None else []

        if not self._validar_vecs_ingresados():
            return "" if operacion is not None else []

        mensaje = self._get_mensaje(operacion)
        if operacion in ("ve", "mv"):
            input_vec = self._get_input(mensaje)
            try:
                self._validar_input_vec(input_vec)
            except KeyError as k:
                print(k)
                input("Presione cualquier tecla para regresar al menú de vectores...")
                return ""
            return input_vec
        if operacion is None:
            input_vecs = self._get_input(mensaje).split(",")
            try:
                self._validar_input_vecs(input_vecs)
            except (KeyError, ValueError, ArithmeticError) as e:
                print(e)
                input("Presione cualquier tecla para regresar al menú de vectores...")
                return []
            return input_vecs
        return ""

    def _get_mensaje(self, operacion: Union[str, None]) -> str:
        """
        Helper method usado en seleccionar() para imprimir un
        mensaje apropiado para la operación a realizar.
        """

        match operacion:
            case "ve":
                return "\n¿Cuál vector desea multiplicar por un escalar? "
            case "mv":
                return "\n¿Cuál vector desea multiplicar por una matriz? "
            case None:
                return "\n¿Cuáles vectores desea seleccionar? (separados por comas) "
            case _:
                return ""

    def _get_input(self, mensaje: str) -> str:
        """
        Muestra los vectores ingresados y retorna el input del usuario.
        """

        limpiar_pantalla()
        self._mostrar_vectores()
        return input(mensaje).strip()

    def _validar_input_vec(self, input_vec: str) -> None:
        """
        Valida el vector seleccionado por el usuario.
        * KeyError: si el vector no existe en vecs_ingresados
        """

        if input_vec not in self.vecs_ingresados:
            raise KeyError(f"Error: El vector '{input_vec}' no existe!")

    def _validar_input_vecs(self, input_vecs: list[str]) -> None:
        """
        Valida los vectores seleccionados por el usuario.
        * KeyError: si uno de los vectores seleccionados no existe
        * ValueError: si no se seleccionan dos vectores
        * ArithmeticError: si los vectores no tienen las mismas dimensiones
        """

        vec = next((vec for vec in input_vecs if vec not in self.vecs_ingresados), None)
        if vec is not None:
            raise KeyError(f"Error: El vector '{vec}' no existe!")
        if len(input_vecs) != 2:
            raise ValueError("Error: Debe seleccionar exactamente dos vectores!")
        vec1, vec2 = input_vecs
        if len(vec1) != len(vec2):
            raise ArithmeticError("Error: Los vectores deben tener la misma longitud!")

    def _validar_vecs_ingresados(self) -> bool:
        """
        Valida si el diccionario de vectores ingresados esta vacío o no.
        """

        if self.vecs_ingresados == {}:
            print("\nNo hay vectores ingresados!")
            return False
        return True

    def _mostrar_vectores(self) -> None:
        """
        Imprime los vectores ingresados por el usuario.
        """

        limpiar_pantalla()
        if not self._validar_vecs_ingresados():
            return

        print("\nVectores ingresados:")
        print("---------------------------------------------")
        for nombre, vec in self.vecs_ingresados.items():
            print(f"{nombre}: {vec}")
        print("---------------------------------------------")
        return
