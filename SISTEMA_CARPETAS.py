from os import mkdir
import csv
from drive import crear_carpeta

def crear_carpetas_local():
    nombre_carpeta=input("Ingresa el nombre de la carpeta: ")
    mkdir(nombre_carpeta)


def carpetas():
    DOCENTE_ALUMNO={} #{"DOCENTE":[ALUMNO1,ALUMNO2],"DOCENTE2":[ALUMNO1,ALUMNO2]}
    ALUMNOS_SIN_DOCENTE=[] 
    with open("docentes.csv", newline='', encoding="UTF-8") as archivo_csv:
        csv_reader=csv.reader(archivo_csv, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            DOCENTE_ALUMNO[row[0]]=[]
    print(DOCENTE_ALUMNO)

    with open("docente-alumnos.csv", newline='',encoding="UTF-8") as correctores_csv:
        csv_reader=csv.reader(correctores_csv, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            DOCENTE_ALUMNO[row[0]].append(row[1])
    print(DOCENTE_ALUMNO)

    with open("alumnos.csv", newline='', encoding="UTF-8") as alumnos_csv:
        csv_reader=csv.reader(alumnos_csv, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            ALUMNOS_SIN_DOCENTE.append(row[0])
        print(ALUMNOS_SIN_DOCENTE)
    
    for docente in DOCENTE_ALUMNO.keys():
        for alumno in DOCENTE_ALUMNO[docente]:
            if alumno in ALUMNOS_SIN_DOCENTE:
                ALUMNOS_SIN_DOCENTE.remove(alumno)
    print(ALUMNOS_SIN_DOCENTE)
    carpeta=input("Ingrese el nombre de la carpeta que contendra la entrega de los alumnos: ")
    mkdir(carpeta)
    id_madre = crear_carpeta(carpeta,"")
    for docente in DOCENTE_ALUMNO.keys():
        mkdir(f"{carpeta}\\{docente}")
        id_docente = crear_carpeta(docente, id_madre)
        for alumno in DOCENTE_ALUMNO[docente]:
            mkdir(f"{carpeta}\\{docente}\\{alumno}")
            crear_carpeta(alumno, id_docente)
            #ACA HAY QUE PONER LOS ARCHIVOS DE LA ENTREGA DEL ALUMNO
    mkdir(f"{carpeta}\\Alumnos sin docente")
    id_huerfanos = crear_carpeta("Alumnos sin docente", id_madre)
    for alumno in ALUMNOS_SIN_DOCENTE:
        mkdir(f"{carpeta}\\Alumnos sin docente\\{alumno}")
        crear_carpeta(alumno, id_huerfanos)
        #ACA HAY QUE PONER LOS ARCHIVOS DE LA ENTREGA DEL ALUMNO
    return DOCENTE_ALUMNO, ALUMNOS_SIN_DOCENTE, carpeta