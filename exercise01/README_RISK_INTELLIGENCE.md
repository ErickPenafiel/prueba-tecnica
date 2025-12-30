# FinUp Risk Intelligence Platform 🏦

## 📋 Descripción

Plataforma profesional de análisis de riesgos bancarios que combina **Sentiment Analysis** y **Compliance Check** en un único endpoint unificado. Diseñada para integrarse con n8n y sistemas de automatización empresarial.

### Características Principales

✅ **Análisis Unificado**: Un solo endpoint que combina sentimiento de mercado y riesgos de compliance  
✅ **Respuesta Plana**: Estructura JSON optimizada para n8n e integraciones  
✅ **IA Avanzada**: Modelo BART Large para clasificación zero-shot  
✅ **Profesional**: Tags organizados, documentación completa y manejo de errores robusto  
✅ **Escalable**: Arquitectura en capas preparada para crecer

---

## 🏗️ Arquitectura

```
app/
├── main.py                          # FastAPI application
├── config.py                        # Configuración centralizada
├── models.py                        # Modelos Pydantic (RiskAnalysisResponse)
├── exceptions.py                    # Excepciones personalizadas
│
├── api/
│   └── routes.py                   # Endpoints REST
│
└── services/
    ├── news_service.py             # NewsAPI integration
    ├── sentiment_service.py        # Sentiment Analysis (BART)
    └── compliance_service.py       # Compliance Check (BART)
```

### Capas de la Arquitectura

```
┌─────────────────────────────────────────────┐
│   API Layer (routes.py)                     │  ← REST Endpoints
├─────────────────────────────────────────────┤
│   Service Layer (services/)                 │  ← Business Logic
│   ├── Sentiment Analysis                    │
│   ├── Compliance Check                      │
│   └── News Integration                      │
├─────────────────────────────────────────────┤
│   Models (models.py)                        │  ← Data Validation
├─────────────────────────────────────────────┤
│   Config (config.py)                        │  ← Configuration
└─────────────────────────────────────────────┘
```

---

## 🚀 Instalación

### 1. Clonar e instalar dependencias

```bash
cd exercise01
pip install -r requirements.txt
```

**⚠️ Primera ejecución**: Descargará el modelo BART Large (~1GB). Esto puede tomar 5-10 minutos.

### 2. Configurar variables de entorno

Crea/edita el archivo `.env`:

```env
NEWS_API_KEY=tu_api_key_de_newsapi
```

Obtén tu API key gratuita: https://newsapi.org/

### 3. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La API estará en: **http://localhost:8000**

---

## 📡 API Endpoints

### 🎯 Endpoint Principal: Risk Analysis

**GET** `/api/v1/risk-analysis?company_name={nombre}`

Análisis unificado que combina sentiment y compliance en una respuesta plana.

#### Ejemplo de Uso

```bash
curl "http://localhost:8000/api/v1/risk-analysis?company_name=Tesla"
```

#### Respuesta JSON (estructura plana para n8n)

```json
{
	"company_name": "Tesla",
	"analysis_timestamp": "2025-12-29T10:30:00.123456",
	"overall_risk_status": "clear",
	"overall_risk_score": 0.25,
	"market_sentiment": "positivo",
	"sentiment_confidence": 0.8234,
	"compliance_status": "clear",
	"compliance_risk_type": "operación normal",
	"compliance_confidence": 0.7891,
	"news_found": 15,
	"evidence_headline": "Tesla alcanza nuevos récords de producción",
	"evidence_source": "Reuters",
	"evidence_url": "https://...",
	"message": "Análisis completado: clear. Sin alertas críticas.",
	"requires_manual_review": false
}
```

#### Estados Posibles

| Campo                  | Valores                                                                               | Descripción                 |
| ---------------------- | ------------------------------------------------------------------------------------- | --------------------------- |
| `overall_risk_status`  | `clear`, `warning`, `alert`                                                           | Estado general del análisis |
| `market_sentiment`     | `positivo`, `neutral`, `negativo`                                                     | Sentimiento de mercado      |
| `compliance_status`    | `clear`, `alert`                                                                      | Estado de compliance        |
| `compliance_risk_type` | `fraude financiero`, `lavado de activos`, `corrupción`, `quiebra`, `operación normal` | Tipo de riesgo detectado    |

#### Códigos de Estado HTTP

- **200 OK**: Análisis completado exitosamente
- **404 Not Found**: Empresa no encontrada (sin noticias)
- **500 Internal Server Error**: Error en IA o NewsAPI

---

### 🏥 Health Check

**GET** `/health`

Verifica el estado de la API y modelos de IA.

```json
{
	"status": "healthy",
	"service": "FinUp Risk Intelligence Platform",
	"models_loaded": {
		"compliance_classifier": "BART Large MNLI",
		"sentiment_analyzer": "BART Large MNLI"
	},
	"apis_integrated": ["NewsAPI"]
}
```

---

## 🔧 Configuración Avanzada

En [app/config.py](app/config.py):

```python
# Umbral de riesgo para alertas
RISK_THRESHOLD: float = 0.35

# Etiquetas de riesgo de compliance
RISK_LABELS: list = [
    "fraude financiero",
    "lavado de activos",
    "corrupción",
    "quiebra",
    "operación normal"
]

# Etiquetas de sentimiento
SENTIMENT_LABELS: list = ["positivo", "neutral", "negativo"]
```

---

## 🤖 Integración con n8n

### Workflow de Ejemplo

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Schedule   │────▶│  HTTP Request │────▶│  Filter     │
│ (Daily 9AM) │     │  /risk-analysis│    │ (alerts)    │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │   Email     │
                                         │   Alert     │
                                         └─────────────┘
```

### Configuración n8n

1. **HTTP Request Node**:

   - Method: `GET`
   - URL: `http://localhost:8000/api/v1/risk-analysis`
   - Query Parameters: `company_name={{ $json.company }}`

2. **Filter Node** (alertas críticas):

   ```javascript
   {
   	{
   		$json.overall_risk_status === "alert";
   	}
   }
   ```

3. **Campos útiles para automatización**:
   - `requires_manual_review`: Boolean para filtrar casos
   - `overall_risk_score`: Numérico para ordenar por severidad
   - `analysis_timestamp`: Para tracking temporal

---

## 🧪 Testing

### Script de Prueba Incluido

```bash
python test_compliance.py
```

### Test Manual

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/risk-analysis",
    params={"company_name": "Microsoft"}
)

data = response.json()
print(f"Estado: {data['overall_risk_status']}")
print(f"Sentimiento: {data['market_sentiment']}")
print(f"Revisión manual: {data['requires_manual_review']}")
```

---

## 📊 Lógica de Decisión

### Cálculo de Risk Score

```
overall_risk_score = (sentiment_score * 0.4) + (compliance_confidence * 0.6)
```

- **Sentiment Score**: 0.0 (positivo), 0.5 (neutral), 1.0 (negativo)
- **Compliance Confidence**: Score del modelo de IA

### Estados Generales

| Condición                         | Status    | Revisión Manual |
| --------------------------------- | --------- | --------------- |
| Compliance alert + score > 0.6    | `alert`   | ✅ Requerida    |
| Score > 0.4 OR sentiment negativo | `warning` | ✅ Requerida    |
| Ninguna de las anteriores         | `clear`   | ❌ No requerida |

---

## 🔐 Seguridad

- ✅ Variables de entorno para API keys
- ✅ Validación de inputs con Pydantic
- ✅ Manejo de errores con mensajes descriptivos
- ✅ Rate limiting en NewsAPI (100 requests/día - free tier)

### Recomendaciones para Producción

1. Implementar autenticación (JWT, API Keys)
2. Agregar rate limiting en FastAPI
3. Usar Redis para caché de resultados
4. Monitoreo con Prometheus/Grafana
5. HTTPS obligatorio

---

## 📚 Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

La documentación incluye:

- Descripción de cada endpoint
- Schemas de request/response
- Códigos de error
- Ejemplos interactivos

---

## 🤝 Tags Organizados

La API está organizada en tags profesionales:

- **Risk Intelligence**: Endpoints principales de análisis
- **System Health**: Monitoreo y health checks
- **Legacy Endpoints**: APIs deprecadas (compatibilidad)

---

## 🐛 Troubleshooting

### Error: "NEWS_API_KEY no está configurada"

```bash
# Verificar .env
cat .env | grep NEWS_API_KEY
```

### Error al cargar modelo BART

```bash
# Verificar cache de Hugging Face
ls ~/.cache/huggingface/hub/
```

### Límite de requests excedido (NewsAPI)

- Free tier: 100 consultas/día
- Considera implementar caché con Redis
- O upgrade a plan de pago

---

## 📈 Mejoras Futuras

- [ ] Caché con Redis para optimizar consultas repetidas
- [ ] Análisis de múltiples fuentes de noticias
- [ ] Histórico de análisis por empresa
- [ ] Dashboard web con visualizaciones
- [ ] WebSockets para análisis en tiempo real
- [ ] Integración con bases de datos de sanciones (OFAC, etc.)

---

## 📝 Licencia

MIT License

---

## 🎯 Prueba Técnica - Notas

Esta solución demuestra:

✅ **Arquitectura Limpia**: Separación de responsabilidades en capas  
✅ **Código Profesional**: Documentación, types, manejo de errores  
✅ **IA en Producción**: Integración de modelos transformer  
✅ **APIs RESTful**: Mejores prácticas con FastAPI  
✅ **Integración Enterprise**: Diseño para n8n y automatización  
✅ **Escalabilidad**: Estructura lista para crecer

---

**Desarrollado por**: [Tu Nombre]  
**Versión**: 2.0.0  
**Fecha**: Diciembre 2025
