from bot import crud
from bot import models
from bot import schemas

class Worker:
    def __init__(self):
        self._inventory = Inventory()
        self._cart = Cart()

    def check_stock(self) -> bool:
        return bool(self._inventory.available_products)

    def check_cart(self) -> bool:
        return bool(self._cart.products)
    
    def get_available_products(self) -> list[models.Product]:
        return self._inventory.available_products
    
    def add_to_cart(self, product: models.Product, quantity: int) -> None:
        self._inventory.pick(product, quantity)
        self._cart.add(product, quantity)
    
    def get_cart_products(self) -> list[schemas.Product]:
        return self._cart.products
    
    def calculate_amount(self) -> float:
        amount = 0
        for product in self._cart.products:
            amount += (product.price * product.quantity)
        return amount

    def get_discount_codes(self) -> list[schemas.DiscountCode]:
        codes = crud.get_discount_codes()
        return [
            schemas.DiscountCode(
                id = code.id,
                label = code.label,
                value = code.value,
            ) for code in codes
        ]
    
    def deliver_products(self) -> None:
        crud.update_stock(self._cart.products)


class Inventory:
    def __init__(self):
        self._products = crud.get_products(available=True)
    
    @property
    def all_products(self) -> list[models.Product]:
        return self._products
    
    @property
    def available_products(self) -> list[models.Product]:
        return [product for product in self._products if product.quantity]
        
    def pick(self, product: models.Product, quantity: int) -> None:
        if product not in self._products:
            raise ValueError("Producto inexistente")
        if product.quantity < quantity:
            raise ValueError("Stock insuficiente")
        
        index = self._products.index(product)
        self._products[index].quantity -= quantity
    
    def get_product_price(self, product_id: int) -> float:
        for product in self._products:
            if product.id == product_id:
                return product.price


class Cart:
    def __init__(self):
        self._products = {}
    
    @property
    def empty(self) -> bool:
        return bool(self.products)

    @property
    def products(self) -> list[schemas.Product]:
        return self._products.values()

    
    def add(self, product: models.Product, quantity: int) -> None:
        product = schemas.Product(
            id=product.id,
            name=product.name,
            price=product.price,
            quantity=quantity,
        )
        if cart_products := self._products.get(product.id, None):
            product.quantity += cart_products.quantity
        self._products[product.id] = product