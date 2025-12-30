"""
DEPRECADO: Este archivo se mantiene por compatibilidad.
Usar app.services.ml_service en su lugar.
"""
import warnings
from app.services.ml_service import ml_service

warnings.warn(
    "ml_model.py está deprecado. Usa app.services.ml_service.MLService",
    DeprecationWarning,
    stacklevel=2
)

# Mantener compatibilidad con código existente
sentiment_model = ml_service


# Clase legacy para compatibilidad
class SentimentModel:
    """Clase legacy - usar MLService en su lugar."""
    
    def __init__(self):
        warnings.warn(
            "SentimentModel está deprecado. Usa MLService",
            DeprecationWarning,
            stacklevel=2
        )
        self._service = ml_service
    
    def predict(self, text: str):
        """Método legacy para compatibilidad."""
        return self._service.predict_sentiment(text)
