# Introducción a OpenAI API

Este notebook contiene ejemplos y ejercicios prácticos para aprender a utilizar las APIs de OpenAI, incluyendo:
- Procesamiento de texto
- Generación de imágenes
- Conversión de texto a voz
- Análisis de audio

## Requisitos Previos

Antes de comenzar, necesitarás tener instalado:
- Python 3.10 o superior
- Anaconda (es una herramienta que nos ayudará a manejar el entorno de Python)
- Jupyter Notebook o Jupyter Lab

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
conda create -n openai python=3.10
```
Cuando te pregunte si deseas proceder, escribe 'y' y presiona Enter.

Luego, escribe:
```bash
conda activate openai
```

4. Instala Jupyter:
```bash
conda install jupyter
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
conda create -n openai python=3.10
```
Cuando te pregunte si deseas proceder, escribe 'y' y presiona Enter.

Luego, escribe:
```bash
conda activate openai
```

4. Instala Jupyter:
```bash
conda install jupyter
```

## Configuración de las Claves de API

1. Asegúrate de tener el archivo `.env` en la carpeta principal del diplomado (`casos-ia-ibero-diplomado/.env`) con tus claves de API de OpenAI.

2. Copia este archivo `.env` a la carpeta actual (`01-API-OpenAI/.env`).

## Ejecutar el Notebook

1. Navega a la carpeta del proyecto:
```bash
cd 01-API-OpenAI
```

2. Inicia Jupyter Notebook:
```bash
jupyter notebook
```

3. Se abrirá tu navegador web con Jupyter. Haz clic en `Fundamentals.ipynb` para comenzar.

## Notas Importantes

- Asegúrate de que el entorno `openai` esté activado antes de ejecutar el notebook
- El notebook contiene ejemplos prácticos que requieren una conexión a internet
- Algunos ejemplos pueden consumir créditos de tu cuenta de OpenAI

## Solución de Problemas

Si encuentras algún error, aquí hay algunas soluciones comunes:

1. Si hay problemas al instalar paquetes:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

2. Si Jupyter no se inicia:
- Verifica que el entorno esté activado
- Asegúrate de que Jupyter esté instalado correctamente
- Intenta reiniciar el navegador 