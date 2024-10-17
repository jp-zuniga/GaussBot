from copy import deepcopy
from fractions import Fraction

from gauss_bot.clases.matriz import Matriz
from gauss_bot.clases.sistema_ecuaciones import SistemaEcuaciones
from gauss_bot.utils import limpiar_pantalla, match_input


class MatricesManager:
    """
    Se encarga de realizar pedir y guardar matrices, realizar operaciones y mostrar sus resultados
    """

    def __init__(self, mats_ingresadas: dict[str, Matriz], parent=None) -> None:
        """
        * mats_ingresadas: diccionario con matrices ingresadas por el usuario
        * parent: el objeto que contiene a este manager
        """

        self.mats_ingresadas = mats_ingresadas
        self.parent = parent

        """
        operaciones implementadas:
        * "se": resolver sistema de ecuaciones
        * "s": sumar matrices
        * "r": restar matrices
        * "me": multiplicar matriz por escalar
        * "m": multiplicar matrices
        * "me": multiplicar matriz por vector (implementada en OpsManager)
        * "t": transponer matriz
        * "d": calcular determinante
        """
        self.ops_validas = ("se", "s", "r", "me", "m", "mv", "t", "d", "i")
        self.ops_con_una = ("se", "me", "mv", "t", "d", "i")
        self.ops_con_dos = ("s", "r", "m")

    def menu_matrices(self) -> None:
        """
        Le muestra el menú al usuario y se encarga de procesar y validar las opciones ingresadas.
        """

        while True:
            limpiar_pantalla()
            print("\n###############################")
            print("### Operaciones de Matrices ###")
            print("###############################")
            print("\n1. Agregar una matriz")
            print("2. Mostrar matrices\n")
            print("3. Resolver sistema por el método de Gauss-Jordan")
            print("4. Resolver sistema con la Regla de Cramer\n")
            print("5. Sumar matrices")
            print("6. Restar matrices")
            print("7. Multiplicar matriz por escalar")
            print("8. Multiplicar matrices")
            print("9. Multiplicar matriz por vector")
            print("10. Transponer matriz")
            print("11. Calcular determinante de una matriz")
            print("12. Encontrar la inversa una matriz\n")
            print("13. Regresar al menú principal")
            try:
                option = int(input("\n=> Seleccione una opción: ").strip())
                if option < 1 or option > 13:
                    raise ValueError
            except ValueError:
                input("=> Error: Ingrese una opción válida!")
                continue
            if option == 13:
                input("=> Regresando a menú principal...")
                break
            self.procesar_menu(option)

    def procesar_menu(self, opcion: int) -> None:
        """
        Recibe la opción retornada por menu_matrices() y la procesa.
        Se encarga de llamar a los métodos correspondientes para cada opción.
        """

        match opcion:
            case 1:
                self.agregar_matriz()
                return
            case 2:
                limpiar_pantalla()
                print(self.mostrar_matrices(necesita_aumentada=-1))
            case 3:
                resultado = self.procesar_operacion("se")
                if resultado != ():
                    self.mostrar_resultado("se", resultado)
                    return
            case 4:
                nombre_mat = self.seleccionar_mat("se")
                if nombre_mat == "":
                    return

                mat_seleccionada = self.mats_ingresadas[nombre_mat]
                try:
                    mat_seleccionada.resolver_cramer(nombre_mat)
                    input("\nPresione cualquier tecla para regresar al menú de matrices...")
                    return
                except (TypeError, ArithmeticError) as e:
                    print(e)
                except ValueError as v:
                    print("\n" + str(v))
                    resolver_gauss = match_input("\n¿Desea encontrar la solución con el método Gauss-Jordan? (s/n) ")
                    if resolver_gauss == 1:
                        mat_copia = deepcopy(mat_seleccionada)
                        sistema = SistemaEcuaciones(mat_copia)
                        sistema.resolver_sistema()
                        self.mostrar_resultado("se", (nombre_mat, sistema))
                        if not any(sistema.matriz == mat for mat in self.mats_ingresadas.values()):
                            self.mats_ingresadas[f"{nombre_mat}_r"] = sistema.matriz
                        return
                    elif resolver_gauss == 0:
                        print("\nDe acuerdo!")
                    else:
                        print("\nOpción inválida!")
            case 5:
                resultado = self.procesar_operacion("s")
                if resultado != ():
                    self.mostrar_resultado("s", resultado)
                    return
            case 6:
                resultado = self.procesar_operacion("r")
                if resultado != ():
                    self.mostrar_resultado("r", resultado)
                    return
            case 7:
                resultado = self.procesar_operacion("me")
                if resultado != ():
                    self.mostrar_resultado("me", resultado)
                    return
            case 8:
                resultado = self.procesar_operacion("m")
                if resultado != ():
                    self.mostrar_resultado("m", resultado)
                    return
            case 9:
                self.parent.producto_matriz_vector()
            case 10:
                resultado = self.procesar_operacion("t")
                if resultado != ():
                    self.mostrar_resultado("t", resultado)
                    return
            case 11:
                resultado = self.procesar_operacion("d")
                if resultado != ():
                    self.mostrar_resultado("d", resultado)
                    return
            case 12:
                resultado = self.procesar_operacion("i")
                if resultado != ():
                    self.mostrar_resultado("i", resultado)
                    return
        input("Presione cualquier tecla para regresar al menú de matrices...")

    def agregar_matriz(self) -> None:
        """
        Agrega la matriz ingresada al diccionario de matrices ingresadas.
        Llama a pedir_matriz() para recibir los datos.
        """

        try:
            limpiar_pantalla()
            nombre = (
                input("\nIngrese el nombre de la matriz (una letra mayúscula): ")
                .strip()
                .upper()
            )

            # validar nombre ingresado:
            if not nombre.isalpha() or len(nombre) != 1:
                raise NameError
            if nombre in self.mats_ingresadas:
                raise KeyError

            ingresar_aumentada = match_input(
                "¿Se ingresará una matriz aumentada? (s/n) "
            )

            if ingresar_aumentada == 1:
                es_aumentada = True
            elif ingresar_aumentada == 0:
                es_aumentada = False
            else:
                raise ValueError

        except NameError:
            input("Error: Ingrese solamente una letra mayúscula!")
            return
        except KeyError:
            input(f"Error: Ya hay una matriz con el nombre '{nombre}'!")
            return
        except ValueError:
            input("Error: Ingrese una opción válida!")
            return

        self.mats_ingresadas[nombre] = self.pedir_matriz(nombre, es_aumentada)
        print("\nMatriz agregada exitosamente!")

        ingresar_otra = match_input("¿Desea ingresar otra matriz? (s/n) ")
        if ingresar_otra == 1:
            return self.agregar_matriz()
        if ingresar_otra == 0:
            input("\nPresione cualquier tecla para regresar al menú de matrices...")
        else:
            print("\nOpción inválida!")
            input("Presione cualquier tecla para regresar al menú de matrices...")

    def pedir_matriz(self, nombre="M", es_aumentada=True) -> Matriz:
        """
        Se encarga de pedir los valores de la matriz, y
        llama a pedir_dimensiones() para obtener las dimensiones.
        """

        valores = []
        filas, columnas = self.pedir_dimensiones(nombre, es_aumentada)
        i = 0
        if es_aumentada:
            columnas += 1

        while i < filas:
            j = 0
            fila = []
            print(f"\nFila {i+1}:")
            while j < columnas:
                try:
                    # si no es aumentada, siempre pedir variables
                    # si es aumentada, pedir una constante ("b") en la ultima iteracion
                    if not es_aumentada or j != columnas - 1:
                        dato_a_pedir = f"-> X{j+1} = "
                    else:
                        dato_a_pedir = "-> b = "
                    elemento = Fraction(input(dato_a_pedir).strip()).limit_denominator(100)
                    fila.append(elemento)
                    j += 1  # solo incrementar si no ocurre un error

                # capturar inputs invalidos para Fraction():
                except ValueError:
                    input("\nError: Ingrese un número real!")
                    print()
                except ZeroDivisionError:
                    input("\nError: El denominador no puede ser cero!")
                    print()
            i += 1
            valores.append(fila)
        return Matriz(es_aumentada, filas, columnas, valores)

    def pedir_dimensiones(self, nombre: str, es_aumentada: bool) -> tuple[int, int]:
        """
        Pide las filas y columnas de una matriz.
        Si se esta ingresando una matriz aumentada, llamarles "ecuaciones" y "variables".
        """

        palabras = ["ecuaciones", "variables"] if es_aumentada else ["filas", "columnas"]
        try:
            limpiar_pantalla()
            print(f"\nDatos de matriz {nombre}:")
            print("----------------------------")
            filas = int(input(f"Ingrese el número de {palabras[0]}: "))
            if filas <= 0:
                raise ValueError  # raise immediatamente para no pedir columnas
            columnas = int(input(f"Ingrese el número de {palabras[1]}: "))
            if columnas <= 0:
                raise ValueError
        except ValueError:
            input("Error: Ingrese un número entero positivo!")
            return self.pedir_dimensiones(nombre, es_aumentada)
        return (filas, columnas)

    def procesar_operacion(self, operacion: str) -> tuple:
        """
        Recibe un código de operación, selecciona las matrices necesarias
        para esa operación, y retorna una tupla con el resultado.

        Códigos válidos de operación:
        * "se": resolver sistema de ecuaciones
        * "s": sumar matrices
        * "r": restar matrices
        * "me": multiplicar matriz por escalar
        * "m": multiplicar matrices
        * "t": transponer matriz
        * "d": calcular determinante
        * "i": encontrar la inversa de una matriz
        """

        limpiar_pantalla()
        if operacion not in self.ops_validas or not self._validar_mats_ingresadas():
            return ()

        # manejar operaciones que requerien dos matrices
        if operacion in self.ops_con_dos:
            nombres_mats = self.seleccionar_mats(operacion)

            # si hubo un error en seleccionar_mats():
            if nombres_mats == []:
                return ()

            mat1, mat2 = (
                self.mats_ingresadas[nombres_mats[0]],
                self.mats_ingresadas[nombres_mats[1]],
            )

            # retornar matrices seleccionadas y resultado de operacion:
            match operacion:
                case "s":  # ? suma
                    return (nombres_mats, mat1 + mat2)
                case "r":  # ? resta
                    return (nombres_mats, mat1 - mat2)
                case "m":  # ? multiplicacion
                    return (nombres_mats, mat1 * mat2)

        # operaciones que requieren una sola matriz
        elif operacion in self.ops_con_una:
            nombre_mat = self.seleccionar_mat(operacion)

            # si hubo un error en seleccionar_mat():
            if nombre_mat == "":
                return ()

            # duplicar el objeto para no modificar el original
            mat_copia = deepcopy(self.mats_ingresadas[nombre_mat])
            match operacion:
                case "se":  # ? resolver sistema
                    nombre_resultado = f"{nombre_mat}_r"
                    sistema = SistemaEcuaciones(mat_copia)
                    sistema.resolver_sistema()
                    if not any(sistema.matriz == mat for mat in self.mats_ingresadas.values()):
                        self.mats_ingresadas[nombre_resultado] = sistema.matriz

                    return (nombre_mat, sistema)

                case "me":  # ? matriz por escalar
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
                    return (nombre_mat, escalar, mat_copia * escalar)

                case "t":  # ? transponer matriz
                    nombre_resultado = f"{nombre_mat}_t"
                    transpuesta = mat_copia.transponer()
                    if not any(transpuesta == mat for mat in self.mats_ingresadas.values()):
                        self.mats_ingresadas[nombre_resultado] = transpuesta

                    return (nombre_mat, transpuesta)

                case "d":  # ? calcular determinante
                    return (nombre_mat, mat_copia.calcular_det())

                case "i":  # ? encontrar inversa
                    nombre_resultado = f"{nombre_mat}_i"
                    try:
                        inversa, adjunta, det = mat_copia.invertir()
                    except ArithmeticError as e:
                        print(e)
                        input("Presione cualquier tecla para regresar al menú de matrices...")
                        return ()

                    if not any(inversa == mat for mat in self.mats_ingresadas.values()):
                        self.mats_ingresadas[nombre_resultado] = inversa
                    return (nombre_mat, inversa, adjunta, det)
        return ()

    def mostrar_resultado(self, operacion: str, resultado: tuple) -> None:
        """
        Recibe el código de operación recibido por procesar_operacion(),
        y la tupla retornada por el.

        Códigos válidos de operación:
        * "se": resolver sistema de ecuaciones
        * "s": sumar matrices
        * "r": restar matrices
        * "me": multiplicar matriz por escalar
        * "m": multiplicar matrices
        * "t": transponer matriz
        * "d": calcular determinante
        * "i": encontrar la inversa de una matriz
        """

        limpiar_pantalla()
        if operacion not in self.ops_validas or resultado == ():
            return

        # manejar operaciones con dos matrices:
        if operacion in self.ops_con_dos:
            mats_seleccionadas, mat_resultante = resultado
            mat1, mat2 = (
                self.mats_ingresadas[mats_seleccionadas[0]],
                self.mats_ingresadas[mats_seleccionadas[1]],
            )

            limpiar_pantalla()
            print("\nMatriz seleccionadas:")
            print("---------------------------------------------")
            print(f"{mats_seleccionadas[0]}:")
            print(mat1)
            print(f"{mats_seleccionadas[1]}:")
            print(mat2, end="")
            print("---------------------------------------------")

            match operacion:
                case "s":
                    print(f"\n{mats_seleccionadas[0]} + {mats_seleccionadas[1]}:")
                case "r":
                    print(f"\n{mats_seleccionadas[0]} - {mats_seleccionadas[1]}:")
                case "m":
                    print(f"\n{mats_seleccionadas[0]} * {mats_seleccionadas[1]}:")
            print(mat_resultante, end="")

        # manejar operaciones de una matriz:
        match operacion:
            case "se":  # ? resolver sistema de ecuaciones
                mat_seleccionada, sistema = resultado
                print("\nMatriz seleccionada:")
                print(self.mats_ingresadas[mat_seleccionada])
                print("---------------------------------------------")
                print("\nSistema de ecuaciones resuelto:")
                print(sistema.matriz, end="")
                print(sistema.solucion)
                print("---------------------------------------------")
                mostrar_procedimiento = match_input(
                    "\n¿Desea ver el procedimiento? (s/n) "
                )

                if mostrar_procedimiento == 1:
                    limpiar_pantalla()
                    print(sistema.procedimiento, end="")
                    print(sistema.solucion, end="")
                elif mostrar_procedimiento == 0:
                    print("De acuerdo!")
                else:
                    print("Opción inválida!")

            case "me":  # ? multiplicar matriz por escalar
                mat_seleccionada, escalar, mat_multiplicada = resultado
                mat = self.mats_ingresadas[mat_seleccionada]
                if escalar in (1, -1):
                    imprimir_escalar = ""
                elif Fraction(escalar).is_integer():
                    imprimir_escalar = str(escalar)
                else:
                    imprimir_escalar = f"({escalar}) * "

                limpiar_pantalla()
                print(f"\n{mat_seleccionada}:")
                print(mat)
                print(f"{imprimir_escalar}{mat_seleccionada}:")
                print(mat_multiplicada, end="")

            case "t":   # ? transponer matriz
                mat_seleccionada, mat_transpuesta = resultado
                mat_original = self.mats_ingresadas[mat_seleccionada]

                limpiar_pantalla()
                print(f"\n{mat_seleccionada}:")
                print(mat_original)
                print(f"Transposición de {mat_seleccionada}:")
                print(mat_transpuesta, end="")

            case "d":   # ? calcular determinante
                mat_seleccionada, resultado_det = resultado
                det, mat_triangular, intercambio = resultado_det
                mat_original = self.mats_ingresadas[mat_seleccionada]
                diagonales = [mat_triangular[i, i] for i in range(mat_triangular.filas)]
                cambiar_signo = intercambio and det != 0

                limpiar_pantalla()
                print("\n---------------------------------------------")
                print(f"{mat_seleccionada}:")
                print(mat_original)
                print(f"Matriz triangular superior a partir de {mat_seleccionada}:")
                print(mat_triangular, end="")
                print("---------------------------------------------\n")
                print(f"| {mat_seleccionada} | = {" * ".join(str(d) for d in diagonales)}")
                print(f"| {mat_seleccionada} | = {det if not cambiar_signo else -det}")

                if cambiar_signo:
                    print("\nComo hubo un número impar de intercambios, el signo se invierte:")
                    print(f"-| {mat_seleccionada} | = {det}")

            case "i":   # ? encontrar inversa
                mat_seleccionada, inversa, adjunta, det = resultado
                mat_original = self.mats_ingresadas[mat_seleccionada]

                limpiar_pantalla()
                print("\n---------------------------------------------")
                print(f"{mat_seleccionada}:")
                print(mat_original)
                print(f"adj({mat_seleccionada}):")
                print(adjunta)
                print(f"| {mat_seleccionada} | = {det}")
                print("---------------------------------------------")
                print(f"\n{mat_seleccionada}_i = (1 / {det}) * adj({mat_seleccionada})")
                print("A_i =")
                print(inversa, end="")

        input("\nPresione cualquier tecla para regresar al menú de matrices...")

    def seleccionar_mat(self, operacion: str) -> str:
        """
        Selecciona una sola matriz para realizar la operación especificada.
        Usa _validar_input_mat() para verificar que la matriz seleccionada
        es valida para la operación a realizar. Si ocurre alguna excepción,
        retorna un string vacío.
        """

        if operacion in self.ops_con_una and self._validar_mats_ingresadas():
            mensaje = self._get_mensaje(operacion)
            input_mat = self._get_input(mensaje, operacion)
            try:
                self._validar_input_mat(input_mat, operacion)
            except (KeyError, TypeError, ArithmeticError) as e:
                print(e)
                return ""
            return input_mat
        return ""

    def seleccionar_mats(self, operacion: str) -> list[str]:
        """
        Selecciona dos matrices para realizar la operación especificada.
        Usa _validar_input_mats() para verificar que las matrices seleccionadas
        son válidas para la operación a realizar.
        * KeyError: si una de las matrices seleccionadas no existe
        * ArithmeticError: si las matrices seleccionadas no son válidas para la operación
        """

        if operacion in self.ops_con_dos and self._validar_mats_ingresadas():
            mensaje = "\n¿Cuáles matrices desea seleccionar? (separadas por comas) "
            input_mats = self._get_input(mensaje, operacion).split(",")
            try:
                self._validar_input_mats(input_mats, operacion)
            except (KeyError, ValueError, ArithmeticError) as e:
                print(e)
                return []
            return input_mats
        return []

    def _get_mensaje(self, operacion: str) -> str:
        """
        Helper method usado en seleccionar_mat() para imprimir
        un mensaje apropiado para la operación a realizar.
        """

        match operacion:
            case "se":
                return "\n¿Cuál matriz desea resolver? "
            case "me":
                return "\n¿Cuál matriz desea multiplicar por un escalar? "
            case "mv":
                return "\n¿Cuál matriz desea multiplicar por un vector? "
            case "t":
                return "\n¿Cuál matriz desea transponer? "
            case "d":
                return "\n¿Para cuál matriz desea calcular su determinante? "
            case "i":
                return "\n¿Para cuál matriz desea encontrar su inversa? "
            case _:
                return ""

    def _get_input(self, mensaje: str, operacion: str) -> str:
        """
        Muestra las matrices apropiadas ingresadas y retorna el input del usuario.
        """

        limpiar_pantalla()
        necesita_aumentada = operacion == "se"
        print(self.mostrar_matrices(necesita_aumentada), end="")
        return input(mensaje).strip()

    def _validar_input_mat(self, input_mat: str, operacion: str) -> None:
        """
        Valida la matriz seleccionada por el usuario.
        * KeyError: si la matriz seleccionada no existe
        * TypeError: si se resolverá un sistema de ecuaciones y la matriz seleccionada no es aumentada
        * ArithmeticError: si se desea calcular determinante y la matriz seleccionada no es cuadrada
        """

        if input_mat not in self.mats_ingresadas:
            raise KeyError(f"Error: La matriz '{input_mat}' no existe!")
        if operacion == "se" and not self.mats_ingresadas[input_mat].aumentada:
            raise TypeError(f"Error: La matriz '{input_mat}' no es aumentada!")
        if operacion in ("d", "i") and not self.mats_ingresadas[input_mat].es_cuadrada():
            raise ArithmeticError(f"Error: La matriz '{input_mat}' no es cuadrada!")

    def _validar_input_mats(self, input_mats: list[str], operacion: str) -> None:
        """
        Valida las matrices seleccionadas por el usuario.
        * KeyError: si una de las matrices seleccionadas no existe
        * TValueError: si no se seleccionan dos matrices
        * ArithmeticError: si las matrices no tienen las dimensiones válidas para la operación
        """

        mat = next((mat for mat in input_mats if mat not in self.mats_ingresadas), None)
        if mat is not None:
            raise KeyError(f"Error: La matriz '{mat}' no existe!")
        if len(input_mats) != 2:
            raise ValueError("Error: Debe seleccionar dos matrices!")

        if operacion in ("s", "r"):
            mat1, mat2 = (
                self.mats_ingresadas[input_mats[0]],
                self.mats_ingresadas[input_mats[1]],
            )

            dimensiones_validas = mat1.filas == mat2.filas and mat1.columnas == mat2.columnas
            if not dimensiones_validas:
                raise ArithmeticError("Error: Las matrices deben tener las mismas dimensiones!")
        elif operacion == "m":
            mat1, mat2 = (
                self.mats_ingresadas[input_mats[0]],
                self.mats_ingresadas[input_mats[1]],
            )

            dimensiones_validas = mat1.columnas == mat2.filas
            if not dimensiones_validas:
                raise ArithmeticError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz!")

    def _validar_mats_ingresadas(self) -> bool:
        """
        Valida si el diccionario de matrices ingresadas esta vacío o no.
        """

        if self.mats_ingresadas == {}:
            print("\nNo hay matrices ingresadas!")
            return False
        return True

    def mostrar_matrices(self, necesita_aumentada: int) -> str:
        """
        Imprime las matrices ingresadas en self.mats_ingresadas.

        necesita_aumentada actúa como filtro:
        *  1: solo mostrar matrices aumentadas
        *  0: solo mostrar matrices no aumentadas
        * -1: mostrar todas las matrices ingresadas
        """

        if necesita_aumentada not in (1, 0, -1):
            return "\nArgumento inválido!"
        if not self._validar_mats_ingresadas():
            return "\nNo hay matrices ingresadas!"

        solo_aumentadas = all(mat.aumentada for mat in self.mats_ingresadas.values())
        solo_no_aumentadas = all(not mat.aumentada for mat in self.mats_ingresadas.values())

        # verificar si no hay matrices que cumplan con el filtro dado:
        if necesita_aumentada == 1 and solo_no_aumentadas:
            return "\nNo hay matrices aumentadas ingresadas!"
        if necesita_aumentada == 0 and solo_aumentadas:
            return "\nNo hay matrices no aumentadas ingresadas!"

        matrices = ""
        adj = "aumentadas " if necesita_aumentada == 1 else "no aumentadas "

        matrices += f"\nMatrices {adj if necesita_aumentada != -1 else " "}guardadas:\n"
        matrices += "---------------------------------------------"
        for nombre, mat in self.mats_ingresadas.items():
            if (necesita_aumentada == 1 and not mat.aumentada) or (
                necesita_aumentada == 0 and mat.aumentada):
                continue
            matrices += f"\n{nombre}:\n"
            matrices += str(mat)
        matrices += "---------------------------------------------\n"
        return matrices
