import os

# funciones para validar sistemas de ecuaciones:
# -------------------------------------------------------

def limpiar_pantalla():
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)

def validar_consistencia(M):
    filas = len(M)

    for i in range(filas):
        # ver si la fila tiene la forma de 0 = b (donde b != 0)
        if [0 for _ in range(len(M[0])-1)] == M[i][:-1] and M[i][-1] != 0: return [False, i]

        # encontrar la primera entrada no 0 en la fila
        try: indice = M[i].index(next(filter(lambda x: x != 0, M[i])))
        except StopIteration: indice = -1

        # ver si la fila tiene la forma de b = b (donde b != 1)
        if indice != -1 and M[i][indice] == M[i][-1] and M[i][indice] != 1: return [True, None]

    return [True, None] # si no se ha retornado False, entonces la matriz si es consistente

def validar_escalonada(M):
    filas = len(M)
    columnas = len(M[0])

    # si las filas distintas de cero no estan en orden descendiente, no es escalonada
    fila_cero = [0 for _ in range(columnas)]
    for i in range(filas):
        if M[i] == fila_cero:
            # checkear si alguna fila debajo de la fila de ceros no es cero
            if any(M[j] != fila_cero for j in range(i+1, filas)):
                return False # si se encuentra una fila no cero, no es escalonada

    entrada_anterior = -1 # para guardar el indice de la entrada anterior (inicializada en -1 para la primera iteracion)
    for i in range(filas):
        for j in range(columnas):
            if M[i][j] != 0:
                # si la entrada no es 0 y está a la izquierda de la entrada anterior, no es escalonada
                if j <= entrada_anterior:
                    return False

                # si hay otra entrada que no es 0 en la misma columna, no es escalonada
                for k in range(i+1, filas):
                    if M[k][j] != 0:
                        return False
                
                entrada_anterior = j # actualizar indice para la proxima iteracion
                break # ir a la proxima entrada principal

    return True

def validar_escalonada_reducida(M):
    filas = len(M)
    columnas = len(M[0])

    # solo validar que es reducida si tambien es escalonada
    if validar_escalonada(M):
        for i in range(filas):
            for j in range(columnas):
                # validar que la entrada principal sea 1
                if M[i][j] == 1:
                    for k in range(filas):
                        # si hay otra entrada que no es 0 en la misma columna, no es reducida
                        if M[k][j] != 0 and k != i:
                            return False
                        
                    break # ir a la proxima entrada principal
        
        return True # si no se retorno False despues del bucle, la matriz es escalonada reducida
    return False # si validar_escalonada no retorno True, la matriz tampoco es escalonada reducida, y se retorna False

def encontrar_variables_libres(M):
    filas = len(M)
    columnas = len(M[0])
    entradas = []
    
    # encontrar entradas principales en cada fila
    for i in range(filas):
        for j in range(columnas-1):
            if M[i][j] != 0:
                entradas.append(j)
                break
    
    # las variables que no son entradas principales son variables libres
    libres = [j for j in range(columnas-1) if j not in entradas]
    if libres == []: return None
    return libres
