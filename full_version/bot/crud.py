from bot.database import Session
from bot import models
from bot import schemas

def get_products(available: bool = False) -> list:
    with Session() as session:
        products = session.query(models.Product)
        if available:
            products = products.filter(models.Product.quantity > 0)
        return products.all()


def get_discount_codes() -> list:
    with Session() as session:
        return session.query(models.DiscountCode).all()

def update_stock(products: schemas.Product) -> None:
    with Session() as session:
        for product in products:
            session.query(models.Product) \
                .filter(models.Product.id == product.id) \
                .update({
                    "quantity": models.Product.quantity - product.quantity
                })
        session.commit()