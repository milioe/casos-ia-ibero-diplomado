# API-ExtractInfo

Esta es una API de Flask que utiliza el modelo GPT-4o de OpenAI para extraer información de tickets y facturas a partir de imágenes.

## Requisitos

- Python 3.8+
- OpenAI API Key
- OpenAI Organization ID (opcional)

## Instalación

1. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno:

```bash
export OPENAI_API_KEY=tu_api_key
export OPENAI_ORG_ID=tu_org_id  # Opcional
```

O crear un archivo `.env` en el directorio raíz:

```
OPENAI_API_KEY=tu_api_key
OPENAI_ORG_ID=tu_org_id  # Opcional
```

## Ejecución

```bash
python app.py
```

Esto iniciará el servidor en `http://localhost:7071`.

## Endpoints

### POST /api/extract_info

Extrae información de imágenes de tickets o facturas.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Archivos de imágenes (cualquier nombre de campo)

**Response:**
```json
{
  "nombre_compania": "string",
  "rfc": "string",
  "fecha": "string",
  "productos": ["string"],
  "unidades": ["string"],
  "montos": [0.0],
  "clave_facturacion": "string",
  "ubicacion": "string",
  "telefono": "string"
}
```

## Integración con la UI

La UI existente está configurada para conectarse a este endpoint en `http://localhost:7071/api/extract_info`. Si se cambia la URL o el puerto de la API, también debe actualizarse en la aplicación UI. 