import azure.functions as func
import json
import logging
import pandas as pd

from tools import (obtener_info_alumno, obtener_cursos_alumno, obtener_pedidos_biblioteca, obtener_horarios_ocupados_semana, crear_evento_calendario)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Encabezados CORS completos
headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"
}


# Endpoint: Google Sheets - Información del Alumno
@app.route(route="ObtenerInfoAlumno", methods=["GET", "POST", "OPTIONS"])
def ObtenerInfoAlumno(req: func.HttpRequest) -> func.HttpResponse:
    if req.method.upper() == "OPTIONS":
        return func.HttpResponse(status_code=200, headers=headers)
    
    body = req.get_json()
    id_alumno = body.get('id_alumno')
    tool_call_id = "default_call_id"
    
    if 'message' in body:
        message = body['message']
        if 'toolCalls' in message and message['toolCalls']:
            tool_call = message['toolCalls'][0]
            tool_call_id = tool_call.get('id', tool_call_id)
            if 'function' in tool_call and 'arguments' in tool_call['function']:
                id_alumno = tool_call['function']['arguments'].get('id_alumno')
    
    respuesta = json.loads(obtener_info_alumno(id_alumno))
    
    if respuesta.get("estado") == "ok":
        info = respuesta.get("datos", {})
        
        nombre_completo = f"{info.get('Nombre')} {info.get('Apellido_Paterno')} {info.get('Apellido_Materno')}"
        
        mensaje = f"El alumno {nombre_completo} con matrícula {info.get('ID_Alumno')} está estudiando la carrera de {info.get('Carrera')} y su estado es {info.get('Estado')}. Su correo es {info.get('Email')}. Su teléfono es {info.get('Teléfono')}"
    else:
        mensaje = f"No se encontró información para el alumno con ID {id_alumno}."
    
    return func.HttpResponse(
        json.dumps({
            "results": [{
                "toolCallId": tool_call_id,
                "result": mensaje
            }]
        }, ensure_ascii=False),
        mimetype="application/json; charset=utf-8",
        status_code=200,
        headers=headers
    )


# Endpoint: Google Sheets - Cursos del Alumno
@app.route(route="ObtenerCursosAlumno", methods=["GET", "POST", "OPTIONS"])
def ObtenerCursosAlumno(req: func.HttpRequest) -> func.HttpResponse:
    if req.method.upper() == "OPTIONS":
        return func.HttpResponse(status_code=200, headers=headers)
    
    body = req.get_json()
    id_alumno = body.get('id_alumno')
    tool_call_id = "default_call_id"
    
    if 'message' in body:
        message = body['message']
        if 'toolCalls' in message and message['toolCalls']:
            tool_call = message['toolCalls'][0]
            tool_call_id = tool_call.get('id', tool_call_id)
            if 'function' in tool_call and 'arguments' in tool_call['function']:
                id_alumno = tool_call['function']['arguments'].get('id_alumno')
    
    respuesta = json.loads(obtener_cursos_alumno(id_alumno))
    
    logging.info(f"Respuesta: {respuesta}")
    
    if respuesta.get("estado") == "ok":
        cursos = respuesta.get("cursos", [])
        if cursos:
            cursos_info = []
            for curso_data in cursos:
                curso = curso_data.get('curso', {})
                inscripcion = curso_data.get('inscripcion', {})
                estado = inscripcion.get('Estado', '')
                calificacion = inscripcion.get('Calificación_Final', 'No disponible')
                if isinstance(calificacion, float) and not pd.isna(calificacion):
                    calificacion = f"{calificacion:.1f}"
                elif pd.isna(calificacion):
                    calificacion = "No disponible"
                
                curso_info = f"{curso.get('Nombre_Curso', '')} ({curso.get('Modalidad', '')}) - Estado: {estado}, Calificación: {calificacion}"
                cursos_info.append(curso_info)
            
            mensaje = f"Cursos del alumno (Total: {len(cursos)}): " + " -".join([''] + cursos_info)
        else:
            mensaje = "El alumno no tiene cursos registrados."
    else:
        mensaje = respuesta.get("mensaje", f"No se encontraron cursos para el alumno con ID {id_alumno}.")
    
    return func.HttpResponse(
        json.dumps({
            "results": [{
                "toolCallId": tool_call_id,
                "result": mensaje
            }]
        }, ensure_ascii=False),
        mimetype="application/json; charset=utf-8",
        status_code=200,
        headers=headers
    )

# Endpoint: Google Sheets - Pedidos de Biblioteca
@app.route(route="ObtenerPedidosBiblioteca", methods=["GET", "POST", "OPTIONS"])
def ObtenerPedidosBiblioteca(req: func.HttpRequest) -> func.HttpResponse:
    if req.method.upper() == "OPTIONS":
        return func.HttpResponse(status_code=200, headers=headers)
    
    body = req.get_json()
    id_alumno = body.get('id_alumno')
    tool_call_id = "default_call_id"
    
    if 'message' in body:
        message = body['message']
        if 'toolCalls' in message and message['toolCalls']:
            tool_call = message['toolCalls'][0]
            tool_call_id = tool_call.get('id', tool_call_id)
            if 'function' in tool_call and 'arguments' in tool_call['function']:
                id_alumno = tool_call['function']['arguments'].get('id_alumno')
    
    respuesta = json.loads(obtener_pedidos_biblioteca(id_alumno))
    
    logging.info(f"Respuesta: {respuesta}")
    
    if respuesta.get("estado") == "ok":
        pedidos = respuesta.get("pedidos", [])
        if pedidos:
            pedidos_info = []
            for pedido in pedidos:
                fecha_entrega = pedido.get('Fecha_Entrega', 'No especificada')
                titulo = pedido.get('Titulo', 'Sin título')
                estado = pedido.get('Estado', 'No especificado')
                fecha_prestamo = pedido.get('Fecha_Prestamo', 'No especificada')
                
                pedido_info = f"'{titulo}' - Prestado: {fecha_prestamo}, Entrega: {fecha_entrega}, Estado: {estado}"
                pedidos_info.append(pedido_info)
            
            mensaje = f"Pedidos de biblioteca (Total: {len(pedidos)}): " + " -".join([''] + pedidos_info)
        else:
            mensaje = "El alumno no tiene pedidos de biblioteca activos."
    else:
        mensaje = respuesta.get("mensaje", f"No se encontraron pedidos de biblioteca para el alumno con ID {id_alumno}.")
    
    return func.HttpResponse(
        json.dumps({
            "results": [{
                "toolCallId": tool_call_id,
                "result": mensaje
            }]
        }, ensure_ascii=False),
        mimetype="application/json; charset=utf-8",
        status_code=200,
        headers=headers
    )

# Endpoint: Google Calendar - Obtener Horarios Ocupados
@app.route(route="ObtenerHorariosOcupados", methods=["GET", "POST", "OPTIONS"])
def ObtenerHorariosOcupados(req: func.HttpRequest) -> func.HttpResponse:
    if req.method.upper() == "OPTIONS":
        return func.HttpResponse(status_code=200, headers=headers)
    
    body = req.get_json()
    tool_call_id = "default_call_id"
    
    if 'message' in body:
        message = body['message']
        if 'toolCalls' in message and message['toolCalls']:
            tool_call = message['toolCalls'][0]
            tool_call_id = tool_call.get('id', tool_call_id)
    
    respuesta = json.loads(obtener_horarios_ocupados_semana())
    
    if respuesta.get("estado") == "ok":
        semana_actual = respuesta.get("semana_actual", {})
        semana_proxima = respuesta.get("semana_proxima", {})
        
        mensaje = "Horarios ocupados:Semana Actual: "
        for dia, datos in semana_actual.items():
            if datos["bloques_ocupados"]:
                mensaje += f"{dia.capitalize()}: "
                eventos = [f"{ev['titulo']} ({ev['hora_inicio']}-{ev['hora_fin']})" 
                          for ev in datos["bloques_ocupados"]]
                mensaje += ", ".join(eventos) + " "
        
        mensaje += "\nSemana Próxima: "
        for dia, datos in semana_proxima.items():
            if datos["bloques_ocupados"]:
                mensaje += f"{dia.capitalize()}: "
                eventos = [f"{ev['titulo']} ({ev['hora_inicio']}-{ev['hora_fin']})" 
                          for ev in datos["bloques_ocupados"]]
                mensaje += ", ".join(eventos) + " "
        
        if not any(datos["bloques_ocupados"] for datos in semana_actual.values()) and \
           not any(datos["bloques_ocupados"] for datos in semana_proxima.values()):
            mensaje = "No hay horarios ocupados en las próximas dos semanas."
    else:
        mensaje = respuesta.get("mensaje", "Error al obtener los horarios ocupados.")
    
    return func.HttpResponse(
        json.dumps({
            "results": [{
                "toolCallId": tool_call_id,
                "result": mensaje
            }]
        }, ensure_ascii=False),
        mimetype="application/json; charset=utf-8",
        status_code=200,
        headers=headers
    )

# Endpoint: Google Calendar - Crear Evento
@app.route(route="CrearEvento", methods=["GET", "POST", "OPTIONS"])
def CrearEvento(req: func.HttpRequest) -> func.HttpResponse:
    if req.method.upper() == "OPTIONS":
        return func.HttpResponse(status_code=200, headers=headers)
    
    body = req.get_json()
    tool_call_id = "default_call_id"
    
    if 'message' in body:
        message = body['message']
        if 'toolCalls' in message and message['toolCalls']:
            tool_call = message['toolCalls'][0]
            tool_call_id = tool_call.get('id', tool_call_id)
            if 'function' in tool_call and 'arguments' in tool_call['function']:
                args = tool_call['function']['arguments']
                titulo = args.get('titulo', '')
                fecha = args.get('fecha', '')
                hora_inicio = args.get('hora_inicio', '')
                correo_invitado = args.get('correo_invitado', '')
                descripcion = args.get('descripcion', '')
    else:
        titulo = body.get('titulo', '')
        fecha = body.get('fecha', '')
        hora_inicio = body.get('hora_inicio', '')
        correo_invitado = body.get('correo_invitado', '')
        descripcion = body.get('descripcion', '')
    
    respuesta = json.loads(crear_evento_calendario(
        titulo=titulo,
        fecha=fecha,
        hora_inicio=hora_inicio,
        correo_invitado=correo_invitado,
        descripcion=descripcion
    ))
    
    logging.info(f"Respuesta: {respuesta}")
    
    if respuesta.get("estado") == "ok":
        mensaje = f"Evento '{titulo}' creado exitosamente con la fecha {fecha} y el horario {hora_inicio}"
        if respuesta.get("id_evento"):
            mensaje += f", con id {respuesta.get('id_evento')}"
        if correo_invitado:
            mensaje += f". Se ha enviado una invitación a {correo_invitado}"
    else:
        mensaje = respuesta.get("mensaje", "Error al crear el evento")
    
    return func.HttpResponse(
        json.dumps({
            "results": [{
                "toolCallId": tool_call_id,
                "result": mensaje
            }]
        }, ensure_ascii=False),
        mimetype="application/json; charset=utf-8",
        status_code=200,
        headers=headers
    )

