import __init__

from bot.database import Session
from bot.models import DiscountCode, Product

with Session() as db:
    db.query(Product).delete()
    db.query(DiscountCode).delete()
    db.commit()