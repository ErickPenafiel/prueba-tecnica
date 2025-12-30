"""
Excepciones personalizadas de la aplicación.
"""


class WeatherServiceError(Exception):
    """Excepción base para errores del servicio de clima."""
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class APIKeyNotFoundError(WeatherServiceError):
    """Excepción cuando no se encuentra la API key."""
    
    def __init__(self):
        super().__init__(
            "No se encontró la variable de entorno OPENWEATHER_API_KEY. "
            "Configura tu API key de OpenWeatherMap.",
            status_code=500
        )


class InvalidCityError(WeatherServiceError):
    """Excepción cuando la ciudad es inválida."""
    
    def __init__(self, city: str = ""):
        super().__init__(
            f"El parámetro 'city' es requerido y no puede estar vacío." if not city 
            else f"Ciudad '{city}' no encontrada.",
            status_code=400 if not city else 404
        )


class MLModelError(Exception):
    """Excepción para errores del modelo de ML."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
