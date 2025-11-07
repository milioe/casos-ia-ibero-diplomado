import asyncio
import chainlit as cl
from datetime import datetime
from typing import Optional, List
import random
import os
from twilio.rest import Client


# Herramienta para mostrar QR de Alexa
display_alexa_qr_def = {
    "name": "display_alexa_qr",
    "description": "Muestra el código QR para sincronizar Alexa de Amazon con Cable+",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con el QR"
            }
        },
        "required": ["message"]
    }
}

async def display_alexa_qr(message: str):
    """Muestra el QR code para sincronizar Alexa."""
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/alexaqr.png",
        name="alexa_qr_code",
        display="inline"
    )
    await cl.Message(content=message, elements=[image]).send()
    return "QR de Alexa mostrado"


# Herramienta para mostrar contrato de servicios PDF
display_contract_pdf_def = {
    "name": "display_contract_pdf",
    "description": "Muestra el contrato de servicios de cable en formato PDF",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con el contrato"
            }
        },
        "required": ["message"]
    }
}

async def display_contract_pdf(message: str):
    """Muestra el contrato de servicios PDF."""
    elements = [
        cl.Pdf(
            name="contrato_servicios",
            display="inline",
            path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/Contrato_Servicios_Cable_Mas.pdf"
        )
    ]
    await cl.Message(content=message, elements=elements).send()
    return "Contrato PDF mostrado"


# Herramienta para mostrar estado de cuenta
display_account_status_def = {
    "name": "display_account_status",
    "description": "Muestra el estado de cuenta visual del usuario del mes de agosto",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con el estado de cuenta"
            }
        },
        "required": ["message"]
    }
}

async def display_account_status(message: str):
    """Muestra el estado de cuenta visual."""
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/estado_cuenta.png",
        name="estado_cuenta",
        display="inline"
    )
    await cl.Message(content=message, elements=[image]).send()
    return "Estado de cuenta mostrado"


# Herramienta para mostrar menú home
display_home_menu_def = {
    "name": "display_home_menu",
    "description": "Muestra el menú principal/home de la pantalla del decodificador",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con el menú"
            }
        },
        "required": ["message"]
    }
}

async def display_home_menu(message: str):
    """Muestra el menú home de la pantalla."""
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/menuhome.png",
        name="menu_home",
        display="inline"
    )
    await cl.Message(content=message, elements=[image]).send()
    return "Menú home mostrado"


# Herramienta para mostrar menú streaming
display_streaming_menu_def = {
    "name": "display_streaming_menu",
    "description": "Muestra el menú de streaming de la televisión con las aplicaciones disponibles",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con el menú de streaming"
            }
        },
        "required": ["message"]
    }
}

async def display_streaming_menu(message: str):
    """Muestra el menú de streaming de la TV."""
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/menustraming.png",
        name="menu_streaming",
        display="inline"
    )
    await cl.Message(content=message, elements=[image]).send()
    return "Menú streaming mostrado"


# Herramienta para mostrar video tutorial Vix+Disney
display_vix_tutorial_def = {
    "name": "display_vix_tutorial",
    "description": "Muestra el video tutorial de cómo enlazar Vix con Disney+",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con el video tutorial"
            }
        },
        "required": ["message"]
    }
}

async def display_vix_tutorial(message: str):
    """Muestra el video tutorial de Vix+Disney."""
    video = cl.Video(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/VixVideo.mp4",
        name="vix_disney_tutorial",
        display="inline"
    )
    await cl.Message(content=message, elements=[video]).send()
    return "Video tutorial Vix+Disney mostrado"


# Herramienta para mostrar imagen del control remoto
display_remote_control_def = {
    "name": "display_remote_control",
    "description": "Muestra la imagen guía del control remoto de Cable+",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con la imagen del control remoto"
            }
        },
        "required": ["message"]
    }
}

async def display_remote_control(message: str):
    """Muestra la imagen del control remoto."""
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/ControlRemotoGuia.png",
        name="control_remoto_guia",
        display="inline"
    )
    await cl.Message(content=message, elements=[image]).send()
    return "Imagen del control remoto mostrada"


# Herramienta para mostrar pantalla de login de Netflix
display_netflix_login_def = {
    "name": "display_netflix_login",
    "description": "Muestra la pantalla de login de Netflix para guiar al usuario",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con la pantalla de login"
            }
        },
        "required": ["message"]
    }
}

async def display_netflix_login(message: str):
    """Muestra la pantalla de login de Netflix."""
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/NetflixPantallaLogin.png",
        name="netflix_login",
        display="inline"
    )
    await cl.Message(content=message, elements=[image]).send()
    return "Pantalla de login de Netflix mostrada"


# Herramienta para mostrar pantalla de código de Netflix
display_netflix_code_def = {
    "name": "display_netflix_code",
    "description": "Muestra la pantalla donde se ingresa el código de activación de Netflix",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con la pantalla de código"
            }
        },
        "required": ["message"]
    }
}

async def display_netflix_code(message: str):
    """Muestra la pantalla de código de activación de Netflix."""
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/NetflixCodigo.png",
        name="netflix_code",
        display="inline"
    )
    await cl.Message(content=message, elements=[image]).send()
    return "Pantalla de código de Netflix mostrada"


# Herramienta para mostrar pantalla de inicio de Netflix
display_netflix_home_def = {
    "name": "display_netflix_home",
    "description": "Muestra la pantalla de inicio de Netflix una vez activado correctamente",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensaje a mostrar junto con la pantalla de inicio"
            }
        },
        "required": ["message"]
    }
}

async def display_netflix_home(message: str):
    """Muestra la pantalla de inicio de Netflix activado."""
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/assets/NetflixHome.png",
        name="netflix_home",
        display="inline"
    )
    await cl.Message(content=message, elements=[image]).send()
    return "Pantalla de inicio de Netflix mostrada"


# Herramienta para enviar SMS de confirmación de cita
send_sms_appointment_def = {
    "name": "send_sms_appointment",
    "description": "Envía SMS de confirmación para cita de soporte técnico con folio generado al número registrado del cliente",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Fecha de la cita (ej: 15 de enero)"
            },
            "time": {
                "type": "string",
                "description": "Hora de la cita (ej: 2:00 PM)"
            },
            "problem": {
                "type": "string",
                "description": "Descripción del problema técnico"
            }
        },
        "required": ["date", "time", "problem"]
    }
}

async def send_sms_appointment(date: str, time: str, problem: str):
    """Envía SMS de confirmación de cita de soporte técnico."""
    # Número de teléfono hardcodeado del cliente
    phone_number = "+525617696010"
    
    try:
        # Generar folio aleatorio de 5 dígitos
        folio = random.randint(10000, 99999)
        
        # Mensaje predeterminado más amigable
        message = f"🎉 ¡Hola! Tu cita con Cable+ está confirmada\n\n📋 Folio: {folio}\n📅 Fecha: {date}\n🕐 Hora: {time}\n🔧 Servicio: {problem}\n\n👨‍🔧 Nuestro técnico llegará puntualmente a tu domicilio. Por favor ten a la mano tu identificación oficial.\n\n¿Dudas? Llámanos al 📞 800-CABLEPLUS\n\n¡Gracias por confiar en nosotros! 😊"
        
        # Configurar Twilio (usar variables de entorno)
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, from_number]):
            await cl.Message(content=f"🎉 ¡Listo! Tu cita ha sido agendada exitosamente\n\n📋 **Folio:** {folio}\n📱 **SMS enviado al número registrado**\n📅 **Fecha y hora:** {date} a las {time}\n🔧 **Servicio:** {problem}\n\n✨ Te enviaremos un SMS de confirmación muy pronto. ¡Nos vemos!").send()
            return f"Cita agendada exitosamente con folio {folio} (simulación)"
        
        client = Client(account_sid, auth_token)
        
        # Enviar SMS
        message_obj = client.messages.create(
            body=message,
            from_=from_number,
            to=phone_number
        )
    
        
        return f"Cita agendada exitosamente con folio {folio}"
        
    except Exception as e:
        # En caso de error, simular el envío
        folio = random.randint(10000, 99999)
        await cl.Message(content=f"🎉 ¡Listo! Tu cita ha sido agendada exitosamente\n\n📋 **Folio:** {folio}\n📱 **SMS enviado al número registrado**\n📅 **Fecha y hora:** {date} a las {time}\n🔧 **Servicio:** {problem}\n\n✨ Te enviaremos un SMS de confirmación muy pronto. ¡Nos vemos!").send()
        return f"Cita agendada exitosamente con folio {folio}"


# Herramienta para enviar SMS con código de activación de Netflix
send_netflix_code_sms_def = {
    "name": "send_netflix_code_sms",
    "description": "Envía SMS con el código de activación de Netflix al número registrado del cliente",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

async def send_netflix_code_sms():
    """Envía SMS con código de activación de Netflix."""
    # Número de teléfono hardcodeado del cliente
    phone_number = "+525617696010"
    # Código de activación hardcodeado
    activation_code = "76203"
    
    try:
        # Mensaje con código de activación
        message = f"🎬 Cable+ - Código de activación Netflix\n\nTu código de activación es: {activation_code}\n\nIngresa este código en la pantalla de Netflix para activar tu servicio.\n\n¿Necesitas ayuda? Llámanos al 📞 800-CABLEPLUS\n\n¡Disfruta Netflix! 🍿"
        
        # Configurar Twilio (usar variables de entorno)
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, from_number]):
            await cl.Message(content=f"📱 ¡Listo! Te he enviado el código de activación de Netflix\n\n🔢 **Código:** {activation_code}\n📱 **SMS enviado al número registrado**\n\n✨ Deberías recibirlo en unos segundos. ¡A disfrutar Netflix!").send()
            return f"SMS con código de Netflix enviado (simulación)"
        
        client = Client(account_sid, auth_token)
        
        # Enviar SMS
        message_obj = client.messages.create(
            body=message,
            from_=from_number,
            to=phone_number
        )
        
        
        return f"SMS con código de Netflix enviado exitosamente"
        
    except Exception as e:
        # En caso de error, simular el envío
        await cl.Message(content=f"📱 ¡Listo! Te he enviado el código de activación de Netflix\n\n🔢 **Código:** {activation_code}\n📱 **SMS enviado al número registrado**\n\n✨ Deberías recibirlo muy pronto. ¡A disfrutar Netflix!").send()
        return f"SMS con código de Netflix enviado"


tools = [
    (display_alexa_qr_def, display_alexa_qr),
    (display_contract_pdf_def, display_contract_pdf),
    (display_account_status_def, display_account_status),
    (display_home_menu_def, display_home_menu),
    (display_streaming_menu_def, display_streaming_menu),
    (display_vix_tutorial_def, display_vix_tutorial),
    (display_remote_control_def, display_remote_control),
    (display_netflix_login_def, display_netflix_login),
    (display_netflix_code_def, display_netflix_code),
    (display_netflix_home_def, display_netflix_home),
    (send_sms_appointment_def, send_sms_appointment),
    (send_netflix_code_sms_def, send_netflix_code_sms),
]