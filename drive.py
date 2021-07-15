from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload
import os

SERVICIO = obtener_servicio()

def crear_archivo():
    name = input("Ingrese el nombre (con la extension) del archivo que desea crear: ")
    metadata = {"name" : name}

    directorio = os.path.dirname(os.path.realpath(name))
    ruta = os.path.join(directorio, name)
    
    parents = []
    carpeta = input("Si desea que el archivo este adentro de una carpeta en Drive, copie y pegue el ID de la misma aqui. De lo contrario, presione ENTER. ")
    while carpeta != "":
        parents.append(carpeta)
        carpeta = input("Si desea crear el archivo en otra subcarpeta, copie y pegue el ID de la misma aqui. ")
    
    if len(parents) != 0:
        metadata["parents"] = parents        

    media = MediaFileUpload(ruta, mimetype="image/jpeg")
    subir = SERVICIO.files().create(body=metadata, media_body=media, fields="id").execute()

    if subir:
        print(f"{name} fue subido con exito. \n")

crear_archivo()
