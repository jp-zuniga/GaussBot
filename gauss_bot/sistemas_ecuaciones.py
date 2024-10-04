from utils import List, Mat, Validacion, limpiar_pantalla

# funciones para resolver sistemas de ecuaciones con matrices
# --------------------------------------------------------------------------------

class SistemaEcuaciones:
    def __init__(self):
        from matrices import Matriz
        from validaciones import Validaciones
        self.mat = Matriz()
        self.vals = Validaciones()

    def resolver_sistema(self, M: Mat) -> Mat:
        limpiar_pantalla()
        M = self.reducir_matriz(M)
        if not M: return None
        
        libres = self.vals.encontrar_variables_libres(M)
        if self.vals.validar_escalonada_reducida(M) and not libres: # solucion unica:
            self.imprimir_soluciones(M, unica=True, libres=None, validacion=(True, None))
            return M
        
        # solucion general:
        self.imprimir_soluciones(M, unica=False, libres=libres, validacion=(True, None))
        return M

    def reducir_matriz(self, M: Mat) -> Mat:
        filas = len(M)
        columnas = len(M[0])
        test_inicial = self.vals.validar_matriz(M)
        if test_inicial != -1:
            self.imprimir_soluciones(M, unica=False, libres=[], validacion=(False, test_inicial))
            return None
        elif self.vals.validar_escalonada_reducida(M): return M

        print("\nMatriz inicial:")
        self.mat.imprimir_matriz(M)
        print("\nReduciendo la matriz a su forma escalonada:")

        # encontrar los pivotes y eliminar los elementos debajo de ellos
        fila_actual = 0
        for j in range(columnas-1):
            fila_pivote = None
            maximo = 0

            # buscar la entrada con el valor mas grande para usarla como pivote
            for i in range(fila_actual, filas):
                if abs(M[i][j]) > maximo:
                    maximo = abs(M[i][j])
                    fila_pivote = i
            
            # si fila_pivote sigue siendo None, significa que todas las entradas de la columna son 0
            # entonces no hay pivote y se pasa a la siguiente columna
            if fila_pivote is None or maximo == 0: continue

            # si la fila actual no es la pivote, se intercambian
            if fila_pivote != fila_actual:
                M[fila_actual], M[fila_pivote] = M[fila_pivote], M[fila_actual]
                print(f"\nF{fila_actual+1} <==> F{fila_pivote+1}")
                self.mat.imprimir_matriz(M)
            
            # si el diagonal no es 1, dividir toda la fila por el diagonal para que sea 1
            pivote = M[fila_actual][j]
            if pivote != 1 and pivote != 0:
                for k in range(columnas):
                    M[fila_actual][k] /= pivote

                if pivote == -1: print(f"\nF{fila_actual+1} => -F{fila_actual+1}")
                else: print(f"\nF{fila_actual+1} => F{fila_actual+1} / {str(pivote.limit_denominator(100))}")
                self.mat.imprimir_matriz(M)

            # eliminar los elementos debajo del pivote
            for f in range(fila_actual+1, filas):
                factor = M[f][j]
                if factor == 0: continue
                for k in range(columnas):
                    M[f][k] -= factor * M[fila_actual][k]

                print(f"\nF{fila_actual+1} => F{fila_actual+1} - ({str(factor.limit_denominator(100))} * F{fila_pivote+1})")
                self.mat.imprimir_matriz(M)

            fila_actual += 1 # ir a la siguiente fila

        # se termina de reducir la matriz, eliminando los elementos encima de los pivotes
        for i in reversed(range(filas)):
            try: columna_pivote = M[i].index(next(filter(lambda x: x != 0, M[i])))
            except StopIteration: columna_pivote = None
                
            # si columna_pivote es None, no hay entrada pivote en la fila, y se pasa a la siguiente
            if columna_pivote is None: continue

            # eliminar los elementos encima del pivote
            for f in reversed(range(i)):
                factor = M[f][columna_pivote]
                if factor == 0: continue
                for k in range(columnas):
                    M[f][k] -= factor * M[i][k]
                    
                print(f"\nF{f+1} => F{f+1} - ({str(factor.limit_denominator(100))} * F{i+1})")
                self.mat.imprimir_matriz(M)

        # validar si la matriz resultante es consistente
        test_final = self.vals.validar_matriz(M)
        if test_final != -1:
            self.imprimir_soluciones(M, unica=False, libres=[], validacion=(False, test_inicial))
            return None
        return M

    def despejar_variables(self, M: Mat, libres: List[int]) -> List[str]:
        filas = len(M)
        columnas = len(M[0])
        ecuaciones = []
        for variable in libres:
            ecuaciones.append(f"| X{variable+1} es libre")
        
        for i in range(filas):
            for j in range(columnas-1):
                if M[i][j] == 0: continue
                constante = M[i][-1].limit_denominator(100)
                expresion = str(constante) if constante != 0 else ''

                for k in range(j+1, columnas-1):
                    if M[i][k] == 0: continue
                    coeficiente = -M[i][k].limit_denominator(100)

                    signo = '+' if coeficiente >= 0 else '-'
                    if expresion: signo = f" {signo} "
                    else: signo = '' if signo == '+' else '-'

                    variable = f"{abs(coeficiente)}*X{k+1}" if abs(coeficiente) != 1 else f"X{k+1}"
                    expresion += f"{signo}{variable}"
                        
                if not expresion: expresion = '0'
                ecuaciones.append(f"| X{j+1} = {expresion}")
                break
        
        ecuaciones.sort(key=lambda x: x[3])
        return ecuaciones

    def imprimir_soluciones(self, M: Mat, unica: bool, libres: List[int | None], validacion: Validacion) -> None:
        filas = len(M)
        solucion, fila_inconsistente = validacion
        if solucion and unica and not libres:
            solucion_trivial = all(M[i][-1] == 0 for i in range(filas))

        if not solucion:
            print(f"\n| En F{fila_inconsistente+1}: 0 != {str(M[fila_inconsistente][-1].limit_denominator(100))}")
            input("| Sistema es inconsistente!")
            return None
        elif unica and not solucion_trivial:
            print("\n| Solución no trivial encontrada:")
            for i in range(filas):
                if all(x == 0 for x in M[i]): continue
                print(f"| X{i+1} = {str(M[i][-1].limit_denominator(100))}")
            return None
        elif unica and solucion_trivial:
            print("\n| Solución trivial encontrada:")
            for i in range(filas):
                if all(x == 0 for x in M[i]): continue
                print(f"| X{i+1} = {str(M[i][-1].limit_denominator(100))}")
            return None
        
        # solucion general:
        ecuaciones = self.despejar_variables(M, libres)
        print("\n| Sistema no tiene solución única!")
        print("| Solución general encontrada:")
        for linea in ecuaciones: print(linea)
        return None
