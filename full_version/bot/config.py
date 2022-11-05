from pydantic import BaseSettings

from bot.schemas import Temperature


class TemperatureSettings(BaseSettings):
    units = Temperature.celsius
    limit = 28.0


class WeatherSettings(BaseSettings):
    api_key: str
    urls = {
        "weather": "https://api.openweathermap.org/data/2.5/weather",
        "geolocation": "https://api.openweathermap.org/geo/1.0/direct"
    }
    location = "Pehuajó"
    temperature = TemperatureSettings()
    timeout = 3
    
    class Config:
        env_prefix = "OPEN_WEATHER_"
        env_file = ".env"


class LoggingSettings(BaseSettings):
    format = "%(asctime)s [%(levelname)s] %(message)s"
    filename = "app.log"


class DatabaseSettings(BaseSettings):
    url = "sqlite:///./app.db"

class UISettings(BaseSettings):
    header = True
    welcome = {
        "hot": "¡Que el calor no te derrita! ¡Elegí tu helado ya!",
        "cold": "!Acompañá este clima fresco con un rico helado!"
    }
    title = "🍦 Heladería Frozen 🍦"


class Settings(BaseSettings):
    app_name = "Heladería Frozen Bot"
    version = 1.0
    product_type = {
        "singular": "helado",
        "plural": "helados"
    }
    weather = WeatherSettings()
    logging = LoggingSettings()
    db = DatabaseSettings()
    ui = UISettings()
    max_attempts = 3

settings = Settings()