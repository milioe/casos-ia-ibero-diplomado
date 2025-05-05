# Asistente Virtual Iberia

Este proyecto es un asistente virtual para la Universidad Iberoamericana que proporciona información y servicios a estudiantes y personal.

## Características

- Agenda citas en Google Calendar
- Consulta horarios ocupados
- Accede a información de estudiantes desde Google Sheets
- Consulta cursos e inscripciones
- Verifica préstamos de biblioteca

## Requisitos

- Python 3.9+
- Cuenta de Google con permisos para Calendar API (solo si usas la función de calendario)

## Configuración

1. Clona este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` con las siguientes variables:

```
OPENAI_API_KEY=tu_clave_de_api_openai
OPENAI_ORG_ID=tu_id_de_organizacion_openai
GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/1aFL9U_Z556GnURZ-K35zV4bKsheHHfwMp4KNCty0lEg/edit?usp=sharing
```

4. Para el acceso a Google Calendar (SOLO NECESARIO SI USAS EL CALENDARIO):
   - Ejecuta `python generate_token.py` para generar tu token de autenticación
   - Sigue las instrucciones en pantalla para autorizar la aplicación

## Acceso a Google Sheets

El sistema está configurado para acceder a Google Sheets de dos formas:

1. **Hojas públicas**: No requiere autenticación ni token. Simplemente asegúrate de que la hoja sea pública o esté compartida con "Cualquiera con el enlace puede ver".

2. **Hojas privadas**: Requiere autenticación OAuth. En este caso, necesitarás ejecutar `python generate_token.py` para generar el token.

La configuración por defecto intenta primero el acceso como hoja pública y, si falla, recurre a la autenticación OAuth.

## Ejecución

Para iniciar el asistente:

```bash
chainlit run app.py
```

## Herramientas Disponibles

### Calendario
- `obtener_horarios_ocupados_semana`: Muestra los horarios ocupados de las próximas dos semanas
- `crear_evento_calendario`: Crea un nuevo evento en el calendario con duración de 30 min

### Base de Datos Académica
- `obtener_info_alumno`: Consulta información personal de un estudiante por ID
- `obtener_cursos_alumno`: Obtiene cursos e inscripciones de un estudiante
- `obtener_pedidos_biblioteca`: Consulta préstamos de biblioteca de un estudiante

## Estructura de la Base de Datos

La base de datos académica está alojada en Google Sheets con las siguientes hojas:

1. **alumnos**: Información personal de estudiantes
   - ID_Alumno, Nombre, Apellidos, Email, Teléfono, Carrera, Estado, etc.

2. **cursos**: Catálogo de cursos disponibles
   - ID_Curso, Nombre, Profesor, Modalidad, Fecha_Inicio, Estado

3. **inscripciones**: Registro de inscripciones de alumnos a cursos
   - ID_Inscripción, ID_Alumno, ID_Curso, Fecha, Estado, Calificación_Final

4. **pedidos_biblioteca**: Registro de préstamos de libros
   - ID_Pedido, ID_Alumno, Libro, Fecha_Pedido, Estado, Fecha_Devolución