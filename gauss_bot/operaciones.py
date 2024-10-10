from fractions import Fraction
from typing import Tuple, List, Dict, overload
from copy import deepcopy

from .clases.matriz import Matriz
from .clases.vector import Vector
from .clases.sistema_ecuaciones import SistemaEcuaciones
from .utils import limpiar_pantalla, match_input

DictMatrices = Dict[str, Matriz]
DictVectores = Dict[str, Vector]

# TODO: mejorar .procesar_operacion() en MatricesManager y VectoresManager
# TODO implementer producto matriz-vector en ambos menus

class MatricesManager:
    def __init__(self, vec_manager: "VectoresManager", mats_ingresadas: DictMatrices = {}) -> None:
        self.vec_manager = vec_manager
        self.mats_ingresadas = mats_ingresadas

    def menu_matrices(self) -> None:
        while True:
            limpiar_pantalla()
            print("\n###########################")
            print("### Operaciones de Matrices ###")
            print("###########################")
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
                self._imprimir_matrices(necesita_aumentada = -1)
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
        * "mv": multiplicar matriz por vector
        """

        if operacion not in ("se", "s", "r", "me", "m", "t", "mv"):
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
        
        elif operacion == "mv":
            ...  # TODO: producto matriz-vector

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
        self._imprimir_matrices(necesita_aumentada)
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

    def _imprimir_matrices(self, necesita_aumentada: int) -> None:
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

        return None


class VectoresManager:
    def __init__(self, mat_manager: MatricesManager, vecs_ingresados: DictVectores = {}) -> None:
        self.mat_manager = mat_manager
        self.vecs_ingresados = vecs_ingresados

    def menu_vectores(self) -> None:
        while True:
            limpiar_pantalla()
            print("\n###########################")
            print("### Operaciones de Vectores ###")
            print("###########################")
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
                self._imprimir_vectores()
            case 3:
                self.procesar_operacion("s")
            case 4:
                self.procesar_operacion("r")
            case 5:
                self.procesar_operacion("ve")
            case 6:
                self.procesar_operacion("m")
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
        ? operacion:
        * "s": sumar vectores
        * "r": restar vectores
        * "ve": multiplicar vector por escalar
        * "m": multiplicar vectores
        * "mv": multiplicar matriz por vector
        """

        if operacion not in ("s", "r", "ve", "m", "mv"):
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
        elif operacion == "mv":
            ...  # TODO: producto matriz-vector

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
        self._imprimir_vectores()
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

    def _imprimir_vectores(self, es_matricial=False) -> None:
        if not self._validar_vecs_ingresados():
            return None

        mensaje = "seleccionados" if es_matricial else "ingresados"
        print(f"\nVectores {mensaje}:")
        print("---------------------------------------------")
        for nombre, vec in self.vecs_ingresados.items():
            print(f"{nombre}: {vec}")
        print("---------------------------------------------")

        return None


class OpsManager:
    def __init__(self, mat_manager: MatricesManager, vec_manager: VectoresManager) -> None:
        self.mat_manager = mat_manager
        self.vec_manager = vec_manager

    def start_exec_loop(self) -> None:
        while True:
            option = self.main_menu()
            match option:
                case 1:
                    self.mat_manager._imprimir_matrices(necesita_aumentada = -1)
                case 2: ...
                    # self.vec_manager._imprimir_vectores()
                case 3:
                    self.mat_manager.menu_matrices()
                case 4:
                    self.vec_manager.menu_vectores()
                case 5:
                    input("Cerrando programa...")
                    break
        return None

    def main_menu(self) -> int:
        limpiar_pantalla()
        print("\n################")
        print("### GaussBot ###")
        print("################\n")
        print("1. Mostrar matrices")
        print("2. Mostrar vectores")
        print("3. Operaciones de matrices")
        print("4. Operaciones de vectores")
        print("5. Cerrar programa")
        try:
            option = int(input("\n=> Seleccione una opción: ").strip())
            if option < 1 or option > 5:
                raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.main_menu()
        return option
