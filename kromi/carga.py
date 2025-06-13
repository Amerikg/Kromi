import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Cargar datos del Excel
df = pd.read_excel("KromiDB.xlsx")

# Limpieza básica
df.columns = df.columns.str.strip()
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="kromi_db",
    user="postgres",  
    password="0509"  
)
cur = conn.cursor()

# Insertar categorías únicas
categorias = df["Categoría"].dropna().unique()
for cat in categorias:
    cur.execute(
        "INSERT INTO categorias (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING",
        (cat,)
    )

# Mapeo de nombre de categoría a ID
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

# Obtener IDs de productos insertados
cur.execute("SELECT id, codigo_barras FROM productos")
producto_map = {cb: pid for pid, cb in cur.fetchall()}

# Insertar enlaces/deeplinks
enlaces = []
for _, row in df.iterrows():
    pid = producto_map.get(row["Código de Barras"])
    if pid:
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
execute_values(cur, query_enlaces, enlaces)

# Confirmar y cerrar
conn.commit()
cur.close()
conn.close()
print("Carga completada exitosamente.")
