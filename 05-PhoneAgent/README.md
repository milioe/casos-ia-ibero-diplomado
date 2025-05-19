# Phone Agent - Azure Functions

Este proyecto implementa los endpoints necesarios para el agente conversacional utilizando Azure Functions, permitiendo la integración con servicios de Google como Calendar y Sheets.

## Requisitos Previos

Antes de comenzar, necesitarás tener instalado:
- Python 3.10 o superior
- Azure Functions Core Tools
- Git (para descargar el código)
- Una cuenta de Google con acceso a Calendar y Sheets

## Configuración del Entorno

### Windows

1. Instala Azure Functions Core Tools:
   - Ve a [docs.microsoft.com](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
   - Descarga e instala el instalador de Windows

2. Abre una terminal (PowerShell o CMD) y navega a la carpeta del proyecto:
```bash
cd 05-PhoneAgent/CODE/Function-AgentTools
```

3. Crea y activa un entorno virtual:
```bash
python -m venv env
.\env\Scripts\activate
```

### macOS

1. Instala Azure Functions Core Tools:
```bash
brew tap azure/functions
brew install azure-functions-core-tools@4
```

2. Abre Terminal y navega a la carpeta del proyecto:
```bash
cd 05-PhoneAgent/CODE/Function-AgentTools
```

3. Crea y activa un entorno virtual:
```bash
python -m venv env
source env/bin/activate
```

## Instalación de Dependencias

Con el entorno virtual activado, instala las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración de Azure Functions

1. Crea un archivo `local.settings.json` en la carpeta `Function-AgentTools` con el siguiente contenido:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "GOOGLE_SHEETS_URL": ""
  }
}
```

2. Asegúrate de que el archivo `host.json` tenga la configuración correcta:
```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  },
  "cors": {
    "allowedOrigins": [
      "*"
    ],
    "supportCredentials": false
  }
}
```

## Configuración de Google API

1. Asegúrate de tener el archivo `.env` en la carpeta principal del diplomado (`casos-ia-ibero-diplomado/.env`) con tus claves de API de OpenAI.

2. Copia este archivo `.env` a la carpeta actual (`Function-AgentTools/.env`).

3. Ejecuta el script de generación de token:
```bash
python generate_token.py
```

4. Se abrirá tu navegador web para que inicies sesión con tu cuenta de Google
5. Autoriza la aplicación para acceder a tu Calendar
6. Se generarán los archivos `token.json` y `client_secret.json` necesarios para la autenticación

## Ejecutar la Función

1. Asegúrate de que el entorno virtual esté activado:
```bash
# Windows
.\env\Scripts\activate

# macOS
source env/bin/activate
```

2. Inicia la función:
```bash
func start
```

La función estará disponible en `http://localhost:7071`

## Notas Importantes

- Esta función implementa los mismos endpoints que vimos en el proyecto 03-Agent
- Los endpoints están diseñados para ser consumidos por una aplicación móvil
- Asegúrate de tener una conexión estable a internet
- Las credenciales de Google se guardan localmente en `token.json`

## Solución de Problemas

Si encuentras algún error, aquí hay algunas soluciones comunes:

1. Si hay problemas al instalar paquetes:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

2. Si la función no inicia:
- Verifica que el entorno virtual esté activado
- Asegúrate de que Azure Functions Core Tools esté instalado correctamente
- Verifica que el puerto 7071 no esté siendo usado por otra aplicación

3. Si hay problemas con la autenticación de Google:
- Verifica que los archivos `token.json` y `client_secret.json` existan
- Asegúrate de haber autorizado la aplicación correctamente
- Si es necesario, elimina `token.json` y vuelve a ejecutar `generate_token.py` 