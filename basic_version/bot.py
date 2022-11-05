import pandas as pd
import requests


class GeoAPI:
    API_KEY: str = "d81015613923e3e435231f2740d5610b"
    LAT: float = -35.836948753554054
    LON: float = -61.870523905384076
    UNITS: str = "metric"
    URL: str = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units={UNITS}"

    @classmethod
    def is_hot_in_pehuajo(cls) -> bool:
        try:
            response = requests.get(cls.URL)
            response.raise_for_status()
            content = response.json()
            temperature = float(content["main"]["temp"])
        except requests.exceptions.RequestException:
            return False
        else:
            return True if temperature > 28 else False


_PRODUCT_DF = pd.DataFrame({
    "product_name": ["Chocolate", "Granizado", "Limon", "Dulce de Leche"],
    "quantity": [3, 10, 0, 5]
})


def is_product_available(
    product_name: str,
    quantity: int,
    attemps: int,
    allowed_attemps: int = 3
) -> bool:
    if attemps > allowed_attemps:
        exit()  # an exception could be raised here as well
    product = _PRODUCT_DF[_PRODUCT_DF["product_name"] == product_name]
    product_stock = product.quantity.values[0]
    return product_stock >= quantity


_AVAILABLE_DISCOUNT_CODES = [
    "Primavera2021", "Verano2021", "Navidad2x1", "heladoFrozen"
]

def validate_discount_code(discount_code: str) -> bool:
    for code in _AVAILABLE_DISCOUNT_CODES:
        difference = set(code).symmetric_difference(discount_code)
        if len(difference) < 3:
            return True
    return False
