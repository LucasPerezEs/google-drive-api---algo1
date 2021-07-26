from os import mkdir
import csv
from drive import crear_carpeta

def crear_carpetas_local():
    nombre_carpeta=input("Ingresa el nombre de la carpeta: ")
    mkdir(nombre_carpeta)


def obtener_padrones():
    padrones={}
    with open("alumnos.csv", newline='', encoding="UTF-8") as alumnos_csv:

            csv_reader=csv.reader(alumnos_csv, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                padrones[row[0]]=row[1]
    return padrones

def crear_datos(condicion, docente_alumno):
    if condicion== True:
        #docente_alumno={}{"DOCENTE":[ALUMNO1,ALUMNO2],"DOCENTE2":[ALUMNO1,ALUMNO2]}
        with open("docentes.csv", newline='', encoding="UTF-8") as archivo_csv:

            csv_reader=csv.reader(archivo_csv, delimiter=',')
            next(csv_reader)
            for row in csv_reader:

                docente_alumno[row[0]]=[]

        with open("docente-alumnos.csv", newline='',encoding="UTF-8") as correctores_csv:

            csv_reader=csv.reader(correctores_csv, delimiter=',')
            next(csv_reader)
            for row in csv_reader:

                docente_alumno[row[0]].append(row[1])
        return docente_alumno
    else:
        alumnos_sin_docente=[]
        with open("alumnos.csv", newline='', encoding="UTF-8") as alumnos_csv:

            csv_reader=csv.reader(alumnos_csv, delimiter=',')
            next(csv_reader)
            for row in csv_reader:

                alumnos_sin_docente.append(row[0])
        for docente in docente_alumno.keys():

            for alumno in docente_alumno[docente]:

                if alumno in alumnos_sin_docente:

                    alumnos_sin_docente.remove(alumno)
        return alumnos_sin_docente



def carpetas():
    verdad=True
    falso=False
    docente_alumno={} #{"DOCENTE":[ALUMNO1,ALUMNO2],"DOCENTE2":[ALUMNO1,ALUMNO2]}
    docente_alumno=crear_datos(verdad,docente_alumno)
    alumnos_sin_docente=crear_datos(falso,docente_alumno)

    carpeta=input("Ingrese el nombre de la carpeta que contendra la entrega de los alumnos: ")
    mkdir(carpeta)
    id_madre = crear_carpeta(carpeta,"")

    for docente in docente_alumno.keys():

        mkdir(f"{carpeta}\\{docente}")
        id_docente = crear_carpeta(docente, id_madre)
        for alumno in docente_alumno[docente]:

            mkdir(f"{carpeta}\\{docente}\\{alumno}")
            crear_carpeta(alumno, id_docente)
    mkdir(f"{carpeta}\\Alumnos sin docente")
    id_huerfanos = crear_carpeta("Alumnos sin docente", id_madre)
    for alumno in alumnos_sin_docente:

        mkdir(f"{carpeta}\\Alumnos sin docente\\{alumno}")
        crear_carpeta(alumno, id_huerfanos)

    return docente_alumno, alumnos_sin_docente, carpeta