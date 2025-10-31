CREATE SCHEMA IF NOT EXISTS chromabags;
SET search_path = chromabags;

-- TIPOS ENUM
CREATE TYPE esquema_color AS ENUM ('armonico','complementario','analogo');
CREATE TYPE tipo_modelo AS ENUM ('simple','combinado','especial');
CREATE TYPE estado_pedido AS ENUM ('pendiente','en_produccion','entregado','cancelado');
CREATE TYPE estado_cotizacion AS ENUM ('pendiente','aceptada','rechazada','expirada');
CREATE TYPE tipo_cliente AS ENUM ('FRECUENTE', 'PRIMERIZO', 'OCASIONAL');

-- TABLA USUARIO
CREATE TABLE usuario_admin (
    id_admin SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL, -- hash de contraseña
    rol VARCHAR(50) DEFAULT 'administrador',
    fecha_registro TIMESTAMP DEFAULT NOW(),
    activo BOOLEAN DEFAULT TRUE
);

-- Trigger para máximo 2 administradores activos
CREATE OR REPLACE FUNCTION validar_max_dos_admins()
RETURNS TRIGGER AS $$
DECLARE
    total INT;
BEGIN
    SELECT COUNT(*) INTO total FROM usuario_admin WHERE activo = TRUE;
    IF total >= 2 THEN
        RAISE EXCEPTION 'Solo se permiten hasta dos usuarios administradores activos.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_max_dos_admins
BEFORE INSERT ON usuario_admin
FOR EACH ROW EXECUTE FUNCTION validar_max_dos_admins();

-- TABLA PALETAS_COLORES
CREATE TABLE paletas_colores (
    id_paleta SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    esquema esquema_color NOT NULL,
    descripcion TEXT
);

-- TABLA COLORES
CREATE TABLE colores (
    id_color SERIAL PRIMARY KEY,
    nombre_color VARCHAR(100) NOT NULL,
    codigo_hex CHAR(7) NOT NULL CHECK (codigo_hex ~ '^#[0-9A-Fa-f]{6}$'),
    id_paleta INT REFERENCES paletas_colores(id_paleta) ON DELETE SET NULL
);

-- TABLA MODELOS_BOLSAS
CREATE TABLE modelos_bolsas (
    id_modelo SERIAL PRIMARY KEY,
    nombre_modelo VARCHAR(100) NOT NULL,
    tipo tipo_modelo NOT NULL,
    descripcion TEXT,
    ancho NUMERIC(6,2) DEFAULT 30.00,
    alto NUMERIC(6,2) DEFAULT 40.00
);

-- TABLA COMBINACIONES
CREATE TABLE combinaciones (
    id_combinacion SERIAL PRIMARY KEY,
    id_modelo INT REFERENCES modelos_bolsas(id_modelo),
    esquema esquema_color DEFAULT 'armonico',
    id_color_principal INT REFERENCES colores(id_color),
    id_color_secundario INT REFERENCES colores(id_color),
    id_color_hilo INT REFERENCES colores(id_color),
    id_color_asa INT REFERENCES colores(id_color),
    nombre_guardado VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- TABLA MATERIALES 
CREATE TABLE materiales (
    id_material SERIAL PRIMARY KEY,
    nombre_material VARCHAR(120) NOT NULL,
    tipo VARCHAR(80),
    unidad_medida VARCHAR(10) DEFAULT 'm',
    costo_unitario NUMERIC(12,2) NOT NULL,
    descripcion TEXT
);

-- TABLA INVENTARIO_MATERIALES 
CREATE TABLE inventario_materiales (
    id_inventario SERIAL PRIMARY KEY,
    id_material INT REFERENCES materiales(id_material),
    cantidad NUMERIC(12,2) NOT NULL,
    fecha_actualizacion TIMESTAMP DEFAULT NOW()
);

-- TABLA CLIENTES 
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre_cliente VARCHAR(200) NOT NULL,
    telefono VARCHAR(30),
    correo VARCHAR(150),
    direccion TEXT,
    tipo_cliente tipo_cliente NOT NULL DEFAULT 'PRIMERIZO',
    fecha_registro TIMESTAMP DEFAULT NOW()
);

-- TABLA PRODUCTOS_TERMINADOS
CREATE TABLE productos_terminados (
    id_producto SERIAL PRIMARY KEY,
    id_modelo INT REFERENCES modelos_bolsas(id_modelo),
    id_combinacion INT REFERENCES combinaciones(id_combinacion),
    nombre_producto VARCHAR(150) NOT NULL,
    costo_produccion NUMERIC(12,2),
    precio_sugerido NUMERIC(12,2),
    stock INT DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT NOW()
);

-- TABLA COTIZACIONES
CREATE TABLE cotizaciones (
    id_cotizacion SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    fecha_emision TIMESTAMP DEFAULT NOW(),
    total_estimado NUMERIC(14,2),
    estado estado_cotizacion DEFAULT 'pendiente'
);

-- TABLA DETALLE_COTIZACION
CREATE TABLE detalle_cotizacion (
    id_detalle SERIAL PRIMARY KEY,
    id_cotizacion INT REFERENCES cotizaciones(id_cotizacion) ON DELETE CASCADE,
    id_material INT REFERENCES materiales(id_material),
    cantidad NUMERIC(12,2),
    costo_unitario NUMERIC(12,2),
    subtotal NUMERIC(12,2)
);

-- TABLA PEDIDOS 
CREATE TABLE pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    fecha_pedido TIMESTAMP DEFAULT NOW(),
    fecha_entrega DATE,
    estado estado_pedido DEFAULT 'pendiente',
    total NUMERIC(14,2)
);

-- TABLA DETALLE_PEDIDO
CREATE TABLE detalle_pedido (
    id_detalle SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    id_producto INT REFERENCES productos_terminados(id_producto),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(12,2),
    subtotal NUMERIC(12,2)
);

-- Consulta SQL para generar el catálogo
SELECT 
    pt.id_producto,
    pt.nombre_producto,
    mb.nombre_modelo,
    mb.tipo AS tipo_modelo,
    cp.nombre_color AS color_principal,
    cs.nombre_color AS color_secundario,
    ch.nombre_color AS color_hilo,
    ca.nombre_color AS color_asa,
    pt.precio_sugerido,
    pt.stock
FROM productos_terminados pt
JOIN modelos_bolsas mb ON pt.id_modelo = mb.id_modelo
LEFT JOIN combinaciones c ON pt.id_combinacion = c.id_combinacion
LEFT JOIN colores cp ON c.id_color_principal = cp.id_color
LEFT JOIN colores cs ON c.id_color_secundario = cs.id_color
LEFT JOIN colores ch ON c.id_color_hilo = ch.id_color
LEFT JOIN colores ca ON c.id_color_asa = ca.id_color
ORDER BY pt.nombre_producto;




