"""
Servicio de análisis de sentimiento de mercado usando IA.
"""
from typing import Tuple
from transformers import pipeline

from app.config import settings
from app.exceptions import MLModelError


class SentimentAnalysisService:
    """Servicio de análisis de sentimiento de mercado usando BART."""
    
    _instance = None
    _classifier = None
    
    def __new__(cls):
        """Singleton para evitar cargar el modelo múltiples veces."""
        if cls._instance is None:
            cls._instance = super(SentimentAnalysisService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa el clasificador de sentimiento."""
        if self._classifier is None:
            try:
                # Reutilizar el mismo modelo BART para clasificación zero-shot
                self._classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
            except Exception as e:
                raise MLModelError(f"Error al cargar el modelo de sentiment: {str(e)}")
    
    def analyze_market_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analiza el sentimiento de mercado de un texto de noticias.
        
        Args:
            text: Texto a analizar (titular + descripción de noticia)
            
        Returns:
            Tupla (sentiment_label, confidence)
            - sentiment_label: 'positivo', 'neutral', 'negativo'
            - confidence: float entre 0 y 1
        """
        if not self._classifier:
            raise MLModelError("El clasificador no está inicializado")
        
        try:
            # Clasificar usando las etiquetas de sentimiento configuradas
            result = self._classifier(text, settings.SENTIMENT_LABELS)
            
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            return top_label, top_score
            
        except Exception as e:
            raise MLModelError(f"Error al analizar sentimiento: {str(e)}")
    
    def analyze_multiple_articles(self, articles: list) -> Tuple[str, float]:
        """
        Analiza el sentimiento agregado de múltiples artículos.
        
        Args:
            articles: Lista de diccionarios con 'title' y 'description'
            
        Returns:
            Tupla (sentiment_promedio, confidence_promedio)
        """
        if not articles:
            return "neutral", 0.5
        
        sentiments = []
        confidences = []
        
        # Analizar hasta 3 artículos más relevantes
        for article in articles[:3]:
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title} {description}"
            
            if text.strip():
                sentiment, confidence = self.analyze_market_sentiment(text)
                sentiments.append(sentiment)
                confidences.append(confidence)
        
        if not sentiments:
            return "neutral", 0.5
        
        # Calcular sentimiento dominante
        sentiment_counts = {
            'positivo': sentiments.count('positivo'),
            'neutral': sentiments.count('neutral'),
            'negativo': sentiments.count('negativo')
        }
        
        dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        avg_confidence = sum(confidences) / len(confidences)
        
        return dominant_sentiment, avg_confidence


# Instancia singleton del servicio
sentiment_service = SentimentAnalysisService()
