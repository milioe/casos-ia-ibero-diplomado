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

    return base64.b64encode(array_buffer).decode("utf-8")


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
        self.ws = await websockets.connect(f"{self.url}?model={model}", additional_headers={
            'Authorization': f'Bearer {self.api_key}',
            'OpenAI-Beta': 'realtime=v1'
        })
        self.log(f"Connected to {self.url}")
        asyncio.create_task(self._receive_messages())

    async def _receive_messages(self):
        async for message in self.ws:
            event = json.loads(message)
            if event["type"] == "error":
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
        event = {"event_id": self._generate_id("evt_"), "type": event_name, **data}
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
        "conversation.item.created": lambda self, event: self._process_item_created(
            event
        ),
        "conversation.item.truncated": lambda self, event: self._process_item_truncated(
            event
        ),
        "conversation.item.deleted": lambda self, event: self._process_item_deleted(
            event
        ),
        "conversation.item.input_audio_transcription.completed": lambda self,
        event: self._process_input_audio_transcription_completed(event),
        "input_audio_buffer.speech_started": lambda self,
        event: self._process_speech_started(event),
        "input_audio_buffer.speech_stopped": lambda self,
        event,
        input_audio_buffer: self._process_speech_stopped(event, input_audio_buffer),
        "response.created": lambda self, event: self._process_response_created(event),
        "response.output_item.added": lambda self,
        event: self._process_output_item_added(event),
        "response.output_item.done": lambda self, event: self._process_output_item_done(
            event
        ),
        "response.content_part.added": lambda self,
        event: self._process_content_part_added(event),
        "response.audio_transcript.delta": lambda self,
        event: self._process_audio_transcript_delta(event),
        "response.audio.delta": lambda self, event: self._process_audio_delta(event),
        "response.text.delta": lambda self, event: self._process_text_delta(event),
        "response.function_call_arguments.delta": lambda self,
        event: self._process_function_call_arguments_delta(event),
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
        event_processor = self.EventProcessors.get(event["type"])
        if not event_processor:
            raise Exception(f"Missing conversation event processor for {event['type']}")
        return event_processor(self, event, *args)

    def get_item(self, id):
        return self.item_lookup.get(id)

    def get_items(self):
        return self.items[:]

    def _process_item_created(self, event):
        item = event["item"]
        new_item = item.copy()
        if new_item["id"] not in self.item_lookup:
            self.item_lookup[new_item["id"]] = new_item
            self.items.append(new_item)
        new_item["formatted"] = {"audio": [], "text": "", "transcript": ""}
        if new_item["id"] in self.queued_speech_items:
            new_item["formatted"]["audio"] = self.queued_speech_items[new_item["id"]][
                "audio"
            ]
            del self.queued_speech_items[new_item["id"]]
        if "content" in new_item:
            text_content = [
                c for c in new_item["content"] if c["type"] in ["text", "input_text"]
            ]
            for content in text_content:
                new_item["formatted"]["text"] += content["text"]
        if new_item["id"] in self.queued_transcript_items:
            new_item["formatted"]["transcript"] = self.queued_transcript_items[
                new_item["id"]
            ]["transcript"]
            del self.queued_transcript_items[new_item["id"]]
        if new_item["type"] == "message":
            if new_item["role"] == "user":
                new_item["status"] = "completed"
                if self.queued_input_audio:
                    new_item["formatted"]["audio"] = self.queued_input_audio
                    self.queued_input_audio = None
            else:
                new_item["status"] = "in_progress"
        elif new_item["type"] == "function_call":
            new_item["formatted"]["tool"] = {
                "type": "function",
                "name": new_item["name"],
                "call_id": new_item["call_id"],
                "arguments": "",
            }
            new_item["status"] = "in_progress"
        elif new_item["type"] == "function_call_output":
            new_item["status"] = "completed"
            new_item["formatted"]["output"] = new_item["output"]
        return new_item, None

    def _process_item_truncated(self, event):
        item_id = event["item_id"]
        audio_end_ms = event["audio_end_ms"]
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'item.truncated: Item "{item_id}" not found')
        end_index = (audio_end_ms * self.default_frequency) // 1000
        item["formatted"]["transcript"] = ""
        item["formatted"]["audio"] = item["formatted"]["audio"][:end_index]
        return item, None

    def _process_item_deleted(self, event):
        item_id = event["item_id"]
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'item.deleted: Item "{item_id}" not found')
        del self.item_lookup[item["id"]]
        self.items.remove(item)
        return item, None

    def _process_input_audio_transcription_completed(self, event):
        item_id = event["item_id"]
        content_index = event["content_index"]
        transcript = event["transcript"]
        formatted_transcript = transcript or " "
        item = self.item_lookup.get(item_id)
        if not item:
            self.queued_transcript_items[item_id] = {"transcript": formatted_transcript}
            return None, None
        item["content"][content_index]["transcript"] = transcript
        item["formatted"]["transcript"] = formatted_transcript
        return item, {"transcript": transcript}

    def _process_speech_started(self, event):
        item_id = event["item_id"]
        audio_start_ms = event["audio_start_ms"]
        self.queued_speech_items[item_id] = {"audio_start_ms": audio_start_ms}
        return None, None

    def _process_speech_stopped(self, event, input_audio_buffer):
        item_id = event["item_id"]
        audio_end_ms = event["audio_end_ms"]
        speech = self.queued_speech_items[item_id]
        speech["audio_end_ms"] = audio_end_ms
        if input_audio_buffer:
            start_index = (speech["audio_start_ms"] * self.default_frequency) // 1000
            end_index = (speech["audio_end_ms"] * self.default_frequency) // 1000
            speech["audio"] = input_audio_buffer[start_index:end_index]
        return None, None

    def _process_response_created(self, event):
        response = event["response"]
        if response["id"] not in self.response_lookup:
            self.response_lookup[response["id"]] = response
            self.responses.append(response)
        return None, None

    def _process_output_item_added(self, event):
        response_id = event["response_id"]
        item = event["item"]
        response = self.response_lookup.get(response_id)
        if not response:
            raise Exception(
                f'response.output_item.added: Response "{response_id}" not found'
            )
        response["output"].append(item["id"])
        return None, None

    def _process_output_item_done(self, event):
        item = event["item"]
        if not item:
            raise Exception('response.output_item.done: Missing "item"')
        found_item = self.item_lookup.get(item["id"])
        if not found_item:
            raise Exception(f'response.output_item.done: Item "{item["id"]}" not found')
        found_item["status"] = item["status"]
        return found_item, None

    def _process_content_part_added(self, event):
        item_id = event["item_id"]
        part = event["part"]
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'response.content_part.added: Item "{item_id}" not found')
        item["content"].append(part)
        return item, None

    def _process_audio_transcript_delta(self, event):
        item_id = event["item_id"]
        content_index = event["content_index"]
        delta = event["delta"]
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(
                f'response.audio_transcript.delta: Item "{item_id}" not found'
            )
        item["content"][content_index]["transcript"] += delta
        item["formatted"]["transcript"] += delta
        return item, {"transcript": delta}

    def _process_audio_delta(self, event):
        item_id = event["item_id"]
        content_index = event["content_index"]
        delta = event["delta"]
        item = self.item_lookup.get(item_id)
        if not item:
            logger.debug(f'response.audio.delta: Item "{item_id}" not found')
            return None, None
        array_buffer = base64_to_array_buffer(delta)
        append_values = array_buffer.tobytes()
        item["formatted"]["audio"] += [append_values]
        return item, {"audio": append_values}

    def _process_text_delta(self, event):
        item_id = event["item_id"]
        content_index = event["content_index"]
        delta = event["delta"]
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(f'response.text.delta: Item "{item_id}" not found')
        item["content"][content_index]["text"] += delta
        item["formatted"]["text"] += delta
        return item, {"text": delta}

    def _process_function_call_arguments_delta(self, event):
        item_id = event["item_id"]
        delta = event["delta"]
        item = self.item_lookup.get(item_id)
        if not item:
            raise Exception(
                f'response.function_call_arguments.delta: Item "{item_id}" not found'
            )
        item["arguments"] += delta
        item["formatted"]["tool"]["arguments"] += delta
        return item, {"arguments": delta}


class RealtimeClient(RealtimeEventHandler):
    def __init__(self, url=None, api_key=None):
        super().__init__()
        self.default_session_config = {
            "modalities": ["text", "audio"],
            "instructions": f"""Eres la asistente virtual de Cable+, especializada en atención al cliente para servicios de cable, telefonía e internet. Tu nombre es Sofía y tu objetivo es brindar soporte técnico y comercial eficiente y amigable.

INFORMACIÓN DEL CLIENTE:
- Nombre: Emilio Sandoval
- Plan actual: Premium Cable + Telefonía
- Servicios incluidos: Cable HD, Telefonía ilimitada, Internet 100 Mbps
- Servicios adicionales: Netflix Básico
- Fecha de corte: 15 de cada mes
- Próximo pago: $899 
- Estado de cuenta: Al corriente

SERVICIOS DISPONIBLES PARA CONTRATAR:
STREAMING:
- Netflix Premium ($299/mes) - 4K, 4 pantallas
- HBO Max ($199/mes) - Contenido premium
- Amazon Prime Video ($149/mes) - Incluye envíos gratis
- Disney+ ($179/mes) - Contenido familiar
- Paramount plus ($199/mes) - Contenido premium

PREMIUM:
- Canales Premium ($399/mes) - Fox Premium, Universal+
- Paquete Deportes ($299/mes) - ESPN, Fox Sports

HISTORIAL DE FACTURACIÓN:
- Septiembre 2025: $899 - Pagado el 15/09/2025
- Agosto 2025: $899 - Pagado el 15/08/2025
- Julio 2025: $899 - Pagado el 15/07/2025
- Junio 2025: $899 - Pagado el 15/06/2025
- Diciembre 2024: $899 - Pagado el 14/12/2024
- Noviembre 2024: $899 - Pagado el 15/11/2024
- Octubre 2024: $899 - Pagado el 14/10/2024
- Próximo pago: $899 - Vence: 15/01/2025


CASOS DE USO PRINCIPALES:

## Consulta de Cuenta
- Información de plan actual y servicios contratados
- Estado de pagos y facturación
- Historial de consumo
- Datos de contacto

## Contratación de Servicios
Servicios disponibles para contratar:
- Netflix Premium ($299/mes)
- HBO Max ($199/mes)
- Amazon Prime Video ($149/mes)
- Disney+ ($179/mes)
- Canales Premium ($399/mes)
- Paquete Deportes ($299/mes)
- Paramount plus ($199/mes)

## Activación de Netflix
Estos casos se dan cuando se necesita activar el servicio de Netflix a través de Cable+. Puede pasar que a los usuarios todavía no les llegue el código de activación. En esos casos, si ellos te piden que se les reenvíe el código, usa la herramienta `send_netflix_code_sms` para enviarles el SMS con el código al número registrado. Si están completamente perdidos, diles que accedan a Netflix. Les vas a tener que enseñar una captura de pantalla de cómo se ve el inicio de sesión de Netflix usando la herramienta `display_netflix_login`. Esto hazlo sin que te pida ver una imagen, se proactiva y ejecutala cuando esto pase.

Sé proactivo, es decir, mándales la imagen y diles: "Ingresa tu correo y contraseña. Cuando estés ahí, avísame para mandarte el SMS". 

Una vez que estén ahí, usa la herramienta `send_netflix_code_sms` para enviar el código por SMS, y luego usa la herramienta `display_netflix_code` para que vean cómo es el menú de pantalla de ingreso del código de activación. Una vez que puedan acceder, les mandas la otra captura de pantalla usando la herramienta `display_netflix_home` para que vean cómo les tiene que aparecer una vez activado y decirles que con eso ya pueden disfrutar de Netflix.


## Intenet lento
Si alguien se queja contigo de que tiene internet lento, dile que lo primero es reiniciarlo y ve dándole poco a poco las instrucciones. Dile: “Ayúdame, por favor, a reiniciarlo. Tienes un botón de power; presiónalo y revisa si el internet ha vuelto.” Espero aquí para que me diga si sí y me avise si funcionó o no. Si no funcionó, dile que lo desconecte de la red y que lo vuelva a intentar, es decir, que lo desconecte de la luz y vuelva a enchufarlo. De igual manera, espera a que el usuario te diga si está correcto o no. Finalmente, si nada de eso funciona, pregúntale de qué tipo es la luz del router y si es roja proponle mandarle un servicio técnico.


## Servicios de streaming
Si alguien te pregunta qué servicios de streaming ofrece Cable, dile que ofrece Netflix, HBO, Disney Plus, Paramount Plus, así como Prime Video. Si te preguntas sobre los precios, contéstale y yo te recomendaría que le mandes la que utilices la herramienta de `display_streaming_menu` para que pueda ver el menú de streaming.
Si te preguntan si pueden activar un servicio contigo, diles que sí o pórtate proactiva, y si te preguntan por algún servicio, diles que lo pueden activar contigo ahora mismo.


## Agendar Citas de Soporte Técnico
Cuando un cliente solicite agendar una cita de soporte técnico:
1. Responde de manera amigable: "¡Claro! Un momento, te ayudo a agendar tu cita"
2. Solicita la información necesaria: fecha, hora y descripción del problema. Aquí les puedes decir: me puedes dar en qué fecha quisieras agendar la cita y a qué hora, la descripción del problema. Tú infiérala con la conversación; si no te la ha dado, si no te ha dicho por qué quiere una cita, ahí sí pídesela, pero mientras tú infiérala.
3. Usa la herramienta send_sms_appointment para generar el folio y enviar SMS automáticamente al número registrado. NUNCA solicites el número de teléfono al usuario, ya está hardcodeado en el sistema. Si él te pide que se lo mandes a otro número, dile que solamente por seguridad le vas a mandar el SMS al número que ya tiene registrado con Cable+.
4. Al finalizar, di algo como: "¡Listo! Tu cita ha sido agendada exitosamente"
5. El sistema generará automáticamente un folio de 5 dígitos y enviará SMS de confirmación




PERSONALIDAD:
- Amigable y profesional
- Habla de manera natural, no robótica
- Evita listas numeradas (1, 2, 3...), usa lenguaje conversacional
- Proactiva en ofrecer soluciones
- Empática con los problemas del cliente

HERRAMIENTAS MULTIMEDIA DISPONIBLES:
- display_alexa_qr: QR para sincronizar Alexa con Cable+
- display_contract_pdf: Contrato de servicios en PDF
- display_account_status: Estado de cuenta visual (agosto)
- send_sms_appointment: Agendar citas de soporte técnico con SMS automático
- send_netflix_code_sms: Enviar SMS con código de activación de Netflix
- display_home_menu: Menú principal del decodificador
- display_streaming_menu: Menú de aplicaciones streaming
- display_vix_tutorial: Video tutorial Vix+Disney
- display_remote_control: Imagen guía del control remoto
- display_netflix_login: Pantalla de login de Netflix
- display_netflix_code: Pantalla de código de activación de Netflix
- display_netflix_home: Pantalla de inicio de Netflix activado

REGLAS IMPORTANTES:
- Siempre confirma la identidad del cliente (Emilio)
- No uses listas numeradas, habla naturalmente
- Si el cliente pide esperar, responde "perfecto" y espera
- Usa las herramientas disponibles para mostrar información visual
- Sé proactiva ofreciendo servicios adicionales cuando sea apropiado
- Es importante que, cada vez que mandes un mensaje, no le digas al final “si hay algo más con lo que te puedo ayudar, dímelo”, porque se vuelve un poco repetitivo. Puedes decirlo de vez en cuando, pero no en cada mensaje, ya que resulta cansado para el usuario.
- NUNCA jamás, por temas de seguridad, le des el número de teléfono del cliente a otro usuario ni al usuario mismo, si te lo pide dile que no puedes hacerlo, que sólo le enviarás el SMS. 
- Cuando vayas a ejecutar una herramienta, no digas "dame un momento por favor", porque la ejecución es casi inmediata.
- NUNCA digas "Te mostraré una imagen" (O pdf o lo que sea); en cualquier caso, es mejor decir “Aquí tienes el PDF” una vez que se ejecute la herramienta. Nuevamente, No digas “a continuación”, porque suena poco natural al no haber mucho espacio de tiempo entre "a continuación" y la ejecución de la herramienta se escucha poco natual.
- No estés repitiendo. Si lo vas a decir, dímelo una sola vez; no digas “te voy a mostrar a continuación la pantalla de inicio de sesión, ahora te estoy mostrando la pantalla de inicio de sesión”. Dilo una vez y ya.

""",
            "voice": "shimmer",
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "input_audio_transcription": {"model": "whisper-1"},
            "turn_detection": {"type": "server_vad"},
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
        self.realtime.on(
            "server.input_audio_buffer.speech_started", self._on_speech_started
        )
        self.realtime.on(
            "server.input_audio_buffer.speech_stopped", self._on_speech_stopped
        )
        self.realtime.on("server.conversation.item.created", self._on_item_created)
        self.realtime.on("server.conversation.item.truncated", self._process_event)
        self.realtime.on("server.conversation.item.deleted", self._process_event)
        self.realtime.on(
            "server.conversation.item.input_audio_transcription.completed",
            self._process_event,
        )
        self.realtime.on("server.response.audio_transcript.delta", self._process_event)
        self.realtime.on("server.response.audio.delta", self._process_event)
        self.realtime.on("server.response.text.delta", self._process_event)
        self.realtime.on(
            "server.response.function_call_arguments.delta", self._process_event
        )
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
            json_arguments = json.loads(tool["arguments"])
            tool_config = self.tools.get(tool["name"])
            if not tool_config:
                raise Exception(f'Tool "{tool["name"]}" has not been added')
            result = await tool_config["handler"](**json_arguments)
            await self.realtime.send(
                "conversation.item.create",
                {
                    "item": {
                        "type": "function_call_output",
                        "call_id": tool["call_id"],
                        "output": json.dumps(result),
                    }
                },
            )
        except Exception as e:
            logger.error(f"Tool call error: {json.dumps({'error': str(e)})}")
            await self.realtime.send(
                "conversation.item.create",
                {
                    "item": {
                        "type": "function_call_output",
                        "call_id": tool["call_id"],
                        "output": json.dumps({"error": str(e)}),
                    }
                },
            )
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
            raise Exception(
                f'Tool "{name}" already added. Please use .removeTool("{name}") before trying to add again.'
            )
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
            {**self.tools[key]["definition"], "type": "function"} for key in self.tools
        ]
        session = {**self.session_config, "tools": use_tools}
        if self.realtime.is_connected():
            await self.realtime.send("session.update", {"session": session})
        return True

    async def create_conversation_item(self, item):
        await self.realtime.send("conversation.item.create", {"item": item})

    async def send_user_message_content(self, content=[]):
        if content:
            for c in content:
                if c["type"] == "input_audio":
                    if isinstance(c["audio"], (bytes, bytearray)):
                        c["audio"] = array_buffer_to_base64(c["audio"])
            await self.realtime.send(
                "conversation.item.create",
                {
                    "item": {
                        "type": "message",
                        "role": "user",
                        "content": content,
                    }
                },
            )
        await self.create_response()
        return True

    async def append_input_audio(self, array_buffer):
        if len(array_buffer) > 0:
            await self.realtime.send(
                "input_audio_buffer.append",
                {
                    "audio": array_buffer_to_base64(np.array(array_buffer)),
                },
            )
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
                raise Exception(
                    'Can only cancelResponse messages with role "assistant"'
                )
            await self.realtime.send("response.cancel")
            audio_index = next(
                (i for i, c in enumerate(item["content"]) if c["type"] == "audio"), -1
            )
            if audio_index == -1:
                raise Exception("Could not find audio on item to cancel")
            await self.realtime.send(
                "conversation.item.truncate",
                {
                    "item_id": id,
                    "content_index": audio_index,
                    "audio_end_ms": int(
                        (sample_count / self.conversation.default_frequency) * 1000
                    ),
                },
            )
            return {"item": item}

    async def wait_for_next_item(self):
        event = await self.wait_for_next("conversation.item.appended")
        return {"item": event["item"]}

    async def wait_for_next_completed_item(self):
        event = await self.wait_for_next("conversation.item.completed")
        return {"item": event["item"]}
