from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import random
import os
from mercadopago_config import sdk

app = Flask(__name__)

# 🔗 Conexión a PostgreSQL (copiá tu string real acá)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tienda_user:postgresql://tienda_user:y7nmCICXWeXhWsXRMEZ8I0vcxHxabA38@dpg-d0uecce3jp1c73fu16rg-a/tienda_rbjg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 🧾 Tabla ordenes
class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    email = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    calle = db.Column(db.String(150))
    numero = db.Column(db.String(20))
    depto = db.Column(db.String(50))
    barrio = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(20))
    provincia = db.Column(db.String(100))
    dni = db.Column(db.String(20))
    producto_id = db.Column(db.Integer)
    talle = db.Column(db.String(20))
    cantidad = db.Column(db.Integer)
    total = db.Column(db.Float)
    estado = db.Column(db.String(50), default="pendiente")
    fecha = db.Column(db.DateTime, server_default=db.func.now())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crear-tablas')
def crear_tablas():
    try:
        db.create_all()
        return "✅ Tablas creadas en PostgreSQL"
    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/pagar', methods=['GET'])
def pagar():
    preference_data = {
        "items": [{
            "title": "Traje de Spider-Man",
            "quantity": 1,
            "currency_id": "ARS",
            "unit_price": 64900.00
        }],
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
        return "❌ Error: No se recibió un init_point."

    return redirect(init_point)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and data.get("type") == "payment":
        payment_id = data.get("data", {}).get("id")
        result = sdk.payment().get(payment_id)
        payment_info = result["response"]

        if payment_info.get("status") == "approved":
            print("✅ Pago aprobado")
            # Acá pondremos la lógica de stock en PostgreSQL más adelante

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
