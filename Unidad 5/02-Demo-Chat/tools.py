import json
import os
import random
import smtplib
import io
import base64
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pyairtable import Api
from jinja2 import Template
from twilio.rest import Client
from email_templates import CONFIRMACION_CITA_TEMPLATE, FACTURA_TEMPLATE
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(".env")

# Cliente OpenAI para análisis de imágenes
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analizar_imagen(ruta_imagen):
    """
    Analiza una imagen usando GPT-4o y retorna una descripción detallada.
    Esta herramienta se usa cuando el usuario adjunta una imagen (factura, equipo, etc.)
    """
    try:
        # Leer la imagen desde el path
        with open(ruta_imagen, 'rb') as f:
            image_bytes = f.read()
        
        # Convertir a base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Detectar tipo MIME
        if ruta_imagen.lower().endswith('.png'):
            mime_type = "image/png"
        elif ruta_imagen.lower().endswith(('.jpg', '.jpeg')):
            mime_type = "image/jpeg"
        else:
            mime_type = "image/jpeg"
        
        # Llamar a GPT-4o-mini (más rápido y económico) para analizar la imagen
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Analiza imágenes de telecomunicaciones: facturas, equipos, capturas. Sé preciso y conciso."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe esta imagen brevemente: si es factura menciona planes, montos, fechas, IVA y total. Si es equipo menciona luces y estado. Máximo 200 palabras."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}",
                                "detail": "low"  # Procesamiento más rápido
                            }
                        }
                    ]
                }
            ],
            max_tokens=500,  # Reducido de 1000 a 500
            temperature=0.3  # Más determinista = más rápido
        )
        
        descripcion = response.choices[0].message.content
        
        return json.dumps({
            "success": True,
            "descripcion": descripcion,
            "mensaje": "Imagen analizada exitosamente"
        })
    except Exception as e:
        return json.dumps({
            "error": f"Error al analizar imagen: {str(e)}",
            "success": False
        })


def obtener_info_cliente(id_cliente):
    """Obtiene la información completa de un cliente desde Airtable."""
    try:
        api = Api(os.getenv("AIRTABLE_API_KEY"))
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = os.getenv("AIRTABLE_CLIENTES_TABLE_NAME")
        
        table = api.table(base_id, table_name)
        
        # Buscar cliente por id_cliente
        formula = f"{{id_cliente}}='{id_cliente}'"
        records = table.all(formula=formula)
        
        if not records:
            return json.dumps({
                "encontrado": False,
                "mensaje": f"No se encontró ningún cliente con ID {id_cliente}"
            })
        
        # Tomar el primer registro encontrado
        cliente = records[0]["fields"]
        
        return json.dumps({
            "encontrado": True,
            "id_cliente": id_cliente,
            "nombre": cliente.get("nombre", ""),
            "apellido": cliente.get("apellido", ""),
            "telefono": cliente.get("telefono", ""),
            "email": cliente.get("email", ""),
            "direccion": cliente.get("direccion", ""),
            "mensaje": f"Cliente {cliente.get('nombre', '')} {cliente.get('apellido', '')} encontrado exitosamente"
        })
    except Exception as e:
        return json.dumps({
            "error": f"Error al consultar cliente: {str(e)}",
            "encontrado": False
        })


def obtener_contratos_cliente(id_cliente, filtro_status=None):
    """Obtiene los contratos/planes de un cliente desde Airtable, con opción de filtrar por status."""
    try:
        api = Api(os.getenv("AIRTABLE_API_KEY"))
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = os.getenv("AIRTABLE_CONTRATOS_TABLE_NAME")
        
        table = api.table(base_id, table_name)
        
        # Buscar contratos donde id_cliente coincida
        if filtro_status and filtro_status.lower() in ["activo", "inactivo"]:
            formula = f"AND({{id_cliente}}='{id_cliente}', {{status}}='{filtro_status.capitalize()}')"
        else:
            formula = f"{{id_cliente}}='{id_cliente}'"
        
        records = table.all(formula=formula)
        
        if not records:
            mensaje_filtro = f" con status {filtro_status}" if filtro_status else ""
            return json.dumps({
                "encontrado": False,
                "total_contratos": 0,
                "mensaje": f"No se encontraron contratos{mensaje_filtro} para el cliente {id_cliente}"
            })
        
        # Formatear contratos (incluir id_contrato para uso interno, pero no mostrarlo al usuario)
        contratos = []
        for record in records:
            fields = record["fields"]
            contratos.append({
                "id_contrato": fields.get("id_contrato", ""),  # Para uso interno
                "nombre_contrato": fields.get("nombre_contrato", ""),
                "descripcion": fields.get("descripcion", ""),
                "pago_mensual": fields.get("pago_mensual", ""),
                "status": fields.get("status", ""),
                "fecha_pago": fields.get("fecha_pago", "")
            })
        
        return json.dumps({
            "encontrado": True,
            "id_cliente": id_cliente,
            "total_contratos": len(contratos),
            "contratos": contratos,
            "filtro_aplicado": filtro_status or "todos",
            "mensaje": f"Se encontraron {len(contratos)} contrato(s) para el cliente {id_cliente}"
        })
    except Exception as e:
        return json.dumps({
            "error": f"Error al consultar contratos: {str(e)}",
            "encontrado": False
        })


def agendar_cita(id_cliente, nombre, apellido, descripcion_problema, sucursal, fecha_reporte=None):
    """Agenda una cita técnica en Airtable."""
    try:
        # Generar ID de cita aleatorio de 5 dígitos
        id_cita = random.randint(10000, 99999)
        
        # Procesar fecha y hora
        if not fecha_reporte:
            fecha_reporte = datetime.now().isoformat()
        else:
            # Convertir fecha recibida a formato ISO con zona horaria
            try:
                # Intentar parsear el formato que GPT envía
                fecha_obj = datetime.strptime(fecha_reporte, "%Y-%m-%d %H:%M:%S")
                fecha_reporte = fecha_obj.isoformat()
            except:
                # Si ya está en otro formato, dejarlo como está
                pass
        
        api = Api(os.getenv("AIRTABLE_API_KEY"))
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = os.getenv("AIRTABLE_CITAS_TABLE_NAME")
        
        table = api.table(base_id, table_name)
        
        # Convertir id_cliente a número si es posible
        try:
            id_cliente_num = int(id_cliente)
        except:
            id_cliente_num = id_cliente
        
        # Crear registro en Airtable
        record = table.create({
            "id_cita": id_cita,
            "id_cliente": id_cliente_num,
            "nombre": nombre,
            "apellido": apellido,
            "descripcion_problema": descripcion_problema,
            "sucursal": sucursal,
            "fecha_reporte": fecha_reporte
        })
        
        return json.dumps({
            "success": True,
            "id_cita": id_cita,
            "id_cliente": id_cliente,
            "nombre_completo": f"{nombre} {apellido}",
            "descripcion_problema": descripcion_problema,
            "sucursal": sucursal,
            "fecha_reporte": fecha_reporte,
            "airtable_record_id": record["id"],
            "mensaje": f"Cita agendada exitosamente con ID {id_cita} en sucursal {sucursal}. Recibirá confirmación pronto."
        })
    except Exception as e:
        return json.dumps({
            "error": f"Error al agendar cita: {str(e)}",
            "success": False
        })


def enviar_confirmacion_cita(email_cliente, nombre, apellido, id_cita, fecha_hora, sucursal, descripcion):
    """Envía correo de confirmación de cita al cliente."""
    try:
        # Mapa de direcciones de sucursales
        direcciones_sucursales = {
            "Tlalpan": "Av. Insurgentes Sur 4000, Tlalpan, CDMX",
            "Coyoacán": "Av. Universidad 1200, Coyoacán, CDMX",
            "Venustiano Carranza": "Av. Circunvalación 500, Venustiano Carranza, CDMX",
            "Benito Juárez": "Av. Insurgentes Sur 1500, Benito Juárez, CDMX",
            "Xochimilco": "Av. Guadalupe I. Ramírez 100, Xochimilco, CDMX",
            "Indios Verdes": "Eje Central Lázaro Cárdenas 5000, Gustavo A. Madero, CDMX"
        }
        
        # Configuración SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("SMTP_SENDER_EMAIL")
        sender_password = os.getenv("SMTP_APP_PASSWORD")
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"✅ Cita Confirmada #{id_cita} - Telefonía PTA"
        msg['From'] = f"Telefonía PTA <{sender_email}>"
        msg['To'] = email_cliente
        
        # Renderizar template HTML
        template = Template(CONFIRMACION_CITA_TEMPLATE)
        html_content = template.render(
            nombre=f"{nombre} {apellido}",
            id_cita=id_cita,
            fecha_hora=fecha_hora,
            sucursal=sucursal,
            direccion_sucursal=direcciones_sucursales.get(sucursal, sucursal),
            descripcion=descripcion
        )
        
        # Adjuntar HTML
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Enviar correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return json.dumps({
            "success": True,
            "mensaje": f"Correo de confirmación enviado a {email_cliente}"
        })
    except Exception as e:
        return json.dumps({
            "error": f"Error al enviar correo: {str(e)}",
            "success": False
        })


def enviar_sms_confirmacion_cita(telefono, nombre, id_cita, fecha_hora, sucursal):
    """Envía SMS de confirmación de cita usando Twilio."""
    try:
        # Mapa de direcciones de sucursales
        direcciones_sucursales = {
            "Tlalpan": "Av. Insurgentes Sur 4000, Tlalpan, CDMX",
            "Coyoacán": "Av. Universidad 1200, Coyoacán, CDMX",
            "Venustiano Carranza": "Av. Circunvalación 500, Venustiano Carranza, CDMX",
            "Benito Juárez": "Av. Insurgentes Sur 1500, Benito Juárez, CDMX",
            "Xochimilco": "Av. Guadalupe I. Ramírez 100, Xochimilco, CDMX",
            "Indios Verdes": "Eje Central Lázaro Cárdenas 5000, Gustavo A. Madero, CDMX"
        }
        
        # Configuración Twilio
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        client = Client(account_sid, auth_token)
        
        # Normalizar número de teléfono a formato internacional
        # Si no empieza con +, agregar +52 (México)
        if not telefono.startswith('+'):
            # Remover espacios, guiones, paréntesis
            telefono_limpio = telefono.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            # Si tiene 10 dígitos, es número mexicano
            if len(telefono_limpio) == 10:
                telefono = f"+52{telefono_limpio}"
            else:
                telefono = f"+{telefono_limpio}"
        
        # Obtener dirección completa de la sucursal
        direccion_completa = direcciones_sucursales.get(sucursal, sucursal)
        
        # Crear mensaje SMS conciso con dirección completa
        mensaje = (
            f"Telefonia PTA - Cita Confirmada\n"
            f"ID: {id_cita}\n"
            f"Fecha: {fecha_hora}\n\n"
            f"Sucursal: {sucursal}\n"
            f"{direccion_completa}\n\n"
            f"IMPORTANTE: Presentate con este ID #{id_cita} para ser atendido. Llega 10 min antes."
        )
        
        # Enviar SMS
        message = client.messages.create(
            body=mensaje,
            from_=twilio_number,
            to=telefono
        )
        
        return json.dumps({
            "success": True,
            "mensaje": f"SMS enviado a {telefono}",
            "message_sid": message.sid
        })
    except Exception as e:
        return json.dumps({
            "error": f"Error al enviar SMS: {str(e)}",
            "success": False
        })




def enviar_factura_contratos(email_cliente, nombre_completo, id_cliente, contratos_ids=None):
    """Envía factura de contratos activos al cliente por correo electrónico con HTML profesional."""
    try:
        # Obtener contratos
        api = Api(os.getenv("AIRTABLE_API_KEY"))
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_contratos = api.table(base_id, os.getenv("AIRTABLE_CONTRATOS_TABLE_NAME"))
        
        if contratos_ids and len(contratos_ids) > 0:
            # Filtrar por IDs específicos
            formula_contratos = f"AND({{id_cliente}}='{id_cliente}', {{status}}='Activo', OR(" + ",".join([f"{{id_contrato}}='{cid}'" for cid in contratos_ids]) + "))"
        else:
            # Todos los contratos activos
            formula_contratos = f"AND({{id_cliente}}='{id_cliente}', {{status}}='Activo')"
        
        records_contratos = table_contratos.all(formula=formula_contratos)
        
        if not records_contratos:
            return json.dumps({"error": "No se encontraron contratos activos", "success": False})
        
        # Formatear contratos para el template
        contratos_data = []
        total = 0
        for record in records_contratos:
            fields = record["fields"]
            pago = float(fields.get("pago_mensual", 0))
            contratos_data.append({
                "nombre": fields.get("nombre_contrato", ""),
                "descripcion": fields.get("descripcion", ""),
                "pago_mensual": int(pago),  # Convertir a entero para evitar decimales
                "fecha_pago": fields.get("fecha_pago", ""),
                "status": fields.get("status", "")
            })
            total += pago
        
        # Calcular subtotal e IVA
        subtotal = int(total)
        iva = int(subtotal * 0.16)
        total_con_iva = subtotal + iva
        
        # Fecha actual
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        meses_es = {
            "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
            "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
            "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
        }
        for en, es in meses_es.items():
            fecha_actual = fecha_actual.replace(en, es)
        
        # Configuración SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("SMTP_SENDER_EMAIL", "soporte@telefoniaPTA.com.mx")
        sender_password = os.getenv("SMTP_APP_PASSWORD")
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"💳 Tu Factura de Telefonía PTA - {fecha_actual}"
        msg['From'] = f"Telefonía PTA <{sender_email}>"
        msg['To'] = email_cliente
        
        # Renderizar template HTML
        template = Template(FACTURA_TEMPLATE)
        html_content = template.render(
            nombre=nombre_completo,
            id_cliente=id_cliente,
            fecha_actual=fecha_actual,
            contratos=contratos_data,
            len_contratos=len(contratos_data),
            subtotal=f"{subtotal:,}",
            iva=f"{iva:,}",
            total=f"{total_con_iva:,}"
        )
        
        # Adjuntar HTML
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Enviar correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        resultado = {
            "success": True,
            "contratos_enviados": len(contratos_data),
            "total": f"${total_con_iva:,}.00 MXN",
            "mensaje": f"Factura enviada exitosamente a {email_cliente} con {len(contratos_data)} plan(es)"
        }
        
        return json.dumps(resultado)
    except Exception as e:
        return json.dumps({
            "error": f"Error al enviar factura: {str(e)}",
            "success": False
        })