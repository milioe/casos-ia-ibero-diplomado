from openai import OpenAI
import json

client = OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORG_ID
)

# Definir el JSON Schema para la extracción del currículum
json_schema = {
    "type": "json_schema",
    "name": "curriculum_info",
    "schema": {
        "type": "object",
        "properties": {
            "informacion_personal": {
                "type": "object",
                "properties": {
                    "nombre_completo": {"type": "string"},
                    "correo": {"type": "string"},
                    "telefono": {"type": "string"},
                    "linkedin": {"type": "string"},
                    "ubicacion": {"type": "string"}
                },
                "required": ["nombre_completo", "correo"],
                "additionalProperties": False
            },
            "perfil_profesional": {
                "type": "object",
                "properties": {
                    "titulo_profesional": {"type": "string"},
                    "anios_experiencia": {"type": "integer"},
                    "resumen_profesional": {"type": "string"}
                },
                "required": ["titulo_profesional", "anios_experiencia"],
                "additionalProperties": False
            },
            "experiencia_laboral": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "puesto": {"type": "string"},
                        "empresa": {"type": "string"},
                        "fecha_inicio": {"type": "string"},
                        "fecha_fin": {"type": "string"},
                        "responsabilidades": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["puesto", "empresa", "fecha_inicio", "responsabilidades"],
                    "additionalProperties": False
                }
            },
            "educacion": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "grado": {"type": "string"},
                        "campo_estudio": {"type": "string"},
                        "institucion": {"type": "string"},
                        "anio_inicio": {"type": "integer"},
                        "anio_fin": {"type": "integer"},
                        "promedio": {"type": "number"}
                    },
                    "required": ["grado", "institucion"],
                    "additionalProperties": False
                }
            },
            "habilidades_tecnicas": {
                "type": "object",
                "properties": {
                    "lenguajes_programacion": {"type": "array", "items": {"type": "string"}},
                    "herramientas_big_data": {"type": "array", "items": {"type": "string"}},
                    "plataformas_cloud": {"type": "array", "items": {"type": "string"}},
                    "bases_datos": {"type": "array", "items": {"type": "string"}},
                    "herramientas_devops": {"type": "array", "items": {"type": "string"}},
                    "herramientas_visualizacion": {"type": "array", "items": {"type": "string"}}
                },
                "additionalProperties": False
            },
            "certificaciones": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "nombre_certificacion": {"type": "string"},
                        "anio_obtencion": {"type": "integer"}
                    },
                    "required": ["nombre_certificacion"],
                    "additionalProperties": False
                }
            },
            "idiomas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "idioma": {"type": "string"},
                        "nivel": {"type": "string"}
                    },
                    "required": ["idioma", "nivel"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["informacion_personal", "perfil_profesional", "experiencia_laboral", "educacion", "habilidades_tecnicas"],
        "additionalProperties": False
    },
    "strict": True
}

print(json.dumps(json_schema, indent=2))

