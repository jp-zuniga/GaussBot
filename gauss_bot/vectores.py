from fractions import Fraction
from typing import List
from utils import Mat, Vec, DictVectores, limpiar_pantalla

# funciones para realizar operaciones con vectores
# --------------------------------------------------------------------------------

class Vector:
    def __init__(self):
        from matrices import Matriz
        from validaciones import Validaciones
        self.mat = Matriz()
        self.vals = Validaciones()
        self.vecs_ingresados = {}

    def imprimir_vectores(self, es_matricial=False) -> None:
        if not self.vals.validar_vecs(self.vecs_ingresados): return None
        mensaje = "seleccionados" if es_matricial else "ingresados"
        print(f"\nVectores {mensaje}:")
        print("---------------------------------------------")
        for nombre, vector in self.vecs_ingresados.items():
            vec = [str(num.limit_denominator(100)) for num in vector]
            print(f"{nombre}: {vec}")
        print("---------------------------------------------")
        return None

    def menu_vectores(self) -> int:
        limpiar_pantalla()
        print("\n###############################")
        print("### Operaciones Vectoriales ###")
        print("###############################")
        self.imprimir_vectores()
        print("\n1. Agregar un vector")
        print("2. Producto matriz-vector")
        print("3. Multiplicación escalar")
        print("4. Multiplicación de vectores")
        print("5. Suma de vectores")
        print("6. Resta de vectores")
        print("7. Regresar al menú principal")

        try:
            option = int(input("\nSeleccione una opción: "))
            if option < 1 or option > 7: raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.menu_vectores()
        return option

    def operaciones_vectoriales(self) -> None:
        option = self.menu_vectores()
        while option != 7:
            match option:
                case 1:
                    limpiar_pantalla()
                    self.vecs_ingresados = self.agregar_vector()
                    option = self.menu_vectores()
                    continue
                case 2:
                    limpiar_pantalla()
                    A = self.matriz_por_suma_vectores()
                    option = self.menu_vectores()
                    continue
                case 3:
                    limpiar_pantalla()
                    self.vecs_ingresados = self.mult_escalar()
                    option = self.menu_vectores()
                    continue
                case 4:
                    limpiar_pantalla()
                    self.vecs_ingresados = self.mult_vectorial()
                    option = self.menu_vectores()
                    continue
                case 5:
                    limpiar_pantalla()
                    self.input_suma_resta(option=True)
                    option = self.menu_vectores()
                    continue
                case 6:
                    limpiar_pantalla()
                    self.input_suma_resta(option=False)
                    option = self.menu_vectores()
                    continue
                case 7: break
                case _:
                    input("Opción inválida! Por favor, intente de nuevo...")
                    continue

        input("Regresando al menú principal...")
        return None

    def agregar_vector(self) -> DictVectores:
        try:
            limpiar_pantalla()
            nombre = input("\nIngrese el nombre del vector (una letra minúscula): ").strip().lower()
            if not nombre.isalpha() or len(nombre) != 1: raise NameError
            if nombre in self.vecs_ingresados: raise KeyError
            longitud = int(input(f"¿Cuántas dimensiones tendrá el vector? ").strip())
        except NameError:
            input("Error: Ingrese solamente una letra minúscula!")
            return self.agregar_vector()
        except KeyError:
            input(f"Error: Ya hay un vector con el nombre {nombre}!")
            return self.agregar_vector()
        except ValueError:
            input("Error: Ingrese un número entero!")
            return self.agregar_vector()

        self.vecs_ingresados[nombre] = self.ingresar_vector(longitud)
        print(f"\nVector agregado exitosamente!")
        match input("¿Desea agregar otro vector? (s/n) ").strip().lower():
            case 's': return self.agregar_vector()
            case 'n': input("Regresando al menú de vectores...")
            case _: input("Opción inválida! Regresando al menú de vectores...")
        return self.vecs_ingresados

    def ingresar_vector(self, longitud: int) -> Vec:
        try:
            vec = [Fraction(x).limit_denominator(100) for x in input(f"Ingrese los componentes (separados por comas): ").strip().split(',')]
            if len(vec) != longitud: raise TypeError
        except TypeError:
            input("Error: El vector no tiene las dimensiones correctas!")
            return self.ingresar_vector(longitud)
        except ValueError:
            input("Error: Ingrese un número real!")
            return self.ingresar_vector(longitud)
        return vec

    def mult_escalar(self) -> DictVectores:
        if not self.vals.validar_vecs(self.vecs_ingresados): return self.vecs_ingresados
        try:
            limpiar_pantalla()
            self.imprimir_vectores()
            vec_nombre = input("\n¿Cuál vector desea multiplicar escalarmente? ").strip()
            if vec_nombre not in self.vecs_ingresados: raise KeyError(vec_nombre)
            escalar = Fraction(input("Ingrese el escalar: ").strip())
        except KeyError as k:
            input(f"Error: El vector {k} no existe!")
            return self.mult_escalar()
        except ValueError:
            input("Error: Ingrese un número real!")
            return self.mult_escalar()
        except ZeroDivisionError:
            input("Error: El denominador no puede ser cero!")
            return self.mult_escalar()
        
        self.vecs_ingresados[vec_nombre] = [Fraction(x*escalar) for x in self.vecs_ingresados[vec_nombre]]
        imprimir_escalar = escalar if escalar.is_integer() else f"({str(Fraction(escalar))})*"
        input(f"\n{imprimir_escalar}{vec_nombre} = {[str(x.limit_denominator(100)) for x in self.vecs_ingresados[vec_nombre]]}")
        return self.vecs_ingresados

    def mult_vectorial(self) -> DictVectores:
        if not self.vals.validar_vecs(self.vecs_ingresados): return self.vecs_ingresados
        try:
            limpiar_pantalla()
            self.imprimir_vectores()
            input_vecs = input("\n¿Cuáles vectores desea multiplicar? (separados por comas): ").strip().split(',')
            if len(input_vecs) != 2: raise IndexError
            vec1, vec2 = input_vecs
            for vec in input_vecs:
                if vec not in self.vecs_ingresados: raise KeyError(vec)
            if len(self.vecs_ingresados[vec1]) != len(self.vecs_ingresados[vec2]): raise ArithmeticError
        except IndexError:
            input("Error: Debe ingresar dos vectores para multiplicar!")
            return self.mult_vectorial()
        except KeyError as k:
            input(f"Error: El vector {k} no existe!")
            return self.mult_vectorial()
        except ArithmeticError:
            input("Error: Los vectores deben tener la misma longitud!")
            return self.mult_vectorial()

        producto_punto = sum(i*j for i in self.vecs_ingresados[vec1] for j in self.vecs_ingresados[vec2])
        input(f"\n{vec1}.{vec2} = {str(producto_punto)}")
        return self.vecs_ingresados

    def input_suma_resta(self, option: bool, es_matricial=False) -> None:
        if not self.vals.validar_vecs(self.vecs_ingresados): return self.vecs_ingresados
        try:
            limpiar_pantalla()
            self.imprimir_vectores()
            operacion = "sumar" if option else "restar"
            input_vecs = input(f"\n¿Cuáles vectores desea {operacion}? (separados por comas): ").strip().split(',')
            if len(input_vecs) <= 1 or (es_matricial and len(input_vecs) != 2): raise IndexError
            for vec in input_vecs:
                if vec not in self.vecs_ingresados: raise KeyError(vec)
            if not all(len(self.vecs_ingresados[j]) == len(self.vecs_ingresados[input_vecs[0]]) for j in input_vecs):
                raise ArithmeticError
        except KeyError as k:
            input(f"Error: El vector {k} no existe!")
            return self.input_suma_resta(option, es_matricial)
        except IndexError:
            error = "dos vectores para realizar el producto matriz-vector" if es_matricial else f"dos o más vectores para {operacion}"
            input(f"Error: Debe ingresar {error}!")
            return self.input_suma_resta(option, es_matricial)
        except ArithmeticError:
            input("Error: Los vectores deben tener la misma longitud!")
            return self.input_suma_resta(option, es_matricial)

        if es_matricial: return input_vecs
        if option:
            resultado = self.sumar_vectores(input_vecs)
            signo = '+'
        else:
            resultado = self.restar_vectores(input_vecs)
            signo = '-'

        mensaje = ""
        for i in input_vecs:
            if i != input_vecs[-1]: mensaje += f"{i} {signo} "
            else: mensaje += i

        input(f"\n{mensaje} = {[str(num.limit_denominator(100)) for num in resultado]}")
        return None

    def sumar_vectores(self, input_vecs: List[str]) -> Vec:
        suma_vecs = [0 for _ in self.vecs_ingresados[input_vecs[0]]]
        for i in range(len(suma_vecs)):
            for j in input_vecs:
                suma_vecs[i] += self.vecs_ingresados[j][i]
        
        return suma_vecs

    def restar_vectores(self, input_vecs: List[str]) -> Vec:
        resta_vecs = self.vecs_ingresados[input_vecs[0]]
        for i in range(len(resta_vecs)):
            for j in input_vecs[1:]:
                resta_vecs[i] -= self.vecs_ingresados[j][i]
        
        return resta_vecs

    def matriz_por_suma_vectores(self) -> Mat:
        if not self.vals.validar_vecs(self.vecs_ingresados): return None
        A = self.mat.pedir_matriz(es_aumentada=False, nombre='A')
        limpiar_pantalla()
        input_vecs = self.input_suma_resta(option=True, es_matricial=True) # pedir los vectores
        suma_vecs = self.sumar_vectores(input_vecs) # sumar los vectores seleccionados por el usuario
        
        if len(A[0]) != len(self.vecs_ingresados[input_vecs[0]]): # validar las dimensiones
            input("\nError: Las dimensiones de A y los vectores no son compatibles!")
            return self.matriz_por_suma_vectores()

        # calcular A(u + v)
        resultado = []
        for i in range(len(A)):
            resultado.append(sum([A[i][j] * suma_vecs[j] for j in range(len(suma_vecs))]))
        
        # imprimir las operaciones realizadas
        self.imprimir_MPSV(A, input_vecs, suma_vecs, resultado)
        match input("\nDesea comprobar la propiedad distributiva (A(u + v) = Au + Av)? (s/n) ").strip().lower():
            case 's': self.suma_matriz_por_vector(A, input_vecs)
            case 'n': input("De acuerdo! Regresando al menú de vectores...")
            case _: input("Opción inválida! Regresando al menú de vectores...")
        return resultado

    def suma_matriz_por_vector(self, A: Mat, input_vecs: List[str]) -> None:
        limpiar_pantalla()
        u, v = self.vecs_ingresados[input_vecs[0]], self.vecs_ingresados[input_vecs[1]]
        mult_u = []
        mult_v = []

        # calcular Au y Av
        for i in range(len(A)):
            mult_u.append(sum([A[i][j] * u[j] for j in range(len(u))]))
            mult_v.append(sum([A[i][j] * v[j] for j in range(len(v))]))

        suma_mults = [i+j for i in mult_u for j in mult_v] # calcular Au + Av
        self.imprimir_SMPV(A, input_vecs, [mult_u, mult_v], suma_mults) # imprimir las operaciones realizadas
        input("\nLa respuesta sigue siendo la misma, asi que la propiedad distributiva se cumple!")
        return None

    def imprimir_MPSV(self, A: Mat, input_vecs: List[str], suma_vecs: Vec, resultado: Mat) -> None: 
        filas = len(A)
        columnas = len(A[0])
        u, v = self.vecs_ingresados[input_vecs[0]], self.vecs_ingresados[input_vecs[1]]

        limpiar_pantalla()
        print("\nMatriz A:")
        self.mat.imprimir_matriz(A, es_aumentada=False)
        self.imprimir_vectores(es_matricial=True)

        # encontrar la longitud maxima de todos los elementos de todas las listas (u, v, suma_vecs, A, resultado)
        lens_uv = [len(str(i)) for i in u]
        lens_uv += [len(str(j)) for j in v]
        max_uv = max(lens_uv)
        max_suma = max(len(str(k)) for k in suma_vecs)
        max_A = max(len(str(A[i][j])) for i in range(filas) for j in range(columnas))
        max_resultado = max(len(str(i)) for i in resultado)

        # imprimir procedimiento de u + v
        print("\nu + v:")
        for i in range(len(u)):
            signo = '+' if v[i] >= 0 else '-'
            igual = ' ' if (i != len(u) // 2) else '='
            uv = f"{str(u[i]).center(max_uv)} {signo} {str(abs(v[i])).center(max_uv)}"
            print(f"[ {uv} ] {igual} [ {str(suma_vecs[i]).center(max_suma)} ]")

        # imprimir procedimiento de A(u + v)
        operaciones = []
        for j in range(filas):
            fila = ""
            for k in range(columnas):
                linea = f"({str(A[j][k]).center(max_A)} * {str(suma_vecs[k]).center(max_A)})"
                if k == 0: linea = f"[ {linea} + "
                elif k == columnas-1: linea = f"{linea} ]"
                else: linea = f"{linea} + "
                fila += linea
            operaciones.append(fila)

        print("\nA(u + v):")
        for k in range(len(operaciones)):
            igual = ' ' if (k != len(operaciones) // 2) else '='
            print(f"{operaciones[k]} {igual} [ {str(resultado[k]).center(max_resultado)} ]")

        return None

    def imprimir_SMPV(self, A: Mat, input_vecs: List[str], mults: List[Mat], suma_mults: Mat) -> None:
        filas = len(A)
        columnas = len(A[0])
        u, v = self.vecs_ingresados[input_vecs[0]], self.vecs_ingresados[input_vecs[1]]
        mult_u, mult_v = mults[0], mults[1]

        limpiar_pantalla()
        print("\nMatriz A:")
        self.mat.imprimir_matriz(A, es_aumentada=False)
        self.imprimir_vectores(es_matricial=True)

        # encontrar la longitud maxima de todos los elementos de todas las listas (u, v, A, mult_u, mult_v)
        lens_uv = [len(str(i)) for i in u]
        lens_uv += [len(str(j)) for j in v]
        max_mult_u = max(len(str(mult_u[i])) for i in range(filas))
        max_mult_v = max(len(str(mult_v[i])) for i in range(filas))
        max_A = max(len(str(A[i][j])) for i in range(filas) for j in range(columnas))
        max_suma_mults = max(len(str(suma_mults[i])) for i in range(filas))

        # guardar procedimiento de Au
        operaciones_u = []
        for j in range(filas):
            fila = ""
            for k in range(columnas):
                linea = f"({str(A[j][k]).center(max_A)} * {str(u[k]).center(max_A)})"
                if k == 0: linea = f"[ {linea} + "
                elif k == columnas-1: linea = f"{linea} ]"
                else: linea = f"{linea} + "
                fila += linea
            operaciones_u.append(fila)

        print("\nAu:") # imprimir procedimiento
        for k in range(len(operaciones_u)):
            igual = ' ' if (k != len(operaciones_u) // 2) else '='
            print(f"{operaciones_u[k]} {igual} [ {str(mult_u[k]).center(max_mult_u)} ]")

        # guardar procedimiento de Av
        operaciones_v = []
        for j in range(filas):
            fila = ""
            for k in range(columnas):
                linea = f"({str(A[j][k]).center(max_A)} * {str(v[k]).center(max_A)})"
                if k == 0: linea = f"[ {linea} + "
                elif k == columnas-1: linea = f"{linea} ]"
                else: linea = f"{linea} + "
                fila += linea
            operaciones_v.append(fila)

        print("\nAv:") # imprimir procedimiento
        for k in range(len(operaciones_v)):
            igual = ' ' if (k != len(operaciones_v) // 2) else '='
            print(f"{operaciones_v[k]} {igual} [ {str(mult_v[k]).center(max_mult_v)} ]")

        # calcular y imprimir procedimiento de Au + Av
        print("\nAu + Av:")
        for i in range(filas):
            print(f"[ {str(mult_u[i]).center(max_mult_u)} + {str(mult_v[i]).center(max_mult_v)} ] = [ {str(suma_mults[i]).center(max_suma_mults)} ]")
        
        return None
