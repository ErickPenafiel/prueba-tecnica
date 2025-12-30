"""
Servicio de clasificación de riesgos de compliance usando IA.
"""
from typing import Dict, Tuple
from transformers import pipeline

from app.config import settings
from app.exceptions import MLModelError


class ComplianceMLService:
    """Servicio de análisis de riesgos de compliance usando BART."""
    
    _instance = None
    _classifier = None
    
    def __new__(cls):
        """Singleton para evitar cargar el modelo múltiples veces."""
        if cls._instance is None:
            cls._instance = super(ComplianceMLService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa el clasificador de IA."""
        if self._classifier is None:
            try:
                # Inicializar modelo BART para clasificación zero-shot
                # La primera ejecución descargará el modelo (~1GB)
                self._classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
            except Exception as e:
                raise MLModelError(f"Error al cargar el modelo BART: {str(e)}")
    
    def classify_risk(self, text: str) -> Dict:
        """
        Clasifica el riesgo de un texto usando el modelo BART.
        
        Args:
            text: Texto a analizar (titular + descripción de noticia)
            
        Returns:
            Diccionario con la clasificación:
            {
                "labels": ["fraude financiero", "operación normal", ...],
                "scores": [0.65, 0.20, ...]
            }
        """
        if not self._classifier:
            raise MLModelError("El clasificador no está inicializado")
        
        try:
            # Clasificar usando las etiquetas de riesgo configuradas
            result = self._classifier(text, settings.RISK_LABELS)
            return result
        except Exception as e:
            raise MLModelError(f"Error al clasificar texto: {str(e)}")
    
    def analyze_compliance_risk(
        self,
        text: str,
        threshold: float = None
    ) -> Tuple[bool, str, float]:
        """
        Analiza si un texto representa un riesgo de compliance.
        
        Args:
            text: Texto a analizar
            threshold: Umbral de confianza (default: configuración)
            
        Returns:
            Tupla (is_risk, top_label, top_score)
        """
        if threshold is None:
            threshold = settings.RISK_THRESHOLD
        
        result = self.classify_risk(text)
        
        top_label = result['labels'][0]
        top_score = result['scores'][0]
        
        # Determinar si es un riesgo real
        risk_categories = ["fraude financiero", "lavado de activos", "corrupción"]
        is_risk = top_label in risk_categories and top_score > threshold
        
        return is_risk, top_label, top_score


# Instancia singleton del servicio
compliance_ml_service = ComplianceMLService()
