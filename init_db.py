from app import db, Producto, StockPorTalle

def cargar_datos():
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
            slug="upgraded-suit",
            nombre="Upgraded Suit",
            precio=64900,
            descripcion="Versión mejorada del traje clásico rojo y negro",
            imagen="upgraded1.jpg",
            imagenes="upgraded1.jpg,upgraded2.jpg"
        ),
        Producto(
            slug="gold-black",
            nombre="Traje Gold and Black",
            precio=64900,
            descripcion="Traje con detalles dorados, basado en No Way Home",
            imagen="gold1.jpg",
            imagenes="gold1.jpg"
        ),
        Producto(
            slug="ps4-advanced",
            nombre="Traje Spider-Man PS4",
            precio=64900,
            descripcion="Traje del juego de PS4 con el logo blanco",
            imagen="ps4.jpg",
            imagenes="ps4.jpg"
        ),
        Producto(
            slug="classic-suit",
            nombre="Traje Clásico",
            precio=64900,
            descripcion="El traje tradicional rojo y azul",
            imagen="classic.jpg",
            imagenes="classic.jpg"
        ),
        Producto(
            slug="iron-spider",
            nombre="Traje Iron Spider",
            precio=64900,
            descripcion="Basado en Avengers: Infinity War",
            imagen="iron.jpg",
            imagenes="iron.jpg"
        ),
    ]

    db.session.add_all(productos)
    db.session.commit()

    # Asignar stock por talle (ejemplos reales)
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
