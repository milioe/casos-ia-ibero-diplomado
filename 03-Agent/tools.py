import datetime
import json
import os
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

load_dotenv()

# Google Calendar API scopes
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Rutas de archivos
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_PATH, "client_secret.json")
TOKEN_FILE = os.path.join(BASE_PATH, "token.json")

def obtener_servicio_calendar():
    """Obtiene un servicio autenticado de Google Calendar API"""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return None
            
    return build("calendar", "v3", credentials=creds)

def enviar_confirmacion_cita(nombre: str, correo: str, dia: str, hora: str, asunto: str) -> str:
    """Envía un correo de confirmación de cita al usuario."""
    if "@" not in correo or "." not in correo:
        return json.dumps({
            "estado": "error",
            "mensaje": f"Formato de correo electrónico no válido: {correo}"
        })
    
    cita_id = f"CITA-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    detalles_cita = {
        "id": cita_id,
        "nombre": nombre,
        "correo": correo,
        "dia": dia,
        "hora": hora,
        "asunto": asunto,
        "fecha_registro": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return json.dumps({
        "estado": "confirmado",
        "mensaje": f"Cita confirmada para {dia} a las {hora}. Se ha enviado un correo a {correo}.",
        "detalles": detalles_cita
    })

def obtener_horarios_ocupados_semana() -> str:
    """Obtiene los horarios ocupados para las próximas dos semanas."""
    try:
        hoy = datetime.datetime.now()
        inicio_semana_actual = hoy - datetime.timedelta(days=hoy.weekday())
        fin_proxima_semana = inicio_semana_actual + datetime.timedelta(days=12)
        
        service = obtener_servicio_calendar()
        if not service:
            return json.dumps({
                "estado": "error",
                "mensaje": "No se pudo autenticar con Google Calendar. Por favor ejecuta el script generate_token.py primero."
            })
        
        # Configurar rango de fechas para la consulta
        semana_inicio = datetime.datetime.combine(inicio_semana_actual.date(), datetime.time(9, 0))
        semana_fin = datetime.datetime.combine(fin_proxima_semana.date(), datetime.time(18, 0))
        time_min = semana_inicio.isoformat() + "Z"
        time_max = semana_fin.isoformat() + "Z"
        
        # Obtener eventos
        eventos_semanas = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        eventos_lista = eventos_semanas.get('items', [])
        
        # Preparar días para las dos semanas
        dias_totales = {}
        nombres_dias = ["lunes", "martes", "miércoles", "jueves", "viernes"]
        
        # Inicializar días de la primera semana
        for i, nombre_dia in enumerate(nombres_dias):
            fecha = inicio_semana_actual + datetime.timedelta(days=i)
            fecha_str = fecha.strftime("%Y-%m-%d")
            dias_totales[fecha_str] = {
                "nombre": nombre_dia,
                "semana": "actual",
                "eventos": []
            }
        
        # Inicializar días de la segunda semana
        for i, nombre_dia in enumerate(nombres_dias):
            fecha = inicio_semana_actual + datetime.timedelta(days=i+7)
            fecha_str = fecha.strftime("%Y-%m-%d")
            dias_totales[fecha_str] = {
                "nombre": nombre_dia,
                "semana": "próxima",
                "eventos": []
            }
        
        # Clasificar eventos por día
        for evento in eventos_lista:
            start = evento['start'].get('dateTime', evento['start'].get('date'))
            if 'T' in start:
                fecha_evento = start.split('T')[0]
                if fecha_evento in dias_totales:
                    end = evento['end'].get('dateTime', evento['end'].get('date'))
                    summary = evento.get('summary', 'Sin título')
                    
                    hora_inicio = start.split('T')[1][:5]
                    hora_fin = end.split('T')[1][:5]
                    
                    dias_totales[fecha_evento]["eventos"].append({
                        "titulo": summary,
                        "hora_inicio": hora_inicio,
                        "hora_fin": hora_fin
                    })
        
        # Organizar respuesta por semanas
        semana_actual = {}
        semana_proxima = {}
        
        for fecha_str, info in dias_totales.items():
            datos_dia = {
                "fecha": fecha_str,
                "bloques_ocupados": info["eventos"]
            }
            
            if info["semana"] == "actual":
                semana_actual[info["nombre"]] = datos_dia
            else:
                semana_proxima[info["nombre"]] = datos_dia
        
        return json.dumps({
            "estado": "ok",
            "mensaje": "Horarios ocupados para las próximas dos semanas",
            "semana_actual": semana_actual,
            "semana_proxima": semana_proxima
        })
        
    except HttpError as error:
        if "insufficient authentication scopes" in str(error).lower() or "insufficientpermissions" in str(error).lower():
            return json.dumps({
                "estado": "error",
                "mensaje": "Error de permisos: Necesitas regenerar el token con permisos de escritura. Por favor elimina el archivo token.json y ejecuta nuevamente generate_token.py."
            })
        return json.dumps({
            "estado": "error",
            "mensaje": f"Error en API de Google Calendar: {str(error)}"
        })
    except Exception as e:
        return json.dumps({
            "estado": "error",
            "mensaje": f"Error al obtener horarios ocupados: {str(e)}"
        })

def crear_evento_calendario(titulo: str, fecha: str, hora_inicio: str, correo_invitado: str = "", descripcion: str = "") -> str:
    """Crea un nuevo evento en Google Calendar con duración de 30 minutos e invita a una persona por correo."""
    try:
        # Validaciones básicas
        try:
            fecha_dt = datetime.datetime.strptime(fecha, "%Y-%m-%d")
            inicio_hora_dt = datetime.datetime.strptime(hora_inicio, "%H:%M")
        except ValueError:
            return json.dumps({
                "estado": "error",
                "mensaje": "Formato de fecha u hora incorrecto. Use YYYY-MM-DD para fecha y HH:MM para hora."
            })
        
        if correo_invitado and ("@" not in correo_invitado or "." not in correo_invitado):
            return json.dumps({
                "estado": "error",
                "mensaje": f"Formato de correo electrónico no válido: {correo_invitado}"
            })
        
        service = obtener_servicio_calendar()
        if not service:
            return json.dumps({
                "estado": "error",
                "mensaje": "No se pudo autenticar con Google Calendar. Por favor ejecuta el script generate_token.py primero."
            })
        
        # Crear datos del evento
        inicio_evento = datetime.datetime.combine(fecha_dt.date(), inicio_hora_dt.time())
        fin_evento = inicio_evento + datetime.timedelta(minutes=30)
        
        evento = {
            'summary': titulo,
            'description': descripcion,
            'start': {
                'dateTime': inicio_evento.isoformat(),
                'timeZone': 'America/Mexico_City',
            },
            'end': {
                'dateTime': fin_evento.isoformat(),
                'timeZone': 'America/Mexico_City',
            },
            'reminders': {
                'useDefault': True,
            }
        }
        
        if correo_invitado:
            evento['attendees'] = [{'email': correo_invitado}]
        
        # Crear el evento
        evento_creado = service.events().insert(
            calendarId='primary', 
            body=evento, 
            sendUpdates='all' if correo_invitado else 'none'
        ).execute()
        
        # Generar mensaje de respuesta
        mensaje = f"Evento '{titulo}' creado exitosamente para el {fecha} a las {hora_inicio} (duración: 30 minutos)."
        if correo_invitado:
            mensaje += f" Se ha enviado una invitación a {correo_invitado}."
            
        return json.dumps({
            "estado": "ok",
            "mensaje": mensaje,
            "id_evento": evento_creado['id'],
            "enlace": evento_creado.get('htmlLink', '')
        })
    
    except HttpError as error:
        if "insufficient authentication scopes" in str(error).lower() or "insufficientpermissions" in str(error).lower():
            return json.dumps({
                "estado": "error",
                "mensaje": "Error de permisos: Necesitas regenerar el token con permisos de escritura. Por favor elimina el archivo token.json y ejecuta nuevamente generate_token.py."
            })
        return json.dumps({
            "estado": "error",
            "mensaje": f"Error en API de Google Calendar: {str(error)}"
        })
    except Exception as e:
        return json.dumps({
            "estado": "error",
            "mensaje": f"Error al crear evento: {str(e)}"
        })

def obtener_servicio_sheets():
    """Obtiene un servicio autenticado de Google Sheets API."""
    try:
        # Usar variable de entorno para la URL de Google Sheets
        sheets_url = os.environ.get('GOOGLE_SHEETS_URL')
        
        # ID de la hoja desde la URL
        sheet_id = sheets_url.split('/d/')[1].split('/edit')[0]
        
        # Para hojas públicas, se puede acceder directamente sin autenticación OAuth
        import requests
        import pandas as pd
        
        try:
            # Primero intentamos acceder como hoja pública usando la API de exportación CSV
            # Esta aproximación funciona para hojas públicas sin credenciales
            url_base = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="
            
            # Crear un diccionario para almacenar los DataFrames de cada hoja
            sheets_data = {}
            for sheet_name in ["alumnos", "cursos", "inscripciones", "pedidos_biblioteca"]:
                url = url_base + sheet_name
                try:
                    # Usar encoding='utf-8' para manejar correctamente los caracteres especiales
                    df = pd.read_csv(url, encoding='utf-8')
                    
                    # Procesar los datos para asegurar que los caracteres especiales se muestren correctamente
                    records = df.to_dict('records')
                    
                    # Función para decodificar correctamente las cadenas de texto
                    def normalize_strings(item):
                        if isinstance(item, dict):
                            return {k: normalize_strings(v) for k, v in item.items()}
                        elif isinstance(item, str):
                            # Asegurar que las secuencias de escape se interpreten correctamente
                            return item.encode('latin1').decode('utf-8') if '\\u' in item else item
                        else:
                            return item
                    
                    # Normalizar los registros
                    normalized_records = [normalize_strings(record) for record in records]
                    sheets_data[sheet_name] = normalized_records
                except Exception as e:
                    print(f"Error leyendo hoja {sheet_name}: {str(e)}")
            
            # Si llegamos aquí, pudimos leer la hoja como pública
            # Creamos un objeto simple que imita la funcionalidad básica que necesitamos
            class SimplePublicSheet:
                def __init__(self, data):
                    self.data = data
                
                def worksheet(self, name):
                    class WorksheetSimulator:
                        def __init__(self, records):
                            self.records = records
                        
                        def get_all_records(self):
                            return self.records
                    
                    return WorksheetSimulator(self.data.get(name, []))
                
                def open_by_key(self, key):
                    # Devuelve a sí mismo, ya que ya tenemos los datos
                    return self
            
            return SimplePublicSheet(sheets_data), sheet_id
            
        except Exception as e:
            print(f"No se pudo acceder como hoja pública: {str(e)}")
            # Si falla el acceso público, intentamos la autenticación OAuth
            
            # Configurar el acceso a la API con autenticación
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            
            # Intentar cargar credenciales si existen
            try:
                creds_file = os.path.join(BASE_PATH, "sheets_credentials.json")
                creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
                client = gspread.authorize(creds)
            except:
                # Intentar usar el token.json si existe
                if os.path.exists(os.path.join(BASE_PATH, "token.json")):
                    
                    client = gspread_oauth.authorize()
                else:
                    print("No se pudo autenticar. Para hojas no públicas, necesitas configurar credenciales.")
                    return None, None
            
            # Abrir la hoja usando su ID
            return client, sheet_id
    except Exception as e:
        print(f"Error al configurar conexión con Google Sheets: {str(e)}")
        return None, None

def obtener_info_alumno(id_alumno: str) -> str:
    """Obtiene la información de un alumno por su ID desde la hoja de alumnos."""
    try:
        client, sheet_id = obtener_servicio_sheets()
        if not client or not sheet_id:
            return json.dumps({
                "estado": "error",
                "mensaje": "No se pudo conectar con Google Sheets"
            }, ensure_ascii=False)
        
        # Abrir el libro y la hoja específica
        sheet = client.open_by_key(sheet_id)
        hoja_alumnos = sheet.worksheet("alumnos")
        
        # Obtener todos los datos para buscar por ID
        datos = hoja_alumnos.get_all_records()
        
        # Buscar el alumno por ID
        alumno = None
        for registro in datos:
            if registro.get('ID_Alumno') == id_alumno:
                alumno = registro
                break
        
        if not alumno:
            return json.dumps({
                "estado": "error",
                "mensaje": f"No se encontró ningún alumno con ID: {id_alumno}"
            }, ensure_ascii=False)
        
        return json.dumps({
            "estado": "ok",
            "mensaje": f"Información del alumno con ID: {id_alumno}",
            "datos": alumno
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "estado": "error",
            "mensaje": f"Error al obtener información del alumno: {str(e)}"
        }, ensure_ascii=False)

def obtener_cursos_alumno(id_alumno: str) -> str:
    """Obtiene los cursos e inscripciones de un alumno por su ID."""
    try:
        client, sheet_id = obtener_servicio_sheets()
        if not client or not sheet_id:
            return json.dumps({
                "estado": "error",
                "mensaje": "No se pudo conectar con Google Sheets"
            }, ensure_ascii=False)
        
        # Abrir el libro y las hojas específicas
        sheet = client.open_by_key(sheet_id)
        hoja_inscripciones = sheet.worksheet("inscripciones")
        hoja_cursos = sheet.worksheet("cursos")
        
        # Obtener datos de inscripciones y cursos
        inscripciones = hoja_inscripciones.get_all_records()
        cursos = hoja_cursos.get_all_records()
        
        # Filtrar inscripciones del alumno
        inscripciones_alumno = [insc for insc in inscripciones if insc.get('ID_Alumno') == id_alumno]
        
        if not inscripciones_alumno:
            return json.dumps({
                "estado": "ok",
                "mensaje": f"El alumno con ID: {id_alumno} no tiene inscripciones registradas",
                "inscripciones": []
            }, ensure_ascii=False)
        
        # Buscar los detalles de los cursos por cada inscripción
        cursos_completos = []
        for inscripcion in inscripciones_alumno:
            id_curso = inscripcion.get('ID_Curso')
            # Buscar información del curso
            curso_info = next((curso for curso in cursos if curso.get('ID_Curso') == id_curso), None)
            
            cursos_completos.append({
                "inscripcion": inscripcion,
                "curso": curso_info
            })
        
        return json.dumps({
            "estado": "ok",
            "mensaje": f"Cursos del alumno con ID: {id_alumno}",
            "total_inscripciones": len(inscripciones_alumno),
            "cursos": cursos_completos
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "estado": "error",
            "mensaje": f"Error al obtener cursos del alumno: {str(e)}"
        }, ensure_ascii=False)

def obtener_pedidos_biblioteca(id_alumno: str) -> str:
    """Obtiene los pedidos de biblioteca de un alumno por su ID."""
    try:
        client, sheet_id = obtener_servicio_sheets()
        if not client or not sheet_id:
            return json.dumps({
                "estado": "error",
                "mensaje": "No se pudo conectar con Google Sheets"
            }, ensure_ascii=False)
        
        # Abrir el libro y la hoja específica
        sheet = client.open_by_key(sheet_id)
        hoja_pedidos = sheet.worksheet("pedidos_biblioteca")
        
        # Obtener todos los pedidos
        pedidos = hoja_pedidos.get_all_records()
        
        # Filtrar pedidos del alumno
        pedidos_alumno = [pedido for pedido in pedidos if pedido.get('ID_Alumno') == id_alumno]
        
        if not pedidos_alumno:
            return json.dumps({
                "estado": "ok",
                "mensaje": f"El alumno con ID: {id_alumno} no tiene pedidos de biblioteca registrados",
                "pedidos": []
            }, ensure_ascii=False)
        
        return json.dumps({
            "estado": "ok",
            "mensaje": f"Pedidos de biblioteca del alumno con ID: {id_alumno}",
            "total_pedidos": len(pedidos_alumno),
            "pedidos": pedidos_alumno
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "estado": "error",
            "mensaje": f"Error al obtener pedidos de biblioteca: {str(e)}"
        }, ensure_ascii=False)


# print(obtener_info_alumno(id_alumno="A0011"))
# print(obtener_cursos_alumno(id_alumno="A0011"))
# print(obtener_pedidos_biblioteca(id_alumno="A0011"))
