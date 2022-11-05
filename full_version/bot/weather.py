import requests

from bot.config import settings
from bot.exceptions import GeolocateException, WeatherException
from bot.schemas import Location


def geolocate(
    location: str, 
    state: str = "Buenos Aires", 
    country: str = "AR"
) -> Location:
    url = settings.weather.urls["geolocation"]
    try:
        response = requests.get(
            url,
            params={
                "q": ",".join([location, state, country]),
                "appid": settings.weather.api_key
            },
            timeout=settings.weather.timeout
        )
    except requests.exceptions.RequestException:
        raise GeolocateException("Error al conectarse con la API de geolocalización")
    
    content = response.json()
    if len(content) != 1:
        raise ValueError("Configurar localización adecuamente")
    return Location(**content.pop())


def get_temperature(qualitative: bool = False) -> float | str:
    url = settings.weather.urls["weather"]
    location = geolocate(settings.weather.location)
    try:
        response = requests.get(
            url,
            params={
                "lat": location.lat,
                "lon": location.lon,
                "units": settings.weather.temperature.units,
                "appid": settings.weather.api_key,
            },
            timeout=settings.weather.timeout
        )
    except requests.exceptions.RequestException:
        raise WeatherException("Error al conectarse con la API del clima")
    
    content = response.json()
    if int(content["cod"]) != 200:
        raise WeatherException(content["message"])
    
    temperature = content["main"]["temp"]
    if qualitative:
        limit = settings.weather.temperature.limit
        temperature = "hot" if temperature > limit else "cold"
    return temperature