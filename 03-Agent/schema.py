# Definir las herramientas del asistente
tools = [
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "enviar_confirmacion_cita",
    #         "description": "Envía un correo de confirmación de cita al usuario",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "nombre": {
    #                     "type": "string",
    #                     "description": "Nombre completo del estudiante o profesor",
    #                 },
    #                 "correo": {
    #                     "type": "string",
    #                     "description": "Correo electrónico de contacto",
    #                 },
    #                 "dia": {
    #                     "type": "string",
    #                     "enum": ["lunes", "martes", "miércoles", "jueves", "viernes"],
    #                     "description": "Día de la semana para la cita",
    #                 },
    #                 "hora": {
    #                     "type": "string",
    #                     "description": "Hora de la cita en formato HH:MM",
    #                 },
    #                 "asunto": {
    #                     "type": "string",
    #                     "description": "Breve descripción del asunto a tratar en la cita",
    #                 },
    #             },
    #             "required": ["nombre", "correo", "dia", "hora", "asunto"],
    #         },
    #     },
    # },
    {
        "type": "function",
        "function": {
            "name": "obtener_horarios_ocupados_semana",
            "description": "Obtiene los horarios ocupados para las próximas dos semanas",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "crear_evento_calendario",
            "description": "Crea un nuevo evento en Google Calendar con duración de 30 minutos e invita a una persona por correo",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {
                        "type": "string",
                        "description": "Título del evento",
                    },
                    "fecha": {
                        "type": "string",
                        "description": "Fecha en formato YYYY-MM-DD (por ejemplo, 2023-10-15)",
                    },
                    "hora_inicio": {
                        "type": "string",
                        "description": "Hora de inicio en formato HH:MM (por ejemplo, 14:30)",
                    },
                    "correo_invitado": {
                        "type": "string",
                        "description": "Correo electrónico del invitado",
                    },
                    "descripcion": {
                        "type": "string",
                        "description": "Descripción del evento",
                    }
                },
                "required": ["titulo", "fecha", "hora_inicio", "correo_invitado", "descripcion"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "obtener_info_alumno",
            "description": "Obtiene la información completa de un alumno por su ID desde la base de datos",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_alumno": {
                        "type": "string",
                        "description": "ID del alumno (por ejemplo, A001)",
                    }
                },
                "required": ["id_alumno"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "obtener_cursos_alumno",
            "description": "Obtiene los cursos e inscripciones de un alumno por su ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_alumno": {
                        "type": "string",
                        "description": "ID del alumno (por ejemplo, A001)",
                    }
                },
                "required": ["id_alumno"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "obtener_pedidos_biblioteca",
            "description": "Obtiene los pedidos de biblioteca realizados por un alumno por su ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_alumno": {
                        "type": "string",
                        "description": "ID del alumno (por ejemplo, A001)",
                    }
                },
                "required": ["id_alumno"],
            },
        },
    }
]
