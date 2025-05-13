import base64
import json
import logging
import os
from flask import Flask, request, jsonify
from pydantic import BaseModel, Field
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

class DocumentInfo(BaseModel):
    nombre_compania: str = Field(description="Nombre de la compañía")
    rfc: str = Field(description="RFC de la compañía")
    fecha: str = Field(description="Fecha del ticket")
    productos: List[str] = Field(description="Lista de productos")
    unidades: List[str] = Field(description="Lista de unidades/cantidades de los productos")
    montos: List[float] = Field(description="Lista de montos correspondientes a los productos")
    clave_facturacion: str = Field(description="Clave para facturar")
    ubicacion: str = Field(description="Ubicación de la compañía")
    telefono: str = Field(description="Número telefónico de la compañía")

def process_document(images_binary: List[bytes]) -> DocumentInfo:
    """
    Procesa una o más imágenes de documentos escolares usando GPT-4 Vision.
    
    Args:
        images_binary (List[bytes]): Lista de imágenes en formato binario
        
    Returns:
        DocumentInfo: Objeto Pydantic con la información extraída
    """
    try:
        # Convertir las imágenes binarias a base64
        base64_images = [base64.b64encode(img).decode('utf-8') for img in images_binary]
        
        # Inicializar el cliente de OpenAI con API key y organización
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID")
        )

        # Crear la lista de contenido con todas las imágenes
        content = [
            {
                "type": "text",
                "text": """Analiza las siguientes imágenes y extrae la información solicitada."""
            }
        ]

        # Agregar cada imagen al contenido
        for base64_image in base64_images:
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })

        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un experto en extraer información de tickets y facturas.
                    
                    Debes extraer la siguiente información:
                    - Nombre de la compañía
                    - RFC de la compañía
                    - Fecha del ticket
                    - Lista de productos
                    - Lista de unidades/cantidades de los productos
                    - Lista de montos correspondientes a los productos
                    - Clave para facturar
                    - Ubicación de la compañía
                    - Número telefónico de la compañía
                    
                    Reglas:
                    - Si un campo no se encuentra, devuelve string vacío ("")
                    - Para productos, unidades y montos, devuelve listas vacías si no se encuentran
                    - Para montos, asegúrate de convertirlos a números decimales
                    - Para unidades, incluye la unidad de medida si está disponible (ej: "2 kg", "3 pzas")
                    - Si hay múltiples imágenes, combina la información encontrada
                    - Valida que los RFCs tengan formato válido
                    - Para fechas, usa formato YYYY-MM-DD
                    """
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=1_000,
            temperature=0.1,
            response_format=DocumentInfo
        )

        return response.choices[0].message.parsed

    except Exception as e:
        logging.error(f"Error processing images with GPT-4 Vision: {str(e)}")
        raise

@app.route('/api/extract_info', methods=['POST'])
def extract_info():
    """
    Endpoint Flask para procesar imágenes de documentos escolares y tickets.
    
    Returns:
        response: Respuesta HTTP con la información extraída
    """
    logging.info('Processing document extraction request...')

    try:
        # Obtener todos los archivos de la petición
        images_binary = []
        
        # Iterar sobre todos los archivos en la petición
        for file_key in request.files:
            file = request.files[file_key]
            if file:
                images_binary.append(file.read())
        
        if not images_binary:
            return jsonify({"error": "Please upload at least one image file"}), 400
        
        # Procesar las imágenes y obtener resultados
        result = process_document(images_binary)
        
        return jsonify(result.model_dump()), 200

    except Exception as e:
        logging.error(f"Error in extract_info endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7071, debug=True) 