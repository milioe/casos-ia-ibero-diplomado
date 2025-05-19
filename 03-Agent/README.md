# Agente con Chainlit

Este proyecto implementa un agente conversacional utilizando Chainlit como interfaz de usuario, permitiendo una interacción más amigable y visual con el modelo de lenguaje.

## Requisitos Previos

Antes de comenzar, necesitarás tener instalado:
- Python 3.10 o superior
- Anaconda (es una herramienta que nos ayudará a manejar el entorno de Python)
- Git (para descargar el código)

## Configuración del Entorno

### Windows

1. Primero, descarga e instala Anaconda:
   - Ve a [anaconda.com](https://www.anaconda.com/download)
   - Haz clic en "Download" para Windows
   - Ejecuta el instalador que descargaste
   - Sigue las instrucciones del instalador (puedes dejar todas las opciones por defecto)

2. Abre Anaconda Prompt:
   - Presiona la tecla Windows
   - Escribe "Anaconda Prompt"
   - Haz clic en "Anaconda Prompt" para abrirlo

3. En la ventana de Anaconda Prompt, copia y pega estos comandos uno por uno (presiona Enter después de cada uno):
```bash
conda create -n agent python=3.10
```
Cuando te pregunte si deseas proceder, escribe 'y' y presiona Enter.

Luego, escribe:
```bash
conda activate agent
```

### macOS

1. Primero, descarga e instala Anaconda:
   - Ve a [anaconda.com](https://www.anaconda.com/download)
   - Haz clic en "Download" para macOS
   - Abre el archivo .pkg descargado
   - Sigue las instrucciones del instalador

2. Abre Terminal:
   - Presiona Command + Espacio
   - Escribe "Terminal"
   - Presiona Enter

3. En la Terminal, copia y pega estos comandos uno por uno (presiona Enter después de cada uno):
```bash
conda create -n agent python=3.10
```
Cuando te pregunte si deseas proceder, escribe 'y' y presiona Enter.

Luego, escribe:
```bash
conda activate agent
```

## Instalación de Dependencias

1. Navega a la carpeta del proyecto:
```bash
cd 03-Agent
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración de las Claves de API

1. Asegúrate de tener el archivo `.env` en la carpeta principal del diplomado (`casos-ia-ibero-diplomado/.env`) con tus claves de API de OpenAI.

2. Copia este archivo `.env` a la carpeta actual (`03-Agent/.env`).

## Ejecutar la Aplicación

1. Asegúrate de que el entorno `agent` esté activado:
```bash
conda activate agent
```

2. Ejecuta la aplicación:
```bash
chainlit run app.py
```

3. Se abrirá automáticamente tu navegador web con la interfaz de Chainlit en `http://localhost:8000`

## Notas Importantes

- La aplicación utiliza Chainlit para crear una interfaz web interactiva
- El agente puede realizar múltiples tareas a través de diferentes herramientas
- Asegúrate de tener una conexión estable a internet
- Algunas funcionalidades pueden consumir créditos de tu cuenta de OpenAI

## Solución de Problemas

Si encuentras algún error, aquí hay algunas soluciones comunes:

1. Si hay problemas al instalar paquetes:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

2. Si Chainlit no se inicia:
- Verifica que el entorno esté activado
- Asegúrate de que todas las dependencias estén instaladas correctamente
- Verifica que el puerto 8000 no esté siendo usado por otra aplicación

3. Si hay problemas con las APIs:
- Verifica que el archivo `.env` esté correctamente configurado
- Asegúrate de que las claves de API sean válidas
- Verifica tu conexión a internet