from fractions import Fraction
from copy import deepcopy
from typing import Tuple, List, overload

from gauss_bot.clases.matriz import Matriz, DictMatrices
from gauss_bot.clases.sistema_ecuaciones import SistemaEcuaciones
from gauss_bot.utils import limpiar_pantalla, match_input

class MatricesManager:
    def __init__(self, mats_ingresadas: DictMatrices = {}) -> None:
        self.mats_ingresadas = mats_ingresadas

    def menu_matrices(self) -> None:
        while True:
            limpiar_pantalla()
            print("\n###############################")
            print("### Operaciones de Matrices ###")
            print("###############################")
            print("\n1. Agregar una matriz")
            print("2. Mostrar matrices\n")
            print("3. Resolver sistema de ecuaciones")
            print("4. Sumar matrices")
            print("5. Restar matrices")
            print("6. Multiplicar matriz por escalar")
            print("7. Multiplicar matrices")
            print("8. Multiplicar matriz por vector")
            print("9. Transponer matriz")
            print("10. Regresar al menú principal")
            try:
                option = int(input("\n=> Seleccione una opción: ").strip())
                if option < 1 or option > 10:
                    raise ValueError
            except ValueError:
                input("\nError: Ingrese una opción válida!")
                continue
            if option == 10:
                input("Regresando a menú principal...")
                break
            self.procesar_menu(option)
        return None

    def procesar_menu(self, opcion: int) -> None:
        match opcion:
            case 1:
                self.agregar_matriz()
            case 2:
                self._mostrar_matrices(necesita_aumentada = -1)
            case 3:
                self.procesar_operacion("se")
            case 4:
                self.procesar_operacion("s")
            case 5:
                self.procesar_operacion("r")
            case 6:
                self.procesar_operacion("me")
            case 7:
                self.procesar_operacion("m")
            case 8:
                ...  # TODO: producto matriz-vector
            case 9:
                self.procesar_operacion("t")
        return None

    def agregar_matriz(self) -> None:
        try:
            limpiar_pantalla()
            nombre = input("\nIngrese el nombre de la matriz (una letra mayúscula): ").strip().upper()
            if not nombre.isalpha() or len(nombre) != 1:
                raise NameError("Error: Ingrese solamente una letra mayúscula!")
            if nombre in self.mats_ingresadas:
                raise KeyError(f"Error: Ya hay una matriz con el nombre {nombre}!")

            ingresar_aumentada = match_input("¿Se ingresará una matriz aumentada? (s/n) ")
            if ingresar_aumentada:
                es_aumentada = True
            elif not ingresar_aumentada:
                es_aumentada = False
            else:
                raise ValueError("Error: Ingrese una opción válida!")

        except NameError as n:
            input(n)
            return self.agregar_matriz()
        except KeyError as k:
            input(k)
            return self.agregar_matriz()
        except ValueError as v:
            input(v)
            return self.agregar_matriz()

        self.mats_ingresadas[nombre] = self.pedir_matriz(nombre, es_aumentada)
        print("\nMatriz agregada exitosamente!")
        ingresar_otra = match_input("¿Desea ingresar otra matriz? (s/n) ")
        if ingresar_otra:
            return self.agregar_matriz()
        elif not ingresar_otra:
            input("Regresando al menú de matrices...")
        else:
            input("Opción inválida! Regresando al menú de matrices...")
        return None

    def pedir_matriz(self, nombre="M", es_aumentada=True) -> Matriz:
        valores = []
        filas, columnas = self.pedir_dimensiones(nombre, es_aumentada)

        fila_actual = 0
        if es_aumentada:
            columnas += 1

        while fila_actual < filas:
            columna_actual = 0
            fila = []
            print(f"\nFila {fila_actual+1}:")
            while columna_actual < columnas:
                try:
                    if not es_aumentada or columna_actual != columnas - 1:
                        dato_a_pedir = f"-> X{columna_actual+1} = "
                    else:
                        dato_a_pedir = "-> b = "
                    elemento = Fraction(input(dato_a_pedir).strip()).limit_denominator(100)
                    fila.append(elemento)
                    columna_actual += 1

                except ValueError:
                    input("\nError: Ingrese un número real!")
                    print()
                except ZeroDivisionError:
                    input("\nError: El denominador no puede ser cero!")
                    print()

            fila_actual += 1
            valores.append(fila)

        mat = Matriz(es_aumentada, filas, columnas, valores)
        return mat

    def pedir_dimensiones(self, nombre: str, es_aumentada: bool) -> Tuple[int, int]:
            palabras = ["ecuaciones", "variables"] if es_aumentada else ["filas", "columnas"]
            try:
                print(f"\nDatos de matriz {nombre}:")
                print("----------------------------")
                filas = int(input(f"Ingrese el número de {palabras[0]}: "))
                if filas <= 0:
                    raise ValueError("Error: Ingrese un número entero positivo!")
                columnas = int(input(f"Ingrese el número de {palabras[1]}: "))
                if columnas <= 0:
                    raise ValueError("Error: Ingrese un número entero positivo!")
            except ValueError as v:
                input(v)
                return self.pedir_dimensiones(nombre, es_aumentada)
            return (filas, columnas)

    def procesar_operacion(self, operacion: str):
        """
        ? operacion:
        * "se": resolver sistema de ecuaciones
        * "m": multiplicar matrices
        * "s": sumar matrices
        * "r": restar matrices
        * "t": transponer matriz
        """

        if operacion not in ("se", "s", "r", "me", "m", "t"):
            return None

        if operacion in ("s", "r", "m"):
            nombres_mats = self.seleccionar(None)
            mat1, mat2 = self.mats_ingresadas[nombres_mats[0]], self.mats_ingresadas[nombres_mats[1]]
            match operacion:
                case "s":
                    return (nombres_mats, mat1 + mat2)
                case "r":
                    return (nombres_mats, mat1 - mat2)
                case "m":
                    return (nombres_mats, mat1 * mat2)

        elif operacion in ("se", "me", "t"):
            nombre_mat = self.seleccionar(operacion)
            mat_copia = deepcopy(self.mats_ingresadas[nombre_mat])
            match operacion:
                case "se":
                    nombre_mat_modded = f"{nombre_mat}_r"
                    resolver = SistemaEcuaciones(mat_copia)
                    resolver.resolver_sistema()
                    respuesta, procedimiento, mat_copia_modded = resolver.respuesta, resolver.procedimiento, resolver.matriz

                    if nombre_mat_modded not in self.mats_ingresadas.keys():
                        self.mats_ingresadas[nombre_mat_modded] = mat_copia_modded
                    return (respuesta, procedimiento, mat_copia_modded)
                case "me":
                    escalar = Fraction(input("Ingrese el escalar: ").strip())
                    return (nombre_mat, mat_copia * escalar)
                case "t":
                    nombre_mat_modded = f"{nombre_mat}_t"
                    mat_copia_modded = mat_copia.transponer()

                    if nombre_mat_modded not in self.mats_ingresadas.keys():
                        self.mats_ingresadas[nombre_mat_modded] = mat_copia_modded
                    return (nombre_mat, mat_copia_modded)

    @overload
    def seleccionar(self, operacion: str) -> str: ...

    @overload
    def seleccionar(self, operacion: None) -> List[str]: ...

    def seleccionar(self, operacion: str | None) -> str | List[str]:
        if operacion not in ("t", "se", None):
            return "" if operacion else []

        if not self._validar_mats_ingresadas():
            return "" if operacion else []

        if operacion is not None:
            mensaje = self._get_mensaje(operacion)
            input_mat = self._get_input(mensaje, operacion)
            try:
                self._validate_input_mat(input_mat, operacion)
            except (KeyError, TypeError) as e:
                input(e)
                return self.seleccionar(operacion)
            return input_mat

        else:
            mensaje = "\n¿Cuáles matrices desea seleccionar? (separadas por comas) "
            input_mats = self._get_input(mensaje, operacion).split(",")
            try:
                self._validate_input_mats(input_mats)
            except (KeyError, ArithmeticError) as e:
                input(e)
                return self.seleccionar(None)
            return input_mats

    def _get_mensaje(self, operacion: str) -> str:
        match operacion:
            case "se":
                return "\n¿Cuál matriz desea resolver? "
            case "t":
                return "\n¿Cuál matriz desea transponer? "
            case _:
                return ""

    def _get_input(self, mensaje: str, operacion: str | None) -> str:
        limpiar_pantalla()
        necesita_aumentada = operacion == "se"
        self._mostrar_matrices(necesita_aumentada)
        return input(mensaje).strip()

    def _validate_input_mat(self, input_mat: str, operacion: str) -> None:
        if input_mat not in self.mats_ingresadas:
            raise KeyError(f"Error: La matriz {input_mat} no existe!")
        elif operacion == "se" and not self.mats_ingresadas[input_mat][1]:
            raise TypeError("Error: La matriz seleccionada no es aumentada!")

    def _validate_input_mats(self, input_mats: List[str]) -> None:
        mat = next((mat for mat in input_mats if mat not in self.mats_ingresadas), None)
        if mat is not None:
            raise KeyError(f"Error: La matriz {mat} no existe!")
        elif len(input_mats) != 2:
            raise ArithmeticError("Error: Debe seleccionar dos matrices!")

    def _validar_mats_ingresadas(self) -> bool:
        if self.mats_ingresadas == {}:
            input("\nNo hay matrices ingresadas!")
            return False
        return True

    def _mostrar_matrices(self, necesita_aumentada: int) -> None:
        """
        ? necesita_aumentada:
        *  1: necesita que la matriz sea aumentada
        *  0: no necesita que la matriz sea aumentada
        * -1: no importa que sea aumentada o no (mostrar todas)
        """

        if not self._validar_mats_ingresadas() or necesita_aumentada not in (1, 0, -1):
            return None

        print("\nMatrices guardadas:")
        print("---------------------------------------------")
        for nombre, mat in self.mats_ingresadas.items():
            if (necesita_aumentada == 1 and not mat.aumentada) or (necesita_aumentada == 0 and mat.aumentada):
                continue
            print(f"\n{nombre}:")
            print(mat)
        print("---------------------------------------------")

        input("\nPresione cualquier tecla para regresar al menú de matrices...")
        return None
