import os
import os.path, time
import zipfile
from datetime import date, datetime
from Drive_actions import  crear_carpetas_local, carpetas, obtener_carpeta_madre , listar_por_parametro, obtener_id, subir_archivo, crear_archivo, descargar_archivo, obtener_tiempo_modificacion, borrar_archivo, navegacion_drive, MIME_TYPES

MENU = '''
Bienvenido  al sistema de DriveHub para poder organizar las evaluaciones de sus alumnos, ¿Que desea hacer? 
        
        1.Listar archivos de la carpeta actual
        
        2.Cree un nuevo archivo
        
        3.Suba un nuevo archivo
        
        4.Descargue el archivo
        
        5.Sincronice las carpetas

        6.Generar nueva carpeta de evaluacion

        7.Actualizar las entregas de los alumnos

        8.Cerrar el programa '''

def listar_archivos()-> None:
    archivos = int(input("Para ver los archivos de una carpeta local presione 1, para ver los archivos en remoto presione 2: "))
    navegar_carpetas_local(archivos)

def navegar_carpetas_local(archivos: int)-> None:
    if archivos == 1 :
        ruta = os.getcwd()
        lista_de_archivos = os.listdir(ruta)
        for i in range (len(lista_de_archivos)):
            print(lista_de_archivos[i])
        opcion = int(input("Si desea ingresar a alguna subcarpeta presione 1, si no, presione 2: "))
        subcarpetas_local(opcion, ruta)
    
    elif archivos == 2 :
        navegacion_drive()

def subcarpetas_local(opcion: int, ruta: str)-> None:
    if opcion == 1 :
            salir = False
            while not salir:
                ruta2 = input("Ingrese el nombre de la subcarpeta a la subcarpeta que desea entrar: ") 
                ruta_f = ruta + "\\" + ruta2
                lista_de_archivos2 = os.listdir(ruta_f)
                for i in range (len(lista_de_archivos2)):
                    print(lista_de_archivos2[i])
                opcion2 = int(input("Si desea ingresar a alguna subcarpeta presione 1, si no, presione 2: "))
                ruta = ruta_f
                if opcion2 == 2:
                    salir = True

def crear_archivos()-> None:
    archivos = int(input("Para crear un archivo localmente presione 1, para crearlo remotamente (Drive) presione 2: "))
    if archivos == 1:
        eleccion = input("Si desea crear un nuevo archivo presione 1, si desea crear una nueva carpeta presione 2: ")
        if eleccion == "1":
            nombre = input("Ingrese el nombre del nuevo archivo: ")
            extension = input("Ingrese la extension que desea para crear el nuevo archivo: ")
            if extension in MIME_TYPES.keys():
                ruta = input("Ingrese la ruta en donde desea crear el nuevo archivo: ")
                file = open(r"{}\{}.{}".format(ruta, nombre, extension), "w")
                if extension == "txt" : 
                    escritura = input("Ingrese lo que desea que tenga el nuevo archivo: ")
                    file.write(f"{escritura}" + os.linesep)
                    escritura2 = input("Si desea ingresar algo mas escribalo, si no presione enter: ")
                    file.write(f"{escritura2}")
                    file.close()
                else :
                    file.close()

            else :
                print("Error, esa extension no esta permitida, por favor escoja otra: ")
                crear_archivos()
        elif eleccion == "2": 
            crear_carpetas_local()

    elif archivos == 2:
        crear_archivo()

def subir_archivos()-> None:
    nombre = input("Ingrese el nombre y extension del archivo que desea subir: ")
    carpeta_madre = input("Si desea poner el archivo en una carpeta existente, ingrese su Nombre, si no, presione enter: ") #Corregir
    nueva_carpeta = input("Si quiere crear una nueva carpeta, ingrese el nombre: ")
    subir_archivo(nombre, carpeta_madre, nueva_carpeta, "")
    
def descargar_archivos ()-> None: 
    nombre_archivo = input("Ingrese el nombre y extension del archivo que desea descargar: ")
    ruta = input("Copie la ruta en donde desea descargar el archivo: ")
    descargar_archivo(nombre_archivo, ruta)

def obtener_lista_archivos(ruta: str)-> list:
    lista_archivos = os.listdir(ruta)
    archivos_totales = list()

    for archivo in lista_archivos:
        ruta_nueva = os.path.join(ruta, archivo)
        
        if os.path.isdir(ruta_nueva):
            archivos_totales = archivos_totales + obtener_lista_archivos(ruta_nueva)
        else:
            archivos_totales.append(ruta_nueva)
    
    return archivos_totales

def sincronizacion(ruta: str)-> None:
    ruta_sinc = rf"{ruta}"
    archivos_local = obtener_lista_archivos(ruta_sinc)
    for i in range(len(archivos_local)):
        ruta_archivo = archivos_local[i]
        nombre_separado = ruta_archivo.split("\\")
        nombre_archivo = nombre_separado[len(nombre_separado)-1]
        nombre_carpeta = nombre_separado[len(nombre_separado)-2]
        fecha = time.ctime(os.path.getmtime(ruta_archivo))
        informacion_fecha = fecha.split()
        informacion_fecha2 = " ".join([informacion_fecha[4], informacion_fecha[1], informacion_fecha[2]])
        horario = informacion_fecha[3]
        fecha_correcta = cambiar_formato(informacion_fecha2)
        fecha_modificacion = (fecha_correcta, horario)
        fecha_modificacion_drive = obtener_tiempo_modificacion(nombre_archivo)
        if len(fecha_modificacion_drive) == 0:
            print(f"El archivo {nombre_archivo} no estaba en el Drive.")
            subir_archivo(nombre_archivo, nombre_carpeta, "", ruta_archivo)
        else: 
            comparar_archivos(nombre_archivo, fecha_modificacion_drive, fecha_modificacion, ruta_archivo, nombre_carpeta)
    print("Los Archivos fueron sincronizados exitosamente")

def cambiar_formato (informacion_fecha2: tuple)-> str:
    meses = {"Jan" : "01" , "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", "Jul" : "07", "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12" }
    informacion_fecha = informacion_fecha2.split()
    mes = informacion_fecha[1]
    mes = meses[mes]
    horario_cambiado = [informacion_fecha[0], mes, informacion_fecha[2]]
    horario_cambiado = "-".join(horario_cambiado)
    return horario_cambiado

def comparar_fechas (fecha_drive: list, fecha_local: list, nombre_archivo: str, ruta: str, nombre_carpeta: str)-> bool:
    dia_drive = fecha_drive.split("-")
    dia_drive = (int(dia_drive[0]), int(dia_drive[1]), int(dia_drive[2]))
    dia_local = fecha_local.split("-")
    dia_local = (int(dia_local[0]), int(dia_local[1]), int(dia_local[2]))
    local_date = date(dia_local[0], dia_local[1], dia_local[2])
    drive_date = date(dia_drive[0], dia_drive[1], dia_drive[2])
    delta = drive_date - local_date
    if delta.days != 0:
        if delta.days > 0:
            print(f"La version mas nueva de {nombre_archivo} es del drive")
            ruta_separada = ruta.split("\\")
            ruta_separada.pop()
            ruta_f = "\\".join(ruta_separada)
            descargar_archivo(nombre_archivo, ruta_f)
            return True
        else :
            print(f"La version mas nueva de {nombre_archivo} es la local")
            borrar_archivo(nombre_archivo)
            subir_archivo(nombre_archivo, nombre_carpeta, "", ruta)
            return True
    else :
        return False

def comparar_hora (hora_drive: str, hora_local: str, nombre_archivo: str, ruta: str, nombre_carpeta: str)-> bool: 
    h_drive = hora_drive.split(":")
    h_drive = (str(h_drive[0]), str(h_drive[1]), str(h_drive[2]))
    h_local = hora_local.split(":")
    h_local = (str(h_local[0]), str(h_local[1]), str(h_local[2]))
    FMT = '%H:%M:%S'
    tdelta = (datetime.strptime(hora_drive, FMT) - datetime.strptime(hora_local, FMT)).total_seconds()
    if tdelta > 60 or tdelta < -60:
        if tdelta > 0:
            print(f"La version mas nueva de {nombre_archivo} es del drive")
            ruta_separada = ruta.split("\\")
            ruta_separada.pop()
            ruta_f = "\\".join(ruta_separada)
            descargar_archivo(nombre_archivo, ruta_f)
            return True
        else :
            print(f"La version mas nueva de {nombre_archivo} es la local")
            borrar_archivo(nombre_archivo)
            subir_archivo(nombre_archivo, nombre_carpeta, "", ruta)
            return True
    else :
        return False

def comparar_archivos (nombre_archivo: str, fecha_modificacion_drive: str, fecha_modificacion_local: str, ruta: str, nombre_carpeta: str)-> None:
    fecha_drive = fecha_modificacion_drive[0]
    horario_drive = fecha_modificacion_drive[1]
    fecha_local = fecha_modificacion_local[0]
    horario_local = fecha_modificacion_local[1]
    actualizado = comparar_fechas(fecha_drive, fecha_local, nombre_archivo, ruta, nombre_carpeta)
    if not actualizado :
        comparar_hora(horario_drive, horario_local, nombre_archivo, ruta, nombre_carpeta)
    
def nueva_carpeta()-> tuple:
    '''
    Pre : 
    Post : Crea una nueva carpeta con el nombre seleccionado, y retorna una variable (tupla) que contiene a los alumnos y
    docentes de la materia
    '''
    datos = carpetas()
    return datos
 
def descomprimir (ruta: str)-> None:
    '''
    Post : Extrae el ZIP de la ruta seleciconada, a la ruta de extraccion
    '''
    ruta_z = input("Ingrese la ruta en donde esta el zip: ")
    nombrezip = input("Ingrese el nombre del ZIP con su debida extension: ")
    ruta_zip = rf"{ruta_z}" + "\\"+rf"{nombrezip}"
    ruta_extraccion = rf"{ruta}"
    archivo_zip = zipfile.ZipFile(ruta_zip, "r")
    password = None
    try:
        print("El archivo ZIP fue descomprimido correctamente")
        archivo_zip.extractall(pwd=password, path=ruta_extraccion)
    except:
        print("Hubo un problema con la extraccion del ZIP, lo volveremos a intentar")
        descomprimir(ruta)
    archivo_zip.close()

def actualizar_entregas(datos: tuple) -> None: #FALTAAAAAAAAAAAAAAAA
    
    DOCENTE_ALUMNO = datos[0]
    ALUMNOS_SIN_DOCENTE = datos[1]
    CARPETA = datos[2]

    #lista_zips = lista con todos los nombres de los zips validos recibidos
    #for i in range (len(lista_zips)):

    for i in range (5) : #LARGO ENTREGAS VALIDAS
        for docente in DOCENTE_ALUMNO.keys():
            for alumno in DOCENTE_ALUMNO[docente]:
                if "BAUTI" == alumno: #ALUMNOS ENTREGAS VALIDAS
                    ruta = (f"{CARPETA}\{docente}\{alumno}")
                    ruta_madre = os.getcwd()
                    ruta_archivo = os.path.join(ruta_madre, ruta)
                    descomprimir (ruta)
                    archivos_alumno = os.listdir(ruta)
                    for i in range (len(archivos_alumno)):
                        ruta_final = os.path.join(ruta_archivo, archivos_alumno[i])
                        subir_archivo(archivos_alumno[i], alumno, "", ruta_final)
        for alumno in ALUMNOS_SIN_DOCENTE:
            if "Lucas" == alumno: 
                ruta = (f"{CARPETA}\\Alumnos sin docente\\{alumno}")
                ruta_madre = os.getcwd()
                ruta_archivo = os.path.join(ruta_madre, ruta)
                descomprimir(ruta)
                archivos_alumno = os.listdir(ruta)
                for i in range (len(archivos_alumno)):
                    ruta_final = os.path.join(ruta_archivo, archivos_alumno[i])
                    subir_archivo(archivos_alumno[i], alumno, "", ruta_final)

def validar_opcion_modificacion(mensaje_input: str, mensaje_error: str, tope_inferior: int, tope_superior: int)-> int:
    '''
    Pre: Recibe mensajes de input y error, el tope inferior y el superior.
    Post:Retorna la opcion validada por el usuario
    '''
    respuesta = input(mensaje_input)
    while(not respuesta.isnumeric() or int(respuesta) > tope_superior or int(respuesta) < tope_inferior):
        print(mensaje_error)
        respuesta = input(mensaje_input)
    return int(respuesta)

def opciones(datos: tuple)-> None:
    '''
    Pre: Recibe la opcion del menu 
    Post : Lo lleva a la funcion que selecciono en el menu
    '''
    terminar_programa = False
    while(terminar_programa == False):
        print (MENU)
        opcion = validar_opcion_modificacion('Ingrese una opcion: ', 'Ingreso invalido', 1, 8)
        if(opcion != 8):
            if(opcion == 1):
                listar_archivos()
            elif(opcion == 2):
                crear_archivos()
            elif(opcion == 3):
                subir_archivos()
            elif(opcion == 4):
                descargar_archivos()
            elif(opcion == 5):
                ruta = input("Ingrese la ruta en la que desea realizar la sincronizacion: ")
                sincronizacion(ruta)
            elif(opcion == 6):
                datos = nueva_carpeta()
                print("Las carpetas fueron creadas con exito")
            elif(opcion == 7):
                if datos != "":
                    actualizar_entregas(datos)
                else :
                    print("Disculpe, no tenemos la informacion necesaria")
        else:
            terminar_programa = True

def main():
    datos = ""
    opciones(datos)   

main()