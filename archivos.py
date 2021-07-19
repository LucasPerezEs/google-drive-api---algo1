import os







def listar_archivo():
    archivos = int(input("Para ver los archivos en local presione 1, para ver los archivos en remoto presione 2: "))
    while archivos == 1:
        lista_de_archivos = os.listdir(ruta_de_la_carpeta)
    pass


def crear_archivo():
    
    file = open("/ruta/filename.txt", "w")
    file.write("Primera línea" + os.linesep)
    file.write("Segunda línea")
    file.close()

def subir_archivo():
    pass

def descarga_archivos():
    pass

def sincronizacion():
    pass

def nueva_carpeta():
    pass

def actualizar_entregas():
    pass


def opciones(opcion, cursos):
    '''
    Pre: Recibe la opcion del menu y una lista con los cursos sin asistentes al principio
    '''
    if(opcion == 1):
        listar_archivo()
    elif(opcion == 2):
        crear_archivo()
    elif(opcion == 3):
        subir_archivo()
    elif(opcion == 4):
        descarga_archivos()
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

        opcion = #validar_opcion_modificacion('Ingrese una opcion: ', 'Ingreso invalido', 1, 8)
        if(opcion != 8):
            opciones(opcion)
        else:
            terminar_programa = True

main()