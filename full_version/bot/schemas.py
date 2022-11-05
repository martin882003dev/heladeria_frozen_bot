from enum import Enum
from pydantic import BaseModel


class Temperature(str, Enum):
    celsius = "metric"
    fahrenheit = "imperial"
    kelvin = "standard"

class ExitStatus(Enum):
    ok = "green"
    error = "red"
    warning = "cyan"


class Location(BaseModel):
    name: str
    state: str
    country: str
    lat: float
    lon: float

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

class DiscountCode(BaseModel):
    label: str
    value: float