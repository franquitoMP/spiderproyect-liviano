from app import db, Producto, StockPorTalle

def cargar_datos():
    # 🔴 1. Borrar productos viejos antes de cargar nuevos
    Producto.query.delete()
    db.session.commit()

    # 🟢 2. Cargar nuevos productos
    productos = [
        Producto(
            slug="miles-morales",
            nombre="Traje Miles Morales",
            precio=45900,
            descripcion="Inspirado en Spider-Man: Into the Spider-Verse",
            imagen="miles0_.webp",
            imagenes="miles0_.webp,miles1_.webp,miles1_.webp,miles2_.webp,miles3_.webp,miles4_.webp,miles5_.webp,talles.webp"
        ),
        Producto(
            slug="traje-mejorado",
            nombre="Upgraded Suit",
            precio=64900,
            descripcion="Versión mejorada del traje clásico rojo y negro",
            imagen="mejorado0_.webp",
            imagenes="mejorado0_.webp,mejorado4_.webp,mejorado5_.webp,mejorado6_.webp,talles.webp"
        ),
        Producto(
            slug="electro",
            nombre="Traje Gold and Black",
            precio=64900,
            descripcion="Traje con detalles dorados, basado en No Way Home",
            imagen="electro0_.webp",
            imagenes="electro0_.webp,electro1_.webp,electro2_.webp,electro3_.webp,electro4_.webp,electro5_.webp,talles.webp"
        ),
        Producto(
            slug="spiderman-ps4",
            nombre="Traje Spider-Man PS4",
            precio=64900,
            descripcion="Traje del juego de PS4 con el logo blanco",
            imagen="ps40_.webp",
            imagenes="ps40_.webp,ps41_.webp,talles.webp"
        ),
        Producto(
            slug="traje-clasico",
            nombre="Traje Clásico",
            precio=64900,
            descripcion="El traje tradicional rojo y azul",
            imagen="clasico0.webp",
            imagenes="clasico0.webp,clasico1.webp,clasico2.webp,clasico3.webp,clasico4.webp,clasico5.webp,clasico9.webp,talles.webp"
        ),
        Producto(
            slug="iron-spider",
            nombre="Traje Iron Spider",
            precio=64900,
            descripcion="Basado en Avengers: Infinity War",
            imagen="iron-spider0_.webp",
            imagenes="iron-spider0_.webp,iron-spider1_.webp,iron-spider2_.webp,iron-spider3_.webp,iron-spider4_.webp,talles.webp"
        ),
    ]

    db.session.add_all(productos)
    db.session.commit()

    # Asignar stock por talle
    stock = [
        StockPorTalle(producto_id=1, talle='120', stock=1),
        StockPorTalle(producto_id=1, talle='130', stock=1),
        StockPorTalle(producto_id=1, talle='170', stock=1),
        StockPorTalle(producto_id=2, talle='100', stock=1),
        StockPorTalle(producto_id=2, talle='120', stock=1),
        StockPorTalle(producto_id=2, talle='130', stock=1),
        StockPorTalle(producto_id=2, talle='180', stock=1),
        StockPorTalle(producto_id=3, talle='150', stock=1),
        StockPorTalle(producto_id=4, talle='120', stock=1),
        StockPorTalle(producto_id=5, talle='110', stock=1),
        StockPorTalle(producto_id=5, talle='130', stock=1),
        StockPorTalle(producto_id=6, talle='140', stock=1),
    ]

    db.session.add_all(stock)
    db.session.commit()
    print("✅ Productos y stock cargados correctamente")

if __name__ == '__main__':
    from app import app  # 👈 esto importa tu instancia de Flask

    with app.app_context():
        cargar_datos()

