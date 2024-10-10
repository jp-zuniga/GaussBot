from fractions import Fraction
from typing import Tuple, List, Dict, overload
from copy import deepcopy

from gauss_bot.clases.matriz import Matriz
from gauss_bot.clases.vector import Vector
from gauss_bot.clases.sistema_ecuaciones import SistemaEcuaciones
from gauss_bot.utils import limpiar_pantalla, match_input

DictMatrices = Dict[str, Matriz]
DictVectores = Dict[str, Vector]

class MatricesManager:
    def __init__(self, mats_ingresadas: DictMatrices = {}):
        self.mats_ingresadas = mats_ingresadas

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

        ingresar_otra = match_input("¿Se ingresará una matriz aumentada? (s/n) ")
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

    # TODO: mejorar esta mierda
    def procesar_operacion(self, operacion: str):
        """
        "m": multiplicar matrices
        "s": sumar matrices
        "r": restar matrices
        "t": transponer matriz
        "se": resolver sistema de ecuaciones
        """

        if operacion not in ("m", "s", "r", "t", "se"):
            return None

        if operacion == "m" or operacion == "s" or operacion == "r":
            nombres_mats = self.seleccionar(None)
            mat1, mat2 = self.mats_ingresadas[nombres_mats[0]], self.mats_ingresadas[nombres_mats[1]]
            match operacion:
                case "m":
                    mat_resultante = mat1 * mat2
                case "s":
                    mat_resultante = mat1 + mat2
                case "r":
                    mat_resultante = mat1 - mat2
            return (nombres_mats, mat_resultante)

        elif operacion == "t" or operacion == "se":
            nombre_mat = self.seleccionar(operacion)
            mat_copia = deepcopy(self.mats_ingresadas[nombre_mat])
            match operacion:
                case "t":
                    nombre_mat_modded = f"{nombre_mat}_t"
                    mat_copia_modded = mat_copia.transponer()

                    if nombre_mat_modded not in self.mats_ingresadas.keys():
                        self.mats_ingresadas[nombre_mat_modded] = mat_copia_modded
                    return (nombre_mat, mat_copia_modded)
                case "se":
                    nombre_mat_modded = f"{nombre_mat}_r"
                    resolver = SistemaEcuaciones(mat_copia)
                    resolver.resolver_sistema()
                    respuesta, procedimiento, mat_copia_modded = resolver.respuesta, resolver.procedimiento, resolver.matriz

                    if nombre_mat_modded not in self.mats_ingresadas.keys():
                        self.mats_ingresadas[nombre_mat_modded] = mat_copia_modded
                    return (respuesta, procedimiento, mat_copia_modded)

    @overload
    def seleccionar(self, operacion: str) -> str: ...

    @overload
    def seleccionar(self, operacion: None) -> List[str]: ...

    def seleccionar(self, operacion: str | None) -> str | List[str]:
        if operacion not in ("t", "se", None):
            return "" if operacion else []

        if not self._validar_mats_ingresadas():
            return "" if operacion else []

        if operacion:
            mensaje = self._get_mensaje(operacion)
            input_mat = self._get_input(mensaje)
            try:
                self._validate_input_mat(input_mat, operacion)
            except (KeyError, TypeError) as e:
                input(e)
                return self.seleccionar(operacion)
            return input_mat

        else:
            mensaje = "\n¿Cuáles matrices desea seleccionar? (separadas por comas) "
            input_mats = self._get_input(mensaje).split(",")
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

    def _get_input(self, mensaje: str) -> str:
        limpiar_pantalla()
        self._imprimir_matrices()
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

    def _imprimir_matrices(self) -> None:
        if not self._validar_mats_ingresadas():
            return None

        print("\nMatrices guardadas:")
        print("---------------------------------------------", end="")
        for nombre, mat in self.mats_ingresadas.items():
            print(f"\n{nombre}:")
            print(mat)
        print("---------------------------------------------")

        return None


class VectoresManager: ...

class OpsManager:
    def __init__(self, manager_mats: MatricesManager, manager_vecs: VectoresManager) -> None:
        self.manager_mats = manager_mats
        self.manager_vecs = manager_vecs

    def start(self) -> None:
        option = self.menu_operaciones()
        while option != 7:
            match option:
                case 1:  # agregar
                    self.manager_mats.agregar_matriz()
                    option = self.menu_operaciones()
                    continue
                case 2:  # resolver sistema de ecuaciones
                    respuesta, procedimiento, mat_resultante = self.manager_mats.procesar_operacion("se")
                    print("\n---------------------------------------------")
                    print("\nSistema de ecuaciones resuelto:")
                    print(mat_resultante)
                    print(respuesta)

                    print("\n---------------------------------------------")
                    mostrar_procedimiento = match_input("\n¿Desea ver el procedimiento? (s/n) ")
                    if mostrar_procedimiento:
                        limpiar_pantalla()
                        print(procedimiento)
                        print(respuesta)
                    elif not mostrar_procedimiento:
                        print("\nDe acuerdo!")
                    else:
                        print("\nOpción inválida!")

                    resolver_otra = match_input("¿Desea resolver otra matriz? (s/n) ")
                    if resolver_otra:
                        continue
                    elif not resolver_otra:
                        input("De acuerdo! Regresando al menú de matrices...")
                    else:
                        input("Opción inválida! Regresando al menú de matrices...")

                    option = self.menu_operaciones()
                    continue
                case 3:  # sumar matrices
                    mats_seleccionadas, resultado = self.manager_mats.procesar_operacion("s")
                    mat1, mat2 = self.manager_mats.mats_ingresadas[mats_seleccionadas[0]], self.manager_mats.mats_ingresadas[mats_seleccionadas[1]]

                    limpiar_pantalla()
                    print(f"\n{mats_seleccionadas[0]}:")
                    print(mat1)
                    print(f"\n{mats_seleccionadas[1]}:")
                    print(mat2)
                    print(f"\n{mats_seleccionadas[0]} + {mats_seleccionadas[1]}:")
                    print(resultado)

                    input("\nPresione cualquier tecla para continuar...")
                    option = self.menu_operaciones()
                    continue
                case 4:  # restar matrices
                    mats_seleccionadas, resultado = self.manager_mats.procesar_operacion("r")
                    mat1, mat2 = self.manager_mats.mats_ingresadas[mats_seleccionadas[0]], self.manager_mats.mats_ingresadas[mats_seleccionadas[1]]

                    limpiar_pantalla()
                    print(f"\n{mats_seleccionadas[0]}:")
                    print(mat1)
                    print(f"\n{mats_seleccionadas[1]}:")
                    print(mat2)
                    print(f"\n{mats_seleccionadas[0]} - {mats_seleccionadas[1]}:")
                    print(resultado)

                    input("\nPresione cualquier tecla para continuar...")
                    option = self.menu_operaciones()
                    continue
                case 5:  # multiplicar matrices
                    mats_seleccionadas, resultado = self.manager_mats.procesar_operacion("m")
                    mat1, mat2 = self.manager_mats.mats_ingresadas[mats_seleccionadas[0]], self.manager_mats.mats_ingresadas[mats_seleccionadas[1]]

                    limpiar_pantalla()
                    print(f"\n{mats_seleccionadas[0]}:")
                    print(mat1)
                    print(f"\n{mats_seleccionadas[1]}:")
                    print(mat2)
                    print(f"\n{mats_seleccionadas[0]} * {mats_seleccionadas[1]}:")
                    print(resultado)

                    input("\nPresione cualquier tecla para continuar...")
                    option = self.menu_operaciones()
                    continue
                case 6:  # transponer matriz
                    mat_seleccionada, resultado = self.manager_mats.procesar_operacion("t")
                    mat_original = self.manager_mats.mats_ingresadas[mat_seleccionada]

                    limpiar_pantalla()
                    print(f"\n{mat_seleccionada}:")
                    print(mat_original)
                    print(f"\n{mat_seleccionada}_t:")
                    print(resultado)

                    input("\nPresione cualquier tecla para continuar...")
                    option = self.menu_operaciones()
                    continue
                case 7:
                    input("Regresando al menú principal...")
                    break
                case _:
                    input("Opción inválida! Por favor, intente de nuevo...")
                    continue
        return None

    def menu_operaciones(self) -> int:
        limpiar_pantalla()
        print("\n###########################")
        print("### Menú de Operaciones ###")
        print("###########################")
        self.manager_mats._imprimir_matrices()
        print("\n1. Agregar una matriz")
        print("2. Agregar un vector\n")
        print("3. Mostrar matrices")
        print("4. Mostrar vectores\n")
        print("5. Resolver sistema de ecuaciones")
        print("6. Sumar matrices")
        print("7. Restar matrices")
        print("8. Multiplicar matriz por escalar")
        print("9. Multiplicar matrices")
        print("10. Transponer matriz\n")
        print("11. Sumar vectores")
        print("12. Restar vectores")
        print("13. Multiplicar vector por escalar")
        print("14. Multiplicar vectores")
        print("\n15. Multiplicar matriz por vector")
        print("\n16. Regresar al menú principal")
        try:
            option = int(input("\nSeleccione una opción: ").strip())
            if option < 1 or option > 16:
                raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.menu_operaciones()
        return option
