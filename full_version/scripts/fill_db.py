import __init__

from sqlalchemy.exc import IntegrityError

from bot.models import Product, DiscountCode
from bot.database import Session

products = [
    (1, "Chocolate", 3, 10.5),
    (2, "Granizado", 10, 8),
    (3, "Limón", 0, 13.5),
    (4, "Dulce de Leche", 5, 15.2),
]

discount_codes = [
    (1, "Primavera2021", 0.10),
    (2, "Verano2021", 0.25),
    (3, "Navidad2x1", 0.15),
    (4, "heladoFrozen", 0.20),
]

try:
    with Session() as db:
        for pk, name, quantity, price in products:
            product = Product(id=pk, name=name, quantity=quantity, price=price)
            db.add(product)
        
        for pk, label, value in discount_codes:
            code = DiscountCode(id=pk, label=label, value=value)
            db.add(code)
        
        db.commit()
except IntegrityError as e:
    print(f" [!] Error al cargar los datos: {e}")