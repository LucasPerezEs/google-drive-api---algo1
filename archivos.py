import os
from drive import subir_archivo, crear_archivo, descargar_archivo, listar_por_parametro, navegacion_drive
from SISTEMA_CARPETAS import crear_carpetas_local, carpetas
import zipfile
#f"mimeType!='application/vnd.google-apps.folder' and trashed=False

MENU = '''Bienvenido  al sistema de DriveHub para poder organizar las evaluaciones de sus alumnos, ¿Que desea hacer? 
        
        1.Listar archivos de la carpeta actual
        
        2.Cree un nuevo archivo
        
        3.Suba un nuevo archivo
        
        4.Descargue el archivo
        
        5.Sincronice las carpetas

        6.Generar nueva carpeta de evaluacion

        7.Actualizar las entregas de los alumnos

        8.Cerrar el programa '''


def listar_archivos():
    archivos = int(input("Para ver los archivos de una carpeta local presione 1, para ver los archivos en remoto presione 2: "))
    if archivos == 1 :
        ruta = input("Ingrese la ruta de la carpeta que desea listar: ")
        lista_de_archivos = os.listdir(ruta)
        for i in range (len(lista_de_archivos)):
            print(lista_de_archivos[i])
        opcion = input("Desea ingresar a alguna subcarpeta? (s/n) ").lower()
        if opcion == "s" :
            salir = False
            while not salir:
                ruta2 = input("Ingrese el nombre de la subcarpeta a la subcarpeta que desea entrar: ") 
                ruta_f = ruta + "\\" + ruta2
                lista_de_archivos2 = os.listdir(ruta_f)
                for i in range (len(lista_de_archivos2)):
                    print(lista_de_archivos2[i])
                opcion2 = input("Desea ingresar a alguna subcarpeta? (s/n) ").lower()
                ruta = ruta_f
                if opcion2 == "n":
                    salir = True
        
    elif archivos == 2 :
        navegacion_drive()
    
def crear_archivos():
    archivos = int(input("Para crear un archivo localmente presione 1, para crearlo remotamente (Drive) presione 2: "))
    if archivos == 1:
        eleccion = input("Si desea crear un nuevo archivo presione 1, si desea crear una nueva carpeta presione 2: ")
        if eleccion == "1":
            nombre = input("Ingrese el nombre del nuevo archivo: ")
            ruta = input("Ingrese la ruta en donde desea crear el nuevo archivo: ")
            file = open(r"{}\{}.txt".format(ruta, nombre), "w")
            escritura = input("Ingrese lo que desea que tenga el nuevo archivo: ")
            file.write(f"{escritura}" + os.linesep)
            escritura2 = input("Si desea ingresar algo mas escribalo, si no presione enter: ")
            file.write(f"{escritura2}")
            file.close()
        elif eleccion == "2": 
            crear_carpetas_local()

    elif archivos == 2:
        crear_archivo()

def subir_archivos():
    nombre = input("Ingrese el nombre y extension del archivo que desea subir: ")
    carpeta_madre = input("Si desea poner el archivo en una carpeta existente, ingrese su Nombre, si no, presione enter: ") #Corregir
    nueva_carpeta = input("Si quiere crear una nueva carpeta, ingrese el nombre: ")
    subir_archivo(nombre, carpeta_madre, nueva_carpeta)
    
def descargar_archivos (): 
    id_archivo = input("Ingrese el ID del archivo que desea descargar: ")
    nombre_archivo = input("Ingrese el nombre y extension del archivo que desea descargar: ")
    ruta = input("Copie la ruta en donde desea descargar el archivo: ")
    descargar_archivo(id_archivo, nombre_archivo, ruta)

def sincronizacion(): #FALTA
    pass

def nueva_carpeta():
    gente = carpetas()
    return gente
 
def descomprimir (ruta):

    ruta_zip = r"C:\Users\lucas\OneDrive\Escritorio\TP2\Tp-DriveHub---Lucas-al-Cubo\10 - BAUTI.zip" #PONER RUTA DONDE SE DESCAGAN LOS ZIPS
    ruta_extraccion = rf"{ruta}"
    archivo_zip = zipfile.ZipFile(ruta_zip, "r")
    password = None
    try:
        print("El archivo ZIP fue descomprimido correctamente")
        archivo_zip.extractall(pwd=password, path=ruta_extraccion)
    except:
        pass
    archivo_zip.close()

def actualizar_entregas(gente): #FALTA 
    
    DOCENTE_ALUMNO = gente[0]
    ALUMNOS_SIN_DOCENTE = gente[1]
    CARPETA = gente[2]
    
    for i in range (5) : #LARGO ENTREGAS VALIDAS
        for docente in DOCENTE_ALUMNO.keys():
            for alumno in DOCENTE_ALUMNO[docente]:
                if "BAUTI" == alumno: #ALUMNOS ENTREGAS VALIDAS
                    ruta = (f"{CARPETA}\{docente}\{alumno}")
                    descomprimir (ruta)
                    subir_archivos()
        for alumno in ALUMNOS_SIN_DOCENTE:
            if "Lucas" == alumno: 
                ruta = (f"{CARPETA}\\Alumnos sin docente\\{alumno}")
                descomprimir(ruta)
                subir_archivos()

def validar_opcion_modificacion(mensaje_input, mensaje_error, tope_inferior, tope_superior):
    '''
    Pre: Recibe mensajes de input y error, el tope inferior y el superior.
    Post:Retorna la opcion validada por el usuario
    '''
    respuesta = input(mensaje_input)
    while(not respuesta.isnumeric() or int(respuesta) > tope_superior or int(respuesta) < tope_inferior):
        print(mensaje_error)
        respuesta = input(mensaje_input)
    return int(respuesta)

def opciones(gente):
    '''
    Pre: Recibe la opcion del menu y una lista con los cursos sin asistentes al principio
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
                sincronizacion()
            elif(opcion == 6):
                gente = nueva_carpeta()
            elif(opcion == 7):
                if gente != "":
                    actualizar_entregas(gente)
                else :
                    print("Disculpe, no tenemos la informacion necesario")
        else:
            terminar_programa = True

def main():
    gente = ""
    opciones(gente)

main()
