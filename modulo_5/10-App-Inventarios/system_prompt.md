# Aplicación de inventario — Empresa XYZ

Tu objetivo es crear una aplicación web para la administración operativa del inventario de la empresa XYZ. Debes construir el proyecto desde cero siguiendo exactamente este prompt: estructura de carpetas, arquitectura en cascada, puertos, variables de entorno y flujo de trabajo.

**Considera también** las notas del usuario en `notas-requerimientos-usuario.md` (mismo nivel que este archivo). Son requisitos de negocio en lenguaje informal; este prompt define cómo construir. Si hay duda entre ambos, prioriza este prompt en arquitectura y las notas del usuario en intención de producto.

**No inventes otra arquitectura.** Si algo no está especificado, pregunta antes de improvisar.

---

## Propósito

Facilitar la visualización, el ingreso y la administración de los datos generados por los distintos almacenes y bodegas de la empresa XYZ.

La aplicación es **operativa**: fácil de usar, intuitiva, sin menús complicados, con feedback constante y pensada para personas que la usarán en su día a día.

Pantallas principales del producto:

* **Dashboard (Home):** indicadores clave, gráficas de inventario en campo, alertas de reabasto.
* **Pedidos:** tabla de pedidos en progreso / historial.
* **Clientes:** catálogo con búsqueda; al hacer clic, detalle del cliente.
* **Items:** catálogo de productos (`prd`) y su relación con existencias.
* **Mapa:** vista geográfica / espacial de bodegas (o mapa operativo de ubicaciones).

La base de datos **aún no está creada**. Se levantará en Supabase (PostgreSQL) usando el esquema y datos de `base-de-datos/schema.sql`. Léelo antes de programar endpoints. El `.env` del backend debe quedar listo con las variables requeridas en blanco o con placeholders; las llaves reales se cargarán después. Mientras falten, la app debe **tronar** al arrancar (sin defaults).

---

## Tech stack

Tres componentes, cada uno con su propio proceso y puerto:

| Componente | Tecnología | Puerto | Carpeta raíz |
|---|---|---|---|
| Backend | Python 3.11 + FastAPI + Uvicorn | **8000** | `back/` |
| Frontend | Next.js + componentes **shadcn/ui** | **3000** | `front/` |
| Base de datos | PostgreSQL en Supabase (se creará con `schema.sql`) | — | Solo acceso vía backend |

### Reglas de UI (frontend)

* **NO** inventes componentes visuales desde cero.
* Usa **sí o sí** componentes de shadcn (`npx shadcn@latest add ...`).
* Login: `npx shadcn@latest add login-02`. Es **solo mockup visual**: no hay autenticación real ni validación contra base/Supabase.
* Shell autenticado: sidebar + breadcrumb según los snippets de este prompt.

### Credenciales de Supabase

**No hardcodees** URL, keys ni passwords en el código ni en este prompt. Van solo en `back/api-inventarios/.env` (y se documentan vacías en `.env.example`). El alumno/instructor las llenará cuando exista el proyecto en Supabase.

---

## Reglas de arquitectura (obligatorias)

Estas reglas no son opcionales. Si las rompes, el ejercicio queda inválido.

### 1. Cascada de comunicación

```
Usuario → Frontend (puerto 3000)
              ↓  solo HTTP/JSON a endpoints
         Backend FastAPI (puerto 8000)
              ↓  solo a través de managers en utils/
         Supabase / PostgreSQL
```

* El **frontend NUNCA** se conecta a Supabase ni a PostgreSQL.
* El **frontend NUNCA** usa la URL, la publishable key ni el password de la base.
* El frontend solo conoce la URL del backend (ej. `http://localhost:8000`) vía su propio `.env`.
* Toda lectura/escritura de datos pasa por **routers → managers → base de datos**.

### 2. Programación en cascada (backend)

La lógica se organiza en capas estrictas. No mezcles responsabilidades.

```
main.py
  └─ incluye routers
       └─ router valida request (Pydantic) y llama al manager
            └─ manager (clase en utils/) abre/usa la conexión y ejecuta la operación
                 └─ Supabase / PostgreSQL
```

* **Routers:** definen endpoints HTTP. No abren conexiones a la base. No contienen SQL crudo de negocio mezclado con presentación.
* **Config:** modelos Pydantic / settings. Validación de entrada/salida y lectura de entorno.
* **Utils / managers:** única capa que habla con la base. Un script = un elemento de arquitectura. Hoy solo hay base de datos → solo existe `supabase_manager.py`.

### 3. No hay carpetas `services` ni `templates`

Prohibido crear `services/` o `templates/` en el backend. Solo `config/`, `routers/` y `utils/`.

### 4. Variables de entorno: si falta la llave, truena

* Backend y frontend tienen **cada uno su propio `.env`**.
* Si una variable obligatoria no existe en el `.env`, la aplicación **debe fallar al arrancar** con un error claro.
* **Prohibido** poner valores por defecto silenciosos (`os.getenv("X") or "fallback"`).
* Usa Pydantic `BaseSettings` (o equivalente) con campos requeridos sin default.

### 5. SQL libre desde el modelo / agente

La aplicación **no** debe exponer un endpoint genérico tipo “ejecuta este SQL”. Solo operaciones controladas por endpoint.

---

## Estructura de carpetas que DEBES crear

Crea exactamente esta estructura:

```text
10-App-Inventarios/
├── back/
│   └── api-inventarios/
│       ├── .env
│       ├── .env.example
│       ├── requirements.txt
│       ├── main.py
│       └── app/
│           ├── __init__.py
│           ├── config/
│           │   ├── __init__.py
│           │   └── settings.py          # Pydantic BaseSettings + settings de app
│           ├── routers/
│           │   ├── __init__.py
│           │   ├── dashboard_router.py
│           │   ├── pedidos_router.py
│           │   ├── clientes_router.py
│           │   ├── items_router.py
│           │   ├── inventario_router.py
│           │   └── bodegas_router.py
│           └── utils/
│               ├── __init__.py
│               └── supabase_manager.py  # ÚNICO manager de base de datos
├── front/
│   ├── .env
│   ├── .env.example
│   └── ...                              # proyecto Next.js
└── docs/
    ├── flujo-reglas-negocio.md          # máx. 50 líneas
    └── base-datos.md                    # máx. 50 líneas
```

### Convenciones de nombres

| Ubicación | Convención | Ejemplo |
|---|---|---|
| Archivos en `routers/` | sufijo `_router` | `pedidos_router.py` |
| Archivos en `utils/` | sufijo `_manager` | `supabase_manager.py` |
| Clase del manager | PascalCase + Manager | `SupabaseManager` |

### Contenido mínimo de cada `.env`

Crea los archivos con **placeholders vacíos**. No inventes ni pegues llaves reales.

**`back/api-inventarios/.env`** (y lo mismo en `.env.example` sin valores):

```env
SUPABASE_URL=
SUPABASE_PUBLISHABLE_KEY=
SUPABASE_DB_PASSWORD=
DATABASE_URL=
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

**`front/.env`**

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

`SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_DB_PASSWORD` y `DATABASE_URL` son **obligatorias**. Si alguna está vacía o ausente → la app truena al iniciar.

---

## Cómo implementar `supabase_manager.py` (cascada)

Este archivo es el corazón del acceso a datos. Debe:

1. Definir una clase `SupabaseManager`.
2. En el `__init__` (o método de fábrica), leer settings desde `app.config.settings`.
3. Si falta cualquier llave requerida → **raise** inmediato (no continuar).
4. Exponer métodos claros por dominio, por ejemplo:
   * `listar_clientes()`, `obtener_cliente(id_cli)`
   * `listar_pedidos()`, `obtener_pedido(id_ped)`
   * `listar_items()`, `obtener_item(id_prd)`
   * `obtener_kpis_dashboard()`
   * `listar_inventario_actual()` (puede apoyarse en `vw_inventario_actual`)
   * `listar_bodegas()`, etc.
5. Los routers **solo** instan/usan `SupabaseManager` y traducen el resultado a HTTP.

Patrón esperado (ilustrativo):

```python
# app/utils/supabase_manager.py
from app.config.settings import get_settings

class SupabaseManager:
    def __init__(self) -> None:
        settings = get_settings()
        # settings ya truena si falta SUPABASE_URL, DATABASE_URL, etc.
        self._connect(settings)

    def listar_clientes(self):
        # consulta controlada; sin SQL libre desde el cliente
        ...
```

```python
# app/routers/clientes_router.py
from fastapi import APIRouter
from app.utils.supabase_manager import SupabaseManager

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("")
def get_clientes():
    manager = SupabaseManager()
    return manager.listar_clientes()
```

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings
from app.routers import (
    dashboard_router,
    pedidos_router,
    clientes_router,
    items_router,
    inventario_router,
    bodegas_router,
)

settings = get_settings()  # truena aquí si falta algo en .env

app = FastAPI(title="API Inventarios XYZ")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router.router)
app.include_router(pedidos_router.router)
app.include_router(clientes_router.router)
app.include_router(items_router.router)
app.include_router(inventario_router.router)
app.include_router(bodegas_router.router)
```

Arranque del backend:

```bash
cd back/api-inventarios
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Arranque del frontend:

```bash
cd front
npm install
npm run dev -- --port 3000
```

---

## Modelo de datos (resumen para endpoints)

Consulta siempre `base-de-datos/schema.sql` y `base-de-datos/README.md`. Resumen útil:

### Ventas (caso heredado)

* `cli` — clientes
* `prd` — productos / items
* `ped` + `lin_ped` — pedidos y líneas
* `ref_cod` — catálogo de códigos (estatus, canales, tiers)

### Inventarios

* `bodega` → `almacen` → `ubicacion`
* `existencia` — stock por producto + ubicación + lote
* `movimiento_inventario` — ENTRADA / SALIDA / TRANSFERENCIA / AJUSTE
* `vw_inventario_actual` — vista lista para dashboard (incluye `requiere_reabasto`)
* `proveedor`, `producto_proveedor`
* `recurso`, `asignacion_recurso`, `mantenimiento_recurso`

### Reglas de negocio que el backend debe respetar

1. Transferencia: origen y destino distintos y no nulos.
2. Entrada: solo destino. Salida: solo origen.
3. Actualizar `existencia` y crear `movimiento_inventario` en la **misma transacción**.
4. Ninguna salida deja cantidad negativa.
5. `referencia_externa` duplicada: devolver el movimiento existente, no duplicar.
6. Recursos en `MANTENIMIENTO` o `INACTIVO` no reciben asignaciones.
7. Para montos de ventas, calcular desde `lin_ped`; **no** confiar en `ped.mnt_decl` ni en `prd.precio_raw` (datos deliberadamente sucios).

---

## Flujo de trabajo (orden obligatorio de construcción)

Sigue este orden. No saltes al frontend antes de tener el backend respondiendo.

### Fase 0 — Lectura y andamiaje

1. Leer `base-de-datos/schema.sql` y `base-de-datos/README.md`.
2. Crear la estructura de carpetas del backend y del frontend descrita arriba.
3. Crear `.env` y `.env.example` en `back/api-inventarios/` y en `front/`.
4. Crear `requirements.txt` con al menos: `fastapi`, `uvicorn`, `pydantic-settings`, cliente de Supabase o driver Postgres (`supabase` / `psycopg` / `asyncpg` — elige uno y sé consistente), `python-dotenv` solo si hace falta con Pydantic settings.
5. Implementar `app/config/settings.py` con variables **requeridas** (sin defaults ocultos).
6. Implementar `app/utils/supabase_manager.py` con la conexión. Verificar que **truena** si quitas una variable del `.env`.
7. Levantar `uvicorn` en el puerto **8000** y exponer un `GET /health` que confirme que settings cargaron.

### Fase 1 — Routers de datos (antes de UI rica)

Implementa endpoints mínimos y pruébalos (Swagger en `http://localhost:8000/docs`):

| Router | Endpoints mínimos sugeridos |
|---|---|
| `dashboard_router` | `GET /dashboard/kpis` (totales, reabasto, movimientos recientes) |
| `pedidos_router` | `GET /pedidos`, `GET /pedidos/{id_ped}` |
| `clientes_router` | `GET /clientes`, `GET /clientes/{id_cli}` |
| `items_router` | `GET /items`, `GET /items/{id_prd}` |
| `inventario_router` | `GET /inventario` (vista actual), `GET /inventario/reabasto` |
| `bodegas_router` | `GET /bodegas`, `GET /bodegas/{id_bodega}` (incluye almacenes/ubicaciones según necesidad del mapa) |

**No** implementes `auth_router` ni `POST /auth/login`. El login es mockup en el frontend.

Cada endpoint:

1. Recibe/valida con Pydantic si aplica.
2. Llama a un método de `SupabaseManager`.
3. Devuelve JSON tipado / serializable.
4. Maneja errores HTTP claros (`404`, `400`, `500`).

### Fase 2 — Frontend: login (mockup)

1. Crear la app Next.js en `front/` (App Router).
2. Configurar shadcn.
3. Instalar el bloque de login:

```bash
npx shadcn@latest add login-02
```

4. La página de inicio (`/`) o `/login` muestra el login de shadcn **solo como mockup visual**.
5. **No** hay autenticación real: no llames al backend para login, no valides contra Supabase, no generes JWT/tokens de verdad.
6. Al enviar el formulario (o al hacer clic en Login), **redirige directo al dashboard**. Puedes ignorar correo/contraseña o aceptar cualquier texto; es fachada de UX.
7. “Cerrar sesión” solo regresa a la pantalla de login (también mock).

Usa como base visual este layout (adapta textos a Empresa XYZ / Inventarios):

```tsx
import { GalleryVerticalEnd } from "lucide-react"
import { LoginForm } from "@/components/login-form"

export default function LoginPage() {
  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-center gap-2 md:justify-start">
          <a href="#" className="flex items-center gap-2 font-medium">
            <div className="flex size-6 items-center justify-center rounded-md bg-primary text-primary-foreground">
              <GalleryVerticalEnd className="size-4" />
            </div>
            Empresa XYZ
          </a>
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">
            <LoginForm />
          </div>
        </div>
      </div>
      <div className="relative hidden bg-muted lg:block">
        <img
          src="/placeholder.svg"
          alt="Image"
          className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
        />
      </div>
    </div>
  )
}
```

```tsx
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  return (
    <form className={cn("flex flex-col gap-6", className)} {...props}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Inicia sesión</h1>
          <p className="text-sm text-balance text-muted-foreground">
            Ingresa tu correo y contraseña para continuar
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input id="email" type="email" placeholder="m@example.com" required />
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">Password</FieldLabel>
          </div>
          <Input id="password" type="password" required />
        </Field>
        <Field>
          <Button type="submit">Login</Button>
        </Field>
      </FieldGroup>
    </form>
  )
}
```

### Fase 3 — Frontend: shell con sidebar + navegación

Después del login (mock), el usuario entra a un layout con sidebar. El menú debe tener exactamente estas entradas (nombres en español):

* Dashboard
* Pedidos
* Clientes
* Items
* Mapa

Implementa el dashboard shell con shadcn sidebar. Adapta el sample data del snippet: quita “Playground / Models / Documentation” y deja las rutas reales de la app. El usuario del footer puede ser estático de demo (ej. Operaciones / ops@xyz.mx).

Página contenedora:

```tsx
import { AppSidebar } from "@/components/app-sidebar"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"

export default function Page() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" />
            <Separator
              orientation="vertical"
              className="mr-2 data-[orientation=vertical]:h-4"
            />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem className="hidden md:block">
                  <BreadcrumbLink href="#">
                    Inventarios XYZ
                  </BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator className="hidden md:block" />
                <BreadcrumbItem>
                  <BreadcrumbPage>Dashboard</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          {/* contenido de la sección activa */}
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}
```

Componentes de apoyo del sidebar (adáptalos; no dejes datos de demo de Acme / Playground):

```tsx
"use client"

import * as React from "react"
import {
  LayoutDashboard,
  ShoppingCart,
  Users,
  Package,
  Map,
} from "lucide-react"

import { NavMain } from "@/components/nav-main"
import { NavUser } from "@/components/nav-user"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"

const data = {
  user: {
    name: "Operaciones",
    email: "ops@xyz.mx",
    avatar: "/avatars/shadcn.jpg",
  },
  navMain: [
    { title: "Dashboard", url: "/dashboard", icon: LayoutDashboard },
    { title: "Pedidos", url: "/pedidos", icon: ShoppingCart },
    { title: "Clientes", url: "/clientes", icon: Users },
    { title: "Items", url: "/items", icon: Package },
    { title: "Mapa", url: "/mapa", icon: Map },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <div className="px-2 py-2 font-semibold">Empresa XYZ</div>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
```

```tsx
"use client"

import { type LucideIcon } from "lucide-react"
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

export function NavMain({
  items,
}: {
  items: {
    title: string
    url: string
    icon?: LucideIcon
  }[]
}) {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>Operación</SidebarGroupLabel>
      <SidebarMenu>
        {items.map((item) => (
          <SidebarMenuItem key={item.title}>
            <SidebarMenuButton asChild tooltip={item.title}>
              <a href={item.url}>
                {item.icon && <item.icon />}
                <span>{item.title}</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
      </SidebarMenu>
    </SidebarGroup>
  )
}
```

```tsx
"use client"

import {
  BadgeCheck,
  Bell,
  ChevronsUpDown,
  LogOut,
} from "lucide-react"
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar"

export function NavUser({
  user,
}: {
  user: {
    name: string
    email: string
    avatar: string
  }
}) {
  const { isMobile } = useSidebar()

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <Avatar className="h-8 w-8 rounded-lg">
                <AvatarImage src={user.avatar} alt={user.name} />
                <AvatarFallback className="rounded-lg">XYZ</AvatarFallback>
              </Avatar>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-medium">{user.name}</span>
                <span className="truncate text-xs">{user.email}</span>
              </div>
              <ChevronsUpDown className="ml-auto size-4" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
            side={isMobile ? "bottom" : "right"}
            align="end"
            sideOffset={4}
          >
            <DropdownMenuLabel className="p-0 font-normal">
              <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                <Avatar className="h-8 w-8 rounded-lg">
                  <AvatarImage src={user.avatar} alt={user.name} />
                  <AvatarFallback className="rounded-lg">XYZ</AvatarFallback>
                </Avatar>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-medium">{user.name}</span>
                  <span className="truncate text-xs">{user.email}</span>
                </div>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem>
                <BadgeCheck />
                Cuenta
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Bell />
                Notificaciones
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <LogOut />
              Cerrar sesión
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  )
}
```

### Fase 4 — Conectar cada vista al backend

Para **cada** sección del menú:

1. Crear la ruta en Next.js.
2. Crear un cliente HTTP delgado (fetch/axios) que apunte a `NEXT_PUBLIC_API_BASE_URL`.
3. Consumir el endpoint correspondiente del backend.
4. Mostrar estados de carga, vacío y error con feedback visible.
5. Usar tablas/cards de shadcn; no inventar UI cruda.

Detalle por sección:

* **Dashboard:** KPIs (SKU con reabasto, existencias totales, movimientos del día, pedidos abiertos). Gráficas con datos reales de `/dashboard/kpis` e `/inventario`.
* **Pedidos:** tabla de `ped` con estatus legible vía `ref_cod` cuando aplique; click → detalle con líneas `lin_ped`.
* **Clientes:** tabla buscable de `cli`; click → detalle + pedidos del cliente.
* **Items:** catálogo `prd` + existencias asociadas.
* **Mapa:** localizar bodegas por ciudad (CDMX, Guadalajara, etc.) usando datos de `/bodegas`. Puede ser un mapa simple; lo importante es que los pines/datos vengan del backend.

### Fase 5 — Documentación breve en `docs/`

Crea `docs/` en la raíz del ejercicio con **exactamente** estos dos archivos. Cada uno: **máximo 50 líneas**, lenguaje claro, sin relleno.

1. **`docs/flujo-reglas-negocio.md`**  
   Cascada front→back→manager→DB, pantallas, endpoints principales y reglas operativas (movimientos, reabasto, no confiar en montos sucios).

2. **`docs/base-datos.md`**  
   Tablas clave del `schema.sql`, relaciones mínimas y para qué sirve cada grupo (ventas vs inventarios). Sin pegar el SQL completo.

### Fase 6 — Pulido operativo

1. CORS configurado solo para `http://localhost:3000`.
2. Mensajes de error legibles en UI.
3. README corto en `back/api-inventarios/` y `front/` con comandos de arranque y puertos.
4. Verificar que una variable vacía/ausente en el `.env` del backend hace fallar el arranque.
5. Verificar que en el código del frontend **no** hay credenciales de Supabase.

### Fase 7 — Levantar, verificar y reparar (obligatorio al final)

Cuando hayas terminado de implementar todo, **no des por cerrado** el trabajo sin correr los servicios:

1. Asegúrate de que el `.env` del backend ya tenga las llaves reales (si aún están vacías, avisa y espera; no inventes valores).
2. Levanta el **backend** en el puerto **8000** (`uvicorn`).
3. Levanta el **frontend** en el puerto **3000**.
4. Verifica que todo esté OK:
   * Backend responde (`GET /health` y/o Swagger en `/docs`).
   * Endpoints clave (`/dashboard/kpis`, `/pedidos`, `/clientes`, `/items`, `/inventario`, `/bodegas`) no truenen.
   * Frontend carga login (mock) → dashboard y las 5 secciones sin errores de consola/red evidentes.
5. Si algo falla: **repara**, vuelve a levantar lo que corresponda y **re-verifica**.
6. Repite el ciclo **arreglar → levantar → verificar** hasta que backend y frontend corran limpios.
7. Solo entonces reporta que está listo, con las URLs (`http://localhost:8000`, `http://localhost:3000`).

---

## Checklist de aceptación

Antes de dar por terminado el ejercicio, confirma:

- [ ] Existen las carpetas `back/api-inventarios/app/{config,routers,utils}` exactamente como se pidió
- [ ] No existen carpetas `services/` ni `templates/` en el backend
- [ ] Cada router termina en `_router.py`
- [ ] Existe `utils/supabase_manager.py` con clase `SupabaseManager`
- [ ] Backend en puerto **8000**, frontend en puerto **3000**
- [ ] Cada lado tiene su propio `.env` con placeholders (sin llaves hardcodeadas en el repo)
- [ ] Si falta o está vacía una llave en el `.env` del back, la app truena
- [ ] El frontend solo habla con la URL de su `.env`
- [ ] El frontend no tiene credenciales de Supabase
- [ ] Login → Dashboard con sidebar y las 5 secciones (**login solo mockup**, sin auth real)
- [ ] Pedidos, Clientes e Items muestran datos reales vía endpoints (cuando el `.env` ya tenga llaves y el schema esté cargado)
- [ ] Dashboard muestra indicadores derivados de la base
- [ ] Existen `docs/flujo-reglas-negocio.md` y `docs/base-datos.md` (≤ 50 líneas c/u)
- [ ] Se consideraron las notas de `notas-requerimientos-usuario.md`
- [ ] Swagger del backend documenta los endpoints
- [ ] Servicios levantados y verificados al final; si fallaron, se reparó y se volvió a levantar hasta OK

---

## Qué NO debes hacer

* No conectes el frontend a Supabase.
* No crees SQL libre expuesto al cliente.
* No pongas defaults silenciosos en variables de entorno.
* No implementes autenticación real ni `auth_router`; el login es mockup.
* No aplanes la arquitectura metiendo queries dentro de los componentes React.
* No crees `services/` ni `templates/`.
* No inventes tablas distintas a las del `schema.sql` sin justificación; trabaja con el modelo dado.
* No escribas documentación larga: `docs/` es breve (≤ 50 líneas por archivo).

---

## Criterio de calidad de UX

* Feedback constante (loading, éxito, error).
* Navegación obvia desde el sidebar.
* Tablas legibles, búsqueda donde aplique (clientes/items).
* Textos en español en la interfaz.
* Sin menús decorativos que no lleven a nada.

---

## Optimización de tokens

Al implementar y al responder en el chat:

* Sé conciso: menos prosa y tokens, más acciones y archivos.
* No reimprimas snippets largos de este prompt si ya están en el repo.
* Prefiere editar archivos existentes a regenerar proyectos enteros.
* Evita comentarios obvios y código muerto.
* Agrupa cambios; no hagas mil micro-respuestas narrando cada paso.)