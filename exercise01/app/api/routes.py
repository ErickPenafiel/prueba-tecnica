"""
Definición de rutas y endpoints de la API.
"""
from fastapi import APIRouter, HTTPException

from app.models import RiskAnalysisResponse, RiskAnalysisData, ComplianceCheckResponse, ComplianceAnalysis
from app.services.news_service import news_service
from app.services.compliance_service import compliance_ml_service
from app.services.sentiment_service import sentiment_service
from app.exceptions import WeatherServiceError, MLModelError

router = APIRouter()


@router.get("/", tags=["System Health"])
def root():
    """Endpoint raíz con información de la API."""
    return {
        "service": "FinUp Risk Intelligence Platform",
        "version": "2.0.0",
        "status": "operational",
        "documentation": "/docs",
        "main_endpoint": "/api/v1/risk-analysis?company_name=Tesla"
    }


@router.get("/health", tags=["System Health"])
def health_check():
    """Endpoint para verificar el estado de la API y servicios de IA."""
    return {
        "status": "healthy",
        "service": "FinUp Risk Intelligence Platform",
        "models_loaded": {
            "compliance_classifier": "BART Large MNLI",
            "sentiment_analyzer": "BART Large MNLI"
        },
        "apis_integrated": ["NewsAPI"]
    }


# ========== ENDPOINT PRINCIPAL - RISK INTELLIGENCE ==========

@router.get(
    "/api/v1/risk-analysis",
    response_model=RiskAnalysisResponse,
    tags=["Risk Intelligence"],
    summary="Análisis Unificado de Riesgos Empresariales",
    description=(
        "Endpoint principal que combina análisis de sentimiento de mercado y verificación de compliance. "
        "Busca noticias de la empresa y aplica modelos de IA para evaluar riesgos financieros. "
        "Respuesta optimizada para integración con n8n y sistemas de automatización."
    )
)
async def analyze_company_risk(company_name: str):
    """
    Realiza un análisis completo de riesgos de una empresa.
    
    Combina:
    - **Sentiment Analysis**: Analiza el sentimiento del mercado basado en noticias
    - **Compliance Check**: Detecta riesgos de fraude, lavado de activos, corrupción, etc.
    
    Args:
        company_name: Nombre de la empresa a analizar
        
    Returns:
        RiskAnalysisResponse: Estructura plana con todos los indicadores de riesgo
        
    Raises:
        HTTPException 404: Si no se encuentra información de la empresa
        HTTPException 500: Si hay errores en el análisis de IA o consulta de noticias
    """
    try:
        # 1. Búsqueda de noticias
        articles = news_service.get_articles(company_name, language="es")
        
        print(f"\n{'='*80}")
        print(f"📊 ANÁLISIS DE RIESGOS PARA: {company_name}")
        print(f"   Noticias encontradas: {len(articles)}")
        print(f"{'='*80}")
        
        # 2. Sin noticias = empresa no encontrada
        if not articles:
            print("   ℹ️  No se encontraron noticias - Empresa no encontrada")
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró información de la empresa '{company_name}'. Verifica el nombre."
            )
        
        # 3. Extraer información de la noticia más relevante
        first_article = articles[0]
        title = first_article.get('title', '')
        description = first_article.get('description', '')
        source = first_article.get('source', {}).get('name', 'Desconocido')
        url = first_article.get('url', '')
        
        print(f"\n📄 Noticia principal:")
        print(f"   Fuente: {source}")
        print(f"   Título: {title}")
        print(f"{'='*80}")
        
        text_to_analyze = f"{title} {description}"
        
        # 4. ANÁLISIS DE SENTIMIENTO
        print(f"\n🎭 Analizando sentimiento de mercado...")
        market_sentiment, sentiment_conf = sentiment_service.analyze_market_sentiment(text_to_analyze)
        print(f"   Resultado: {market_sentiment} (confianza: {sentiment_conf:.2%})")
        
        # 5. ANÁLISIS DE COMPLIANCE
        print(f"\n🔍 Analizando riesgos de compliance...")
        is_risk, compliance_risk_type, compliance_conf = compliance_ml_service.analyze_compliance_risk(
            text_to_analyze
        )
        compliance_status = "alert" if is_risk else "clear"
        print(f"   Riesgo detectado: {compliance_risk_type}")
        print(f"   Estado: {compliance_status} (confianza: {compliance_conf:.2%})")
        
        # 6. CÁLCULO DE RIESGO GLOBAL
        # Combinar scores: peso 40% sentiment, 60% compliance
        sentiment_score = 0.0 if market_sentiment == "positivo" else (0.5 if market_sentiment == "neutral" else 1.0)
        overall_risk_score = (sentiment_score * 0.4) + (compliance_conf * 0.6) if is_risk else sentiment_score * 0.4
        
        # Determinar estado general
        if is_risk and overall_risk_score > 0.6:
            overall_status = "alert"
            requires_review = True
        elif overall_risk_score > 0.4 or market_sentiment == "negativo":
            overall_status = "warning"
            requires_review = True
        else:
            overall_status = "clear"
            requires_review = False
        
        print(f"\n📈 RESULTADO FINAL:")
        print(f"   Estado General: {overall_status.upper()}")
        print(f"   Risk Score: {overall_risk_score:.2%}")
        print(f"   Revisión Manual: {'SÍ' if requires_review else 'NO'}")
        print(f"{'='*80}\n")
        
        # 7. Construir respuesta con estructura status_code, message, data
        message = f"Análisis completado: {overall_status}. {'Requiere revisión manual.' if requires_review else 'Sin alertas críticas.'}"
        
        risk_data = RiskAnalysisData(
            company_name=company_name,
            overall_risk_status=overall_status,
            overall_risk_score=round(overall_risk_score, 4),
            market_sentiment=market_sentiment,
            sentiment_confidence=round(sentiment_conf, 4),
            compliance_status=compliance_status,
            compliance_risk_type=compliance_risk_type,
            compliance_confidence=round(compliance_conf, 4),
            news_found=len(articles),
            evidence_headline=title,
            evidence_source=source,
            evidence_url=url,
            requires_manual_review=requires_review
        )
        
        return RiskAnalysisResponse(
            status_code=200,
            message=message,
            data=risk_data
        )
        
    except HTTPException:
        raise
    except WeatherServiceError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar noticias: {str(e)}"
        )
    except MLModelError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el análisis de IA: {str(e)}"
        )
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado en el análisis: {str(e)}"
        )


# ========== ENDPOINTS LEGACY (COMPATIBILIDAD) ==========

@router.get(
    "/api/v1/compliance-check",
    response_model=ComplianceCheckResponse,
    tags=["Legacy Endpoints"],
    summary="[LEGACY] Verificación de cumplimiento bancario",
    description="⚠️ Endpoint legacy. Use /api/v1/risk-analysis para análisis completo.",
    deprecated=True
)
async def compliance_check(client_name: str):
    """
    Verifica el cumplimiento de un cliente buscando noticias y analizando riesgos.
    
    Args:
        client_name: Nombre del cliente a consultar
        
    Returns:
        Resultado del análisis de compliance con estado (alert/clear)
        
    Raises:
        HTTPException: Si hay errores en la consulta o análisis
    """
    try:
        # 1. Búsqueda de noticias relacionadas al cliente
        articles = news_service.get_articles(client_name, language="es")
        
        print(f"\n{'='*80}")
        print(f"📰 Búsqueda de noticias para: {client_name}")
        print(f"   Total de artículos encontrados: {len(articles)}")
        print(f"{'='*80}")
        
        if not articles:
            print("   ℹ️  No se encontraron noticias")
            return ComplianceCheckResponse(
                client=client_name,
                status="clear",
                risk_score=0.0,
                message="No se encontraron registros adversos."
            )
        
        # 2. Análisis de IA sobre el titular más relevante
        first_article = articles[0]
        title = first_article.get('title', '')
        description = first_article.get('description', '')
        source = first_article.get('source', {}).get('name', 'Desconocido')
        published_at = first_article.get('publishedAt', 'N/A')
        
        print(f"\n📄 Artículo más relevante:")
        print(f"   Fuente: {source}")
        print(f"   Fecha: {published_at}")
        print(f"   Título: {title}")
        print(f"   Descripción: {description[:100]}...")
        print(f"{'='*80}\n")
        
        text_to_analyze = f"{title} {description}"
        
        # 3. Clasificar riesgo usando el modelo BART
        is_risk, top_label, top_score = compliance_ml_service.analyze_compliance_risk(
            text_to_analyze
        )
        
        # 4. Construir respuesta
        analysis = ComplianceAnalysis(
            top_risk=top_label,
            confidence=round(top_score, 4),
            evidence_snippet=title
        )
        
        return ComplianceCheckResponse(
            client=client_name,
            status="alert" if is_risk else "clear",
            risk_score=round(top_score, 4) if is_risk else 0.0,
            analysis=analysis
        )
        
    except WeatherServiceError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar noticias: {str(e)}"
        )
    except MLModelError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el análisis de IA: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )
