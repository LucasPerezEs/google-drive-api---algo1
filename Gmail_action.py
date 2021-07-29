from email.mime.text import MIMEText
import base64
from typing import Tuple
import service_gmail
from Drive_action import obtener_padrones

def main():

    service = service_gmail.obtener_servicio()
    
    padrones = obtener_padrones()

    numero_del_dia = input("Seleccione el numero del dia limite: ")
    mes = input("Seleccione el mes limite (Jan, May, etc): ")
    hora = input("Seleccione la hora limite: ")

    lista_fechayhora = [numero_del_dia, mes, hora]

    entrega = validar_entregas(service, padrones, lista_fechayhora)

    entregas_validas = entrega[0]
    entregas_invalidas = entrega[1]
    remitentes_validos = entrega[2]
    remitentes_invalidos = entrega[3]


    valido = True
    invalido = False

    for i in entregas_validas:

        mensaje_valido = crear_mensaje(entregas_validas, valido, remitentes_validos, service, i)
        enviar_mensaje(service, mensaje_valido)
    
    for i in entregas_invalidas:

        mensaje_invalido = crear_mensaje(entregas_invalidas, invalido, remitentes_invalidos, service, i)
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

        messageheader= service.users().messages().get(userId="me", id= id_mails[i]).execute()

        headers=messageheader["payload"]["headers"]
        headers2 = messageheader["payload"]["parts"]
        subject= [i['value'] for i in headers if i["name"]=="Subject"]
        remitente =  [i['value'] for i in headers if i["name"]=="From"]
        fecha = [i['value'] for i in headers if i["name"]=="Date"]
        attachment_id = headers2[1]["body"]["attachmentId"]

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

        if fecha[1] <= numero_dia and fecha[2] == mes and horario[0] <= hora_max:
            if numero in padrones.keys():
                if nombre == padrones[numero]:
                    print("valida")
                    entregas_validas.append(id_mails[i])
                    remitentes_validos.append(remitente)
                    obtener_zip(service, id_mails[i], messageheader, i, attachment_id)
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


def crear_mensaje(entrega, booleano, remitentes, service, i) -> None:

    if booleano == True:

                messageheader= service.users().messages().get(userId="me", id= i).execute()
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

                messageheader= service.users().messages().get(userId="me", id= i).execute()
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
        mensaje_creado = service.users().messages().send(userId="Lucasalcuboybauti@gmail.com", body=mensaje_creado).execute()
        print('Message Id: %s' % mensaje_creado['id'])
        print("se envio tu mensaje")
        return None #message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def obtener_zip(service, id_mails, message, i, attachment_id):

    for part in message['payload']['parts']:
        if part['filename']:
            if 'data' in part['body']:
                data = part['body']['data']
            else:
                att = service.users().messages().attachments().get(userId="me", messageId=id_mails[i],id=attachment_id).execute()
                data = att['data']
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
            path = part['filename']

            with open(path, 'w') as f:
                file_data = str(file_data)
                f.write(file_data)


main()
