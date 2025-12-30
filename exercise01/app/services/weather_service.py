"""
Servicio para consultar datos del clima desde OpenWeatherMap.
"""
from typing import Dict, Any
import pandas as pd
import requests
from requests import HTTPError

from app.config import settings
from app.exceptions import (
    WeatherServiceError,
    APIKeyNotFoundError,
    InvalidCityError
)


class WeatherService:
    """Servicio para obtener datos del clima."""
    
    @staticmethod
    def get_weather(city: str, lang: str = None, units: str = None) -> Dict[str, Any]:
        """
        Consulta el clima actual de una ciudad.
        
        Args:
            city: Nombre de la ciudad
            lang: Idioma de la respuesta (por defecto: configuración)
            units: Unidades de medida (por defecto: configuración)
            
        Returns:
            Diccionario con data, message y status_code
        """
        # Validaciones
        if not settings.OPENWEATHER_API_KEY:
            return {
                "data": None,
                "message": "No se encontró la variable de entorno OPENWEATHER_API_KEY. Configura tu API key de OpenWeatherMap.",
                "status_code": 500
            }
        
        if not city or not city.strip():
            return {
                "data": None,
                "message": "El parámetro 'city' es requerido y no puede estar vacío.",
                "status_code": 400
            }
        
        # Configuración
        lang = lang or settings.DEFAULT_LANGUAGE
        units = units or settings.DEFAULT_UNITS
        
        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "lang": lang,
            "units": units,
        }
        
        # Realizar petición
        try:
            response = requests.get(
                settings.OPENWEATHER_BASE_URL,
                params=params,
                timeout=settings.REQUEST_TIMEOUT
            )
            response.raise_for_status()
        except HTTPError:
            return WeatherService._handle_http_error(response, city)
        except requests.exceptions.Timeout:
            return {
                "data": None,
                "message": "Tiempo de espera agotado al consultar el servicio de clima.",
                "status_code": 504
            }
        except requests.exceptions.ConnectionError:
            return {
                "data": None,
                "message": "Error de conexión al consultar el servicio de clima.",
                "status_code": 503
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Error inesperado al consultar OpenWeatherMap: {str(e)}",
                "status_code": 500
            }
        
        # Procesar respuesta
        try:
            data = response.json()
        except Exception as e:
            return {
                "data": None,
                "message": f"Error al parsear la respuesta JSON: {str(e)}",
                "status_code": 500
            }
        
        # Extraer y estructurar datos
        try:
            weather_data = WeatherService._extract_weather_data(data)
            df = pd.DataFrame([weather_data])
            
            return {
                "data": df,
                "message": f"Datos del clima obtenidos exitosamente para {weather_data['city']}, {weather_data['country']}.",
                "status_code": 200
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Error procesando los datos de OpenWeatherMap: {str(e)}",
                "status_code": 500
            }
    
    @staticmethod
    def _handle_http_error(response: requests.Response, city: str) -> Dict[str, Any]:
        """Maneja errores HTTP de la API."""
        status_code = response.status_code
        
        error_messages = {
            404: f"Ciudad '{city}' no encontrada.",
            401: "API key inválida o no autorizada.",
            429: "Límite de solicitudes excedido. Intenta más tarde.",
        }
        
        message = error_messages.get(
            status_code,
            f"Error HTTP al consultar OpenWeatherMap: {response.status_code}"
        )
        
        return {
            "data": None,
            "message": message,
            "status_code": status_code
        }
    
    @staticmethod
    def _extract_weather_data(data: dict) -> dict:
        """Extrae los campos relevantes de la respuesta de la API."""
        return {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "description": data.get("weather", [{}])[0].get("description"),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "timestamp": data.get("dt"),
        }
