"""
Servicio de Machine Learning para análisis de sentimiento.
"""
from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from app.exceptions import MLModelError


class MLService:
    """Servicio de análisis de sentimiento."""
    
    def __init__(self):
        """Inicializa y entrena el modelo."""
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
        self.classifier = LogisticRegression()
        self._train_model()
    
    def _train_model(self) -> None:
        """
        Entrena el modelo con un dataset de ejemplo.
        En producción, esto debería cargar un modelo pre-entrenado.
        """
        # Dataset de ejemplo para demostración
        training_texts = [
            "cielo despejado y agradable",
            "tiempo soleado y perfecto para salir",
            "clima muy bueno, temperatura ideal",
            "lluvia ligera y algo de viento",
            "tormenta fuerte con truenos",
            "clima muy frío y desagradable",
            "lluvias intensas y viento fuerte",
            "nubes oscuras y ambiente feo",
        ]
        
        training_labels = [
            "positivo",
            "positivo",
            "positivo",
            "neutral",
            "negativo",
            "negativo",
            "negativo",
            "negativo",
        ]
        
        try:
            X = self.vectorizer.fit_transform(training_texts)
            self.classifier.fit(X, training_labels)
        except Exception as e:
            raise MLModelError(f"Error al entrenar el modelo: {str(e)}")
    
    def predict_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Predice el sentimiento de un texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tupla (etiqueta, probabilidad)
        """
        try:
            X = self.vectorizer.transform([text])
            probabilities = self.classifier.predict_proba(X)[0]
            label_index = probabilities.argmax()
            label = self.classifier.classes_[label_index]
            probability = float(probabilities[label_index])
            
            return label, probability
        except Exception as e:
            raise MLModelError(f"Error al predecir sentimiento: {str(e)}")


# Instancia singleton del servicio
ml_service = MLService()
