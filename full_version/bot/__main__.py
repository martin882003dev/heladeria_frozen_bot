import logging

from bot.database import engine
from bot.ui import Printer
from bot.config import settings
from bot.exceptions import (
    GeolocateException, 
    WeatherException, 
    MaxAttemptsExceededException
)
from bot.models import Base, Product
from bot.auxiliar import Worker
from bot.weather import get_temperature
from bot.utils import max_attempts

from bot import schemas

logging.basicConfig(
    filename=settings.logging.filename,
    format=settings.logging.format
)

Base.metadata.create_all(bind=engine)


class Bot:
    def __init__(self):
        self._worker = Worker()
        self._printer = Printer()
    
    def start(self):
        if settings.ui.welcome:
            self._say_hi()
        
        self._make_sale()
        
        self._say_bye("¡Esperamos verlo pronto!")
            
    
    def _say_hi(self) -> None:
        message = [f"[b]Bienvenido a [u]{settings.app_name}[/u] :)[/b]"]
        temperature = get_temperature(qualitative=True)
        message.append(settings.ui.welcome[temperature])
        message.append("Presione cualquier tecla para continuar...")
        self._printer.multiline(
            message,
            padding=(1,),
            freeze=True,
            justify="center"
        )
    
    def _say_bye(self, message: str) -> None:
        self._printer.exit(message, schemas.ExitStatus.ok)
    
    @max_attempts(display_warning=False)
    def _make_sale(self) -> bool | None:
        finished = None
        while self._still_ordering:
            if self._stock_shortage:
                self._notify_stock_shortage()
                break
            self._take_order()
        
        if self._empty_cart:
            finished = True
        
        payment_received = self._take_payment()
        
        if payment_received:
            self._worker.deliver_products()
            finished = True
        return finished
    
    @property
    @max_attempts()
    def _still_ordering(self) -> bool:
        if self._empty_cart:
            return True
        return self._printer.confirm(
            f"¿Desea llevar algún {settings.product_type['singular']} más?"
        )
    
    @property
    def _stock_shortage(self) -> bool:
        return not self._worker.check_stock()

    def _notify_stock_shortage(self) -> None:
        product_type = settings.product_type["plural"]
        self._printer.oneline(
            f"Lo sentimos, no tenemos más {product_type} disponibles",
            justify="center"
        )
    
    @property
    def _empty_cart(self) -> bool:
        return not self._worker.check_cart()

    def _take_order(self) -> None:
        available_products = self._worker.get_available_products()
        self._printer.show_products(available_products)
        
        selected_product = self._select_product(available_products)
        selected_quantity = self._select_quantity(selected_product)
        
        self._worker.add_to_cart(selected_product, selected_quantity)
    
    @max_attempts()
    def _select_product(self, products: list[Product]) -> Product | None:
        message = f"¿Qué {settings.product_type['singular']} quiere llevar?"
        choice = self._printer.get_answer(message, expected_type=int)
        if choice:
            product = self._identify_product(products, choice)
            return product
    
    def _identify_product(
        self, 
        products: list[Product], 
        choice: int
    ) -> Product | None:
        product = None
        try:
            product = products[choice - 1]
        except IndexError:
            pass
        return product
    
    @max_attempts()
    def _select_quantity(self, product: Product) -> int | None:
        message = "¿Cuántas unidades?"
        choice = self._printer.get_answer(message, expected_type=int)
        if choice:
            if 0 < choice <= product.quantity:
                return choice 
            
    def _take_payment(self) -> bool:
        cart_products = self._worker.get_cart_products()
        amount = self._worker.calculate_amount()
        
        self._printer.show_bill(cart_products, amount)
        
        if self._has_discount_code:
            code = self._get_discount_code()
            amount = self._apply_discount(amount, code)
            self._printer.show_bill(cart_products, amount, discount=True)
        
        return self._confirm_sale            
    
    @property
    @max_attempts()
    def _has_discount_code(self) -> bool:
        return self._printer.confirm("¿Tiene código de descuento?")
    
    @max_attempts()
    def _get_discount_code(self) -> schemas.DiscountCode:
        codes = self._worker.get_discount_codes()
        client_code = self._printer.get_answer(
            "Ingrese el código de descuento", expected_type=str)
        for code in codes:
            difference = set(client_code).symmetric_difference(code.label)
            if len(difference) < 3:
                return code
    
    def _apply_discount(self, amount, code: schemas.DiscountCode) -> float:
        return amount * (1 - code.value)
    
    @property
    @max_attempts()
    def _confirm_sale(self) -> bool:
        return self._printer.confirm("¿Desea confirmar la compra?")
        


def run():
    try:
        bot = Bot()
        bot.start()
    
    except (ValueError, GeolocateException, WeatherException) as e:
        logging.error(f"{e}")
        Printer.exit(
            "Error al iniciar la aplicación (revise el log para más información)",
            schemas.ExitStatus.error
        )
    
    except MaxAttemptsExceededException:
        Printer.exit(
            "Ha excedido el número máximo de intentos",
            schemas.ExitStatus.error
        )
    
    except KeyboardInterrupt:
        Printer.exit(
            "Ejecución interrumpida por el usuario",
            schemas.ExitStatus.warning
        )
