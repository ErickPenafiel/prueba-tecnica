"""
Modelos de datos (schemas) de la aplicación.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


# ========== MODELOS PRINCIPALES - RISK INTELLIGENCE ==========

class RiskAnalysisData(BaseModel):
    """
    Datos del análisis de riesgos.
    Combina sentiment analysis y compliance check en un solo objeto.
    """
    # Identificación
    company_name: str = Field(..., description="Nombre de la empresa analizada")
    analysis_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Timestamp del análisis en ISO 8601")
    
    # Estado general
    overall_risk_status: str = Field(..., description="Estado general: 'clear', 'warning', 'alert'")
    overall_risk_score: float = Field(..., description="Puntuación de riesgo combinada (0-1)", ge=0.0, le=1.0)
    
    # Sentiment Analysis
    market_sentiment: str = Field(..., description="Sentimiento del mercado: 'positivo', 'neutral', 'negativo'")
    sentiment_confidence: float = Field(..., description="Confianza del análisis de sentimiento (0-1)", ge=0.0, le=1.0)
    
    # Compliance Check
    compliance_status: str = Field(..., description="Estado de compliance: 'clear', 'alert'")
    compliance_risk_type: str = Field(..., description="Tipo de riesgo detectado: 'fraude financiero', 'lavado de activos', etc.")
    compliance_confidence: float = Field(..., description="Confianza del análisis de compliance (0-1)", ge=0.0, le=1.0)
    
    # Evidencia
    news_found: int = Field(..., description="Cantidad de noticias encontradas")
    evidence_headline: Optional[str] = Field(None, description="Titular de la noticia más relevante")
    evidence_source: Optional[str] = Field(None, description="Fuente de la noticia")
    evidence_url: Optional[str] = Field(None, description="URL de la noticia")
    
    # Metadata
    requires_manual_review: bool = Field(default=False, description="Indica si requiere revisión manual")


class RiskAnalysisResponse(BaseModel):
    """
    Respuesta estándar de la API con estructura status_code, message, data.
    """
    status_code: int = Field(..., description="Código de estado HTTP")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data: RiskAnalysisData = Field(..., description="Datos del análisis de riesgos")


# ========== MODELOS LEGACY (MANTENER COMPATIBILIDAD) ==========

class ComplianceAnalysis(BaseModel):
    """Modelo de análisis de riesgo de compliance."""
    
    top_risk: str = Field(..., description="Etiqueta de riesgo más probable")
    confidence: float = Field(..., description="Confianza del modelo", ge=0.0, le=1.0)
    evidence_snippet: str = Field(..., description="Fragmento de evidencia de la noticia")


class ComplianceCheckResponse(BaseModel):
    """Respuesta del endpoint de compliance check (legacy)."""
    
    client: str = Field(..., description="Nombre del cliente consultado")
    status: str = Field(..., description="Estado del resultado (alert/clear)")
    risk_score: Optional[float] = Field(None, description="Puntuación de riesgo")
    message: Optional[str] = Field(None, description="Mensaje adicional")
    analysis: Optional[ComplianceAnalysis] = Field(None, description="Análisis detallado")
