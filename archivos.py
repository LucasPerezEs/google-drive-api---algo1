import os
from drive import subir_archivo, crear_archivo, descargar_archivo, listar_por_parametro, crear_carpeta
#f"mimeType!='application/vnd.google-apps.folder' and trashed=False


def listar_archivos(query):
    archivos = int(input("Para ver los archivos en local presione 1, para ver los archivos en remoto presione 2: "))
    if archivos == 1 :
        lista_de_archivos = os.listdir('RUTA CARPETA')
    elif archivos == 2 :
        listar_por_parametro(query)
    
def crear_archivos():
    archivos = int(input("Para crear un archivo localmente presione 1, para crearlo remotamente (Drive) presione 2: "))
    if archivos == 1: #CREAR CARPETA TMBIEN
        nombre = input("Ingrese el nombre del nuevo archivo: ")
        file = open(r"C:\Users\lucas\OneDrive\Escritorio\TP2\Evaluaciones\{}.txt".format(nombre), "w")
        file.write("Primera línea" + os.linesep) #ESCRIBIR LO QUE SE TE OCURRA
        file.write("Segunda línea")
        file.close()

    elif archivos == 2:
        crear_archivo()

def subir_archivos(): #PREGUNTAR SI SIRVE PARA PUNTO 7
    nombre = input("Ingrese el nombre y extension del archivo que desea subir: ")
    carpeta_madre = input("Si desea poner el archivo en una carpeta existente, ingrese su ID, si no, presione enter: ") #Corregir
    nueva_carpeta = input("Si quiere crear una nueva carpeta, ingrese el nombre: ")
    subir_archivo(nombre, carpeta_madre,nueva_carpeta)
    
def descargar_archivos (): 
    id_archivo = input("Ingrese el ID del archivo que desea descargar: ")
    nombre_archivo = input("Ingrese el nombre y extension del archivo que desea descargar: ")
    ruta = input("Copie la ruta en donde desea descargar el archivo: ")
    descargar_archivo(id_archivo, nombre_archivo, ruta)

def sincronizacion():
    pass

def nueva_carpeta():
    archivos = int(input("Para crear un archivo localmente presione 1, para crearlo remotamente (Drive) presione 2: "))
    while archivos == 1:
        pass
    while archivos == 2:()

def actualizar_entregas():
    pass

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

def opciones(opcion):
    '''
    Pre: Recibe la opcion del menu y una lista con los cursos sin asistentes al principio
    '''
    if(opcion == 1):
        listar_archivos(f"mimeType!='application/vnd.google-apps.folder' and trashed=False")
    elif(opcion == 2):
        crear_archivos()
    elif(opcion == 3):
        subir_archivos()
    elif(opcion == 4):
        descargar_archivos()
    elif(opcion == 5):
        sincronizacion()
    elif(opcion == 6):
        nueva_carpeta()
    elif(opcion == 7):
        actualizar_entregas()

def main():
    terminar_programa = False
    while(terminar_programa == False):
        print('''Bienvenido  al sistema de DriveHub para poder organizar las evaluaciones de sus alumnos, ¿Que desea hacer? 
        
        1.Listar archivos de la carpeta actual
        
        2.Cree un nuevo archivo
        
        3.Suba un nuevo archivo
        
        4.Descargue el archivo
        
        5.Sincronice las carpetas

        6.Generar nueva carpeta de evaluacion

        7.Actualizar las entregas de los alumnos

        8.Cerrar el programa ''')

        opcion = validar_opcion_modificacion('Ingrese una opcion: ', 'Ingreso invalido', 1, 8)
        if(opcion != 8):
            opciones(opcion)
        else:
            terminar_programa = True

main()