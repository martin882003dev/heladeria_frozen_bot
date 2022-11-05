import functools
from typing import Callable

from bot.config import settings
from bot.exceptions import MaxAttemptsExceededException
from bot.ui import Printer

def max_attempts(display_warning: bool = True) -> None:
    def outer(func: Callable)-> Callable:
        @functools.wraps(func)
        def inner(*args, **kwargs) -> Callable:
            attempts = 0
            while attempts < settings.max_attempts:
                results = func(*args, **kwargs)
                if results is not None:
                    return results
                if settings.max_attempts:
                    attempts += 1
                    remaining = settings.max_attempts - attempts
                    if remaining and display_warning:
                        print("\033[F\033[2K", end="")
                        msg = f"Opción no válida\n\n(intentos restantes: {remaining})"
                        Printer.error(msg)
            raise MaxAttemptsExceededException
        return inner
    return outer