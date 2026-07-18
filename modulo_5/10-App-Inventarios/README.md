# 10 - App de inventarios

Proyecto guía para construir con Cursor una aplicación web de operación de
bodegas y almacenes.

## Estructura

- `front/`: interfaz web (se entrega vacía para que el alumno la implemente).
- `back/`: API y tools de acceso controlado a datos (se entrega vacía).
- `base-de-datos/`: modelo PostgreSQL, datos iniciales y documentación.
- `system_prompt.md`: prompt maestro para copiar en Cursor e iniciar el proyecto.

Lee primero `base-de-datos/README.md` y después copia el contenido de
`system_prompt.md` en un chat nuevo de Cursor.

## Objetivo

La aplicación deberá permitir consultar inventario, registrar movimientos,
detectar faltantes, revisar capacidad de almacenamiento y administrar recursos
operativos sin permitir que el modelo genere SQL libre.
