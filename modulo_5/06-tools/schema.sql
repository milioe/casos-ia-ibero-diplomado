-- =============================================================================
-- 06-tools | Tienda "La Bodega del Norte" — DDL + datos sucios (15 filas c/u)
-- PostgreSQL 14+. Ejecutar: psql -f schema.sql  (o pegar en Supabase SQL Editor)
-- =============================================================================

BEGIN;

DROP TABLE IF EXISTS lin_ped CASCADE;
DROP TABLE IF EXISTS ped CASCADE;
DROP TABLE IF EXISTS prd CASCADE;
DROP TABLE IF EXISTS cli CASCADE;
DROP TABLE IF EXISTS ref_cod CASCADE;

-- -----------------------------------------------------------------------------
-- DDL
-- -----------------------------------------------------------------------------

CREATE TABLE ref_cod (
    id_ref      SERIAL PRIMARY KEY,
    dominio     VARCHAR(20) NOT NULL,   -- ped_sts | cat_prd | canal | tier | moneda
    codigo      VARCHAR(20) NOT NULL,
    etiqueta    VARCHAR(80),
    factor_num  NUMERIC(12,4),          -- trampa: algunos montos hay que multiplicar
    vigente     CHAR(1) DEFAULT 'S',    -- S/N/1/0 mezclado en datos
    UNIQUE (dominio, codigo)
);

CREATE TABLE cli (
    id_cli      SERIAL PRIMARY KEY,
    nom         VARCHAR(120) NOT NULL,
    tel         VARCHAR(40),            -- formatos inconsistentes
    email       VARCHAR(120),
    ciudad      VARCHAR(60),
    tier_raw    VARCHAR(10),            -- no coincide siempre con ref_cod
    fch_alta    VARCHAR(20) NOT NULL    -- fecha como texto a propósito
);

CREATE TABLE prd (
    id_prd      SERIAL PRIMARY KEY,
    sku         VARCHAR(30) UNIQUE NOT NULL,
    desc_corta  VARCHAR(200),
    cat_cd      VARCHAR(20),            -- FK lógica a ref_cod(dominio='cat_prd')
    precio_raw  VARCHAR(20) NOT NULL,   -- a veces pesos, a veces centavos
    activo_fl   VARCHAR(5)              -- S/N/1/0/si/no
);

CREATE TABLE ped (
    id_ped      SERIAL PRIMARY KEY,
    id_cli      INTEGER REFERENCES cli(id_cli),
    fch         VARCHAR(20) NOT NULL,   -- mezcla ISO, DMY y compacto
    sts         VARCHAR(5) NOT NULL,      -- FK lógica a ref_cod(dominio='ped_sts')
    canal_raw   VARCHAR(10),
    moneda_cd   VARCHAR(5) DEFAULT 'MXN',
    mnt_decl    NUMERIC(14,2),          -- total declarado (a menudo MAL vs líneas)
    nota_int    TEXT                    -- pistas internas, basura
);

CREATE TABLE lin_ped (
    id_lin      SERIAL PRIMARY KEY,
    id_ped      INTEGER NOT NULL REFERENCES ped(id_ped) ON DELETE CASCADE,
    id_prd      INTEGER NOT NULL REFERENCES prd(id_prd),
    cant        NUMERIC(10,2) NOT NULL,
    precio_u    NUMERIC(14,2),          -- precio al momento de venta
    dto_pct     NUMERIC(5,2) DEFAULT 0,
    lin_sts     VARCHAR(5) DEFAULT 'OK'   -- OK | CANC | DEV — no siempre = ped.sts
);

CREATE INDEX idx_ped_cli ON ped(id_cli);
CREATE INDEX idx_ped_fch ON ped(fch);
CREATE INDEX idx_lin_ped ON lin_ped(id_ped);
CREATE INDEX idx_prd_cat ON prd(cat_cd);

-- -----------------------------------------------------------------------------
-- SEED: ref_cod (15) — sin esto el resto es ilegible
-- -----------------------------------------------------------------------------

INSERT INTO ref_cod (dominio, codigo, etiqueta, factor_num, vigente) VALUES
('ped_sts', '1', 'capturado',           1,    'S'),
('ped_sts', '2', 'pagado',              1,    'S'),
('ped_sts', '3', 'en_ruta',             1,    'S'),
('ped_sts', '4', 'entregado',           1,    'S'),
('ped_sts', '9', 'cancelado',           0,    'S'),
('cat_prd', 'ELEC',  'electronica',     NULL, 'S'),
('cat_prd', 'ELECT', 'electronica_legacy', NULL, '1'),
('cat_prd', 'ALIM',  'alimentos',       NULL, 'S'),
('cat_prd', 'HOGAR', 'hogar',           NULL, 'S'),
('cat_prd', 'TEXT',  'textil',          NULL, 'N'),
('canal',   'W',     'web',             NULL, 'S'),
('canal',   'T',     'tienda',          NULL, 'S'),
('canal',   'web',   'web_alias',       NULL, 'S'),
('tier',    '1',     'oro',             NULL, 'S'),
('tier',    'GOLD',  'oro_alias',       NULL, 'si');

-- -----------------------------------------------------------------------------
-- SEED: cli (15)
-- -----------------------------------------------------------------------------

INSERT INTO cli (nom, tel, email, ciudad, tier_raw, fch_alta) VALUES
('María González',      '55-1234-5678',     'maria.g@mail.com',     'CDMX',     'GOLD', '2023-01-10'),
('CARLOS ruiz',         '5512345678',       NULL,                   'GDL',      '1',    '15/02/2023'),
('Ana  Torres',         '(81)555-0199',     'ana.t@corp.mx',        'MTY',      '2',    '20230301'),
('pedro lopez',         '55.8765.4321',     'pedro@',               'CDMX',     'silver', '2023-04-12'),
('Lucía Méndez',        NULL,               'lucia.m@gmail.com',    'PUE',      'GOLD', '2023-05-20'),
('JORGE HERRERA',       '044-331-998-8776', 'jorge.h@x.com',        'GDL',      '1',    '2023-06-01'),
('nora castillo',       '5550001111',       'nora.c@mail.com',      'QRO',      '3',    '2023-07-15'),
('Ricardo Vega',        '55-0000-2222',     'r.vega@empresa.mx',    'CDMX',     '2',    '20230820'),
('Sofía Delgado',       '5588776655',       NULL,                   'CDMX',     'GOLD', '2023-09-05'),
('miguel angel rios',   '55 9988 7766',     'mrios@old.net',        'TIJ',      'bronze', '2023-10-11'),
('Elena Vargas',        '5511223344',       'elena.v@mail.com',     'CDMX',     '1',    '2023-11-22'),
('Héctor Núñez',        NULL,               'hector.n@corp.mx',     'LEO',      '2',    '20231201'),
('patricia solis',      '55-4433-2211',     'p.solis@mail.com',     'CDMX',     'GOLD', '2024-01-08'),
('Daniel Kim',          '+52 55 1234 0000', 'daniel.k@startup.io',  'CDMX',     '1',    '2024-02-14'),
('Valentina Ortiz',     '5500112233',       'vale@mail.com',        'MER',      '2',    '15/03/2024');

-- -----------------------------------------------------------------------------
-- SEED: prd (15) — precios y categorías trampa
-- -----------------------------------------------------------------------------

INSERT INTO prd (sku, desc_corta, cat_cd, precio_raw, activo_fl) VALUES
('SKU-E001', 'Audífonos BT Pro',        'ELEC',  '1299.00',  'S'),
('SKU-E002', 'Cargador 65W USB-C',      'ELECT', '89900',    '1'),      -- centavos disfrazados
('SKU-A001', 'Café molido 500g',        'ALIM',  '189.50',   'si'),
('SKU-A002', 'Aceite oliva 1L',         'ALIM',  '24500',    'S'),      -- centavos
('SKU-H001', 'Sartén antiadherente',    'HOGAR', '459.99',   'N'),      -- inactivo pero aún en líneas viejas
('SKU-H002', 'Juego toallas 3pz',       'hogar', '320.00',   'S'),      -- cat minúscula huérfana
('SKU-T001', 'Playera algodón M',       'TEXT',  '299.00',   '0'),
('SKU-E003', 'Mouse inalámbrico',       'ELEC',  '45000',    'S'),
('SKU-A003', 'Galletas surtidas',       'ALIM',  '45.90',    'S'),
('SKU-H003', 'Lámpara LED escritorio',  'HOGAR', '799.00',   'S'),
('SKU-E004', 'Teclado mecánico',        'ELEC',  '1899.00',  'S'),
('SKU-A004', 'Agua mineral 12pk',       'ALIM',  '15600',    '1'),
('SKU-T002', 'Sudadera unisex L',       'TEXT',  '649.00',   'no'),
('SKU-E005', 'Webcam HD',               'ELEC',  '109900',   'S'),      -- centavos
('SKU-H004', 'Organizador baño',        'HOGAR', '199.00',   'S');

-- -----------------------------------------------------------------------------
-- SEED: ped (15) — fechas mixtas, totales declarados incorrectos
-- -----------------------------------------------------------------------------

INSERT INTO ped (id_cli, fch, sts, canal_raw, moneda_cd, mnt_decl, nota_int) VALUES
(1,  '2024-01-15',      '4', 'W',   'MXN', 1299.00,  'ok'),
(2,  '15/01/2024',      '4', 'T',   'MXN',  899.00,  'precio mal capturado en header'),
(3,  '20240120',        '9', 'web', 'MXN',  378.90,  'cancelado pero revisar líneas'),
(1,  '2024-02-01',      '4', 'W',   'MXN', 2500.00,  'cliente recurrente'),
(5,  '01/02/2024',      '2', 'W',   'MXN',  459.99,  NULL),
(6,  '20240210',        '3', 'T',   'MXN',  770.00,  'en ruta GDL'),
(4,  '2024-02-14',      '4', 'W',   'MXN',  299.00,  'email pedro@ inválido'),
(8,  '14/02/2024',      '1', 'W',   'MXN', 1899.00,  'capturado sin pago'),
(9,  '20240218',        '4', 'T',   'MXN',  156.00,  'monto header en pesos, línea en centavos?'),
(10, '2024-02-22',      '9', 'W',   'MXN',  649.00,  'devolución parcial en nota'),
(11, '22/02/2024',      '4', 'W',   'MXN', 1099.00,  NULL),
(12, '20240228',        '4', 'T',   'MXN',  199.00,  NULL),
(13, '2024-03-05',      '3', 'W',   'MXN', 2348.00,  '2 líneas mismo pedido'),
(13, '05/03/2024',      '4', 'web', 'MXN',  245.00,  'segundo pedido mismo día'),
(14, '20240310',        '2', 'W',   'MXN', 1099.00,  'pago pendiente confirmación');

-- -----------------------------------------------------------------------------
-- SEED: lin_ped (15) — sts de línea ≠ sts de pedido; precios históricos
-- -----------------------------------------------------------------------------

INSERT INTO lin_ped (id_ped, id_prd, cant, precio_u, dto_pct, lin_sts) VALUES
(1,  1,  1,    1299.00,  0,    'OK'),
(2,  2,  1,     899.00,  0,    'OK'),    -- prd dice 89900 centavos; línea en pesos
(3,  3,  2,     189.50,  0,    'OK'),    -- ped cancelado (sts 9), línea sigue OK
(3,  9,  1,      45.90, 10,    'CANC'),
(4,  1,  1,    1299.00,  0,    'OK'),
(4,  11, 1,    1201.00,  5,    'OK'),    -- suma real ≠ mnt_decl 2500
(5,  5,  1,     459.99,  0,    'OK'),    -- producto inactivo
(6,  6,  1,     320.00,  0,    'OK'),
(6,  8,  1,     450.00,  0,    'OK'),    -- prd 45000 centavos vs 450 en línea
(7,  7,  1,     299.00,  0,    'OK'),
(8,  11, 1,    1899.00,  0,    'OK'),
(9,  12, 1,     156.00,  0,    'OK'),    -- agua: 156 pesos vs 15600 centavos en catálogo
(10, 13, 1,     649.00,  0,    'DEV'),   -- ped cancelado, línea devuelta
(11, 14, 1,    1099.00,  0,    'OK'),
(13, 4,  1,     245.00,  0,    'OK');    -- aceite: catálogo 24500 centavos

COMMIT;