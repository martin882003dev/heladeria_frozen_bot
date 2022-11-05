from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table

from bot.config import settings
from bot import models
from bot import schemas

class Printer:
    _console = Console()
    
    def __init__(self):
        self.clear()
    
    def _header(self):
        if not settings.ui.header:
            return
        self._console.print(
            Padding(settings.ui.title, (2, 4)),
            style="bold white on blue", 
            justify="center"
        )
        self._console.print(Padding("", 2))
    
    @classmethod
    def exit(self, message: str, status: schemas.ExitStatus) -> None:
        content = Padding(message, 1, style=f"bold white on {status.value}")
        container = Padding(content, 2)
        self._console.print(container, justify="center")
    
    @classmethod
    def error(self, message: str) -> None:
        message = Panel(
            Align(                
                Padding(
                    Text(message, justify="center"),
                    3, 
                    style="bold white on red"
                ),
                align="center",
                vertical="middle"
            ),
            title="ERROR", 
            subtitle="Presione una tecla para continuar...")
        
        layout = grid()
        layout["middle"]["center"].update(message)
        
        with self._console.screen():
            self._console.print(layout)
            input()
    
    def clear(self, header=True):
        self._console.clear()
        if header:
            self._header()
    
    def get_answer(self, message: str, expected_type: type) -> type | None:
        answer = Prompt.ask(f"[b]{message}[/b]")
        try:
            answer = expected_type(answer)
        except ValueError:
            answer = None
        finally:
            return answer
    
    def confirm(self, message: str) -> bool:
        message += " [yellow bold](s/n)[/yellow bold]"
        answer = Prompt.ask(message)
        match answer.lower():
            case "s":
                return True
            case "n":
                return False
            case _:
                return None
    
    def oneline(
        self, 
        content: str,
        padding: tuple | None = None,
        clear: bool = False,
        header: bool = True,
        freeze: bool = False,
        *args,
        **kwargs
    ) -> None:
        if clear: 
            self.clear(header)
        if padding:
            content = Padding(content, padding)
        self._console.print(content, *args, **kwargs)
        if freeze:
            input()
            self.clear()
    
    def multiline(
        self, 
        content: list[str], 
        padding: tuple | None = None,
        clear: bool = False,
        header: bool = True,
        freeze: bool = False,
        *args,
        **kwargs
    ) -> None:
        if clear:
            self.clear(header)
        for line in content:
            self.oneline(line, padding, *args, **kwargs)    
        if freeze:
            input()
            self.clear()
    
    def show_products(self, products: models.Product) -> None:
        table = Table(
            title=f"[b]{settings.product_type['plural'].upper()} DISPONIBLES[/b]", 
            expand=True
        )
        
        prod_type = settings.product_type["singular"].capitalize()
        for column in ("#", prod_type, "Stock", "Precio"):
            table.add_column(column, justify="center")
        
        for i, product in enumerate(products, start=1):
            table.add_row(
                str(i),
                product.name,
                str(product.quantity),
                str(product.price)
            )
        self.oneline(table, (0, 0, 2, 0), clear=True)
    
    def show_bill(
        self,
        products: list[schemas.Product],
        amount: float,
        discount: float | None = None,
    ) -> None:
        self._show_bill_details(products)
        self._show_amount(amount, discount)
    
    def _show_bill_details(self, products: list[schemas.Product]) -> None:
        table = Table(
            title=f"[b]RESUMEN DE COMPRA[/b]", 
            expand=True
        )
        
        prod_type = settings.product_type["singular"].capitalize()
        for column in (prod_type, "Cantidad", "Precio", "Subtotal"):
            table.add_column(column, justify="center")
        
        for product in products:
            partial_amount = round(product.price * product.quantity, 1)
            table.add_row(
                product.name,
                f"{product.quantity}",
                f"{product.price}",
                f"{partial_amount}"
            )
        self.oneline(table, clear=True)
    
    def _show_amount(self, amount: float, discount: float | None = None) -> None:
        table = Table(show_header=False, expand=True)
        table.add_column('amount', justify="center")
        
        amount = (amount * discount) if discount else amount
        discount_message = "con" if discount else "sin"
        message = f"💸Total: ${amount} ({discount_message} descuento)💸"
        
        table.add_row(message)
        self.oneline(table, (2, 0, 2, 0))
            
        
        
            
    
def grid() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(" ", name="top"),
        Layout(" ", name="middle"),
        Layout(" ", name="bottom")
    )
    layout["middle"].split_row(
        Layout(" ", name="left"),
        Layout(" ", name="center"),
        Layout(" ", name="right")
    )
    return layout
        