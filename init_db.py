import sqlite3
import os

def cargar_datos():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'tienda.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tablas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        imagen TEXT,
        imagenes TEXT,
        slug TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carrito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        cantidad INTEGER,
        talle TEXT,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_por_talle (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER NOT NULL,
        talle TEXT NOT NULL,
        stock INTEGER NOT NULL,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

    # Limpiar datos existentes
    cursor.execute('DELETE FROM productos')
    cursor.execute('DELETE FROM carrito')
    cursor.execute('DELETE FROM stock_por_talle')

    # Insertar productos
    productos = [
        ("iron-spider", "Iron Spider", 64900, "Traje de Spider-Man Iron Spider...", "iron-spider0_.webp","iron-spider1_.webp,iron-spider2_.webp,iron-spider3_.webp,iron-spider4_.webp,talles.webp"),
        ("traje-mejorado", "Traje Mejorado", 64900, "Traje mejorado de Spider-Man...", "mejorado4_.webp", "mejorado4_.webp,mejorado5_.webp,mejorado6_.webp,talles.webp"),
        ("spiderman-ps4", "Spiderman PS4", 59900, "Traje inspirado en el videojuego de PS4...", "ps41_.webp", "ps40_.webp,ps41_.webp,talles.webp"),
        ("traje-clasico", "Traje Clasico", 62900, "Traje clásico de los cómics...", "clasico9.webp", "clasico1.png,clasico2.png,clasico3.png,clasico4.png,clasico5.png,talles.webp"),
        ("miles-morales", "Miles Morales", 59900, "Diseño negro y rojo intenso...", "miles2_.webp", "miles5_.webp,miles1_.webp,miles4_.webp,miles3_.webp,talles.webp"),
        ("electro", "Traje Negro y Dorado", 59901, "Diseño con circuitos dorados...", "electro0_.webp", "electro4_.webp,electro3_.webp,talles.webp"),
        ("traje-mejorado-adulto", "Traje Mejorado (Adulto)", 69900, "Versión mejorada para adultos...", "mejorado-adulto0_.webp", "mejorado-adulto2_.webp,mejorado-adulto0_.webp,mejorado-adulto1_.webp,talles.webp"),
    ]

    cursor.executemany('''
    INSERT INTO productos (slug, nombre, precio, descripcion, imagen, imagenes)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', productos)
    # Obtener IDs y slugs
    cursor.execute("SELECT id, slug FROM productos")
    productos_insertados = cursor.fetchall()

    # Stock real
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

    # Insertar talles
    for producto_id, slug in productos_insertados:
        if slug in stock_real:
            for talle, cantidad in stock_real[slug].items():
                cursor.execute('''
                    INSERT INTO stock_por_talle (producto_id, talle, stock)
                    VALUES (?, ?, ?)
                ''', (producto_id, talle, cantidad))

    conn.commit()
    conn.close()
    print("✅ Base de datos cargada correctamente")
