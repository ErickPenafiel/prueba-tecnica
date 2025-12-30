"""
DEPRECADO: Este archivo se mantiene por compatibilidad.
Usar app.services.weather_service en su lugar.
"""
import warnings
from app.services.weather_service import WeatherService
from app.exceptions import WeatherServiceError

warnings.warn(
    "weather_service.py está deprecado. Usa app.services.weather_service.WeatherService",
    DeprecationWarning,
    stacklevel=2
)


def get_weather_for_city(city: str, lang: str = "es", units: str = "metric"):
    """
    Función legacy para compatibilidad.
    Se recomienda usar WeatherService.get_weather() directamente.
    """
    return WeatherService.get_weather(city, lang, units)


__all__ = ["get_weather_for_city", "WeatherServiceError"]
