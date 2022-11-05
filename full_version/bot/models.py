from sqlalchemy import (
    Column, String, Integer, Float
)
from sqlalchemy.orm import validates

from bot.database import Base


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    @validates("quantity", "cost")
    def non_negative_values(self, _, value):
        if value < 0:
            raise ValueError("cost or quantity cannot be negative")
        return value


class DiscountCode(Base):
    __tablename__ = 'discount_codes'
    
    id = Column(Integer, primary_key=True)
    label = Column(String, unique=True, nullable=False)
    value = Column(Float, nullable=False)
    
    @validates("value")
    def valid_range(self, _, value):
        if not (0 <= value <= 1):
            raise ValueError("discount value must be between 0 and 1")
        return value