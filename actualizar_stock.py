import sqlite3

DB_PATH = "tienda.db"

# Stock real: cantidad de trajes por talle
stock_real = {
    'miles-morales': {
        'M/120': 2,
        '170': 1,
        'L/130': 1
    },
    'traje-mejorado': {
        'L/130': 1,
        '180': 1,
        'XS/100': 1,
        'M/120': 1,
        'L/130': 2
    },
    'electro': {
        'XXL/150': 1,
        'XL/140': 1
    },
    'spiderman-ps4': {
        'M/120': 2
    },
    'traje-clasico': {
        'L/130': 2,
        'S/110': 1
    },
    'iron-spider': {
        'XL/140': 1
    }
}

# Conexión
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Eliminar stock anterior (opcional: podés comentarlo si solo querés sumar)
cursor.execute("DELETE FROM stock_por_talle")

# Buscar ID del producto por slug
def get_producto_id(slug):
    cursor.execute("SELECT id FROM productos WHERE slug = ?", (slug,))
    row = cursor.fetchone()
    return row[0] if row else None

# Insertar o actualizar stock
for slug, talles_dict in stock_real.items():
    producto_id = get_producto_id(slug)
    if producto_id:
        for talle, cantidad in talles_dict.items():
            cursor.execute('''
                SELECT stock FROM stock_por_talle
                WHERE producto_id = ? AND talle = ?
            ''', (producto_id, talle))
            existente = cursor.fetchone()

            if existente:
                nuevo_stock = existente[0] + cantidad
                cursor.execute('''
                    UPDATE stock_por_talle
                    SET stock = ?
                    WHERE producto_id = ? AND talle = ?
                ''', (nuevo_stock, producto_id, talle))
            else:
                cursor.execute('''
                    INSERT INTO stock_por_talle (producto_id, talle, stock)
                    VALUES (?, ?, ?)
                ''', (producto_id, talle, cantidad))
    else:
        print(f"⚠️ Producto con slug '{slug}' no encontrado.")

# Guardar cambios y cerrar
conn.commit()
conn.close()
print("✅ Stock actualizado correctamente.")
