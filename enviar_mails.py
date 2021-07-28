from email.mime.text import MIMEText
import base64
from typing import Tuple
import service_gmail
from carpetas import obtener_padrones

### FALTA DESCARGAR ZIPS


def main():

    service = service_gmail.obtener_servicio()
    
    padrones = obtener_padrones()


    numero_del_dia = input("Seleccione el numero del dia: ")
    mes = input("Seleccione el mes (Jan, May, etc): ")
    hora = input("Seleccione la hora limite: ")

    lista_fechayhora = [numero_del_dia, mes, hora]

    entrega = validar_entregas(service, padrones, lista_fechayhora)

    entregas_validas = entrega[0]
    entregas_invalidas = entrega[1]
    remitentes_validos = entrega[2]
    remitentes_invalidos = entrega[3]


    valido = True
    invalido = False
    mensaje_valido = crear_mensaje(entregas_validas, valido, remitentes_validos, service)
    mensaje_invalido = crear_mensaje(entregas_invalidas, invalido, remitentes_invalidos, service)


    for i in range(len(entregas_validas)):

        enviar_mensaje(service, mensaje_valido)

    for i in range(len(entregas_invalidas)):
        
        enviar_mensaje(service, mensaje_invalido) 


def validar_entregas(service, padrones, lista_fechayhora) -> Tuple:

    numero_dia = lista_fechayhora[0]
    mes = lista_fechayhora[1]
    hora_max = lista_fechayhora[2]


    id_mails = []
    remitentes_validos = []
    remitentes_invalidos = []
    entregas_validas = []
    entregas_invalidas = []

    mensajes = service.users().messages().list(userId='me').execute()


    for i in range(len(mensajes["messages"])):
        id = mensajes["messages"][i]["id"]
        id_mails.append(id)

    for i in range(len(id_mails)):

        messageheader= service.users().messages().get(userId="me", id= id_mails[i], format="metadata").execute()

        headers=messageheader["payload"]["headers"]
        subject= [i['value'] for i in headers if i["name"]=="Subject"]
        remitente =  [i['value'] for i in headers if i["name"]=="From"]
        fecha = [i['value'] for i in headers if i["name"]=="Date"]
        print(subject)

        asuntos = subject[0].split("-")
        fecha = fecha[0].split(" ")
        horario = fecha[4]
        horario = horario.split(":")
        
        numero = (asuntos[0])
        numero = numero[:-1]
        nombre = (asuntos[1])
        nombre = nombre[1:]
        print(fecha)

        if fecha[1] == numero_dia and fecha[2] == mes and horario[0] <= hora_max:
            if numero in padrones.keys():
                if nombre == padrones[numero]:
                    print("valida")
                    entregas_validas.append(id_mails[i])
                    remitentes_validos.append(remitente)
                else:
                    entregas_invalidas.append(id_mails[i])
                    remitentes_invalidos.append(remitente)
                    print("invalida")
            else:
                    entregas_invalidas.append(id_mails[i])
                    remitentes_invalidos.append(remitente)
                    print("invalida")
        else:
            entregas_invalidas.append(id_mails[i])
            remitentes_invalidos.append(remitente)
            print("invalida")


    return entregas_validas, entregas_invalidas, remitentes_validos, remitentes_invalidos


def crear_mensaje(entrega, booleano, remitentes, service) -> None:

    if booleano == True:

        for i in entrega:

            messageheader= service.users().messages().get(userId="me", id= i, format="metadata").execute()
            headers=messageheader["payload"]["headers"]
            remitentes =  [i['value'] for i in headers if i["name"]=="From"]
            remitentes = " ".join(remitentes)

            message_text = "Entrega valida"
            message = MIMEText(message_text)
            message['to'] = remitentes
            message['from'] = "Lucasalcuboybauti@gmail.com"
            message['subject'] = "Entrega valida"
            raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
            return {
                'raw': raw_message.decode("utf-8")
            }

    if booleano == False:

            for i in entrega:

                messageheader= service.users().messages().get(userId="me", id= i, format="metadata").execute()
                headers=messageheader["payload"]["headers"]
                remitentes =  [i['value'] for i in headers if i["name"]=="From"]
                remitentes = " ".join(remitentes)

                message_text = "Entrega invalida"
                message = MIMEText(message_text)
                message['to'] = remitentes
                message['from'] = "Lucasalcuboybauti@gmail.com"
                message['subject'] = "Entrega invalida"
                raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
                return {
                'raw': raw_message.decode("utf-8")
                }


def enviar_mensaje(service, mensaje_creado) -> None:
    try:
        message = service.users().messages().send(userId="Lucasalcuboybauti@gmail.com", body=mensaje_creado).execute()
        print('Message Id: %s' % message['id'])
        return None #message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None

main()
