import json, os
from openai import AsyncOpenAI
import chainlit as cl
import dotenv
from tools import (
    analizar_imagen,
    obtener_info_cliente, 
    obtener_contratos_cliente, 
    agendar_cita, 
    enviar_confirmacion_cita, 
    enviar_sms_confirmacion_cita,
    enviar_factura_contratos
)
from tools_schema import TOOLS_SCHEMA
from system_prompt import SYSTEM_PROMPT

dotenv.load_dotenv()

# ─────────────────── 1. OpenAI & Chainlit ────────────────────────────────────
cl.instrument_openai()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─────────────────── 2. Configuration ────────────────────────────────────────
MAX_ITER = 20

# ─────────────────── 3. conversation helpers ────────────────────────────────
@cl.on_chat_start
def _start():
    cl.user_session.set("full_conversation_history", [])
    cl.user_session.set("previous_response_id", None)
    cl.user_session.set("tool_results", {})
    cl.user_session.set("dev_prompt", SYSTEM_PROMPT)


@cl.step(type="tool")
async def call_function_tool(call, full_history):
    # Set step name to actual function name for better visibility
    s = cl.context.current_step
    s.name = f"{call['name']}"

    try:
        args = json.loads(call.get("arguments") or "{}")
    except json.JSONDecodeError:
        args = {}
        out = json.dumps({"error": "Invalid function arguments"})
        full_history.append(
            {
                "role": "function",
                "name": call["name"],
                "content": out,
                "tool_call_id": call["call_id"],
            }
        )
        tool_results = cl.user_session.get("tool_results")
        tool_results[call["call_id"]] = out
        cl.user_session.set("tool_results", tool_results)
        s.input = {"function": call["name"], "arguments": "invalid_json"}
        s.output, s.language = out, "json"
        return out

    if call["name"] == "analizar_imagen":
        out = analizar_imagen(args.get("ruta_imagen", ""))
    elif call["name"] == "obtener_info_cliente":
        out = obtener_info_cliente(args.get("id_cliente", ""))
    elif call["name"] == "obtener_contratos_cliente":
        out = obtener_contratos_cliente(args.get("id_cliente", ""), args.get("filtro_status"))
    elif call["name"] == "agendar_cita":
        out = agendar_cita(
            args.get("id_cliente", ""),
            args.get("nombre", ""),
            args.get("apellido", ""),
            args.get("descripcion_problema", ""),
            args.get("sucursal", ""),
            args.get("fecha_reporte")
        )
        
        # Enviar correo y SMS de confirmación automáticamente si la cita se creó exitosamente
        try:
            result_data = json.loads(out)
            if result_data.get("success"):
                # Obtener info del cliente
                info_cliente = json.loads(obtener_info_cliente(args.get("id_cliente", "")))
                if info_cliente.get("encontrado"):
                    nombre_completo = f"{args.get('nombre', '')} {args.get('apellido', '')}"
                    
                    # Enviar correo
                    if info_cliente.get("email"):
                        enviar_confirmacion_cita(
                            info_cliente["email"],
                            args.get("nombre", ""),
                            args.get("apellido", ""),
                            result_data["id_cita"],
                            result_data["fecha_reporte"],
                            result_data["sucursal"],
                            result_data["descripcion_problema"]
                        )
                    
                    # Enviar SMS
                    if info_cliente.get("telefono"):
                        enviar_sms_confirmacion_cita(
                            info_cliente["telefono"],
                            nombre_completo,
                            result_data["id_cita"],
                            result_data["fecha_reporte"],
                            result_data["sucursal"]
                        )
        except:
            pass  # Si falla el envío, no afectar el resultado de la cita
    
    elif call["name"] == "enviar_factura_contratos":
        out = enviar_factura_contratos(
            args.get("email_cliente", ""),
            args.get("nombre_completo", ""),
            args.get("id_cliente", ""),
            args.get("contratos_ids")
        )
    else:
        out = json.dumps({"error": f"Unknown function {call['name']}"})

    # Cache successful result
    tool_results = cl.user_session.get("tool_results")
    tool_results[call["call_id"]] = out
    cl.user_session.set("tool_results", tool_results)

    full_history.append(
        {
            "role": "function",
            "name": call["name"],
            "content": out,
            "tool_call_id": call["call_id"],
        }
    )

    s.input = {"function": call["name"], "arguments": args}
    s.output, s.language = out, "json"
    return out


async def _ask_gpt5(input_messages, prev_id=None):
    
    # Si no hay imágenes, usar GPT-5 normal
    dev_input = []
    if not prev_id:
        dev_input.append({
            "role": "developer",
            "content": cl.user_session.get("dev_prompt") or SYSTEM_PROMPT,
        })
    stream = await client.responses.create(
        model="gpt-5",
        reasoning={"effort": "minimal"},
        input=dev_input + input_messages,
        instructions="Utiliza las herramientas cuando sea necesario para ayudar al cliente.",
        stream=True,
        store=True,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
        **({"previous_response_id": prev_id} if prev_id else {}),
    )
    ans = cl.Message(author="Assistant", content="")
    await ans.send()
    calls, resp_id = [], None
    assistant_text = ""

    async for ev in stream:
        if ev.type == "response.created":
            resp_id = ev.response.id
        elif ev.type == "response.output_item.added" and ev.item.type == "function_call":
            calls.append(
                {
                    "id": ev.item.id,
                    "call_id": ev.item.call_id,
                    "name": ev.item.name,
                    "arguments": "",
                }
            )
        elif ev.type == "response.function_call_arguments.delta":
            next(c for c in calls if c["id"] == ev.item_id)["arguments"] += ev.delta
        elif ev.type == "response.output_text.delta":
            assistant_text += ev.delta
            await ans.stream_token(ev.delta)

    await ans.update()

    if assistant_text.strip():
        full_history = cl.user_session.get("full_conversation_history")
        full_history.append({"role": "assistant", "content": assistant_text})
        cl.user_session.set("full_conversation_history", full_history)

    # Handle incomplete responses
    try:
        final_response = stream.get_final_response()
        if (
            hasattr(final_response, "status")
            and final_response.status == "incomplete"
            and final_response.incomplete_details.reason == "max_output_tokens"
        ):
            await cl.Message(
                content="⚠️ Response was truncated due to length limits",
                author="System",
            ).send()
    except Exception:
        pass

    return resp_id, calls


@cl.on_message
async def _on_msg(m: cl.Message):
    full_history = cl.user_session.get("full_conversation_history")

    if not full_history:
        full_history.append(
            {"role": "developer", "content": cl.user_session.get("dev_prompt") or SYSTEM_PROMPT}
        )

    # Procesar mensaje y detectar si hay imágenes
    message_content = m.content
    image_paths = []
    
    # Detectar imágenes adjuntas
    if m.elements:
        for element in m.elements:
            if element.mime and element.mime.startswith("image/") and element.path:
                image_paths.append(element.path)
                print(f"DEBUG - Imagen detectada: {element.path}")
    
    # Si hay imágenes, agregar info al mensaje para que GPT-5 las analice con la tool
    if image_paths:
        message_content += f"\n\n[SISTEMA: El usuario adjuntó {len(image_paths)} imagen(es). Ruta(s): {', '.join(image_paths)}. Usa la herramienta 'analizar_imagen' para ver el contenido.]"
        print(f"DEBUG - Mensaje con {len(image_paths)} imagen(es) adjunta(s)")
    
    full_history.append({"role": "user", "content": message_content})
    cl.user_session.set("full_conversation_history", full_history)

    current_turn_messages = [{"role": "user", "content": message_content}]
    prev_response_id = cl.user_session.get("previous_response_id")

    for _ in range(MAX_ITER):
        resp_id, calls = await _ask_gpt5(current_turn_messages, prev_response_id)

        if not calls:
            break

        for call in calls:
            await call_function_tool(call, full_history)

        tool_results = cl.user_session.get("tool_results")
        current_turn_messages = [
            {
                "type": "function_call_output",
                "call_id": call["call_id"],
                "output": tool_results[call["call_id"]],
            }
            for call in calls
        ]
        prev_response_id = resp_id

    cl.user_session.set("full_conversation_history", full_history)
    cl.user_session.set("previous_response_id", resp_id)