# Carpeta Sources - Telefonía Mex

Esta carpeta contiene todos los recursos multimedia para la aplicación de Telefonía Mex:

## Archivos necesarios:

### Imágenes
- `control_remoto.png` - Imagen del control remoto de Telefonía Mex
- `logo_telefonia_mex.png` - Logo de la empresa
- `menu_principal.png` - Captura del menú principal del decodificador

### PDFs
- `manual_completo.pdf` - Manual completo de servicios y configuración
- `guia_control_remoto.pdf` - Guía detallada del control remoto
- `terminos_servicios.pdf` - Términos y condiciones de servicios

### Videos
- `tutorial_configuracion.mp4` - Video tutorial de configuración inicial
- `como_usar_control.mp4` - Video explicativo del control remoto

## Instrucciones:
1. Agrega los archivos correspondientes en esta carpeta
2. Actualiza las rutas en `tools.py` para que apunten a estos archivos
3. Las herramientas automáticamente mostrarán el contenido multimedia

## Ejemplo de actualización en tools.py:
```python
# Cambiar esto:
await cl.Message(content="*Imagen se mostrará aquí*").send()

# Por esto:
image = cl.Image(
    path="/Users/emiliosandoval/Documents/HD/Demo-Realtime/sources/control_remoto.png",
    name="control_remoto",
    display="inline"
)
await cl.Message(content=message, elements=[image]).send()
```
