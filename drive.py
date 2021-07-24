from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os, io
import pickle

SERVICIO = obtener_servicio()

MIME_TYPES = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "pdf": "application/pdf", "txt": "text/plain", "bin": "application/octet-stream", "doc": "application/msword", "json": "application/json", "mp3": "audio/mpeg", "ppt": "application/vnd.ms-powerpoint", "rar": "application/vnd.rar", "xls": "application/vnd.ms-excel", "zip": "application/zip", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}

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

def subir_archivo(nombre_archivo: str, nombre_carpeta_madre: str, nombre_carpeta_nueva: str): # Si no quiere subir el archivo adentro de una carpeta, en "nombre_carpeta_madre" pasar string vacio. Si no quiere subir el archivo en una carpeta nueva, en "nombre_carpeta_nueva" pasar string vacio. 
    id_carpeta_madre = obtener_id(nombre_carpeta_madre, f"mimeType='application/vnd.google-apps.folder' and trashed=False")
    metadata = {"name" : nombre_archivo}
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

def crear_archivo(): # Hacer que escriba algo
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

    if subir:
        print(f"\nLa carpeta {nombre_carpeta} fue creada con exito. ")
    
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

            print('\t %s (%s) (%s)' % (file.get('name'), file.get('id'), file.get('modifiedTime')))
            
            nombre_id = []
            nombre_id.append(file.get('name'))
            nombre_id.append(file.get('id'))
            archivos.append(nombre_id)
        
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            fin = True
    
    return archivos

def navegacion_drive():
    print("Lista de Carpetas")
    print("Archivos:")
    listar_por_parametro("mimeType!='application/vnd.google-apps.folder' and trashed=False")
    
    print("Carpetas:")
    carpetas = listar_por_parametro("mimeType='application/vnd.google-apps.folder' and trashed=False")
    #for i in range(len(carpetas)):
    #    print(f"Carpeta {i}: {carpetas[i][0]}")

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

def mover_archivo(id_archivo:str, id_carpeta_vieja: str, id_carpeta_nueva: str): # Si no se quiere remover carpetas madre, en "id_carpeta_vieja" pasar string vacio, lo mismo para agregar carpetas madre en "id_carpeta_nueva".
    
    if len(id_carpeta_vieja) != 0:
        mover = SERVICIO.files().update(fileId=id_archivo, removeParents=id_carpeta_vieja).execute()
    
    if len(id_carpeta_nueva) != 0:
        mover = SERVICIO.files().update(fileId=id_archivo, addParents=id_carpeta_nueva).execute()    

descargar_archivo("caracreeper.jpg", r"C:\Users\Lucas\Documents\UBA\FIUBA\Algoritmos\Repositorios\DriveHub\Tp-DriveHub---Lucas-al-Cubo\Primer Parcial 2021")