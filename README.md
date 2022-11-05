# Heladeria Frozen Bot 🤖
Bot desarrollado en Python, diseñado para 🏢 Heladería Frozen SRL 🏢 con el objetivo de automatizar los pedidos de 🍦

## Full Version

### Requerimientos 🚩🚩🚩
1. [Python](https://python.org) (^3.10)
1. [Poetry](https://python-poetry.org/)
1. [API KEY de OpenWeather](https://openweathermap.org/)

### Funcionalidades ✅
- [x] Aplicación configurable
- [x] Geolocalización y averiguación de temperatura a través de OpenWeather
- [x] Mensaje de bienvenida adaptado a la temperatura
- [x] Compra de varios productos (empleo de carrito de compra)
- [x] Utilización de cupones de descuento
- [x] Número de intentos configurable (para evitar loops infinitos)

### Instrucciones para su ejecución
1. Descargar código
```sh
$ git clone https://github.com/martin882003dev/heladeria_frozen_bot.git
```
1. Dirigirse al directorio raíz e instalar las dependencias con poetry:
```sh
$ cd heladeria_frozen_bot/full_version
$ poetry install
```
1. Crear archivo `.env` con la api key de openweather:
```
$ echo OPEN_WEATHER_API_KEY=\"{ingresar_aqui_el_token}\" > .env
```
1. Ejecutar la aplicación con poetry:
```sh
$ poetry run python main.py
```

### Demostración
#### Proceso de compra completo
![Proceso de compra completo](https://media.giphy.com/media/w9FvLZ3JTlJ9fUAthE/giphy.gif)

#### Proceso de compra interrumpido por el usuario
![Proceso de compra interrumpido por el usuario](https://media.giphy.com/media/UA2skxQLn7LQlR2gPU/giphy.gif)

#### Proceso de compra interrumpido por intentos excesivos
![Proceso de compra interrumpido por intentos excesivos](https://media.giphy.com/media/oqVfrquzG7oQQcp1Kz/giphy.gif)
