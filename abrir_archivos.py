'''
docentes.csv
El archivo de docentes contendr´a el siguiente formato de informaci´on:
Formato: nombre del docente, mail del docente.

alumnos.csv
El archivo de alumnos contendr´a el siguiente formato de informaci´on:
Formato: nombre del alumno, padr´on, mail

docente-alumnos.csv
El archivo de docente-alumnos contendr´a el siguiente formato de informaci´on:
Formato: nombre del docente, nombre del alumno
'''
import csv

docentes=list()

with open("prueba_docentes.csv", newline='', encoding="UTF-8") as archivo_csv:
    csv_reader=csv.reader(archivo_csv,delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        docentes.append(row)
    print(docentes)
for i in range(len(docentes)):
    print(f"el nombre del profesor es {docentes[i][0]}")

alumnos=list()
with open("prueba_alumnos.csv", newline='', encoding="UTF-8") as archivo_alumnos:
    csv_reader=csv.reader(archivo_alumnos,delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        alumnos.append(row)
    print(alumnos)
    for i in range(len(alumnos)):
        print(f"el nombre del alumno es {alumnos[i][0]}")


lista_final=list()

with open("prueba_docentes_alumnos.csv", newline='', encoding="UTF-8") as archivo_final:
    csv_reader=csv.reader(archivo_final, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        lista_final.append(row)
    print(lista_final)
    for i in range(len(lista_final)):
        print(f"El docente corrector del alumno {lista_final[i][1]} es {lista_final[i][0]}")