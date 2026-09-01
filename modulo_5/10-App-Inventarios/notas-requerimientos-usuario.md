# Notas — lo que necesitamos (borrador)

Hola. Somos la operación de **Empresa XYZ** (retail / distribución ligera). Vendemos por web y tienda, pero el dolor real hoy no es la venta: es **saber qué hay en piso** entre el CEDIS de Vallejo (CDMX) y el de Occidente (GDL). Hoy se opera con Excel, WhatsApp y “preguntarle a Laura o a Raúl”. Se nos van faltantes, transferencias fantasma y conteos que no cuadran.

Qué ya trae (o va a traer) la base, en cristiano — no es técnico, es lo que de verdad manejamos:
- **Clientes:** nombre, teléfono, correo, ciudad y un “nivel” (oro, etc.). Unos 15 de ejemplo; varios mal capturados.
- **Productos / items:** SKU, descripción corta, categoría (electrónica, alimentos, hogar, textil…) y precio. Unos 15; algunos inactivos o con precio raro.
- **Pedidos y sus líneas:** quién compró, fecha, estatus (capturado → pagado → en ruta → entregado / cancelado), canal (web/tienda) y qué productos llevaba con cantidad. Hay pedidos “en progreso” y otros ya cerrados o cancelados. Ojo: a veces el total del pedido **no cuadra** con la suma de las líneas.
- **Catálogos** de estatus, categorías, canales y niveles de cliente (para no inventar textos a mano).
- **Bodegas:** al menos Vallejo (CDMX) y Occidente (GDL), con responsable.
- **Almacenes dentro de cada bodega:** general, refrigerado, devoluciones, etc.
- **Ubicaciones** tipo pasillo-estante-nivel (ej. A-01-02) donde realmente se acomoda la mercancía.
- **Existencias:** cuánto hay de cada producto en cada ubicación, lote, caducidad si aplica, cuánto está reservado y desde cuándo “pide reabasto”.
- **Movimientos de inventario:** bitácora de entradas (compra), salidas (surtido), pases entre ubicaciones y ajustes por daño/conteo.
- **Proveedores** y qué nos venden (costo, si es el preferido).
- **Gente / equipos / vehículos** del piso (montacargas, camión, personal), con turno o placas en “notitas”, más **quién está asignado a qué** y **mantenimientos** programados.

Contexto de negocio:
- Lo de **clientes y pedidos** ya venía de ventas. Datos **sucios**: fechas en mil formatos, precios raros, tiers tipo GOLD/1/silver, emails incompletos. No pidan magia de limpieza ahora; que la app no se rompa y, si hay duda de montos, **confíen más en las líneas del pedido** que en el total del encabezado.
- Lo de **bodegas / stock / movimientos** es lo nuevo y donde más duele. Si se descuadra, perdemos dinero y tiempo de surtido.
- Proveedores y recursos: útiles, pero **prioridad 2** si el tiempo no alcanza.
- Caducidad en alimentos nos preocupa un poco; no sé si va en el tablero o luego.

Lo que sí queremos en la pantallita web (día a día, nada enterprise):

1. Pantalla de entrada con correo/contraseña (**mock**: con que se vea y pase al tablero está bien; sin login de verdad).
2. **Home / tablero:** stock, qué se está acabando (reabasto), movimientos recientes, pedidos abiertos… ¿eso? No tengo KPI cerrados.
3. **Pedidos** con estatus (capturado, pagado, en ruta, etc.) y detalle de líneas.
4. **Clientes** buscables + ficha (y sus pedidos si se puede).
5. **Items / productos** y dónde están guardados (bodega/almacén/ubicación).
6. Algo tipo **mapa** de bodegas por ciudad (CDMX, GDL…). No sé si pins geográficos o solo lista visual.
7. Que entradas/salidas/transferencias/ajustes **no dejen stock negativo** ni dupliquen operaciones.
8. Que **nadie de piso toque la base** directo: todo por la app.
9. Que se entienda rápido. Celular nice-to-have, no prioridad.

Dudas abiertas: ¿mostramos caducidad ya? ¿proveedores/recursos en v1 o después? Por ahora: **mínimo usable** para dejar de operar a ciegas. Gracias.

























