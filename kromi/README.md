# Kromi Database

## Summary

- [Introduction](#introduction)
- [Database Type](#database-type)
- [Table Structure](#table-structure)
  - [categorias](#categorias)
  - [productos](#productos)
  - [imagenes_productos](#imagenes_productos)
  - [enlaces_productos](#enlaces_productos)
  - [precios_productos](#precios_productos)
- [Relationships](#relationships)
- [Database Diagram](#database-diagram)

## Introduction

This project aims to consolidate and normalize product information from multiple Excel sources into a structured PostgreSQL database. The system is designed to handle data cleaning, field reconciliation, and relational modeling to support a consistent and scalable product catalog for the Kromi platform.

## Database type

- **Database system:** PostgreSQL

## Table structure

### categorias

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **id** | SERIAL | 🔑 PK, null, unique |  | |
| **nombre** | VARCHAR(100) | not null |  | |
| **descripcion** | TEXT | null |  | |
| **activa** | BOOLEAN | null, default: TRUE |  | |

### productos

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **id** | SERIAL | 🔑 PK, null, unique |  | |
| **codigo_barras** | VARCHAR(50) | not null, unique |  | |
| **ean** | VARCHAR(50) | null |  | |
| **nombre_corto** | VARCHAR(255) | not null |  | |
| **nombre_completo** | VARCHAR(255) | null |  | |
| **descripcion_corta** | TEXT | null |  | |
| **categoria_id** | INTEGER | null | fk_Productos_categoria_id_categorias | |
| **produccion** | VARCHAR(100) | null |  | |
| **precio_lista** | DECIMAL(10,2) | null |  | |
| **revision_contenido** | TEXT | null |  | |
| **observaciones** | TEXT | null |  | |
| **activo** | BOOLEAN | null, default: TRUE |  | |
| **fecha_creacion** | TIMESTAMP | null, default: CURRENT_TIMESTAMP |  | |
| **fecha_actualizacion** | TIMESTAMP | null, default: CURRENT_TIMESTAMP |  | |

#### Indexes

| Name | Unique | Fields |
|------|--------|--------|
| productos_index_0 |  | codigo_barras, categoria_id |

### imagenes_productos

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **id** | SERIAL | 🔑 PK, null, unique |  | |
| **producto_id** | INTEGER | null | fk_imagenes_productos_producto_id_productos | |
| **url_imagen** | VARCHAR(500) | null |  | |
| **url_thumbnail** | VARCHAR(500) | null |  | |
| **url_medium** | VARCHAR(500) | null |  | |
| **url_large** | VARCHAR(500) | null |  | |
| **es_principal** | BOOLEAN | null, default: FALSE |  | |
| **orden** | INTEGER | null, default: 0 |  | |
| **descripcion** | VARCHAR(255) | null |  | |
| **fecha_subida** | TIMESTAMP | null, default: CURRENT_TIMESTAMP |  | |

#### Indexes

| Name | Unique | Fields |
|------|--------|--------|
| imagenes_productos_index_0 |  | producto_id |

### enlaces_productos

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **id** | SERIAL | 🔑 PK, null, unique | fk_enlaces_productos_id_productos | |
| **producto_id** | INTEGER | null |  | |
| **id_externo** | VARCHAR(50) | null |  | |
| **nombre_exportacion** | VARCHAR(100) | null |  | |
| **deeplink** | TEXT | null |  | |
| **deeplink_encoded** | TEXT | null |  | |
| **tipo_enlace** | VARCHAR(50) | null, default: editor |  | |

#### Indexes

| Name | Unique | Fields |
|------|--------|--------|
| enlaces_productos_index_0 |  | producto_id |

### precios_productos

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **id** | SERIAL | 🔑 PK, null, unique |  | |
| **producto_id** | INTEGER | null, unique | fk_precios_productos_producto_id_productos | |
| **precio** | DECIMAL(10,2) | null |  | |
| **fecha_inicio** | DATE | not null, unique |  | |
| **fecha_fin** | DATE | null |  | |
| **fuente** | VARCHAR(100) | null |  | |

#### Indexes

| Name | Unique | Fields |
|------|--------|--------|
| precios_productos_index_0 |  | producto_id |

## Relationships

- **productos to categorias**: one_to_one
- **imagenes_productos to productos**: one_to_one
- **enlaces_productos to productos**: one_to_one
- **precios_productos to productos**: one_to_one

## Database Diagram

![Database Diagram](/kromidbDiagram.png)
