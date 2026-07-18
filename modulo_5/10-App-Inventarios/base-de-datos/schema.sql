-- =============================================================================
-- 10-App-Inventarios | PostgreSQL 14+
-- Conserva el caso de ventas de 06-tools y agrega operación de inventarios,
-- bodegas, almacenes, ubicaciones y recursos.
-- Ejecutar: psql -f schema.sql
-- =============================================================================

BEGIN;

DROP VIEW IF EXISTS vw_inventario_actual CASCADE;
DROP TABLE IF EXISTS mantenimiento_recurso CASCADE;
DROP TABLE IF EXISTS asignacion_recurso CASCADE;
DROP TABLE IF EXISTS recurso CASCADE;
DROP TABLE IF EXISTS movimiento_inventario CASCADE;
DROP TABLE IF EXISTS existencia CASCADE;
DROP TABLE IF EXISTS producto_proveedor CASCADE;
DROP TABLE IF EXISTS proveedor CASCADE;
DROP TABLE IF EXISTS ubicacion CASCADE;
DROP TABLE IF EXISTS almacen CASCADE;
DROP TABLE IF EXISTS bodega CASCADE;
DROP TABLE IF EXISTS lin_ped CASCADE;
DROP TABLE IF EXISTS ped CASCADE;
DROP TABLE IF EXISTS prd CASCADE;
DROP TABLE IF EXISTS cli CASCADE;
DROP TABLE IF EXISTS ref_cod CASCADE;

-- -----------------------------------------------------------------------------
-- Caso original de ventas
-- -----------------------------------------------------------------------------

CREATE TABLE ref_cod (
    id_ref      SERIAL PRIMARY KEY,
    dominio     VARCHAR(20) NOT NULL,
    codigo      VARCHAR(20) NOT NULL,
    etiqueta    VARCHAR(80),
    factor_num  NUMERIC(12,4),
    vigente     CHAR(2) DEFAULT 'S',
    UNIQUE (dominio, codigo)
);

CREATE TABLE cli (
    id_cli      SERIAL PRIMARY KEY,
    nom         VARCHAR(120) NOT NULL,
    tel         VARCHAR(40),
    email       VARCHAR(120),
    ciudad      VARCHAR(60),
    tier_raw    VARCHAR(10),
    fch_alta    VARCHAR(20) NOT NULL
);

CREATE TABLE prd (
    id_prd      SERIAL PRIMARY KEY,
    sku         VARCHAR(30) UNIQUE NOT NULL,
    desc_corta  VARCHAR(200),
    cat_cd      VARCHAR(20),
    precio_raw  VARCHAR(20) NOT NULL,
    activo_fl   VARCHAR(5)
);

CREATE TABLE ped (
    id_ped      SERIAL PRIMARY KEY,
    id_cli      INTEGER REFERENCES cli(id_cli),
    fch         VARCHAR(20) NOT NULL,
    sts         VARCHAR(5) NOT NULL,
    canal_raw   VARCHAR(10),
    moneda_cd   VARCHAR(5) DEFAULT 'MXN',
    mnt_decl    NUMERIC(14,2),
    nota_int    TEXT
);

CREATE TABLE lin_ped (
    id_lin      SERIAL PRIMARY KEY,
    id_ped      INTEGER NOT NULL REFERENCES ped(id_ped) ON DELETE CASCADE,
    id_prd      INTEGER NOT NULL REFERENCES prd(id_prd),
    cant        NUMERIC(10,2) NOT NULL,
    precio_u    NUMERIC(14,2),
    dto_pct     NUMERIC(5,2) DEFAULT 0,
    lin_sts     VARCHAR(5) DEFAULT 'OK'
);

CREATE INDEX idx_ped_cli ON ped(id_cli);
CREATE INDEX idx_ped_fch ON ped(fch);
CREATE INDEX idx_lin_ped ON lin_ped(id_ped);
CREATE INDEX idx_prd_cat ON prd(cat_cd);

-- -----------------------------------------------------------------------------
-- Bodegas, almacenes y ubicaciones
-- -----------------------------------------------------------------------------

CREATE TABLE bodega (
    id_bodega       SERIAL PRIMARY KEY,
    clave           VARCHAR(20) UNIQUE NOT NULL,
    nombre          VARCHAR(100) NOT NULL,
    ciudad          VARCHAR(60) NOT NULL,
    direccion       VARCHAR(200),
    responsable     VARCHAR(120),
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE almacen (
    id_almacen      SERIAL PRIMARY KEY,
    id_bodega       INTEGER NOT NULL REFERENCES bodega(id_bodega),
    clave           VARCHAR(20) NOT NULL,
    nombre          VARCHAR(100) NOT NULL,
    tipo            VARCHAR(20) NOT NULL
                    CHECK (tipo IN ('GENERAL', 'REFRIGERADO', 'PELIGROSO', 'DEVOLUCIONES')),
    capacidad_m3    NUMERIC(12,2) NOT NULL CHECK (capacidad_m3 > 0),
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (id_bodega, clave)
);

CREATE TABLE ubicacion (
    id_ubicacion    SERIAL PRIMARY KEY,
    id_almacen      INTEGER NOT NULL REFERENCES almacen(id_almacen),
    codigo          VARCHAR(30) NOT NULL,
    pasillo         VARCHAR(10),
    estante         VARCHAR(10),
    nivel           VARCHAR(10),
    capacidad_kg    NUMERIC(12,2) CHECK (capacidad_kg > 0),
    bloqueada       BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (id_almacen, codigo)
);

-- -----------------------------------------------------------------------------
-- Proveedores y existencias
-- -----------------------------------------------------------------------------

CREATE TABLE proveedor (
    id_proveedor    SERIAL PRIMARY KEY,
    rfc             VARCHAR(20) UNIQUE,
    nombre          VARCHAR(120) NOT NULL,
    email           VARCHAR(120),
    telefono        VARCHAR(40),
    dias_entrega    INTEGER CHECK (dias_entrega >= 0),
    activo          BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE producto_proveedor (
    id_prd          INTEGER NOT NULL REFERENCES prd(id_prd),
    id_proveedor    INTEGER NOT NULL REFERENCES proveedor(id_proveedor),
    sku_proveedor   VARCHAR(40),
    costo           NUMERIC(14,2) NOT NULL CHECK (costo >= 0),
    preferido       BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id_prd, id_proveedor)
);

CREATE TABLE existencia (
    id_existencia       BIGSERIAL PRIMARY KEY,
    id_prd              INTEGER NOT NULL REFERENCES prd(id_prd),
    id_ubicacion        INTEGER NOT NULL REFERENCES ubicacion(id_ubicacion),
    lote                VARCHAR(40) NOT NULL DEFAULT '',
    fecha_caducidad     DATE,
    cantidad            NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    reservado           NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (reservado >= 0),
    punto_reorden       NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (punto_reorden >= 0),
    costo_promedio      NUMERIC(14,2) CHECK (costo_promedio >= 0),
    actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (reservado <= cantidad),
    UNIQUE (id_prd, id_ubicacion, lote)
);

-- -----------------------------------------------------------------------------
-- Movimientos: una fila representa una operación de negocio auditable
-- -----------------------------------------------------------------------------

CREATE TABLE movimiento_inventario (
    id_movimiento       BIGSERIAL PRIMARY KEY,
    tipo                VARCHAR(20) NOT NULL
                        CHECK (tipo IN ('ENTRADA', 'SALIDA', 'TRANSFERENCIA', 'AJUSTE')),
    id_prd              INTEGER NOT NULL REFERENCES prd(id_prd),
    id_ubicacion_origen INTEGER REFERENCES ubicacion(id_ubicacion),
    id_ubicacion_destino INTEGER REFERENCES ubicacion(id_ubicacion),
    cantidad            NUMERIC(14,2) NOT NULL CHECK (cantidad > 0),
    estado              VARCHAR(20) NOT NULL DEFAULT 'COMPLETADO'
                        CHECK (estado IN ('PENDIENTE', 'COMPLETADO', 'CANCELADO')),
    referencia_externa  VARCHAR(80) UNIQUE,
    motivo              VARCHAR(200),
    usuario_registro    VARCHAR(120) NOT NULL,
    creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (
        (tipo = 'ENTRADA' AND id_ubicacion_origen IS NULL AND id_ubicacion_destino IS NOT NULL)
        OR (tipo = 'SALIDA' AND id_ubicacion_origen IS NOT NULL AND id_ubicacion_destino IS NULL)
        OR (tipo = 'TRANSFERENCIA' AND id_ubicacion_origen IS NOT NULL
            AND id_ubicacion_destino IS NOT NULL
            AND id_ubicacion_origen <> id_ubicacion_destino)
        OR (tipo = 'AJUSTE' AND
            ((id_ubicacion_origen IS NOT NULL) <> (id_ubicacion_destino IS NOT NULL)))
    )
);

CREATE INDEX idx_existencia_prd ON existencia(id_prd);
CREATE INDEX idx_existencia_ubicacion ON existencia(id_ubicacion);
CREATE INDEX idx_movimiento_prd_fecha ON movimiento_inventario(id_prd, creado_en DESC);

-- -----------------------------------------------------------------------------
-- Recursos operativos: personas, equipos y vehículos
-- -----------------------------------------------------------------------------

CREATE TABLE recurso (
    id_recurso      SERIAL PRIMARY KEY,
    id_bodega       INTEGER NOT NULL REFERENCES bodega(id_bodega),
    clave           VARCHAR(30) UNIQUE NOT NULL,
    tipo            VARCHAR(20) NOT NULL
                    CHECK (tipo IN ('PERSONA', 'EQUIPO', 'VEHICULO')),
    nombre          VARCHAR(120) NOT NULL,
    estado          VARCHAR(20) NOT NULL DEFAULT 'DISPONIBLE'
                    CHECK (estado IN ('DISPONIBLE', 'ASIGNADO', 'MANTENIMIENTO', 'INACTIVO')),
    capacidad       NUMERIC(12,2) CHECK (capacidad > 0),
    unidad_capacidad VARCHAR(20),
    habilidades     TEXT[],
    metadata        JSONB NOT NULL DEFAULT '{}'::JSONB,
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (
        (capacidad IS NULL AND unidad_capacidad IS NULL)
        OR (capacidad IS NOT NULL AND unidad_capacidad IS NOT NULL)
    )
);

CREATE TABLE asignacion_recurso (
    id_asignacion   BIGSERIAL PRIMARY KEY,
    id_recurso      INTEGER NOT NULL REFERENCES recurso(id_recurso),
    id_almacen      INTEGER NOT NULL REFERENCES almacen(id_almacen),
    actividad       VARCHAR(120) NOT NULL,
    responsable     VARCHAR(120),
    inicio          TIMESTAMPTZ NOT NULL,
    fin             TIMESTAMPTZ,
    estado          VARCHAR(20) NOT NULL DEFAULT 'PROGRAMADA'
                    CHECK (estado IN ('PROGRAMADA', 'EN_CURSO', 'TERMINADA', 'CANCELADA')),
    CHECK (fin IS NULL OR fin > inicio)
);

CREATE TABLE mantenimiento_recurso (
    id_mantenimiento BIGSERIAL PRIMARY KEY,
    id_recurso       INTEGER NOT NULL REFERENCES recurso(id_recurso),
    tipo              VARCHAR(30) NOT NULL,
    descripcion       TEXT NOT NULL,
    fecha_programada  DATE NOT NULL,
    fecha_realizada   DATE,
    costo             NUMERIC(14,2) CHECK (costo >= 0),
    estado            VARCHAR(20) NOT NULL DEFAULT 'PROGRAMADO'
                      CHECK (estado IN ('PROGRAMADO', 'EN_PROCESO', 'REALIZADO', 'CANCELADO'))
);

CREATE INDEX idx_recurso_bodega_estado ON recurso(id_bodega, estado);
CREATE INDEX idx_asignacion_periodo ON asignacion_recurso(inicio, fin);
CREATE INDEX idx_mantenimiento_fecha ON mantenimiento_recurso(fecha_programada);

CREATE VIEW vw_inventario_actual AS
SELECT
    b.clave AS bodega,
    a.clave AS almacen,
    u.codigo AS ubicacion,
    p.sku,
    p.desc_corta AS producto,
    e.lote,
    e.fecha_caducidad,
    e.cantidad,
    e.reservado,
    e.cantidad - e.reservado AS disponible,
    e.punto_reorden,
    (e.cantidad - e.reservado) <= e.punto_reorden AS requiere_reabasto
FROM existencia e
JOIN prd p ON p.id_prd = e.id_prd
JOIN ubicacion u ON u.id_ubicacion = e.id_ubicacion
JOIN almacen a ON a.id_almacen = u.id_almacen
JOIN bodega b ON b.id_bodega = a.id_bodega;

-- -----------------------------------------------------------------------------
-- Datos iniciales del caso original
-- -----------------------------------------------------------------------------

INSERT INTO ref_cod (dominio, codigo, etiqueta, factor_num, vigente) VALUES
('ped_sts', '1', 'capturado', 1, 'S'),
('ped_sts', '2', 'pagado', 1, 'S'),
('ped_sts', '3', 'en_ruta', 1, 'S'),
('ped_sts', '4', 'entregado', 1, 'S'),
('ped_sts', '9', 'cancelado', 0, 'S'),
('cat_prd', 'ELEC', 'electronica', NULL, 'S'),
('cat_prd', 'ELECT', 'electronica_legacy', NULL, '1'),
('cat_prd', 'ALIM', 'alimentos', NULL, 'S'),
('cat_prd', 'HOGAR', 'hogar', NULL, 'S'),
('cat_prd', 'TEXT', 'textil', NULL, 'N'),
('canal', 'W', 'web', NULL, 'S'),
('canal', 'T', 'tienda', NULL, 'S'),
('canal', 'web', 'web_alias', NULL, 'S'),
('tier', '1', 'oro', NULL, 'S'),
('tier', 'GOLD', 'oro_alias', NULL, 'si');

INSERT INTO cli (nom, tel, email, ciudad, tier_raw, fch_alta) VALUES
('María González', '55-1234-5678', 'maria.g@mail.com', 'CDMX', 'GOLD', '2023-01-10'),
('CARLOS ruiz', '5512345678', NULL, 'GDL', '1', '15/02/2023'),
('Ana  Torres', '(81)555-0199', 'ana.t@corp.mx', 'MTY', '2', '20230301'),
('pedro lopez', '55.8765.4321', 'pedro@', 'CDMX', 'silver', '2023-04-12'),
('Lucía Méndez', NULL, 'lucia.m@gmail.com', 'PUE', 'GOLD', '2023-05-20'),
('JORGE HERRERA', '044-331-998-8776', 'jorge.h@x.com', 'GDL', '1', '2023-06-01'),
('nora castillo', '5550001111', 'nora.c@mail.com', 'QRO', '3', '2023-07-15'),
('Ricardo Vega', '55-0000-2222', 'r.vega@empresa.mx', 'CDMX', '2', '20230820'),
('Sofía Delgado', '5588776655', NULL, 'CDMX', 'GOLD', '2023-09-05'),
('miguel angel rios', '55 9988 7766', 'mrios@old.net', 'TIJ', 'bronze', '2023-10-11'),
('Elena Vargas', '5511223344', 'elena.v@mail.com', 'CDMX', '1', '2023-11-22'),
('Héctor Núñez', NULL, 'hector.n@corp.mx', 'LEO', '2', '20231201'),
('patricia solis', '55-4433-2211', 'p.solis@mail.com', 'CDMX', 'GOLD', '2024-01-08'),
('Daniel Kim', '+52 55 1234 0000', 'daniel.k@startup.io', 'CDMX', '1', '2024-02-14'),
('Valentina Ortiz', '5500112233', 'vale@mail.com', 'MER', '2', '15/03/2024');

INSERT INTO prd (sku, desc_corta, cat_cd, precio_raw, activo_fl) VALUES
('SKU-E001', 'Audífonos BT Pro', 'ELEC', '1299.00', 'S'),
('SKU-E002', 'Cargador 65W USB-C', 'ELECT', '89900', '1'),
('SKU-A001', 'Café molido 500g', 'ALIM', '189.50', 'si'),
('SKU-A002', 'Aceite oliva 1L', 'ALIM', '24500', 'S'),
('SKU-H001', 'Sartén antiadherente', 'HOGAR', '459.99', 'N'),
('SKU-H002', 'Juego toallas 3pz', 'hogar', '320.00', 'S'),
('SKU-T001', 'Playera algodón M', 'TEXT', '299.00', '0'),
('SKU-E003', 'Mouse inalámbrico', 'ELEC', '45000', 'S'),
('SKU-A003', 'Galletas surtidas', 'ALIM', '45.90', 'S'),
('SKU-H003', 'Lámpara LED escritorio', 'HOGAR', '799.00', 'S'),
('SKU-E004', 'Teclado mecánico', 'ELEC', '1899.00', 'S'),
('SKU-A004', 'Agua mineral 12pk', 'ALIM', '15600', '1'),
('SKU-T002', 'Sudadera unisex L', 'TEXT', '649.00', 'no'),
('SKU-E005', 'Webcam HD', 'ELEC', '109900', 'S'),
('SKU-H004', 'Organizador baño', 'HOGAR', '199.00', 'S');

INSERT INTO ped (id_cli, fch, sts, canal_raw, moneda_cd, mnt_decl, nota_int) VALUES
(1, '2024-01-15', '4', 'W', 'MXN', 1299.00, 'ok'),
(2, '15/01/2024', '4', 'T', 'MXN', 899.00, 'precio mal capturado en header'),
(3, '20240120', '9', 'web', 'MXN', 378.90, 'cancelado pero revisar líneas'),
(1, '2024-02-01', '4', 'W', 'MXN', 2500.00, 'cliente recurrente'),
(5, '01/02/2024', '2', 'W', 'MXN', 459.99, NULL),
(6, '20240210', '3', 'T', 'MXN', 770.00, 'en ruta GDL'),
(4, '2024-02-14', '4', 'W', 'MXN', 299.00, 'email pedro@ inválido'),
(8, '14/02/2024', '1', 'W', 'MXN', 1899.00, 'capturado sin pago'),
(9, '20240218', '4', 'T', 'MXN', 156.00, 'monto header en pesos, línea en centavos?'),
(10, '2024-02-22', '9', 'W', 'MXN', 649.00, 'devolución parcial en nota'),
(11, '22/02/2024', '4', 'W', 'MXN', 1099.00, NULL),
(12, '20240228', '4', 'T', 'MXN', 199.00, NULL),
(13, '2024-03-05', '3', 'W', 'MXN', 2348.00, '2 líneas mismo pedido'),
(13, '05/03/2024', '4', 'web', 'MXN', 245.00, 'segundo pedido mismo día'),
(14, '20240310', '2', 'W', 'MXN', 1099.00, 'pago pendiente confirmación');

INSERT INTO lin_ped (id_ped, id_prd, cant, precio_u, dto_pct, lin_sts) VALUES
(1, 1, 1, 1299.00, 0, 'OK'),
(2, 2, 1, 899.00, 0, 'OK'),
(3, 3, 2, 189.50, 0, 'OK'),
(3, 9, 1, 45.90, 10, 'CANC'),
(4, 1, 1, 1299.00, 0, 'OK'),
(4, 11, 1, 1201.00, 5, 'OK'),
(5, 5, 1, 459.99, 0, 'OK'),
(6, 6, 1, 320.00, 0, 'OK'),
(6, 8, 1, 450.00, 0, 'OK'),
(7, 7, 1, 299.00, 0, 'OK'),
(8, 11, 1, 1899.00, 0, 'OK'),
(9, 12, 1, 156.00, 0, 'OK'),
(10, 13, 1, 649.00, 0, 'DEV'),
(11, 14, 1, 1099.00, 0, 'OK'),
(13, 4, 1, 245.00, 0, 'OK');

-- -----------------------------------------------------------------------------
-- Datos iniciales de inventarios y recursos
-- -----------------------------------------------------------------------------

INSERT INTO bodega (clave, nombre, ciudad, direccion, responsable) VALUES
('BOD-CDMX', 'Centro de distribución Vallejo', 'CDMX', 'Calz. Vallejo 1200', 'Laura Pérez'),
('BOD-GDL', 'Centro de distribución Occidente', 'Guadalajara', 'Av. Industria 450', 'Raúl Gómez');

INSERT INTO almacen (id_bodega, clave, nombre, tipo, capacidad_m3) VALUES
(1, 'GEN-01', 'Almacén general', 'GENERAL', 2500),
(1, 'REF-01', 'Cámara refrigerada', 'REFRIGERADO', 450),
(1, 'DEV-01', 'Devoluciones', 'DEVOLUCIONES', 180),
(2, 'GEN-01', 'Almacén general Occidente', 'GENERAL', 1800);

INSERT INTO ubicacion (id_almacen, codigo, pasillo, estante, nivel, capacidad_kg) VALUES
(1, 'A-01-01', 'A', '01', '01', 800),
(1, 'A-01-02', 'A', '01', '02', 500),
(1, 'B-03-01', 'B', '03', '01', 1000),
(2, 'R-01-01', 'R', '01', '01', 600),
(3, 'D-01-01', 'D', '01', '01', 400),
(4, 'A-01-01', 'A', '01', '01', 900);

INSERT INTO proveedor (rfc, nombre, email, telefono, dias_entrega) VALUES
('TEC010101AA1', 'Tecnología Mayorista SA', 'ventas@tecmay.example', '55-1000-2000', 3),
('ALI020202BB2', 'Alimentos del Centro SA', 'pedidos@alicentro.example', '55-3000-4000', 2);

INSERT INTO producto_proveedor (id_prd, id_proveedor, sku_proveedor, costo, preferido) VALUES
(1, 1, 'TM-AUD-BT', 820.00, TRUE),
(2, 1, 'TM-CAR-65', 540.00, TRUE),
(3, 2, 'AC-CAFE-500', 112.00, TRUE),
(4, 2, 'AC-ACEITE-1L', 168.00, TRUE);

INSERT INTO existencia
    (id_prd, id_ubicacion, lote, fecha_caducidad, cantidad, reservado, punto_reorden, costo_promedio)
VALUES
(1, 1, '', NULL, 42, 5, 10, 820.00),
(2, 2, '', NULL, 8, 2, 12, 540.00),
(3, 4, 'CAF-2026-07', '2027-01-31', 120, 18, 30, 112.00),
(4, 4, 'ACE-2026-04', '2027-04-30', 18, 0, 20, 168.00),
(11, 3, '', NULL, 25, 4, 8, 1180.00),
(1, 6, '', NULL, 15, 0, 8, 825.00);

INSERT INTO movimiento_inventario
    (tipo, id_prd, id_ubicacion_origen, id_ubicacion_destino, cantidad,
     referencia_externa, motivo, usuario_registro)
VALUES
('ENTRADA', 1, NULL, 1, 50, 'OC-2026-001', 'Recepción de compra', 'ana.operaciones'),
('SALIDA', 1, 1, NULL, 8, 'PED-2026-001', 'Surtido de pedido', 'luis.surtido'),
('TRANSFERENCIA', 1, 1, 6, 15, 'TR-2026-001', 'Reabasto regional', 'ana.operaciones'),
('AJUSTE', 2, 2, NULL, 1, 'AJ-2026-001', 'Daño detectado en conteo', 'maria.auditoria');

INSERT INTO recurso
    (id_bodega, clave, tipo, nombre, estado, capacidad, unidad_capacidad, habilidades, metadata)
VALUES
(1, 'PER-001', 'PERSONA', 'José Ramírez', 'DISPONIBLE', NULL, NULL,
 ARRAY['montacargas', 'conteo_ciclico'], '{"turno":"matutino"}'),
(1, 'EQ-001', 'EQUIPO', 'Montacargas eléctrico 01', 'ASIGNADO', 1800, 'kg',
 ARRAY['carga', 'descarga'], '{"marca":"Toyota","horometro":1240}'),
(1, 'VEH-001', 'VEHICULO', 'Camión rabón 01', 'MANTENIMIENTO', 8, 'ton',
 ARRAY['reparto_local'], '{"placas":"AB-12-CD","kilometraje":84500}'),
(2, 'PER-002', 'PERSONA', 'Elena Torres', 'ASIGNADO', NULL, NULL,
 ARRAY['recepcion', 'calidad'], '{"turno":"vespertino"}'),
(2, 'EQ-002', 'EQUIPO', 'Patín hidráulico 02', 'DISPONIBLE', 2500, 'kg',
 ARRAY['movimiento_interno'], '{"marca":"Mitsubishi"}');

INSERT INTO asignacion_recurso
    (id_recurso, id_almacen, actividad, responsable, inicio, fin, estado)
VALUES
(2, 1, 'Descarga de proveedor OC-2026-001', 'Laura Pérez',
 '2026-07-16 08:00:00-06', '2026-07-16 11:00:00-06', 'TERMINADA'),
(4, 4, 'Recepción de mercancía', 'Raúl Gómez',
 '2026-07-16 14:00:00-06', '2026-07-16 18:00:00-06', 'EN_CURSO');

INSERT INTO mantenimiento_recurso
    (id_recurso, tipo, descripcion, fecha_programada, costo, estado)
VALUES
(3, 'PREVENTIVO', 'Cambio de aceite y revisión de frenos', '2026-07-18', 4800, 'PROGRAMADO'),
(2, 'INSPECCION', 'Inspección mensual de seguridad', '2026-08-01', 0, 'PROGRAMADO');

COMMIT;
