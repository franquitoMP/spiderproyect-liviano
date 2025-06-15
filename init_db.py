from app import db, Producto, StockPorTalle

def cargar_datos():
    # 🔴 Eliminar productos anteriores
    Producto.query.delete()
    db.session.commit()

    # 🟢 Cargar nuevos productos
    productos = [
        Producto(
            slug="miles-morales",
            nombre="Traje Miles Morales",
            precio=45900,
            descripcion="Inspirado en Spider-Man: Into the Spider-Verse",
            imagen="miles3_.webp",
            imagenes="miles5_.webp,miles1_.webp,miles2_.webp,miles3_.webp,miles4_.webp,miles0_.webp,talles.webp"
        ),
        Producto(
            slug="traje-mejorado",
            nombre="Upgraded Suit",
            precio=64900,
            descripcion="Versión mejorada del traje clásico rojo y negro",
            imagen="mejorado0_.webp",
            imagenes="mejorado4_.webp,mejorado0_.webp,mejorado5_.webp,mejorado6_.webp,talles.webp"
        ),
        Producto(
            slug="electro",
            nombre="Traje Gold and Black",
            precio=64900,
            descripcion="Traje con detalles dorados, basado en No Way Home",
            imagen="electro0_.webp",
            imagenes="electro0_.webp,electro1_.webp,electro3_.webp,electro4_.webp,talles.webp"
        ),
        Producto(
            slug="spiderman-ps4",
            nombre="Traje Spider-Man PS4",
            precio=64900,
            descripcion="Traje del juego de PS4 con el logo blanco",
            imagen="ps41_.webp",
            imagenes="ps40_.webp,ps41_.webp,talles.webp"
        ),
        Producto(
            slug="traje-clasico",
            nombre="Traje Clásico",
            precio=64900,
            descripcion="El traje tradicional rojo y azul",
            imagen="clasico9.webp",
            imagenes="clasico3.webp,clasico9.webp,clasico4.webp,clasico5.webp,talles.webp"
        ),
        Producto(
            slug="iron-spider",
            nombre="Traje Iron Spider",
            precio=64900,
            descripcion="Basado en Avengers: Infinity War",
            imagen="iron-spider0_.webp",
            imagenes="iron-spider3_.webp,iron-spider1_.webp,iron-spider2_.webp,iron-spider0_.webp,iron-spider4_.webp,talles.webp"
        ),
    ]

    db.session.add_all(productos)
    db.session.commit()

    # 🔍 Obtener IDs reales desde la base
    productos_map = {p.slug: p.id for p in Producto.query.all()}

    stock = [
        StockPorTalle(producto_id=productos_map['miles-morales'], talle='120', stock=1),
        StockPorTalle(producto_id=productos_map['miles-morales'], talle='130', stock=1),
        StockPorTalle(producto_id=productos_map['miles-morales'], talle='170', stock=1),
        StockPorTalle(producto_id=productos_map['traje-mejorado'], talle='100', stock=1),
        StockPorTalle(producto_id=productos_map['traje-mejorado'], talle='120', stock=1),
        StockPorTalle(producto_id=productos_map['traje-mejorado'], talle='130', stock=1),
        StockPorTalle(producto_id=productos_map['traje-mejorado'], talle='180', stock=1),
        StockPorTalle(producto_id=productos_map['electro'], talle='150', stock=1),
        StockPorTalle(producto_id=productos_map['spiderman-ps4'], talle='120', stock=1),
        StockPorTalle(producto_id=productos_map['traje-clasico'], talle='110', stock=1),
        StockPorTalle(producto_id=productos_map['traje-clasico'], talle='130', stock=1),
        StockPorTalle(producto_id=productos_map['iron-spider'], talle='140', stock=1),
    ]

    db.session.add_all(stock)
    db.session.commit()
    print("✅ Productos y stock cargados correctamente!")

if __name__ == '__main__':
    from app import app

    with app.app_context():
        cargar_datos()
