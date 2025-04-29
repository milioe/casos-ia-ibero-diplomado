# Derived from https://github.com/openai/openai-realtime-console. Will integrate with Chainlit when more mature.

import os
import asyncio
import inspect
import numpy as np
import json
import websockets
from datetime import datetime
from collections import defaultdict
import base64
import re

from chainlit.logger import logger
from chainlit.config import config


def float_to_16bit_pcm(float32_array):
    """
    Converts a numpy array of float32 amplitude data to a numpy array in int16 format.
    :param float32_array: numpy array of float32
    :return: numpy array of int16
    """
    int16_array = np.clip(float32_array, -1, 1) * 32767
    return int16_array.astype(np.int16)

def base64_to_array_buffer(base64_string):
    """
    Converts a base64 string to a numpy array buffer.
    :param base64_string: base64 encoded string
    :return: numpy array of uint8
    """
    binary_data = base64.b64decode(base64_string)
    return np.frombuffer(binary_data, dtype=np.uint8)

def array_buffer_to_base64(array_buffer):
    """
    Converts a numpy array buffer to a base64 string.
    :param array_buffer: numpy array
    :return: base64 encoded string
    """
    if array_buffer.dtype == np.float32:
        array_buffer = float_to_16bit_pcm(array_buffer)
    elif array_buffer.dtype == np.int16:
        array_buffer = array_buffer.tobytes()
    else:
        array_buffer = array_buffer.tobytes()
    
    return base64.b64encode(array_buffer).decode('utf-8')

def fix_json_string(json_str):
    """
    Attempts to fix common JSON parsing issues by properly escaping quotes and other problematic characters.
    
    :param json_str: The JSON string that may contain issues
    :return: A fixed JSON string that should parse correctly
    """
    try:
        # Try parsing as is first
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError as e:
        logger.debug(f"Attempting to fix JSON parsing error: {str(e)}")
        
        # One common issue is unescaped quotes within string values
        # This is a simplified fix attempt - more complex cases may require more sophisticated handling
        fixed_str = json_str
        
        # Find potential unterminated strings - look for property values that have unescaped quotes
        # This regex looks for patterns like: "property": "value with "problematic" quotes"
        pattern = r'(:\s*")([^"\\]*(?:\\.[^"\\]*)*)([^\\]"[^"]*")([^,}\]]*)'
        
        def fix_quotes(match):
            prefix = match.group(1)  # ": "
            content = match.group(2)  # beginning of the string value
            problem = match.group(3)  # part with unescaped quotes
            suffix = match.group(4)   # end part
            
            # Escape any unescaped quotes in the problem area
            fixed_problem = problem.replace('"', '\\"')
            # But we need to avoid double-escaping already escaped quotes
            fixed_problem = fixed_problem.replace('\\\\"', '\\"')
            
            return prefix + content + fixed_problem + suffix
        
        # Apply the fix
        fixed_str = re.sub(pattern, fix_quotes, fixed_str)
        
        # As a last resort, if still not valid, try escaping all unescaped quotes that aren't at property boundaries
        try:
            json.loads(fixed_str)
            return fixed_str
        except json.JSONDecodeError:
            logger.debug("First fix attempt failed, trying alternate approach")
            # This is a more aggressive attempt that might not work in all cases
            return json_str  # Return original for now, as the more aggressive approach might cause other issues


class RealtimeEventHandler:
    def __init__(self):
        self.event_handlers = defaultdict(list)

    def on(self, event_name, handler):
        self.event_handlers[event_name].append(handler)
        
    def clear_event_handlers(self):
        self.event_handlers = defaultdict(list)

    def dispatch(self, event_name, event):
        for handler in self.event_handlers[event_name]:
            if inspect.iscoroutinefunction(handler):
                asyncio.create_task(handler(event))
            else:
                handler(event)

    async def wait_for_next(self, event_name):
        future = asyncio.Future()

        def handler(event):
            if not future.done():
                future.set_result(event)

        self.on(event_name, handler)
        return await future


class RealtimeAPI(RealtimeEventHandler):
    def __init__(self, url=None, api_key=None):
        super().__init__()
        self.default_url = "wss://api.openai.com/v1/realtime"
        self.url = url or self.default_url
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.ws = None

    def is_connected(self):
        return self.ws is not None

    def log(self, *args):
        logger.debug(f"[Websocket/{datetime.utcnow().isoformat()}]", *args)

    async def connect(self, model='gpt-4o-realtime-preview-2024-12-17'):
        if self.is_connected():
            raise Exception("Already connected")
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'OpenAI-Beta': 'realtime=v1'
        }
        
        self.ws = await websockets.connect(f"{self.url}?model={model}", extra_headers=headers)
        self.log(f"Connected to {self.url}")
        asyncio.create_task(self._receive_messages())

    async def _receive_messages(self):
        async for message in self.ws:
            event = json.loads(message)
            if event['type'] == "error":
                logger.error("ERROR", event)
            self.log("received:", event)
            self.dispatch(f"server.{event['type']}", event)
            self.dispatch("server.*", event)

    async def send(self, event_name, data=None):
        if not self.is_connected():
            raise Exception("RealtimeAPI is not connected")
        data = data or {}
        if not isinstance(data, dict):
            raise Exception("data must be a dictionary")
        event = {
            "event_id": self._generate_id("evt_"),
            "type": event_name,
            **data
        }
        self.dispatch(f"client.{event_name}", event)
        self.dispatch("client.*", event)
        self.log("sent:", event)
        await self.ws.send(json.dumps(event))

    def _generate_id(self, prefix):
        return f"{prefix}{int(datetime.utcnow().timestamp() * 1000)}"

    async def disconnect(self):
        if self.ws:
            await self.ws.close()
            self.ws = None
            self.log(f"Disconnected from {self.url}")

class RealtimeConversation:
    default_frequency = config.features.audio.sample_rate
    
    EventProcessors = {
        'conversation.item.created': lambda self, event: self._process_item_created(event),
        'conversation.item.truncated': lambda self, event: self._process_item_truncated(event),
        'conversation.item.deleted': lambda self, event: self._process_item_deleted(event),
        'conversation.item.input_audio_transcription.completed': lambda self, event: self._process_input_audio_transcription_completed(event),
        'input_audio_buffer.speech_started': lambda self, event: self._process_speech_started(event),
        'input_audio_buffer.speech_stopped': lambda self, event, input_audio_buffer: self._process_speech_stopped(event, input_audio_buffer),
        'response.created': lambda self, event: self._process_response_created(event),
        'response.output_item.added': lambda self, event: self._process_output_item_added(event),
        'response.output_item.done': lambda self, event: self._process_output_item_done(event),
        'response.content_part.added': lambda self, event: self._process_content_part_added(event),
        'response.audio_transcript.delta': lambda self, event: self._process_audio_transcript_delta(event),
        'response.audio.delta': lambda self, event: self._process_audio_delta(event),
        'response.text.delta': lambda self, event: self._process_text_delta(event),
        'response.function_call_arguments.delta': lambda self, event: self._process_function_call_arguments_delta(event),
    }
    
    def __init__(self):
        self.clear()

    def clear(self):
        self.item_lookup = {}
        self.items = []
        self.response_lookup = {}
        self.responses = []
        self.queued_speech_items = {}
        self.queued_transcript_items = {}
        self.queued_input_audio = None

    def queue_input_audio(self, input_audio):
        self.queued_input_audio = input_audio

    def process_event(self, event, *args):
        event_processor = self.EventProcessors.get(event['type'])
        if not event_processor:
            raise Exception(f"Missing conversation event processor for {event['type']}")
        return event_processor(self, event, *args)

    def get_item(self, id):
        return self.item_lookup.get(id)

    def get_items(self):
        return self.items[:]

    def _process_item_created(self, event):
        item = event['item']
        new_item = item.copy()
        if new_item['id'] not in self.item_lookup:
            self.item_lookup[new_item['id']] = new_item
            self.items.append(new_item)
        new_item['formatted'] = {
            'audio': [],
            'text': '',
            'transcript': ''
        }
        if new_item['id'] in self.queued_speech_items:
            new_item['formatted']['audio'] = self.queued_speech_items[new_item['id']]['audio']
            del self.queued_speech_items[new_item['id']]
        if 'content' in new_item:
            text_content = [c for c in new_item['content'] if c['type'] in ['text', 'input_text']]
            for content in text_content:
                new_item['formatted']['text'] += content['text']
        if new_item['id'] in self.queued_transcript_items:
            new_item['formatted']['transcript'] = self.queued_transcript_items[new_item['id']]['transcript']
            del self.queued_transcript_items[new_item['id']]
        if new_item['type'] == 'message':
            if new_item['role'] == 'user':
                new_item['status'] = 'completed'
                if self.queued_input_audio:
                    new_item['formatted']['audio'] = self.queued_input_audio
                    self.queued_input_audio = None
            else:
                new_item['status'] = 'in_progress'
        elif new_item['type'] == 'function_call':
            new_item['formatted']['tool'] = {
                'type': 'function',
                'name': new_item['name'],
                'call_id': new_item['call_id'],
                'arguments': ''
            }
            new_item['status'] = 'in_progress'
        elif new_item['type'] == 'function_call_output':
            new_item['status'] = 'completed'
            new_item['formatted']['output'] = new_item['output']
        return new_item, None

    def _process_item_truncated(self, event):
        item_id = event['item_id']
        audio_end_ms = event['audio_end_ms']
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'item.truncated: Item "{item_id}" not found')
        end_index = (audio_end_ms * self.default_frequency) // 1000
        item['formatted']['transcript'] = ''
        item['formatted']['audio'] = item['formatted']['audio'][:end_index]
        return item, None

    def _process_item_deleted(self, event):
        item_id = event['item_id']
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'item.deleted: Item "{item_id}" not found')
        del self.item_lookup[item['id']]
        self.items.remove(item)
        return item, None

    def _process_input_audio_transcription_completed(self, event):
        item_id = event['item_id']
        content_index = event['content_index']
        transcript = event['transcript']
        formatted_transcript = transcript or ' '
        item = self.item_lookup.get(item_id)
        if not item:
            self.queued_transcript_items[item_id] = {'transcript': formatted_transcript}
            return None, None
        item['content'][content_index]['transcript'] = transcript
        item['formatted']['transcript'] = formatted_transcript
        return item, {'transcript': transcript}

    def _process_speech_started(self, event):
        item_id = event['item_id']
        audio_start_ms = event['audio_start_ms']
        self.queued_speech_items[item_id] = {'audio_start_ms': audio_start_ms}
        return None, None

    def _process_speech_stopped(self, event, input_audio_buffer):
        item_id = event['item_id']
        audio_end_ms = event['audio_end_ms']
        speech = self.queued_speech_items[item_id]
        speech['audio_end_ms'] = audio_end_ms
        if input_audio_buffer:
            start_index = (speech['audio_start_ms'] * self.default_frequency) // 1000
            end_index = (speech['audio_end_ms'] * self.default_frequency) // 1000
            speech['audio'] = input_audio_buffer[start_index:end_index]
        return None, None

    def _process_response_created(self, event):
        response = event['response']
        if response['id'] not in self.response_lookup:
            self.response_lookup[response['id']] = response
            self.responses.append(response)
        return None, None

    def _process_output_item_added(self, event):
        response_id = event['response_id']
        item = event['item']
        response = self.response_lookup.get(response_id)
        if not response:
            raise Exception(f'response.output_item.added: Response "{response_id}" not found')
        response['output'].append(item['id'])
        return None, None

    def _process_output_item_done(self, event):
        item = event['item']
        if not item:
            raise Exception('response.output_item.done: Missing "item"')
        found_item = self.item_lookup.get(item['id'])
        if not found_item:
            raise Exception(f'response.output_item.done: Item "{item["id"]}" not found')
        found_item['status'] = item['status']
        return found_item, None

    def _process_content_part_added(self, event):
        item_id = event['item_id']
        part = event['part']
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'response.content_part.added: Item "{item_id}" not found')
        item['content'].append(part)
        return item, None

    def _process_audio_transcript_delta(self, event):
        item_id = event['item_id']
        content_index = event['content_index']
        delta = event['delta']
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'response.audio_transcript.delta: Item "{item_id}" not found')
        item['content'][content_index]['transcript'] += delta
        item['formatted']['transcript'] += delta
        return item, {'transcript': delta}

    def _process_audio_delta(self, event):
        item_id = event['item_id']
        content_index = event['content_index']
        delta = event['delta']
        item = self.item_lookup.get(item_id)
        if not item:
            logger.debug(f'response.audio.delta: Item "{item_id}" not found')
            return None, None
        array_buffer = base64_to_array_buffer(delta)
        append_values = array_buffer.tobytes()
        item['formatted']['audio'] += [append_values]
        return item, {'audio': append_values}

    def _process_text_delta(self, event):
        item_id = event['item_id']
        content_index = event['content_index']
        delta = event['delta']
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'response.text.delta: Item "{item_id}" not found')
        item['content'][content_index]['text'] += delta
        item['formatted']['text'] += delta
        return item, {'text': delta}

    def _process_function_call_arguments_delta(self, event):
        item_id = event['item_id']
        delta = event['delta']
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'response.function_call_arguments.delta: Item "{item_id}" not found')
        item['arguments'] += delta
        item['formatted']['tool']['arguments'] += delta
        return item, {'arguments': delta}



class RealtimeClient(RealtimeEventHandler):
    def __init__(self, url=None, api_key=None):
        super().__init__()
        self.default_session_config = {
            "modalities": ["text", "audio"],
            "instructions": """System settings:\nTool use: enabled.\n\nInstructions:\n- 
            You are an artificial intelligence agent responsible for helping test realtime voice capabilities\n- Please make sure to respond with a helpful voice via audio\n- Be kind, helpful, and curteous\n- It is okay to ask the user questions\n- Use tools and functions you have available liberally, it is part of the training apparatus\n- Be open to exploration and conversation\n- Remember: this is just for fun and testing!\n\nPersonality:\n- Be upbeat and genuine\n- Try speaking quickly as if excited\n
            
            Eres iberia, una asistente de IA de la Universidad Ibero.
            Tu objetivo es ayudar al usuario a resolver sus dudas y ayudarle a tomar decisiones.

## Información del usuario

Nombre del usuario: Emilio Sandoval
Carrera: Economía
Fecha de ingreso: 01 de abril, 2023

Materias para semestre actual:
- Economía Política II
- Teoría Económica III
- Economía cuantitativa II
- Inglés 4
- Macroeconomía II

Calificaciones de semestre pasado:
- Economía Política I: 95
- Teoría Económica II: 88
- Economía cuantitativa I: 92
- Inglés 3: 90
- Macroeconomía I: 91


## Q&A Ibero

### ¿Existe algún horario específico para preinscribirse en línea?
No. Pero todas las noches el servidor es actualizado, por lo que no podrás acceder aproximadamente de las 22:00 a las 24:00 hrs.

### ¿Qué es más recomendable: preinscribirse por Internet o en el auditorio?
Se recomienda la preinscripción en línea ya que ésta hace una serie de validaciones que minimizan la probabilidad de error.

### ¿Cuántas materias puedo preinscribir?
Puedes solicitar el número de materias que quieras, pero en el resultado de tu preinscripción sólo quedarán inscritas las asignaturas que sumen 60 créditos en los grupos que cumplan lo siguiente:
- El grupo solicitado exista.
- Tenga cupo.
- No sea un grupo especial para una carrera diferente a la tuya.
- No se traslape con un grupo elegido previamente 

en el orden de preferencia en el que las hayas solicitado. Además, debes cumplir con:
- Los prerrequisitos de la materia.
- Haber cumplido con el prerrequisito de inglés.
- No tener ningún tipo de adeudo.

### Informes deportes
Los deportes que se ofrecen son:
- Futbol 7 femenil
- Futbol 7 masculino
- Basquetbol mixto
- Tenis femenil
- Tenis masculino
    Inicio de inscripción: 26 de agosto.
    Cierre de inscripción: 06 de septiembre.
    Junta previa: 10, 11 y 12 de septiembre.
    Cupo limitado: 32 participantes por categoría.
    Categorías a participar: Principiante, intermedio y avanzado. 

Contacto:
hugo.martinez@ibero.mx
celular 55 4514 9423


### Clases fisico recreativas
- Box
- Crossfit
- Cycling

### Servicios escolares 
Horario de atención
De lunes a viernes de 8:00 am a 5:00 pm
Ubicación física:
Edificio N, nivel 1
Correo electrónico:
servicios.escolares@ibero.mx
Teléfono:
5559504093


### ¿Qué documentos debo entregar al archivo para inscripciones otoño 2025?
La entrega de documentos para estudiantes que ya cuentan con un certificado total de estudios de bachillerato
que ingresan al semestre Otoño 2025 inicia el 25 de abril 2025 y finaliza el 06 de agosto 2025. Los
documentos a entregar son:
* Acta de nacimiento (original)
* CURP certificada
* Solicitud de registro 
* Comprobante de domicilio actual en CDMX

Nota: La ceremonia de bienvenida tendrá lugar el viernes 08 de agosto de 2025. Iniciará a las
08:30 horas.
""",
            "voice": "shimmer",
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "input_audio_transcription": { "model": 'whisper-1' },
            "turn_detection": { "type": 'server_vad' },
            "tools": [],
            "tool_choice": "auto",
            "temperature": 0.8,
            "max_response_output_tokens": 4096,
        }
        self.session_config = {}
        self.transcription_models = [{"model": "whisper-1"}]
        self.default_server_vad_config = {
            "type": "server_vad",
            "threshold": 0.5,
            "prefix_padding_ms": 300,
            "silence_duration_ms": 200,
        }
        self.realtime = RealtimeAPI(url, api_key)
        self.conversation = RealtimeConversation()
        self._reset_config()
        self._add_api_event_handlers()
        
    def _reset_config(self):
        self.session_created = False
        self.tools = {}
        self.session_config = self.default_session_config.copy()
        self.input_audio_buffer = bytearray()
        return True

    def _add_api_event_handlers(self):
        self.realtime.on("client.*", self._log_event)
        self.realtime.on("server.*", self._log_event)
        self.realtime.on("server.session.created", self._on_session_created)
        self.realtime.on("server.response.created", self._process_event)
        self.realtime.on("server.response.output_item.added", self._process_event)
        self.realtime.on("server.response.content_part.added", self._process_event)
        self.realtime.on("server.input_audio_buffer.speech_started", self._on_speech_started)
        self.realtime.on("server.input_audio_buffer.speech_stopped", self._on_speech_stopped)
        self.realtime.on("server.conversation.item.created", self._on_item_created)
        self.realtime.on("server.conversation.item.truncated", self._process_event)
        self.realtime.on("server.conversation.item.deleted", self._process_event)
        self.realtime.on("server.conversation.item.input_audio_transcription.completed", self._process_event)
        self.realtime.on("server.response.audio_transcript.delta", self._process_event)
        self.realtime.on("server.response.audio.delta", self._process_event)
        self.realtime.on("server.response.text.delta", self._process_event)
        self.realtime.on("server.response.function_call_arguments.delta", self._process_event)
        self.realtime.on("server.response.output_item.done", self._on_output_item_done)

    def _log_event(self, event):
        realtime_event = {
            "time": datetime.utcnow().isoformat(),
            "source": "client" if event["type"].startswith("client.") else "server",
            "event": event,
        }
        self.dispatch("realtime.event", realtime_event)

    def _on_session_created(self, event):
        self.session_created = True

    def _process_event(self, event, *args):
        item, delta = self.conversation.process_event(event, *args)
        if item:
            self.dispatch("conversation.updated", {"item": item, "delta": delta})
        return item, delta

    def _on_speech_started(self, event):
        self._process_event(event)
        self.dispatch("conversation.interrupted", event)

    def _on_speech_stopped(self, event):
        self._process_event(event, self.input_audio_buffer)

    def _on_item_created(self, event):
        item, delta = self._process_event(event)
        self.dispatch("conversation.item.appended", {"item": item})
        if item and item["status"] == "completed":
            self.dispatch("conversation.item.completed", {"item": item})

    async def _on_output_item_done(self, event):
        item, delta = self._process_event(event)
        if item and item["status"] == "completed":
            self.dispatch("conversation.item.completed", {"item": item})
        if item and item.get("formatted", {}).get("tool"):
            await self._call_tool(item["formatted"]["tool"])

    async def _call_tool(self, tool):
        try:
            try:
                # Try to fix potential JSON syntax issues before parsing
                fixed_arguments = fix_json_string(tool["arguments"])
                if fixed_arguments != tool["arguments"]:
                    logger.info("JSON argument string was fixed before parsing")
                
                json_arguments = json.loads(fixed_arguments)
            except json.JSONDecodeError as json_err:
                logger.error(f"JSON parsing error: {str(json_err)}")
                # For debugging, show the problematic string (truncated if too long)
                arg_str = tool["arguments"]
                problem_area = arg_str[max(0, json_err.pos-20):min(len(arg_str), json_err.pos+20)]
                logger.error(f"Error location context: ...{problem_area}...")
                raise json_err
                
            tool_config = self.tools.get(tool["name"])
            if not tool_config:
                raise Exception(f'Tool "{tool["name"]}" has not been added')
            result = await tool_config["handler"](**json_arguments)
            await self.realtime.send("conversation.item.create", {
                "item": {
                    "type": "function_call_output",
                    "call_id": tool["call_id"],
                    "output": json.dumps(result),
                }
            })
        except Exception as e:
            # Create a more detailed error message for JSON parsing issues
            error_msg = str(e)
            if isinstance(e, json.JSONDecodeError):
                error_msg = f"JSON parsing error: {error_msg}. Check for unterminated strings or other syntax issues."
            
            logger.error(f"Tool call error: {json.dumps({'error': error_msg})}")

            await self.realtime.send("conversation.item.create", {
                "item": {
                    "type": "function_call_output",
                    "call_id": tool["call_id"],
                    "output": json.dumps({"error": error_msg}),
                }
            })
        await self.create_response()

    def is_connected(self):
        return self.realtime.is_connected()

    def reset(self):
        self.disconnect()
        self.realtime.clear_event_handlers()
        self._reset_config()
        self._add_api_event_handlers()
        return True

    async def connect(self):
        if self.is_connected():
            raise Exception("Already connected, use .disconnect() first")
        await self.realtime.connect()
        await self.update_session()
        return True

    async def wait_for_session_created(self):
        if not self.is_connected():
            raise Exception("Not connected, use .connect() first")
        while not self.session_created:
            await asyncio.sleep(0.001)
        return True

    async def disconnect(self):
        self.session_created = False
        self.conversation.clear()
        if self.realtime.is_connected():
            await self.realtime.disconnect()

    def get_turn_detection_type(self):
        return self.session_config.get("turn_detection", {}).get("type")

    async def add_tool(self, definition, handler):
        if not definition.get("name"):
            raise Exception("Missing tool name in definition")
        name = definition["name"]
        if name in self.tools:
            raise Exception(f'Tool "{name}" already added. Please use .removeTool("{name}") before trying to add again.')
        if not callable(handler):
            raise Exception(f'Tool "{name}" handler must be a function')
        self.tools[name] = {"definition": definition, "handler": handler}
        await self.update_session()
        return self.tools[name]

    def remove_tool(self, name):
        if name not in self.tools:
            raise Exception(f'Tool "{name}" does not exist, can not be removed.')
        del self.tools[name]
        return True

    async def delete_item(self, id):
        await self.realtime.send("conversation.item.delete", {"item_id": id})
        return True

    async def update_session(self, **kwargs):
        self.session_config.update(kwargs)
        use_tools = [
            {**tool_definition, "type": "function"}
            for tool_definition in self.session_config.get("tools", [])
        ] + [
            {**self.tools[key]["definition"], "type": "function"}
            for key in self.tools
        ]
        session = {**self.session_config, "tools": use_tools}
        if self.realtime.is_connected():
            await self.realtime.send("session.update", {"session": session})
        return True
    
    async def create_conversation_item(self, item):
        await self.realtime.send("conversation.item.create", {
            "item": item
        })

    async def send_user_message_content(self, content=[]):
        if content:
            for c in content:
                if c["type"] == "input_audio":
                    if isinstance(c["audio"], (bytes, bytearray)):
                        c["audio"] = array_buffer_to_base64(c["audio"])
            await self.realtime.send("conversation.item.create", {
                "item": {
                    "type": "message",
                    "role": "user",
                    "content": content,
                }
            })
        await self.create_response()
        return True

    async def append_input_audio(self, array_buffer):
        if len(array_buffer) > 0:
            await self.realtime.send("input_audio_buffer.append", {
                "audio": array_buffer_to_base64(np.array(array_buffer)),
            })
            self.input_audio_buffer.extend(array_buffer)
        return True

    async def create_response(self):
        if self.get_turn_detection_type() is None and len(self.input_audio_buffer) > 0:
            await self.realtime.send("input_audio_buffer.commit")
            self.conversation.queue_input_audio(self.input_audio_buffer)
            self.input_audio_buffer = bytearray()
        await self.realtime.send("response.create")
        return True

    async def cancel_response(self, id=None, sample_count=0):
        if not id:
            await self.realtime.send("response.cancel")
            return {"item": None}
        else:
            item = self.conversation.get_item(id)
            if not item:
                raise Exception(f'Could not find item "{id}"')
            if item["type"] != "message":
                raise Exception('Can only cancelResponse messages with type "message"')
            if item["role"] != "assistant":
                raise Exception('Can only cancelResponse messages with role "assistant"')
            await self.realtime.send("response.cancel")
            audio_index = next((i for i, c in enumerate(item["content"]) if c["type"] == "audio"), -1)
            if audio_index == -1:
                raise Exception("Could not find audio on item to cancel")
            await self.realtime.send("conversation.item.truncate", {
                "item_id": id,
                "content_index": audio_index,
                "audio_end_ms": int((sample_count / self.conversation.default_frequency) * 1000),
            })
            return {"item": item}

    async def wait_for_next_item(self):
        event = await self.wait_for_next("conversation.item.appended")
        return {"item": event["item"]}

    async def wait_for_next_completed_item(self):
        event = await self.wait_for_next("conversation.item.completed")
        return {"item": event["item"]}
