from typing import List
from utils import Mat, DictMatrices, DictVectores, Validacion

# funciones para validar los datos del programa
# -------------------------------------------------------

def validar_vecs(vecs_ingresados: DictVectores) -> bool:
		if not vecs_ingresados or vecs_ingresados is None:
			input("\nNo hay vectores ingresados!")
			return False
		return True

def validar_mats(mats_ingresadas: DictMatrices) -> bool:
		if not mats_ingresadas or mats_ingresadas is None:
			input("\nNo hay matrices ingresadas!")
			return False
		return True

def validar_matriz(M: Mat) -> int:
	consistente = validar_consistencia(M)
	if not consistente[0]: return consistente[1]
	else: return -1

def validar_consistencia(M: Mat) -> Validacion:
	filas = len(M)
	for i in range(filas):
		# ver si la fila tiene la forma de 0 = b (donde b != 0)
		if [0 for _ in range(len(M[0]) - 1)] == M[i][:-1] and M[i][-1] != 0:
			return (False, i) # tambien retornar el indice de la fila para imprimir el mensaje de error
	return (True, -1) # si no se ha retornado False, entonces la matriz es consistente

def validar_escalonada(M: Mat) -> bool:
	filas = len(M)
	columnas = len(M[0])
	matriz_cero = [[0 for _ in range(columnas)] for _ in range(filas)]
	if M == matriz_cero: return False # si la matriz solo son ceros, no es escalonada
	fila_cero = [0 for _ in range(columnas)]
	for i in range(filas):
		if M[i] != fila_cero: continue
		if any(M[j] != fila_cero for j in range(i+1, filas)):
			return False # si se encuentra una fila no-cero despues de una fila cero, no es escalonada
	entrada_anterior = -1
	for i in range(filas):
		# encontrar la entrada principal de la fila actual
		try: entrada_actual = next(j for j in range(columnas-1) if M[i][j] != 0)
		except StopIteration: continue
		# si la entrada actual esta a la izquierda de la entrada anterior, no es escalonada
		if entrada_actual <= entrada_anterior: return False
		if any(M[k][entrada_actual] != 0 for k in range(i+1, filas)):
			return False # si hay otra entrada debajo de la actual en la misma columna, no es escalonada

		entrada_anterior = entrada_actual
	return True

def validar_escalonada_reducida(M: Mat) -> bool:
	filas = len(M)
	columnas = len(M[0])
	# si no es escalonada, no puede ser escalonada reducida
	if not validar_escalonada(M): return False
	for i in range(filas):
		try: entrada_principal = next(j for j in range(columnas-1) if M[i][j] == 1)
		except StopIteration: continue
		if any(M[k][entrada_principal] != 0 and k != i for k in range(filas)):
			return False # si hay otra entrada que no es 0 en la misma columna, no es escalonada reducida
	return True # si no se retorno False despues del bucle, la matriz es escalonada reducida

def encontrar_variables_libres(M: Mat) -> List[int]:
		filas = len(M)
		columnas = len(M[0])
		entradas = []

		# encontrar entradas principales en cada fila
		for i in range(filas):
			try: entradas.append(next(j for j in range(columnas-1) if M[i][j] != 0))
			except StopIteration: continue

		# las variables que no son entradas principales son variables libres
		return [j for j in range(columnas-1) if j not in entradas]
