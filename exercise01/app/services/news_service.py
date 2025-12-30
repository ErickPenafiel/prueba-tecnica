"""
Servicio para consultar NewsAPI.
"""
import requests
from typing import Dict, List, Optional

from app.config import settings
from app.exceptions import WeatherServiceError


class NewsService:
    """Servicio para interactuar con NewsAPI."""
    
    @staticmethod
    def search_news(query: str, language: str = "es") -> Dict:
        """
        Busca noticias relacionadas con un término de búsqueda.
        
        Args:
            query: Término de búsqueda (ej: nombre del cliente)
            language: Idioma de las noticias (default: es)
            
        Returns:
            Diccionario con la respuesta de la API
            
        Raises:
            WeatherServiceError: Si hay un error en la consulta
        """
        if not settings.NEWS_API_KEY:
            raise WeatherServiceError("NEWS_API_KEY no está configurada")
        
        params = {
            "q": query,
            "apiKey": settings.NEWS_API_KEY,
            "language": language,
            "pageSize": 5  # Limitar a 5 artículos
        }
        
        try:
            response = requests.get(
                settings.NEWS_API_BASE_URL,
                params=params,
                timeout=settings.REQUEST_TIMEOUT
            )
            
            if response.status_code == 401:
                raise WeatherServiceError("API Key inválida o no autorizada")
            
            if response.status_code == 429:
                raise WeatherServiceError("Límite de consultas excedido")
            
            if response.status_code != 200:
                raise WeatherServiceError(
                    f"Error al consultar noticias: {response.status_code}"
                )
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise WeatherServiceError("Timeout al consultar NewsAPI")
        except requests.exceptions.RequestException as e:
            raise WeatherServiceError(f"Error de conexión: {str(e)}")
    
    @staticmethod
    def get_articles(query: str, language: str = "es") -> List[Dict]:
        """
        Obtiene la lista de artículos de una búsqueda.
        
        Args:
            query: Término de búsqueda
            language: Idioma de las noticias
            
        Returns:
            Lista de artículos encontrados
        """
        response = NewsService.search_news(query, language)
        return response.get("articles", [])


# Instancia singleton del servicio
news_service = NewsService()
