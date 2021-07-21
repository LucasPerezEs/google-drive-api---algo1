from os import mkdir
import csv

def crear_carpetas():
    nombre_carpeta=input("Ingresa el nombre de la carpeta: ")
    mkdir(nombre_carpeta)


def carpetas_locales(DOCENTE_ALUMNO):
    mkdir("nueva_carpeta")#NECESITO EL ASUNTO DE GMAIL PARA EL NOMBRE DE LA CARPETA
    for docente in DOCENTE_ALUMNO.keys():
        mkdir(f"nueva_carpeta\\{docente}")
        for alumno in DOCENTE_ALUMNO[docente]:
            mkdir(f"nueva_carpeta\\{docente}\\{alumno}")
    



def main():
    DOCENTE_ALUMNO={} #{"DOCENTE":[ALUMNO1,ALUMNO2],"DOCENTE2":[ALUMNO1,ALUMNO2]}
    ALUMNOS_SIN_DOCENTE={} #{ALUMNO:PADRON,ALUMNO2:PADRON2}  CONVIENE MAS UNA LISTA?
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
            ALUMNOS_SIN_DOCENTE[row[0]]=row[1]
        print(ALUMNOS_SIN_DOCENTE)
    
    
    '''carpetas_locales(DOCENTE_ALUMNO)'''

main()