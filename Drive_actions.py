from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os, io
import pickle
from os import mkdir
import csv

SERVICIO = obtener_servicio()

MIME_TYPES = {"csv": "text/csv",  "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "pdf": "application/pdf", "txt": "text/plain", "bin": "application/octet-stream", "doc": "application/msword", "json": "application/json", "mp3": "audio/mpeg", "ppt": "application/vnd.ms-powerpoint", "rar": "application/vnd.rar", "xls": "application/vnd.ms-excel", "zip": "application/zip", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "dat": "application/octet-stream"}

def definir_mime_type(nombre_archivo: str) -> str:
    nombre_separado = nombre_archivo.split(".")
    extension = nombre_separado[1]
    mime = MIME_TYPES[extension]
    
    return mime

def obtener_id(nombre: str, query) -> str:
    response = SERVICIO.files().list(q=query).execute()
    for file in response.get('files', []):
        if file['name'] == nombre:
            id_carpeta = file.get('id')
            return id_carpeta

def subir_archivo(nombre_archivo: str, nombre_carpeta_madre: str, nombre_carpeta_nueva: str, ruta:str) -> None: # Si no quiere subir el archivo adentro de una carpeta, en "nombre_carpeta_madre" pasar string vacio. Si no quiere subir el archivo en una carpeta nueva, en "nombre_carpeta_nueva" pasar string vacio. 
    if nombre_carpeta_madre != "":
        id_carpeta_madre = obtener_id(nombre_carpeta_madre, f"mimeType='application/vnd.google-apps.folder' and trashed=False")
    else:
        id_carpeta_madre = ""

    metadata = {"name" : nombre_archivo}
    
    if ruta == "":
        directorio = os.path.dirname(os.path.realpath(nombre_archivo))
        ruta = os.path.join(directorio, nombre_archivo)
        
    parents = []
    if len(id_carpeta_madre) != 0:
        parents.append(id_carpeta_madre)
        metadata["parents"] = parents
    
    if len(nombre_carpeta_nueva) != 0:
        id_nueva_carpeta = crear_carpeta(nombre_carpeta_nueva, "")
        parents.append(id_nueva_carpeta)
        metadata["parents"] = parents     

    mime = definir_mime_type(nombre_archivo)
    media = MediaFileUpload(ruta, mimetype=mime)
    subir = SERVICIO.files().create(body=metadata, media_body=media, fields="id").execute()

    if subir:
        print(f"El archivo [{nombre_archivo}] fue subido con exito. \n")

def crear_archivo() -> None: # Hacer que escriba algo
    crear = SERVICIO.files().create().execute()
    if crear:
        print("El archivo se ha creado con exito. ")

def crear_carpeta(nombre_carpeta: str, id_carpeta_madre: str) -> str: # Si no se quiere crear la carpeta adentro de otra, en "id_carpeta_madre" poner un string vacio. Gracias!!

    metadata = {}
    
    metadata["name"] = nombre_carpeta
    
    mime_type = "application/vnd.google-apps.folder"
    metadata["mimeType"] = mime_type

    parents = []
    if len(id_carpeta_madre) != 0:
        parents.append(id_carpeta_madre)
        metadata["parents"] = parents

    subir = SERVICIO.files().create(body=metadata).execute()
    
    id_carpeta = subir.get("id")   

    return id_carpeta

def descargar_archivo(nombre_archivo: str, ruta: str) -> None:     # Al pasar el string de la ruta destino, poner una "r" antes del string, como si fuera la "f" de format. Ej: descargar_archivo(id_archivo, messi.jpg, r"C:\Users\Lucas\Documents\UBA\FIUBA\Algoritmos")
    
    id_archivo = obtener_id(nombre_archivo, "mimeType!='application/vnd.google-apps.folder' and trashed=False")
    nombre_separado = nombre_archivo.split(".")
    nombre_sin_extension = nombre_separado[0]

    descargar = SERVICIO.files().get_media(fileId=id_archivo)
    fh = io.BytesIO()
    media = MediaIoBaseDownload(fh, descargar)
    done = False
    while not done:
        status, done = media.next_chunk()
        print( "Download %d%%." % int(status.progress() * 100))
    
    ruta_destino = ruta

    fh.seek(0)

    with open(os.path.join(ruta_destino, nombre_archivo), "wb") as archivo:
        archivo.write(fh.read())
        archivo.close()

    fh.seek(0)
    with open(os.path.join(ruta_destino, nombre_sin_extension + ".dat"), "wb") as archivo_binario:
        pickle.dump(fh.read(), archivo_binario)
        archivo_binario.close()

def listar_por_parametro(query: str) -> list :
    archivos = []
    page_token = None
    fin = False
    while not fin:
        response = SERVICIO.files().list(q=query).execute()
        for file in response.get('files', []):

            print('\t %s' % (file.get('name')))
            
            nombre_id = []
            nombre_id.append(file.get('name'))
            nombre_id.append(file.get('id'))
            archivos.append(nombre_id)
        
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            fin = True
    
    return archivos

def navegacion_drive() -> None:
    print("Lista de Carpetas")
    print("Archivos:")
    listar_por_parametro("mimeType!='application/vnd.google-apps.folder' and trashed=False")
    
    print("Carpetas:")
    carpetas = listar_por_parametro("mimeType='application/vnd.google-apps.folder' and trashed=False")

    opcion = input("Desea navegar a otra carpeta? (s/n) ").lower()
    salir = False
    while not salir:
        if opcion == "s":
            carpeta = input("Ingrese el nombre de la carpeta a la que desea navegar aqui. ")
            id_carpeta = obtener_id(carpeta, "mimeType='application/vnd.google-apps.folder' and trashed=False")
            print("Archivos: ")
            listar_por_parametro(f"mimeType!='application/vnd.google-apps.folder' and trashed=False and '{id_carpeta}' in parents")
            print("Carpetas: ")
            listar_por_parametro(f"mimeType='application/vnd.google-apps.folder' and trashed=False and '{id_carpeta}' in parents")
            opcion = input("Desea navegar a otra carpeta? (s/n) ").lower()
        else:
            salir = True

def mover_archivo(id_archivo:str, id_carpeta_vieja: str, id_carpeta_nueva: str) -> None: # Si no se quiere remover carpetas madre, en "id_carpeta_vieja" pasar string vacio, lo mismo para agregar carpetas madre en "id_carpeta_nueva".
    
    if len(id_carpeta_vieja) != 0:
        mover = SERVICIO.files().update(fileId=id_archivo, removeParents=id_carpeta_vieja).execute()
    
    if len(id_carpeta_nueva) != 0:
        mover = SERVICIO.files().update(fileId=id_archivo, addParents=id_carpeta_nueva).execute()

def obtener_tiempo_modificacion(nombre_archivo: str) -> tuple:
    try:
        id_archivo = obtener_id(nombre_archivo, "mimeType!='application/vnd.google-apps.folder' and trashed=False")
        fecha_mod = SERVICIO.files().get(fileId=id_archivo, fields="modifiedTime").execute()

        lista_completa = fecha_mod['modifiedTime'].split("T")
        dia = lista_completa[0]
        hora_completa = lista_completa[1].split(".")
        hora_utc = hora_completa[0].split(":")
        hora_arg = str(int(hora_utc[0]) - 3)
        hora_final = [hora_arg, hora_utc[1], hora_utc[2]]
        hora_final = ":".join(hora_final)
        
        return (dia, hora_final)
    except:
        return ()

def borrar_archivo(nombre_archivo: str) -> None:
    id_archivo = obtener_id(nombre_archivo, "mimeType!='application/vnd.google-apps.folder' and trashed=False")
    response = SERVICIO.files().delete(fileId=id_archivo).execute()

def obtener_carpeta_madre(nombre_archivo:str) -> str:
    id_archivo = obtener_id(nombre_archivo, "mimeType!='application/vnd.google-apps.folder' and trashed=False")
    carpeta = SERVICIO.files().get(fileId= id_archivo, fields="parents").execute()
    id_carpeta = carpeta["parents"][0]
    nombre_carpeta = SERVICIO.files().get(fileId= id_carpeta, fields="name").execute()
    return nombre_carpeta["name"]

# Sistema Carpetas:

def crear_carpetas_local():
    nombre_carpeta=input("Ingresa el nombre de la carpeta: ")
    mkdir(nombre_carpeta)


def obtener_padrones():
    padrones={}
    with open("alumnos.csv", newline='', encoding="UTF-8") as alumnos_csv:

            csv_reader=csv.reader(alumnos_csv, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                padrones[row[1]]=row[0]
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