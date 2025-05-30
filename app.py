from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from flask import request, redirect
import sqlite3
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'tienda.db')

app = Flask(__name__)

# Función para conectar y obtener productos
def obtener_productos():#Esta función se conecta con la base de datos tienda.db, lee todos los registros de la tabla productos, y devuelve una lista de productos.

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para obtener un solo producto por slug
def obtener_producto_por_slug(slug):
    conn = sqlite3.connect(db_path)    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE slug = ?', (slug,))
    producto = cursor.fetchone()
    conn.close()
    return producto

# Página principal con productos destacados (los primeros 3)
@app.route('/') #decorador de Flask.
def home():
    productos = obtener_productos() 
    destacados = productos[:3]  # solo los primeros 3
    return render_template('index.html', productos_destacados=destacados)


# Página de todos los productos
@app.route('/productos')
def productos():
    productos = obtener_productos()
    return render_template('productos.html', productos=productos)


@app.route('/producto/<slug>')
def producto_detalle(slug):
    producto = obtener_producto_por_slug(slug)
    if not producto:
        return "Producto no encontrado", 404

    imagenes = producto['imagenes'].split(',') if producto['imagenes'] else []

    # Conectar y buscar talles + stock + en_carrito

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            s.talle,
            s.stock,
            COALESCE(c.cantidad, 0) AS en_carrito
        FROM stock_por_talle s
        LEFT JOIN carrito c 
          ON s.producto_id = c.producto_id AND s.talle = c.talle
        WHERE s.producto_id = ?
    ''', (producto['id'],))
    talles = cursor.fetchall()

    conn.close()

    return render_template('producto_detalle.html', producto=producto, imagenes=imagenes, talles=talles)


@app.route('/agregar_al_carrito/<slug>', methods=['POST'])
def agregar_al_carrito(slug):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Buscar producto por slug
    cursor.execute('SELECT id FROM productos WHERE slug = ?', (slug,))
    producto = cursor.fetchone()

    if producto:
        producto_id = producto['id']
        talle = request.form.get('talle')

        if not talle:
            conn.close()
            return "⚠️ Talle no seleccionado.", 400

        # Obtener cuántas unidades ya hay en el carrito
        cursor.execute('''
            SELECT cantidad FROM carrito
            WHERE producto_id = ? AND talle = ?
        ''', (producto_id, talle))
        en_carrito = cursor.fetchone()
        cantidad_en_carrito = en_carrito['cantidad'] if en_carrito else 0

        # Consultar el stock real
        cursor.execute('''
            SELECT stock FROM stock_por_talle
            WHERE producto_id = ? AND talle = ?
        ''', (producto_id, talle))
        stock_row = cursor.fetchone()
        stock_disponible = stock_row['stock'] if stock_row else 0

        # Verificar si hay stock suficiente
        if cantidad_en_carrito >= stock_disponible:
            conn.close()
            return "⚠️ Ya agregaste todas las unidades disponibles de ese talle.", 400

        # Si hay stock disponible, agregar al carrito
        if en_carrito:
            cursor.execute('''
                UPDATE carrito
                SET cantidad = cantidad + 1
                WHERE producto_id = ? AND talle = ?
            ''', (producto_id, talle))
        else:
            cursor.execute('''
                INSERT INTO carrito (producto_id, cantidad, talle)
                VALUES (?, ?, ?)
            ''', (producto_id, 1, talle))

        conn.commit()

    conn.close()
    return redirect(request.referrer + "?agregado=1&_={}".format(random.randint(1, 99999)))


@app.route('/carrito')
def ver_carrito():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            c.producto_id,
            c.talle,
            c.cantidad,
            p.nombre,
            p.precio,
            p.imagen,
            p.slug,
            s.stock
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        JOIN stock_por_talle s ON s.producto_id = c.producto_id AND s.talle = c.talle
    ''')
    productos = cursor.fetchall()

    total = sum(p['precio'] * p['cantidad'] for p in productos)

    conn.close()
    return render_template('carrito.html', productos=productos, total=total)


@app.route('/aumentar/<int:producto_id>/<path:talle>',methods=['POST'])
def aumentar(producto_id, talle):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Obtener cantidad actual en carrito
    cursor.execute('''
        SELECT cantidad FROM carrito
        WHERE producto_id = ? AND talle = ?
    ''', (producto_id, talle))
    carrito = cursor.fetchone()
    cantidad_en_carrito = carrito['cantidad'] if carrito else 0

    # Obtener stock total para ese talle
    cursor.execute('''
        SELECT stock FROM stock_por_talle
        WHERE producto_id = ? AND talle = ?
    ''', (producto_id, talle))
    stock = cursor.fetchone()
    stock_disponible = stock['stock'] if stock else 0

    # Solo aumentar si hay stock disponible
    if cantidad_en_carrito < stock_disponible:
        cursor.execute('''
            UPDATE carrito
            SET cantidad = cantidad + 1
            WHERE producto_id = ? AND talle = ?
        ''', (producto_id, talle))

    conn.commit()
    conn.close()
    return redirect(url_for('ver_carrito'))


# Disminuir cantidad
@app.route('/disminuir/<int:producto_id>/<path:talle>', methods=['POST'])
def disminuir(producto_id, talle):
    conn = sqlite3.connect(db_path)    
    cursor = conn.cursor()

    cursor.execute('SELECT cantidad FROM carrito WHERE producto_id = ? AND talle = ?', (producto_id, talle))
    cantidad = cursor.fetchone()[0]

    if cantidad > 1:
        cursor.execute('UPDATE carrito SET cantidad = cantidad - 1 WHERE producto_id = ? AND talle = ?', (producto_id, talle))
    else:
        cursor.execute('DELETE FROM carrito WHERE producto_id = ? AND talle = ?', (producto_id, talle))

    conn.commit()
    conn.close()
    return redirect(url_for('ver_carrito'))

# Eliminar producto directamente
@app.route('/eliminar/<int:producto_id>/<path:talle>', methods=['POST'])
def eliminar(producto_id, talle):
    conn = sqlite3.connect(db_path)    
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carrito WHERE producto_id = ? AND talle = ?', (producto_id, talle))
    conn.commit()
    conn.close()
    return redirect(url_for('ver_carrito'))

@app.route('/finalizar_compra')
def finalizar_compra():
    return "Gracias por tu compra. En breve recibirás tu pedido."

import mercadopago
from mercadopago_config import sdk

@app.route('/pagar', methods=['GET'])
def pagar():
    
    preference_data = {
        "items": [
            {
                "title": "Traje de Spider-Man",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": 64900.00
            }
        ],
        "back_urls": {
    "success": "https://www.google.com",  # después ponés tu sitio real
    "failure": "https://www.google.com",
    "pending": "https://www.google.com"
},

        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    import pprint
    pprint.pprint(preference_response)

    preference = preference_response["response"]
    init_point = preference.get("init_point")
    if not init_point:
        return "❌ Error: No se recibió un init_point. Verificá tu Access Token o configuración."

    return redirect(preference["init_point"])

@app.route('/webhook', methods=['POST'])
def webhook():
    import mercadopago
    import json
    from mercadopago_config import sdk

    data = request.get_json()
    if data and data.get("type") == "payment":
        payment_id = data.get("data", {}).get("id")

        # Consultamos el pago con la API de MP
        result = sdk.payment().get(payment_id)
        payment_info = result["response"]

        if payment_info.get("status") == "approved":
            print("✅ Pago aprobado")

            # Conectamos con la base y restamos stock
            conn = sqlite3.connect(db_path)            
            cursor = conn.cursor()

            cursor.execute("SELECT producto_id, talle, cantidad FROM carrito")
            items = cursor.fetchall()

            for producto_id, talle, cantidad in items:
                cursor.execute('''
                    UPDATE stock_por_talle
                    SET stock = stock - ?
                    WHERE producto_id = ? AND talle = ?
                ''', (cantidad, producto_id, talle))

            # Limpiar carrito (opcionall)
            cursor.execute("DELETE FROM carrito")

            conn.commit()
            conn.close()

    return '', 200

@app.route('/crear-tablas')
def crear_tablas():
    try:
        import init_db
        return "✅ Base de datos creada en Render"
    except Exception as e:
        return f"❌ Error: {e}"
        
@app.route('/forzar-crear-tablas')
def forzar_crear_tablas():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        descripcion TEXT,
        imagenes TEXT
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

    conn.commit()
    conn.close()
    return "Tablas creadas desde Render."

@app.route("/debug-productos")
def debug_productos():
    import sqlite3
    conn = sqlite3.connect('tienda.db')
    conn.row_factory = sqlite3.Row  # para que devuelva como diccionario
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    return { "productos": [dict(p) for p in productos] }

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
