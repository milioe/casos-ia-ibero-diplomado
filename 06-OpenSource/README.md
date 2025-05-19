# Ejemplos con Ollama - Modelos Open Source

Este proyecto contiene ejemplos de uso de Ollama con diferentes modelos de lenguaje open source, incluyendo chat con historial, salidas estructuradas y procesamiento de imágenes.

## Requisitos Previos

Antes de comenzar, necesitarás tener instalado:
- Python 3.10 o superior
- Anaconda (es una herramienta que nos ayudará a manejar el entorno de Python)
- Git (para descargar el código)
- Ollama (instrucciones de instalación abajo)

## Instalación de Ollama

### Windows

1. Descarga el instalador de Windows desde [ollama.ai](https://ollama.ai/download)
2. Ejecuta el instalador
3. Abre PowerShell o CMD y verifica la instalación:
```bash
ollama --version
```

### macOS

1. Abre Terminal y ejecuta:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

2. Verifica la instalación:
```bash
ollama --version
```

## Iniciar el Servidor de Ollama

1. Abre una nueva terminal y ejecuta:
```bash
ollama serve
```
Mantén esta terminal abierta, el servidor debe estar corriendo para usar Ollama.

## Descargar Modelos

Puedes encontrar todos los modelos disponibles en el [Buscador de Modelos de Ollama](https://ollama-com.translate.goog/search?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc). Algunos modelos populares incluyen:

- `llama2` - Modelo base para chat general (7B, 13B, 70B parámetros)
- `llava` - Modelo para procesamiento de imágenes
- `codellama` - Especializado en código
- `mistral` - Modelo eficiente de 7B parámetros
- `gemma` - Modelo de Google (2B, 7B parámetros)
- `phi` - Modelos ligeros de Microsoft

1. En una nueva terminal, descarga el modelo que desees usar. Por ejemplo:
```bash
# Para chat general
ollama pull llama2

# Para procesamiento de imágenes
ollama pull llava
```

2. Lista los modelos instalados:
```bash
ollama list
```

## Configuración del Entorno Python

### Windows

1. Abre Anaconda Prompt:
   - Presiona la tecla Windows
   - Escribe "Anaconda Prompt"
   - Haz clic en "Anaconda Prompt" para abrirlo

2. Crea y activa el entorno:
```bash
conda create -n ollama python=3.10
conda activate ollama
```

### macOS

1. Abre Terminal:
   - Presiona Command + Espacio
   - Escribe "Terminal"
   - Presiona Enter

2. Crea y activa el entorno:
```bash
conda create -n ollama python=3.10
conda activate ollama
```

## Instalación de Dependencias

1. Navega a la carpeta del proyecto:
```bash
cd 06-OpenSource
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejemplos Disponibles

### 1. Chat con Historial
```bash
python chat-with-history.py
```
Este ejemplo muestra cómo mantener una conversación con contexto usando Ollama.

### 2. Salidas Estructuradas
```bash
python structured-outputs.py
```
Demuestra cómo obtener respuestas en formato JSON o estructurado.

### 3. Notebook de Ejemplos
El archivo `ollama_sdk.ipynb` contiene ejemplos más avanzados usando el SDK de Ollama. Puedes ir ejecutando celda por celda para ver diferentes formas de interactuar con los modelos.

## Comandos Útiles de Ollama

| Comando | Descripción |
|---------|-------------|
| `ollama serve` | Inicia el servidor de Ollama |
| `ollama pull <modelo>` | Descarga un modelo |
| `ollama list` | Lista los modelos instalados |
| `ollama run <modelo>` | Inicia una conversación |
| `ollama rm <modelo>` | Elimina un modelo |

## Notas Importantes

- El servidor de Ollama debe estar corriendo (`ollama serve`) antes de ejecutar cualquier ejemplo
- Los modelos se ejecutan localmente en tu computadora
- La primera ejecución de un modelo puede ser lenta mientras se carga en memoria
- Asegúrate de tener suficiente espacio en disco para los modelos

## Solución de Problemas

1. Si el servidor no inicia:
- Verifica que Ollama esté instalado correctamente
- Asegúrate de que no haya otro proceso usando el puerto 11434
- Reinicia tu computadora y vuelve a intentar

2. Si los modelos son lentos:
- Verifica los recursos de tu sistema
- Cierra aplicaciones innecesarias
- Considera usar un modelo más ligero

3. Si hay problemas con Python:
- Verifica que el entorno esté activado
- Reinstala las dependencias
- Asegúrate de tener la versión correcta de Python 