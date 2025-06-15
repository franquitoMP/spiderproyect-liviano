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
            precio=47900,
            descripcion="Traje de SpiderMan de Miles Morales con diseño negro y rojo intenso inspirado en el estilo urbano y moderno de las peliculas animadas SpiderVerse. Incluye araña roja en el pecho patrones de telaraña estilizados y esta confeccionado en lycra elastica de alta calidad con estampado digital y cierre invisible Ideal para quienes buscan un look original juvenil y diferente dentro del universo SpiderMan. Ideal para fiestas Halloween cosplay o simplemente jugar como un heroe Estado Nuevo sin uso en excelente estado Entrega inmediata Guia de talles en fotos. IMPORTANTE Este producto no es oficial ni licenciado por Marvel. Es un disfraz inspirado de excelente calidad y muy comodo",
            imagen="miles1_.webp",
            imagenes="miles5_.webp,miles1_.webp,miles2_.webp,miles3_.webp,miles4_.webp,miles0_.webp,talles.webp"
        ),
        Producto(
            slug="traje-mejorado",
            nombre="Traje Spider-man: Lejos De Casa",
            precio=49000,
            descripcion="Traje inspirado en SpiderMan ideal para jugar disfrazarse o eventos tematicos. Modelo Traje Mejorado Spiderman Lejos de casa. Completo mascara Material Lycra elastica sublimada Ideal para fiestas Halloween cosplay o simplemente jugar como un heroe. Estado Nuevo sin uso en excelente estado Entrega inmediata Guia de talles en fotos. IMPORTANTE Este producto no es oficial ni licenciado por Marvel Es un disfraz inspirado de excelente calidad y muy comodo",
            imagen="mejorado0_.webp",
            imagenes="mejorado4_.webp,mejorado0_.webp,mejorado5_.webp,mejorado6_.webp,talles.webp"
        ),
        Producto(
            slug="electro",
            nombre="Traje Gold and Black",
            precio=57900,
            descripcion="Traje inspirado en SpiderMan ideal para jugar disfrazarse o eventos tematicos. Modelo Traje negro y dorado Spiderman importado. Completo mascara Material Lycra elastica sublimada Ideal para fiestas Halloween cosplay o simplemente jugar como un heroe. Estado Nuevo sin uso en excelente estado. Entrega inmediata Guia de talles en fotos. IMPORTANTE Este producto no es oficial ni licenciado por Marvel Es un disfraz inspirado de excelente calidad y muy comodo",
            imagen="electro0_.webp",
            imagenes="electro0_.webp,electro1_.webp,electro3_.webp,electro4_.webp,talles.webp"
        ),
        Producto(
            slug="spiderman-ps4",
            nombre="Traje Spider-Man PS4",
            precio=57900,
            descripcion="Traje inspirado en SpiderMan ideal para jugar disfrazarse o eventos tematicos. Modelo Traje PS4 Spiderman importado. Completo mascara Material Lycra elastica sublimada Ideal para fiestas Halloween cosplay o simplemente jugar como un heroe. Estado Nuevo sin uso en excelente estado. Entrega inmediata. Guia de talles en fotos. IMPORTANTE Este producto no es oficial ni licenciado por Marvel Es un disfraz inspirado de excelente calidad y muy comodo",
            imagen="ps41_.webp",
            imagenes="ps40_.webp,ps41_.webp,talles.webp"
        ),
        Producto(
            slug="traje-clasico",
            nombre="Traje Clásico",
            precio=57900,
            descripcion="Traje inspirado en SpiderMan ideal para jugar disfrazarse o eventos tematicos. Modelo Traje Clasico Spiderman Lejos de casa. Completo mascara Material Lycra elastica sublimada Ideal para fiestas Halloween cosplay o simplemente jugar como un heroe. Estado Nuevo sin uso en excelente estado. Entrega inmediata Guia de talles en fotos IMPORTANTE. Este producto no es oficial ni licenciado por Marvel. Es un disfraz inspirado de excelente calidad y muy comodo",
            imagen="clasico9.webp",
            imagenes="clasico3.webp,clasico9.webp,clasico4.webp,clasico5.webp,talles.webp"
        ),
        Producto(
            slug="iron-spider",
            nombre="Traje Iron Spider",
            precio=57900,
            descripcion="Traje inspirado en SpiderMan ideal para jugar disfrazarse o eventos tematicos. Modelo Traje Iron Spider. Completo mascara Material Lycra elastica sublimada Ideal para fiestas Halloween cosplay o simplemente jugar como un heroe. Estado Nuevo sin uso en excelente estado. Entrega inmediata Guia de talles en fotos IMPORTANTE. Este producto no es oficial ni licenciado por Marvel. Es un disfraz inspirado de excelente calidad y muy comodo",
            imagen="iron-spider0_.webp",
            imagenes="iron-spider3_.webp,iron-spider1_.webp,iron-spider2_.webp,iron-spider0_.webp,iron-spider4_.webp,talles.webp"
        ),
    ]

    db.session.add_all(productos)
    db.session.commit()

    # 🔍 Obtener IDs reales desde la base
    productos_map = {p.slug: p.id for p in Producto.query.all()}

    stock = [
        StockPorTalle(producto_id=productos_map['miles-morales'], talle='120', stock=0),
        StockPorTalle(producto_id=productos_map['miles-morales'], talle='130', stock=1),
        StockPorTalle(producto_id=productos_map['miles-morales'], talle='170', stock=2),
        StockPorTalle(producto_id=productos_map['traje-mejorado'], talle='100', stock=0),
        StockPorTalle(producto_id=productos_map['traje-mejorado'], talle='120', stock=1),
        StockPorTalle(producto_id=productos_map['traje-mejorado'], talle='130', stock=2),
        StockPorTalle(producto_id=productos_map['traje-mejorado'], talle='180', stock=2),
        StockPorTalle(producto_id=productos_map['electro'], talle='120', stock=1),
        StockPorTalle(producto_id=productos_map['spiderman-ps4'], talle='120', stock=0),
        StockPorTalle(producto_id=productos_map['traje-clasico'], talle='110', stock=0),
        StockPorTalle(producto_id=productos_map['traje-clasico'], talle='130', stock=0),
        StockPorTalle(producto_id=productos_map['iron-spider'], talle='140', stock=0),
    ]

    db.session.add_all(stock)
    db.session.commit()
    print("✅ Productos y stock cargados correctamente!")

if __name__ == '__main__':
    from app import app

    with app.app_context():
        cargar_datos()
