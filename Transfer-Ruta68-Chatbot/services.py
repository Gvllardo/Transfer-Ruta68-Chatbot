import requests
import sett
import json

def obtener_Mensaje_Whatsapp(message):
    if 'type' not in message:
        text = 'Mensaje no reconocido'
        return text
    
    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'Mensaje no reconocido'

    return text

def enviar_mensaje_Whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json', 
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("Se envia ", data)
        response = requests.post(whatsapp_url, headers=headers, data=data)
        
        if response.status_code == 200:
            return 'Mensaje enviado', 200
        else:
            return 'Error al enviar el mensaje', response.status_code
    except Exception as ex:
        return ex,403
    
def text_message(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                },
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        },
                    ]
                }
            }
        }
    )
    return data

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {"message_id": messageId},
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": messageId
        }
    )
    return data

def administrar_chatbot(text, number, messageId, name):
    text = text.lower() #Mensaje que envio el usuario
    list = []

    if "hola" in text:
        body = "¡Hola! 👋 Bienvenid@ a Transfer Ruta 68 ¿Cómo podemos ayudarte hoy?"
        footer = "Equipo de Transfer Ruta 68"
        options = ["🚐 servicios", "📅 preguntar disponibilidad"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
        replyReaction = replyReaction_Message(number, messageId, "✅")
        list.append(replyReaction)
        list.append(replyButtonData) 
    elif "servicios" in text:
        body = "Estos son nuestros servicios disponibles:"
        footer = "Equipo de Transfer Ruta 68"
        options = ["Traslado privado al Aeropuerto", "Traslados a matrimonios"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2", messageId)
        replyReaction = replyReaction_Message(number, messageId, "✅")
        list.append(replyReaction)
        list.append(listReplyData)
    elif "traslado privado" in text:
        body = "Ofrecemos un servicio directo privado desde u hacia el Aeropuerto de Santiago a turistas nacionales y extranjeros, las 24 horas del día con previa reserva de nuestros servicios"
        footer = "Equipo de Transfer Ruta 68"
        options = ["⬅️ Volver"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3", messageId)
        replyReaction = replyReaction_Message(number, messageId, "✅")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "volver" in text:
        administrar_chatbot("hola", number, messageId, name)
    else:
        data = text_message(number, "Lo siento, no entendi lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)

    for item in list:
        enviar_mensaje_Whatsapp(item)

    data = text_message(number, "hola mundo")
    enviar_mensaje_Whatsapp(data)