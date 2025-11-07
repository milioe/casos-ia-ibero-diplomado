# LangGraph Studio - Agent Development IDE

LangGraph Studio es un entorno de desarrollo integrado (IDE) especializado para la construcción y depuración de agentes de IA. Forma parte del ecosistema LangChain y proporciona herramientas visuales para acelerar el desarrollo de agentes inteligentes.

## Características Principales

### Desarrollo Visual de Agentes
- **Visualización de grafos**: Observa cómo tu agente ejecuta cada nodo del grafo en tiempo real
- **Depuración interactiva**: Establece interrupciones antes y después de cada nodo para análisis detallado
- **Interfaz de chat**: Prueba tu agente en conversaciones multi-turno con una UI tradicional de chat

### Desarrollo en Tiempo Real
- **Auto-recarga**: Los cambios en el código se reflejan instantáneamente en Studio
- **Iteración rápida**: Modifica prompts, modelos y configuraciones sin reiniciar
- **Testing en vivo**: Prueba cambios directamente en la interfaz de Studio

### Gestión de Conversaciones
- **Fork de conversaciones**: Crea bifurcaciones para explorar diferentes caminos de ejecución
- **Modificación de herramientas**: Edita llamadas a herramientas y observa los resultados
- **Historial completo**: Mantén un registro detallado de todas las interacciones

## Configuración Inicial

### Prerrequisitos
- Python 3.11+
- LangGraph CLI instalado
- Archivo `langgraph.json` configurado
- Cuenta en LangSmith Studio (recomendado)
- **Cuenta en Tavily AI** (requerida para herramientas de búsqueda)
- Google Chrome (Safari no es compatible)

### Instalación

1. **Instalar dependencias del proyecto**:
```bash
pip install -r requirements.txt
```

2. **Instalar LangGraph CLI** (si no está incluido en requirements.txt):
```bash
pip install langgraph-cli
```

3. **Configurar API Keys**:
   - Crea una cuenta en [Tavily AI](https://tavily.com/)
   - Obtén tu API key de Tavily
   - Agrégala a tu archivo `.env`:
   ```env
   TAVILY_API_KEY=tu-api-key-de-tavily
   OPENAI_API_KEY=tu-api-key-de-openai
   ```

### Configuración del Proyecto

1. **Crear archivo `langgraph.json`**:
```json
{
  "dependencies": ["./requirements.txt"],
  "graphs": {
    "agent": "./graph.py:graph"
  },
  "env": ".env"
}
```

2. **Estructura del proyecto**:
```
04-LangGraph/
├── graph.py          # Definición del agente
├── langgraph.json    # Configuración del proyecto
├── requirements.txt  # Dependencias
├── .env             # Variables de entorno
└── README.md        # Este archivo
```

## Uso Básico

### Configuración de Cuenta (Recomendado)
Antes de comenzar, es altamente recomendable crear una cuenta en [LangSmith Studio](https://smith.langchain.com/) para aprovechar todas las funcionalidades de integración y monitoreo.

### Iniciar el Servidor de Desarrollo
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar el servidor de desarrollo
langgraph dev
```

**Importante**: 
- Usa **Google Chrome** para la mejor experiencia (Safari no es compatible)
- El comando abrirá Studio automáticamente en tu navegador
- Si tienes una cuenta de LangSmith, podrás asociarla para funcionalidades avanzadas

Este comando:
- Lanza un servidor local que expone tu grafo vía API
- Abre Studio automáticamente en tu navegador
- Habilita la recarga automática de cambios

### Funcionalidades del Studio

#### 1. Visualización de Ejecución
- Observa el flujo de ejecución paso a paso
- Identifica cuellos de botella y puntos de falla
- Analiza el comportamiento de cada nodo

#### 2. Testing con Interrupciones
- Configura puntos de interrupción en cualquier nodo
- Implementa "human-in-the-loop" para validación manual
- Controla el flujo de ejecución de manera granular

#### 3. Experimentación con Prompts
- Modifica prompts del sistema en tiempo real
- Cambia modelos de lenguaje sobre la marcha
- Compara resultados de diferentes configuraciones

## Integración con Producción

### Conexión con LangSmith
Studio se integra seamlessly con LangSmith para:
- **Análisis de trazas de producción**: Importa trazas reales para depuración local
- **Evaluación continua**: Filtra trazas por métricas de evaluación
- **Clonación de threads**: Reproduce escenarios de producción localmente

### Flujo de Trabajo de Depuración

1. **Identificar problemas**: Usa evaluadores online en LangSmith para detectar trazas problemáticas
2. **Importar a Studio**: Clona la traza problemática en tu entorno local
3. **Iterar y mejorar**: Modifica el código y prueba los cambios en tiempo real
4. **Validar solución**: Continúa la conversación o reinicia desde el principio
5. **Desplegar**: Sube los cambios a producción una vez validados

## Ejemplo de Agente React

El proyecto incluye un agente React básico que demuestra:
- Uso de herramientas de búsqueda web (Tavily AI)
- Manejo de prompts del sistema
- Configuración de modelos de lenguaje
- Procesamiento de respuestas estructuradas

### Sobre Tavily AI

**Tavily AI** es un servicio especializado en búsqueda web y scraping inteligente diseñado específicamente para agentes de IA. Proporciona:

- **Búsqueda web optimizada**: Resultados relevantes y actualizados
- **Scraping inteligente**: Extracción automática de contenido de páginas web
- **API sencilla**: Integración fácil con agentes de LangGraph
- **Filtrado de contenido**: Elimina ruido y se enfoca en información útil
- **Respuestas estructuradas**: Formato optimizado para procesamiento por IA

Para usar Tavily, necesitas:
1. Crear una cuenta gratuita en [tavily.com](https://tavily.com/)
2. Obtener tu API key desde el dashboard
3. Configurarla en tu archivo `.env`

### Configuración del Agente
```python
from tavily import TavilySearchResults

# Herramientas disponibles
tools = [TavilySearchResults(
    max_results=10, 
    search_depth="advanced",
    api_key=os.getenv("TAVILY_API_KEY")
)]

# Prompt del sistema con contexto inteligente
system_prompt = """
Eres un asistente de investigación especializado que proporciona información actualizada y relevante.
Usa las herramientas de búsqueda para encontrar datos precisos y contextualizados.

Cuando busques información, considera:
- La relevancia temporal de los eventos
- Múltiples fuentes para validar información
- El contexto geográfico cuando sea relevante
- Tendencias actuales en el tema consultado

Siempre proporciona respuestas bien estructuradas y cita las fuentes cuando sea posible.
"""

# Creación del agente
graph = create_react_agent(model, tools, system_prompt)
```

## Mejores Prácticas

- [Documentación oficial de LangGraph](https://langchain-ai.github.io/langgraph/)
- [LangGraph Platform](https://langchain-ai.github.io/langgraph/cloud/)
- [Comunidad LangChain](https://discord.gg/langchain)

## Notas Importantes

- **Compatibilidad de navegadores**: Usa Google Chrome para la mejor experiencia. Safari no es compatible con todas las funcionalidades
- **Cuenta LangSmith**: Aunque no es obligatoria, una cuenta en LangSmith Studio desbloquea funcionalidades avanzadas de monitoreo y análisis
- **Instalación**: Siempre ejecuta `pip install -r requirements.txt` antes de `langgraph dev`
- **Python**: Requiere Python 3.11 o superior
- Studio es gratuito y está disponible para uso inmediato
- Los cambios en el código se reflejan instantáneamente sin necesidad de reiniciar
- La integración con LangSmith permite un flujo completo desde desarrollo hasta producción
- El playground integrado permite experimentación avanzada con prompts y modelos

---

LangGraph Studio transforma el desarrollo de agentes de IA al proporcionar visibilidad completa del comportamiento del agente y herramientas poderosas para iteración rápida y depuración efectiva.
