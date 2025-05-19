# Diplomado Ibero - Casos de IA

Este repositorio contiene diferentes proyectos y ejemplos prácticos de Inteligencia Artificial desarrollados durante el diplomado. Cada proyecto está diseñado para explorar diferentes aspectos y tecnologías de IA.

## 01-API-OpenAI
Introducción práctica a las APIs de OpenAI, incluyendo:
- Notebook interactivo (`Fundamentals.ipynb`) con ejemplos de uso
- Procesamiento de texto con diferentes modelos
- Generación de imágenes con DALL-E
- Conversión de texto a voz
- Análisis de audio y video
- Ejemplos de salidas estructuradas

[Ver instrucciones detalladas](01-API-OpenAI/README.md)

## 02-VisionApp
Aplicación de visión artificial que utiliza OpenAI para procesar imágenes con dos opciones de backend:
- API con Flask para procesamiento de imágenes
- Azure Functions para escalabilidad en la nube
- Interfaz de usuario con Gradio
- Procesamiento de imágenes con salidas estructuradas
- Integración completa con OpenAI

[Ver instrucciones detalladas](02-VisionApp/README.md)

## 03-Agent
Agente conversacional inteligente implementado con:
- Interfaz web usando Chainlit
- Sistema de herramientas extensible
- Integración con Google Calendar y Sheets
- Manejo de prompts del sistema
- Procesamiento de lenguaje natural
- Capacidades de razonamiento y toma de decisiones

[Ver instrucciones detalladas](03-Agent/README.md)

## 04-RealTime-Demo
Sistema de demostración en tiempo real que incluye:
- Aplicación web con WebSockets
- Interfaz pública interactiva
- Procesamiento de datos en tiempo real
- Integración con Chainlit para chat en vivo
- Componentes de tiempo real modulares
- Sistema de verificación de conexiones

## 05-PhoneAgent
Implementación de agente para dispositivos móviles usando Azure Functions:
- Endpoints para integración con aplicaciones móviles
- Herramientas de agente adaptadas para móvil
- Integración con Google Calendar
- Sistema de autenticación OAuth
- Manejo de hojas de cálculo de Google
- Procesamiento de solicitudes asíncronas

[Ver instrucciones detalladas](05-PhoneAgent/README.md)

## 06-OpenSource
Ejemplos de uso de modelos de lenguaje open source con Ollama:
- Chat con historial y contexto
- Generación de salidas estructuradas
- Procesamiento de imágenes con modelos locales
- Ejemplos de diferentes modelos (llama2, mistral, gemma)
- Notebook con ejemplos avanzados
- Ejecución local sin dependencias en la nube

[Ver instrucciones detalladas](06-OpenSource/README.md)

## Configuración General

### Requisitos del Sistema
- Python 3.10 o superior
- Anaconda o Miniconda (recomendado para gestión de entornos)
- Git para control de versiones
- Acceso a Internet para APIs y dependencias

### Variables de Entorno
El archivo `.env` en la raíz del proyecto debe contener las claves necesarias para el funcionamiento de los proyectos. Se proporciona un archivo `env.example` con la siguiente estructura:

```env
# OpenAI API Keys (Requerido para todos los proyectos)
OPENAI_API_KEY=tu-api-key-de-openai
OPENAI_ORG_ID=tu-organization-id-de-openai

# Google API Keys (Requerido solo para proyectos 03-Agent y 05-PhoneAgent)
GOOGLE_SHEETS_URL=url-de-tu-google-sheet
GOOGLE_CALENDAR_ID=id-de-tu-calendario

# Azure Configuration (Requerido solo para proyectos 02-VisionApp y 05-PhoneAgent)
AZURE_STORAGE_CONNECTION_STRING=tu-connection-string
AZURE_FUNCTION_APP_NAME=nombre-de-tu-function-app

# Otros servicios
PORT=8000
ENVIRONMENT=development
```

Copia el archivo `env.example` a `.env` y reemplaza los valores con tus propias credenciales. Ten en cuenta que:
- La clave de API de OpenAI (`OPENAI_API_KEY`) es **obligatoria** para todos los proyectos
- Las demás variables son necesarias solo para proyectos específicos
- Consulta el README de cada proyecto para ver qué variables son necesarias

### Estructura de Carpetas
Cada proyecto contiene:
- `README.md` con instrucciones específicas
- `requirements.txt` con dependencias
- Código fuente y ejemplos
- Archivos de configuración necesarios

## Notas Importantes
- Cada proyecto tiene su propia documentación detallada
- Se recomienda seguir las instrucciones de instalación de cada proyecto
- Algunos proyectos requieren configuración adicional (API keys, credenciales)
- Los proyectos están diseñados para ser modulares e independientes

## Próximos Pasos
- Mejoras en la documentación de cada proyecto
- Implementación de nuevos casos de uso
- Integración con servicios adicionales
- Optimización de rendimiento
- Ejemplos adicionales y tutoriales

## Contribuciones
Se aceptan contribuciones mediante Pull Requests. Por favor, asegúrate de:
- Seguir las guías de estilo del proyecto
- Documentar adecuadamente los cambios
- Mantener la estructura modular
- Probar los cambios antes de enviarlos
