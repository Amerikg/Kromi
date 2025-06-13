CREATE DATABASE kromi_db;
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE
);

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    ean VARCHAR(50),
    nombre_corto VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(255),
    descripcion_corta TEXT,
    categoria_id INTEGER REFERENCES categorias(id),
    produccion VARCHAR(100),
    precio_lista DECIMAL(10,2),
    revision_contenido TEXT,
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE imagenes_productos (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER REFERENCES productos(id) ON DELETE CASCADE,
    url_imagen VARCHAR(500),
    url_thumbnail VARCHAR(500),
    url_medium VARCHAR(500),
    url_large VARCHAR(500),
    es_principal BOOLEAN DEFAULT FALSE,
    orden INTEGER DEFAULT 0,
    descripcion VARCHAR(255),
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enlaces_productos (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER REFERENCES productos(id) ON DELETE CASCADE,
    id_externo VARCHAR(50),
    nombre_exportacion VARCHAR(100),
    deeplink TEXT,
    deeplink_encoded TEXT,
    tipo_enlace VARCHAR(50) DEFAULT 'editor'
);

CREATE INDEX idx_productos_codigo_barras ON productos(codigo_barras);
CREATE INDEX idx_productos_categoria ON productos(categoria_id);
CREATE INDEX idx_imagenes_producto ON imagenes_productos(producto_id);
CREATE INDEX idx_enlaces_producto ON enlaces_productos(producto_id);
