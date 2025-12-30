"""
Configuración centralizada de la aplicación.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuración de la aplicación."""
    
    # API Keys
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # API URLs
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    NEWS_API_BASE_URL: str = "https://newsapi.org/v2/everything"
    
    # Configuración por defecto
    DEFAULT_LANGUAGE: str = "es"
    DEFAULT_UNITS: str = "metric"
    REQUEST_TIMEOUT: int = 10
    
    # Configuración de compliance
    RISK_THRESHOLD: float = 0.35
    RISK_LABELS: list = ["fraude financiero", "lavado de activos", "corrupción", "quiebra", "operación normal"]
    
    # Configuración de sentiment analysis
    SENTIMENT_LABELS: list = ["positivo", "neutral", "negativo"]
    
    # Información de la aplicación
    APP_TITLE: str = "FinUp Risk Intelligence Platform"
    APP_DESCRIPTION: str = (
        "Plataforma de inteligencia de riesgos bancarios que combina análisis de sentimiento de mercado "
        "y verificación de compliance usando modelos de IA avanzados. Diseñada para integración con n8n "
        "y sistemas de automatización empresarial."
    )
    APP_VERSION: str = "2.0.0"
    
    # Tags de la API
    API_TAGS_METADATA: list = [
        {
            "name": "Risk Intelligence",
            "description": "Endpoints de análisis de riesgos combinando sentiment y compliance"
        },
        {
            "name": "System Health",
            "description": "Monitoreo del estado del sistema y servicios de IA"
        }
    ]


settings = Settings()
