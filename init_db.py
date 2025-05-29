import sqlite3

# Conexión
conn = sqlite3.connect('tienda.db')
cursor = conn.cursor()

# Crear tabla de productos
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    imagen TEXT,
    slug TEXT UNIQUE NOT NULL
)
''')

# Crear tabla de carrito
cursor.execute('''
CREATE TABLE IF NOT EXISTS carrito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    cantidad INTEGER,
    talle TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
''')

# Crear tabla de stock por talle
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

# Insertar productos iniciales
productos = [
    ("iron-spider", "Iron Spider", 64900, "Traje de Spider-Man Iron Spider, inspirado en el diseño de Tony Stark con colores rojo, azul oscuro y detalles dorados metálicos, tal como se ve en Infinity War y No Way Home. Hecho en lycra elástica de alta calidad, con estampado digital detallado, cierre invisible en la espalda y ajuste cómodo. Ideal para quienes buscan un look heroico, tecnológico y cinematográfico.", "iron-spider0_.webp","iron-spider1_.webp,iron-spider2_.webp,iron-spider3_.webp,iron-spider4_.webp,talles.webp"),
    ("traje-mejorado", "Traje Mejorado", 64900, "Traje mejorado de Spider-Man con diseño rojo y negro, como se ve en Far From Home y No Way Home", "mejorado4_.webp", "mejorado4_.webp,mejorado5_.webp,mejorado6_.webp,talles.webp"),
    ("spiderman-ps4", "Spiderman PS4", 59900, "Traje inspirado en el Spider-Man del videojuego de PS4, con diseño moderno en rojo, azul y blanco, y la icónica araña blanca en el pecho. Confeccionado en lycra elástica de alta calidad, incluye estampado digital ultra detallado y cierre invisible en la espalda. Ideal para fans del universo gamer y disponible en talles para niños y adultos.", "ps41_.webp", "ps40_.webp,ps41_.webp,talles.webp"),
    ("traje-clasico", "Traje Clasico", 62900, "Traje clásico de Spider-Man inspirado en los cómics originales, con diseño rojo y azul, líneas de telaraña impresas y una araña negra destacada en el pecho. Confeccionado en lycra elástica cómoda y liviana, incluye máscara completa con ojos blancos grandes. Ideal para niños que quieren convertirse en el Spidey más auténtico y tradicional.", "clasico9.webp", "clasico1.png,clasico2.png,clasico3.png,clasico4.png,clasico5.png,talles.webp"),
    ("miles-morales", "Miles Morales", 59900, "Traje de Spider-Man de Miles Morales con diseño negro y rojo intenso, inspirado en el estilo urbano y moderno de las películas animadas Spider-Verse. Incluye araña roja en el pecho, patrones de telaraña estilizados y está confeccionado en lycra elástica de alta calidad con estampado digital y cierre invisible. Ideal para quienes buscan un look original, juvenil y diferente dentro del universo Spider-Man.", "miles2_.webp", "miles5_.webp,miles1_.webp,miles4_.webp,miles3_.webp,talles.webp"),
    ("electro", "Traje Negro y Dorado", 59900, "Confeccionado con lycra elástica de alta calidad, este traje replica el icónico diseño negro con detalles dorados que Spider-Man usa al enfrentar por primera vez a Electro y Sandman. Su estética única, con circuitos dorados impresos, combina estilo tecnológico y misterio, ideal para quienes buscan un look diferente al clásico rojo y azul.", "electro0_.webp", "electro4_.webp,electro3_.webp,talles.webp"),
    ("traje-mejorado-adulto", "Traje Mejorado (Adulto)", 69900, "Traje de Spider-Man versión mejorada visto en Far From Home y No Way Home, con diseño rojo y negro, araña blanca en la espalda y detalles tecnológicos. Confeccionado en lycra elástica de alta calidad, estampado digital preciso y cierre invisible. Ideal para adultos que buscan un look moderno, fiel al cine y perfecto para eventos o cosplay.", "mejorado-adulto0_.webp", "mejorado-adulto2_.webp,mejorado-adulto0_.webp,mejorado-adulto1_.webp,talles.webp"),
    
]

cursor.executemany('''
INSERT INTO productos (slug, nombre, precio, descripcion, imagen, imagenes)
VALUES (?, ?, ?, ?, ?, ?)
''', productos)


print("Base de datos creada con éxito.")
# 4. Insertar stock por talle
stock = []
cursor.execute('DELETE FROM stock_por_talle')
cursor.execute('SELECT id FROM productos')
productos_insertados = cursor.fetchall()



# 5. Confirmar y cerrar
conn.commit()
conn.close()
print("Base de datos inicializada con productos y stock por talle.")

