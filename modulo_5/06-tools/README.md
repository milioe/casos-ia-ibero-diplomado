# 06 - Tools + base de datos

Importa `schema.sql` en PostgreSQL o Supabase. Tools con SQL encapsulado; el modelo no escribe queries libres.

**Preguntas y respuestas esperadas:**

- **¿Cuánto vendimos en marzo de 2024 sin pedidos cancelados?**  
  **$245.00 MXN** — solo el pedido `13` (patricia solis) tiene línea `OK` en marzo; excluir `sts='9'`; no usar `mnt_decl` (dice 2348 en ese pedido).

- **¿Qué pedidos tiene María González y en qué estado están?**  
  Pedido `1` → entregado (`2024-01-15`). Pedido `4` → entregado (`2024-02-01`). Traducir `sts` con `ref_cod` (`dominio='ped_sts'`).

- **¿Qué productos inactivos aparecen en ventas?**  
  `SKU-H001` (pedido `5`, sartén) y `SKU-T001` (pedido `7`, playera). `activo_fl` no es `S`/`1`/`si`.

- **¿En qué pedidos el total declarado no cuadra con las líneas?**  
  Pedidos `4`, `13`, `14` y `15`. Ejemplo: pedido `4` declara $2500 pero las líneas suman $2439.95; `14` y `15` no tienen líneas.

- **¿Cuánto vendimos por categoría en CDMX?** (líneas `OK`, no cancelados)  
  Electrónica **$6736.95** | Alimentos **$401.00** | Textil **$299.00** | Hogar **$0**. Unificar `ELEC`/`ELECT`; precios desde `lin_ped`, no `precio_raw`.

- **¿Hay pedidos cancelados con líneas aún activas?**  
  Sí: pedido `3` (`sts='9'`) tiene una línea con `lin_sts='OK'` (café, $379.00 en líneas).

- **¿Qué clientes tier oro no tienen ningún pedido?**  
  **Ninguno** — todos con `tier_raw` en `GOLD` o `1` tienen al menos un pedido (mapear con `ref_cod`, `dominio='tier'`).

Si la tool usa otra regla de centavos vs pesos, debe decirlo en la respuesta.
