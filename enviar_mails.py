from email.mime.text import MIMEText
import base64
from typing import Tuple
import service_gmail
import usuarioycontrasenia


def main():

    service = service_gmail.obtener_servicio()

    entrega = validar_entregas(service)

    entregas_validas = entrega[0]
    entregas_invalidas = entrega[1]
    valido = True
    falso = False

    mensaje_valido = crear_mensaje(entregas_validas, valido)
    mensaje_invalido = crear_mensaje(entregas_invalidas, falso)

    enviar_mensaje(service, mensaje_valido)
    enviar_mensaje(service, mensaje_invalido)

def crear_mensaje(entrega, estado):

    if estado == True:
    #entrega = validar_entregas(service)

        for i in entrega:

            message_text = "Entrega valida"
            message = MIMEText(message_text)
            message['to'] = usuarioycontrasenia.username
            message['from'] = usuarioycontrasenia.username
            message['subject'] = "Entrega valida"
            raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
            return {
                'raw': raw_message.decode("utf-8")
            }

    else:
            for i in entrega:

                message_text = "Entrega invalida"
                message = MIMEText(message_text)
                message['to'] = usuarioycontrasenia.username
                message['from'] = usuarioycontrasenia.username
                message['subject'] = "Entrega invalida"
                raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
                return {
                    'raw': raw_message.decode("utf-8")
                }

def validar_entregas(service):

    mensajes = service.users().messages().list(userId='me').execute()

    id_mails = []

    for i in range(len(mensajes["messages"])):
        id = mensajes["messages"][i]["id"]
        id_mails.append(id)

    entregas_validas = []
    entregas_invalidas = []

    for i in range(len(id_mails)):

        messageheader= service.users().messages().get(userId="me", id= id_mails[i], format="metadata").execute()

        headers=messageheader["payload"]["headers"]
        subject= [i['value'] for i in headers if i["name"]=="Subject"]
        print(subject)

        asuntos = subject[0].split("-")

        try:
            numero = int(asuntos[0])
            if numero > 0:
                print("ok")
                entregas_validas.append(id_mails[i])
            #if asuntos[1] in #csv   VERIFICAR QUE ALUMNO ESTE EN LA CATEDRA
        except:
            entregas_invalidas.append(id_mails[i])
            print(asuntos)

    return entregas_validas, entregas_invalidas

def enviar_mensaje(service, mensaje_creado):
    try:
        message = service.users().messages().send(userId=usuarioycontrasenia.username, body=mensaje_creado).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None

main()