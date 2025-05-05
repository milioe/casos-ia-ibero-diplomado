import json
import ast
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from datetime import datetime

from systemt_prompt import SYSTEM_PROMPT
from schema import tools
from tools import enviar_confirmacion_cita, obtener_horarios_ocupados_semana, crear_evento_calendario, obtener_info_alumno, obtener_cursos_alumno, obtener_pedidos_biblioteca

import chainlit as cl

# Cargar variables de entorno
load_dotenv()

# Obtener API key del entorno
api_key = os.environ.get("OPENAI_API_KEY")
org_id = os.environ.get("OPENAI_ORG_ID")

# Inicializar cliente de OpenAI
client = AsyncOpenAI(
    api_key=api_key,
    organization=org_id
)

# Número máximo de iteraciones para llamadas a herramientas
MAX_ITER = 5

@cl.on_chat_start
async def start_chat():

    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": SYSTEM_PROMPT}],
    )
    
    # Enviar mensaje de bienvenida
    try:
        await cl.Message(
            content="¡Hola! Soy Iber.IA, tu asistente virtual de la Universidad Iberoamericana. ¿En qué puedo ayudarte hoy?",
            author="Servicios Escolares"
        ).send()
    except Exception as e:
        await cl.Message(content=f"Error al iniciar: {str(e)}", author="Sistema").send()


async def call_tool(tool_call_id, name, arguments, message_history):
    try:
        # Analizar los argumentos como diccionario Python
        arguments = ast.literal_eval(arguments)
        
        # Llamar a la función correspondiente con los argumentos analizados
        if name == "enviar_confirmacion_cita":
            function_response = enviar_confirmacion_cita(
                nombre=arguments.get("nombre"),
                correo=arguments.get("correo"),
                dia=arguments.get("dia"),
                hora=arguments.get("hora"),
                asunto=arguments.get("asunto")
            )
        elif name == "obtener_horarios_ocupados_semana":
            function_response = obtener_horarios_ocupados_semana()
        elif name == "crear_evento_calendario":
            function_response = crear_evento_calendario(
                titulo=arguments.get("titulo"),
                fecha=arguments.get("fecha"),
                hora_inicio=arguments.get("hora_inicio"),
                correo_invitado=arguments.get("correo_invitado", ""),
                descripcion=arguments.get("descripcion", "")
            )
        elif name == "obtener_info_alumno":
            function_response = obtener_info_alumno(
                id_alumno=arguments.get("id_alumno")
            )
        elif name == "obtener_cursos_alumno":
            function_response = obtener_cursos_alumno(
                id_alumno=arguments.get("id_alumno")
            )
        elif name == "obtener_pedidos_biblioteca":
            function_response = obtener_pedidos_biblioteca(
                id_alumno=arguments.get("id_alumno")
            )
        else:
            function_response = json.dumps({"error": f"Función desconocida: {name}"}, ensure_ascii=False)
        
        # Agregar la respuesta de la función al historial de mensajes
        message_history.append({
            "role": "tool", 
            "tool_call_id": tool_call_id,
            "name": name,
            "content": function_response
        })

        return function_response
    except Exception as e:
        error_response = json.dumps({"error": f"Error al procesar la herramienta: {str(e)}"}, ensure_ascii=False)
        message_history.append({
            "role": "tool", 
            "tool_call_id": tool_call_id,
            "name": name,
            "content": error_response
        })
        return error_response


async def call_gpt4o(message_history):
    try:
        # Configuración para el modelo GPT-4o
        settings = {
            "model": "gpt-4o",
            "tools": tools,
            "tool_choice": "auto",
            "temperature": 0.7,
        }

        # Crear una respuesta desde el modelo
        response = await client.chat.completions.create(
            messages=message_history, **settings
        )
        
        # Obtener el primer choice
        choice = response.choices[0]
        content = choice.message.content
        tool_calls = choice.message.tool_calls
        
        # Agregar respuesta al historial (sin tool_calls si está vacío)
        assistant_message = {
            "role": "assistant",
            "content": content or ""
        }
        
        # Solo agregar tool_calls si existe y no está vacío
        if tool_calls:
            assistant_message["tool_calls"] = tool_calls
            
        message_history.append(assistant_message)
        
        # Mostrar la respuesta en la interfaz si hay contenido
        if content:
            await cl.Message(content=content, author="Servicios Escolares").send()
        
        # Procesar llamadas a herramientas
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments
                tool_call_id = tool_call.id
                
                # Ejecutar la herramienta
                function_response = await call_tool(
                    tool_call_id,
                    function_name,
                    function_args,
                    message_history
                )
                
                # Mostrar resultado en la interfaz
                try:
                    result_json = json.loads(function_response)
                    await cl.Message(
                        content=f"Resultado de {function_name}: {result_json.get('mensaje', result_json.get('estado', ''))}",
                        author="Herramienta"
                    ).send()
                except Exception as e:
                    await cl.Message(
                        content=f"Resultado de {function_name}: {function_response[:100]}...",
                        author="Herramienta"
                    ).send()
                
                return tool_call_id
        
        return None
    except Exception as e:
        await cl.Message(content=f"Lo siento, ocurrió un error al procesar tu solicitud. Por favor, intenta de nuevo.", author="Servicios Escolares").send()
        return None


@cl.on_message
async def on_message(message):
    try:
        # Manejar diferentes estructuras de mensaje según la versión de Chainlit
        if hasattr(message, 'content'):
            message_content = message.content
        elif isinstance(message, str):
            message_content = message
        else:
            try:
                message_content = getattr(message, 'content', None) or getattr(message, 'text', None) or str(message)
            except:
                message_content = str(message)
        
        # Obtener el historial de mensajes
        message_history = cl.user_session.get("message_history")
        
        # Agregar el mensaje del usuario al historial en formato correcto para OpenAI
        message_history.append({"role": "user", "content": message_content})
        
        # Iterar a través de las llamadas a herramientas si es necesario
        cur_iter = 0
        while cur_iter < MAX_ITER:
            tool_call_id = await call_gpt4o(message_history)
            if not tool_call_id:
                break

            cur_iter += 1
    except Exception as e:
        await cl.Message(content=f"Lo siento, ocurrió un error. Por favor, intenta de nuevo más tarde.", author="Servicios Escolares").send()
