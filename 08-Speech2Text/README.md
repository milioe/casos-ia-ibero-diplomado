# 🎙️ Speech to Text - Extractor de Diálogos

Esta herramienta convierte transcripciones de entrevistas en documentos Word estructurados, con formato profesional para uso en expedientes.

## 📋 Requisitos previos

- Python 3.10 o superior
- Anaconda o Miniconda instalado
- Una clave API válida de OpenAI

## 🔧 Configuración del entorno

### En Windows

1. Abre Anaconda Prompt desde el menú de inicio
2. Crea un nuevo entorno conda:
```
conda create -n speech2text python=3.10
```
3. Activa el entorno:
```
conda activate speech2text
```

### En Mac

1. Abre Terminal
2. Crea un nuevo entorno conda:
```
conda create -n speech2text python=3.10
```
3. Activa el entorno:
```
conda activate speech2text
```

## 📦 Instalación de dependencias

1. Navega a la carpeta del proyecto:
```
cd ruta/a/casos-ia-ibero-diplomado/08-Speech2Text
```

2. Instala las dependencias:
```
pip install -r requirements.txt
```

## 🔑 Configuración de la API de OpenAI

1. Asegúrate de tener un archivo `.env` en la carpeta principal `casos-ia-ibero-diplomado/` con tu clave API de OpenAI:
```
OPENAI_API_KEY=tu-clave-api-aquí
OPENAI_ORG_ID=tu-id-de-organizacion-aqui  # opcional
```

## 🚀 Ejecución de la aplicación

1. Desde la carpeta del proyecto, ejecuta:
```
python app.py
```

2. Se abrirá una interfaz web en tu navegador (generalmente en http://localhost:7071)

3. Sube un archivo PDF, DOCX o TXT que contenga una transcripción de entrevista

4. Haz clic en "Process Document" para extraer la estructura del diálogo

5. Completa los campos adicionales (opcional):
   - Nombre de la persona agraviada
   - Número de expediente
   - Fecha y hora
   - Integrantes de la Unidad del Comité

6. Haz clic en "Download as Word" para descargar el documento estructurado 📄

## ❓ Solución de problemas comunes

- **Error de OpenAI API key**: Verifica que tu archivo `.env` contiene una clave API válida
- **Error al procesar archivo**: Asegúrate que el archivo contiene texto que se puede extraer
- **La aplicación no inicia**: Verifica que todas las dependencias se instalaron correctamente

## 🛑 Apagar la aplicación

1. Para detener la aplicación, presiona Ctrl+C en la terminal/prompt donde está ejecutándose
2. Para desactivar el entorno conda:
```
conda deactivate
``` 