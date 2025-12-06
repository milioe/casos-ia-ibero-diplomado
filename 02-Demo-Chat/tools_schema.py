TOOLS_SCHEMA = [
    {
        "type": "function",
        "name": "analizar_imagen",
        "description": "Analiza una imagen adjunta por el usuario (factura, estado de cuenta, equipo, captura de pantalla, etc.) y proporciona una descripción detallada de lo que contiene. ÚSALA CUANDO EL USUARIO MENCIONE QUE ADJUNTÓ O ENVIARÁ UNA IMAGEN.",
        "parameters": {
            "type": "object",
            "properties": {
                "ruta_imagen": {
                    "type": "string",
                    "description": "Ruta del archivo de imagen que el usuario adjuntó. Usa el path del elemento Image recibido en el mensaje."
                }
            },
            "required": ["ruta_imagen"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "obtener_info_cliente",
        "description": "Obtiene la información completa de un cliente utilizando su ID de cliente",
        "parameters": {
            "type": "object",
            "properties": {
                "id_cliente": {
                    "type": "string",
                    "description": "ID único del cliente (número de 4 dígitos)"
                }
            },
            "required": ["id_cliente"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "obtener_contratos_cliente",
        "description": "Obtiene los contratos y planes asociados a un cliente, con opción de filtrar por status",
        "parameters": {
            "type": "object",
            "properties": {
                "id_cliente": {
                    "type": "string",
                    "description": "ID único del cliente para buscar sus contratos"
                },
                "filtro_status": {
                    "type": ["string", "null"],
                    "enum": ["activo", "inactivo", None],
                    "description": "Filtro opcional: 'activo' para planes activos, 'inactivo' para inactivos, null para todos"
                }
            },
            "required": ["id_cliente", "filtro_status"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "agendar_cita",
        "description": "Agenda una cita técnica para un cliente registrado. Solicitar información paso a paso al cliente.",
        "parameters": {
            "type": "object",
            "properties": {
                "id_cliente": {
                    "type": "string",
                    "description": "ID del cliente que agenda la cita"
                },
                "nombre": {
                    "type": "string",
                    "description": "Nombre del cliente"
                },
                "apellido": {
                    "type": "string",
                    "description": "Apellido del cliente"
                },
                "descripcion_problema": {
                    "type": "string",
                    "description": "Descripción detallada del problema o motivo de la cita"
                },
                "sucursal": {
                    "type": "string",
                    "description": "Sucursal donde se realizará la cita (Tlalpan, Coyoacán, Venustiano Carranza, Benito Juárez, Xochimilco, Indios Verdes)"
                },
                "fecha_reporte": {
                    "type": ["string", "null"],
                    "description": "Fecha y hora deseada para la cita en formato YYYY-MM-DD HH:MM:SS"
                }
            },
            "required": ["id_cliente", "nombre", "apellido", "descripcion_problema", "sucursal", "fecha_reporte"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "enviar_factura_contratos",
        "description": "Envía por correo electrónico la factura detallada de contratos activos del cliente. Usa la información del cliente que ya tienes en el historial.",
        "parameters": {
            "type": "object",
            "properties": {
                "email_cliente": {
                    "type": "string",
                    "description": "Email del cliente obtenido previamente con obtener_info_cliente"
                },
                "nombre_completo": {
                    "type": "string",
                    "description": "Nombre completo del cliente (nombre + apellido) obtenido previamente"
                },
                "id_cliente": {
                    "type": "string",
                    "description": "ID del cliente"
                },
                "contratos_ids": {
                    "type": ["array", "null"],
                    "items": {"type": "string"},
                    "description": "Lista de IDs de contratos específicos a incluir. Si es null, envía todos los contratos activos"
                }
            },
            "required": ["email_cliente", "nombre_completo", "id_cliente", "contratos_ids"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]