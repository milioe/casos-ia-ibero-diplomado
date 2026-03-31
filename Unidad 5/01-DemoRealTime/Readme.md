# 📺 Cable+ - Portal de Atención al Cliente

Asistente virtual con voz en tiempo real usando OpenAI Realtime API.

## 🚀 Inicio Rápido

```bash
cd /Users/emiliosandoval/Documents/HD/Demo-Realtime
chainlit run app.py --port 8008
```

Accede a: http://localhost:8008

## 🎤 Usar el Asistente

1. **Presiona la tecla `P`** para activar el micrófono
2. **Habla** con Sofía
3. Ella responderá por voz en tiempo real

## 🛠️ Herramientas Disponibles

Sofía puede:
- 📄 Mostrar contrato de servicios (PDF)
- 💳 Mostrar estado de cuenta
- 🏠 Mostrar menú principal del decodificador
- 🎬 Mostrar menú de streaming
- 📱 Mostrar QR de Alexa
- 📱 Mostrar guía del control remoto
- 🎥 Mostrar video tutorial Vix+Disney

## 📁 Estructura del Proyecto

```
Demo-Realtime/
├── app.py                  # Aplicación principal
├── realtime/              # Cliente Realtime de OpenAI
│   ├── __init__.py
│   └── tools.py           # Herramientas multimedia
├── assets/                # Recursos multimedia
│   ├── alexaqr.png
│   ├── estado_cuenta.png
│   ├── menuhome.png
│   ├── menustraming.png
│   ├── ControlRemotoGuia.png
│   ├── VixVideo.mp4
│   └── Contrato_Servicios_Cable_Mas.pdf
└── .chainlit/
    └── config.toml        # Configuración de Chainlit
```

## ⚙️ Configuración

### Variables de Entorno (.env):

Crea un archivo `.env` en el directorio del proyecto:

```bash
OPENAI_API_KEY=tu_llave_aqui
```

## 🔧 Troubleshooting

### Error: "OPENAI_API_KEY not found"
- Verifica que el archivo `.env` existe en el directorio del proyecto
- Agrega tu llave de OpenAI API

### Puerto ocupado
- Cambia el puerto: `chainlit run app.py --port 8009`

### Micrófono no funciona
- Verifica que el audio esté habilitado en `.chainlit/config.toml`
- Permite el acceso al micrófono cuando el navegador lo solicite

## 📚 Información del Cliente

**Cliente:** Emilio Sandoval
- **Plan actual:** Premium Cable + Telefonía
- **Servicios incluidos:** Cable HD, Telefonía ilimitada, Internet 100 Mbps
- **Servicios adicionales:** Netflix Básico
- **Fecha de corte:** 15 de cada mes
- **Próximo pago:** $899 MXN
- **Estado de cuenta:** Al corriente
- **Teléfono:** 55-1234-5678

## 💬 Servicios Disponibles

**STREAMING:**
- Netflix Premium ($299/mes) - 4K, 4 pantallas
- HBO Max ($199/mes) - Contenido premium
- Amazon Prime Video ($149/mes) - Incluye envíos gratis
- Disney+ ($179/mes) - Contenido familiar

**PREMIUM:**
- Canales Premium ($399/mes) - Fox Premium, Universal+
- Paquete Deportes ($299/mes) - ESPN, Fox Sports

## 👤 Sofía - Tu Asistente Virtual

Sofía es la asistente virtual de Cable+ que puede:
- Responder preguntas sobre tu cuenta
- Ayudar con servicios adicionales (Netflix, HBO, etc.)
- Proporcionar soporte técnico
- Mostrar documentos y manuales
- ¡Y todo por voz en tiempo real!

---

**Desarrollado con ❤️ para Cable+**