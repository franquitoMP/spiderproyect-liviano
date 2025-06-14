from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from mercadopago_config import sdk
from dotenv import load_dotenv
import os
import random

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELOS
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(255))
    imagenes = db.Column(db.Text)

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    talle = db.Column(db.String(20), nullable=False)

class StockPorTalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    talle = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# RUTAS PRINCIPALES
@app.route('/')
def home():
    productos = Producto.query.limit(3).all()
    return render_template('index.html', productos_destacados=productos)

@app.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

from sqlalchemy import func

@app.route('/producto/<slug>')
def producto_detalle(slug):
    producto = Producto.query.filter_by(slug=slug).first()
    if not producto:
        return "Producto no encontrado", 404

    imagenes = producto.imagenes.split(',') if producto.imagenes else []

    raw_talles = (
        db.session.query(
            StockPorTalle.talle,
            StockPorTalle.stock,
            func.coalesce(func.sum(Carrito.cantidad), 0).label("en_carrito")
        )
        .outerjoin(Carrito, (StockPorTalle.producto_id == Carrito.producto_id) & (StockPorTalle.talle == Carrito.talle))
        .filter(StockPorTalle.producto_id == producto.id)
        .group_by(StockPorTalle.talle, StockPorTalle.stock)
        .all()
    )

    talles = [
        {'talle': t[0], 'stock': t[1], 'en_carrito': t[2]}
        for t in raw_talles
    ]

    return render_template('producto_detalle.html', producto=producto, imagenes=imagenes, talles=talles)


@app.route('/agregar_al_carrito/<slug>', methods=['POST'])
def agregar_al_carrito(slug):
    producto = Producto.query.filter_by(slug=slug).first()
    if not producto:
        return "❌ Producto no encontrado.", 404

    talle = request.form.get('talle')
    if not talle:
        return "⚠️ Talle no seleccionado.", 400

    item_carrito = Carrito.query.filter_by(producto_id=producto.id, talle=talle).first()
    stock = StockPorTalle.query.filter_by(producto_id=producto.id, talle=talle).first()

    if not stock or (item_carrito and item_carrito.cantidad >= stock.stock):
        return "⚠️ Ya agregaste todas las unidades disponibles de ese talle.", 400

    if item_carrito:
        item_carrito.cantidad += 1
    else:
        nuevo = Carrito(producto_id=producto.id, talle=talle, cantidad=1)
        db.session.add(nuevo)

    db.session.commit()
    return redirect(request.referrer + "?agregado=1&_={}".format(random.randint(1, 99999)))

@app.route('/carrito')
def ver_carrito():
    productos = db.session.query(
        Carrito.producto_id,
        Carrito.talle,
        Carrito.cantidad,
        Producto.nombre,
        Producto.precio,
        Producto.imagen.label('imagen'),
        Producto.slug,
        StockPorTalle.stock
    ).join(Producto, Carrito.producto_id == Producto.id) \
     .join(StockPorTalle, (StockPorTalle.producto_id == Carrito.producto_id) & (StockPorTalle.talle == Carrito.talle)) \
     .all()

    total = sum(p.precio * p.cantidad for p in productos)
    return render_template('carrito.html', productos=productos, total=total)

@app.route('/aumentar/<int:producto_id>/<path:talle>', methods=['POST'])
def aumentar(producto_id, talle):
    item = Carrito.query.filter_by(producto_id=producto_id, talle=talle).first()
    stock = StockPorTalle.query.filter_by(producto_id=producto_id, talle=talle).first()

    if item and stock and item.cantidad < stock.stock:
        item.cantidad += 1
        db.session.commit()

    return redirect(url_for('ver_carrito'))

@app.route('/disminuir/<int:producto_id>/<path:talle>', methods=['POST'])
def disminuir(producto_id, talle):
    item = Carrito.query.filter_by(producto_id=producto_id, talle=talle).first()
    if item:
        if item.cantidad > 1:
            item.cantidad -= 1
        else:
            db.session.delete(item)
        db.session.commit()
    return redirect(url_for('ver_carrito'))

@app.route('/eliminar/<int:producto_id>/<path:talle>', methods=['POST'])
def eliminar(producto_id, talle):
    item = Carrito.query.filter_by(producto_id=producto_id, talle=talle).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('ver_carrito'))

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
            "success": "https://www.google.com",
            "failure": "https://www.google.com",
            "pending": "https://www.google.com"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    init_point = preference.get("init_point")

    if not init_point:
        return "❌ Error: No se recibió un init_point. Verificá tu Access Token o configuración."

    return redirect(init_point)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and data.get("type") == "payment":
        payment_id = data.get("data", {}).get("id")
        result = sdk.payment().get(payment_id)
        payment_info = result["response"]

        if payment_info.get("status") == "approved":
            items = Carrito.query.all()
            for item in items:
                stock = StockPorTalle.query.filter_by(producto_id=item.producto_id, talle=item.talle).first()
                if stock:
                    stock.stock -= item.cantidad
                db.session.delete(item)
            db.session.commit()
    return '', 200

@app.route('/crear-tablas')
def crear_tablas():
    try:
        db.create_all()
        return "✅ Tablas creadas en PostgreSQL"
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
