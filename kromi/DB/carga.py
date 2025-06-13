import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Cargar archivo Excel
df = pd.read_excel("KromiDB.xlsx")

# Limpiar nombres de columnas y celdas
df.columns = df.columns.str.strip()
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# Asegurar que los códigos de barras sean string
df["Código de Barras"] = df["Código de Barras"].astype(str)

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="kromi_db",
    user="postgres",
    password="0509"
)
cur = conn.cursor()

# Insertar categorías
categorias = df["Categoría"].dropna().unique()
for cat in categorias:
    cur.execute(
        "INSERT INTO categorias (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING",
        (cat,)
    )

# Mapeo categoría → id
cur.execute("SELECT id, nombre FROM categorias")
cat_map = {nombre: id for id, nombre in cur.fetchall()}

# Insertar productos
productos = []
for _, row in df.iterrows():
    categoria_id = cat_map.get(row["Categoría"])
    productos.append((
        row["Código de Barras"],
        row.get("EAN"),
        row["Nombre"],
        row.get("Nombre Precios"),
        row.get("Descripción Corta (Titulo del Producto)"),
        categoria_id,
        row.get("Producción"),
        row.get("Precio Lista 2024", 0),
        row.get("Revisión Contenido"),
        row.get("Observación")
    ))

query_productos = '''
INSERT INTO productos (
    codigo_barras, ean, nombre_corto, nombre_completo,
    descripcion_corta, categoria_id, produccion,
    precio_lista, revision_contenido, observaciones
) VALUES %s
ON CONFLICT (codigo_barras) DO NOTHING;
'''
execute_values(cur, query_productos, productos)
conn.commit()

# Mapeo actualizado con códigos como texto
cur.execute("SELECT id, codigo_barras FROM productos")
producto_map = {str(cb): pid for pid, cb in cur.fetchall()}

# Insertar enlaces
enlaces = []
for _, row in df.iterrows():
    codigo = str(row["Código de Barras"])
    pid = producto_map.get(codigo)
    if not pid:
        print("⚠️ Producto no encontrado para enlace:", codigo)
    elif row.get("Export name"):
        enlaces.append((
            pid,
            row.get("Product Id"),
            row.get("Export name"),
            row.get("DeepLink"),
            row.get("Link Encoded")
        ))

query_enlaces = '''
INSERT INTO enlaces_productos (
    producto_id, id_externo, nombre_exportacion,
    deeplink, deeplink_encoded
) VALUES %s;
'''
if enlaces:
    try:
        execute_values(cur, query_enlaces, enlaces)
        print(f"✅ {len(enlaces)} enlaces insertados.")
    except Exception as e:
        print("❌ Error al insertar enlaces:", e)
else:
    print("⚠️ No hay enlaces para insertar.")

# Insertar imágenes
imagenes = []
for _, row in df.iterrows():
    codigo = str(row["Código de Barras"])
    pid = producto_map.get(codigo)
    if not pid:
        print("⚠️ Producto no encontrado para imagen:", codigo)
    elif row.get("Foto"):
        imagenes.append((pid, row["Foto"]))

query_imagenes = '''
INSERT INTO imagenes_productos (
    producto_id, url_imagen
) VALUES %s;
'''
if imagenes:
    try:
        execute_values(cur, query_imagenes, imagenes)
        print(f"✅ {len(imagenes)} imágenes insertadas.")
    except Exception as e:
        print("❌ Error al insertar imágenes:", e)
else:
    print("⚠️ No hay imágenes para insertar.")

# Finalizar
conn.commit()
cur.close()
conn.close()
print("🎉 Carga completada exitosamente.")
