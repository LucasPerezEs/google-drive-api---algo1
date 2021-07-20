from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os, io

SERVICIO = obtener_servicio()
MIME_TYPES = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "pdf": "application/pdf", "txt": "text/plain", "bin": "application/octet-stream", "doc": "application/msword", "json": "application/json", "mp3": "audio/mpeg", "ppt": "application/vnd.ms-powerpoint", "rar": "application/vnd.rar", "xls": "application/vnd.ms-excel", "zip": "application/zip", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}

def definir_mime_type(nombre_archivo: str) -> str:
    nombre_separado = nombre_archivo.split(".")
    extension = nombre_separado[1]
    mime = MIME_TYPES[extension]
    
    return mime

def subir_archivo(nombre_archivo: str):
    metadata = {"name" : nombre_archivo}
    directorio = os.path.dirname(os.path.realpath(nombre_archivo))
    ruta = os.path.join(directorio, nombre_archivo)
        
    parents = []
    opcion = input("Desea crear el archivo en una carpeta? (s/n) ").lower()
    if opcion == "s":
        opcion = int(input("Desea crear una carpeta o usar una existente?\n 1_Nueva Carpeta | 2_ Carpeta Existente "))
        
        if opcion == 1:
            nombre_carpeta = input("Que nombre le desea poner a la carpeta? ")
            crear_carpeta(nombre_carpeta)
            carpeta = input("Copie y pegue el ID de la carpeta recien creada aqui. ")
            parents.append(carpeta)
        else:
            carpeta = input("Copie y pegue el ID de la carpeta donde desea crear el archivo ")
            parents.append(carpeta)
            
    if len(parents) != 0:
        metadata["parents"] = parents        

    mime = definir_mime_type(nombre_archivo)
    media = MediaFileUpload(ruta, mimetype=mime)
    subir = SERVICIO.files().create(body=metadata, media_body=media, fields="id").execute()

    if subir:
        print(f"El archivo [{nombre_archivo}] fue subido con exito. \n")

def crear_archivo():
    crear = SERVICIO.files().create().execute()
    if crear:
        print("El archivo se ha creado con exito. ")

def crear_carpeta(nombre_carpeta: str):
    metadata = {}
    
    metadata["name"] = nombre_carpeta
    
    mime_type = "application/vnd.google-apps.folder"
    metadata["mimeType"] = mime_type

    parents = []
    opcion = input("Desea crear la carpeta adentro de otra carpeta? (s/n) \n").lower()
    if opcion == "s":
        carpeta = input("Copie y pegue el ID de la carpeta en donde desea meter la carpeta. ")
        parents.append(carpeta)
        opcion = input("Desea especificar una subcarpeta? (s/n)").lower()
        while opcion == "s":
            parents.append(carpeta)
            carpeta = input("Copie y pegue el ID de la carpeta en donde desea meter la carpeta. ")
            opcion = input("Desea especificar una subcarpeta? (s/n)").lower()

    if len(parents) != 0:
        metadata["parents"] = parents

    subir = SERVICIO.files().create(body=metadata).execute()

    if subir:
        print(f"\nLa carpeta {nombre_carpeta} fue creada con exito. ")

def descargar_archivo(id_archivo: str, nombre_archivo: str):
    
    descargar = SERVICIO.files().get_media(fileId=id_archivo)
    fh = io.BytesIO()
    media = MediaIoBaseDownload(fh, descargar)
    done = False
    while done is False:
        status, done = media.next_chunk()
        print( "Download %d%%." % int(status.progress() * 100))
    
    ruta = input("Ingrese la ruta de la ubicacion donde quiere descargar el archivo ")

    fh.seek(0)

    with open(os.path.join(ruta, nombre_archivo), "wb") as archivo:
        archivo.write(fh.read())
        archivo.close()

def listar_por_parametro(query: str):
    archivos = []
    page_token = None
    while True:
        response = SERVICIO.files().list(q=query).execute()
        for file in response.get('files', []):
            # Process change
            print('\t %s (%s)' % (file.get('name'), file.get('id')))
            nombre_id = []
            nombre_id.append(file.get('name'))
            nombre_id.append(file.get('id'))
            archivos.append(nombre_id)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    
    return archivos

def navegacion_drive():
    print("Lista de Carpetas")
    print("Archivos:")
    listar_por_parametro("mimeType!='application/vnd.google-apps.folder' and trashed=False")
    
    print("Carpetas:")
    carpetas = listar_por_parametro("mimeType='application/vnd.google-apps.folder' and trashed=False")
    for i in range(len(carpetas)):
        print(f"Carpeta {i}: {carpetas[i][0]}")

    opcion = input("Desea navegar a otra carpeta? (s/n) ").lower()
    salir = False
    while not salir:
        if opcion == "s":
            id_carpeta = input("Copie y pegue el ID de la carpeta a la que desea navegar aqui. ")
            print("Archivos: ")
            listar_por_parametro(f"mimeType!='application/vnd.google-apps.folder' and trashed=False and '{id_carpeta}' in parents")
            print("Carpetas: ")
            listar_por_parametro(f"mimeType='application/vnd.google-apps.folder' and trashed=False and '{id_carpeta}' in parents")
            opcion = input("Desea navegar a otra carpeta? (s/n) ").lower()
        else:
            salir = True

navegacion_drive()
