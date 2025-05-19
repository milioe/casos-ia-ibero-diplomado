# VisionApp

Este proyecto consiste en utilizar OpenAI para imagenes con outputs estructurados con dos opciones de backend y una interfaz de usuario en Gradio.

## Índice

1. [Estructura del Proyecto](#1-estructura-del-proyecto)
2. [Requisitos Previos](#2-requisitos-previos)
3. [Configuración del Entorno](#3-configuración-del-entorno)
   - 3.1 [Windows](#31-windows)
   - 3.2 [macOS](#32-macos)
4. [Instalación de Dependencias](#4-instalación-de-dependencias)
5. [Backend con Flask (API-ExtractInfo)](#5-backend-con-flask-api-extractinfo)
   - 5.1 [Windows](#51-windows)
   - 5.2 [macOS](#52-macos)
6. [Backend con Azure Functions (Function-ExtractInfo)](#6-backend-con-azure-functions-function-extractinfo)
   - 6.1 [Windows](#61-windows)
   - 6.2 [macOS](#62-macos)
7. [Frontend (UI)](#7-frontend-ui)
8. [Notas Importantes](#8-notas-importantes)
9. [Solución de Problemas](#9-solución-de-problemas)

## 1. Estructura del Proyecto

```
02-VisionApp/
├── CODE/
│   ├── API-ExtractInfo/     # Backend con Flask
│   ├── Function-ExtractInfo/ # Backend con Azure Functions
│   └── UI/                  # Frontend con Gradio
└── requirements.txt         # Dependencias principales
```

## 2. Requisitos Previos

Antes de comenzar, necesitarás tener instalado:
- Python 3.10 o superior
- Anaconda (es una herramienta que nos ayudará a manejar el entorno de Python)
- Git (para descargar el código)

## 3. Configuración del Entorno

### 3.1 Windows

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
conda create -n visionapp python=3.10
```
Cuando te pregunte si deseas proceder, escribe 'y' y presiona Enter.

Luego, escribe:
```bash
conda activate visionapp
```

### 3.2 macOS

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
conda create -n visionapp python=3.10
```
Cuando te pregunte si deseas proceder, escribe 'y' y presiona Enter.

Luego, escribe:
```bash
conda activate visionapp
```

## 4. Instalación de Dependencias

Ahora necesitamos instalar las herramientas necesarias para el proyecto. 

1. Primero, asegúrate de estar en la carpeta correcta:
   - En Windows: Usa el comando `cd` para navegar a la carpeta del proyecto. Por ejemplo:
   ```bash
   cd C:\ruta\a\tu\proyecto\02-VisionApp
   ```
   - En macOS: Usa el comando `cd` para navegar a la carpeta del proyecto. Por ejemplo:
   ```bash
   cd /ruta/a/tu/proyecto/02-VisionApp
   ```

2. Instala las dependencias copiando y pegando este comando:
```bash
pip install -r requirements.txt
```

## 5. Backend con Flask (API-ExtractInfo)

### 5.1 Windows

1. Abre una nueva ventana de Anaconda Prompt y activa el entorno:
```bash
conda activate visionapp
```

2. Navega a la carpeta del backend:
```bash
cd CODE/API-ExtractInfo
```

3. Instala las dependencias específicas:
```bash
pip install -r requirements.txt
```

4. Inicia el servidor:
```bash
python app.py
```

Verás un mensaje indicando que la API está funcionando en `http://localhost:5000`

### 5.2 macOS

Los pasos son los mismos que en Windows, pero usando Terminal en lugar de Anaconda Prompt.

## 6. Backend con Azure Functions (Function-ExtractInfo)

### 6.1 Windows

1. Primero, instala Azure Functions Core Tools:
   - Ve a [docs.microsoft.com](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
   - Descarga e instala el instalador de Windows

2. Abre una nueva ventana de Anaconda Prompt y activa el entorno:
```bash
conda activate visionapp
```

3. Navega a la carpeta del backend:
```bash
cd CODE/Function-ExtractInfo
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Inicia el servidor:
```bash
func start
```

Verás un mensaje indicando que la función está funcionando en `http://localhost:7071`

### 6.2 macOS

1. Primero, instala Azure Functions Core Tools. Abre Terminal y ejecuta:
```bash
brew tap azure/functions
brew install azure-functions-core-tools@4
```

2. Sigue los mismos pasos que en Windows desde el paso 2.

## 7. Frontend (UI)

### Windows y macOS

1. Abre una nueva ventana de Anaconda Prompt (Windows) o Terminal (macOS) y activa el entorno:
```bash
conda activate visionapp
```

2. Navega a la carpeta de la interfaz:
```bash
cd CODE/UI
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Inicia la interfaz:
```bash
python app.py
```

Se abrirá automáticamente tu navegador web con la interfaz en `http://localhost:7860`

## 8. Notas Importantes

- Necesitarás copiar el archivo `.env` que contiene tus claves de API de OpenAI desde la carpeta principal del diplomado (`casos-ia-ibero-diplomado/.env`) a cada una de las carpetas del proyecto (API-ExtractInfo, Function-ExtractInfo y UI)
- Para usar Azure Functions, necesitarás una cuenta de Azure
- La interfaz de Gradio se conectará automáticamente al backend que esté ejecutándose

## 9. Solución de Problemas

Si encuentras algún error, aquí hay algunas soluciones comunes:

1. Si hay problemas al instalar las dependencias:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

2. Si Azure Functions no funciona:
- Verifica que Azure Functions Core Tools esté instalado correctamente
- Asegúrate de tener las credenciales de Azure configuradas

3. Si la interfaz de Gradio no se abre:
- Verifica que el puerto 7860 no esté siendo usado por otra aplicación
- Asegúrate de que el backend esté funcionando antes de iniciar la UI 