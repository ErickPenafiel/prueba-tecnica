# SafeBank AI - Compliance Engine

## 📋 Descripción

Microservicio en FastAPI que analiza riesgos de cumplimiento bancario mediante:

- Búsqueda de noticias relacionadas con clientes (NewsAPI)
- Análisis de IA con modelo BART Large para clasificación de riesgos

## 🏗️ Arquitectura

El proyecto sigue una arquitectura en capas:

```
app/
├── main.py                          # Aplicación FastAPI principal
├── config.py                        # Configuración centralizada
├── models.py                        # Modelos Pydantic
├── exceptions.py                    # Excepciones personalizadas
├── api/
│   └── routes.py                   # Endpoints de la API
└── services/
    ├── news_service.py             # Servicio de noticias (NewsAPI)
    ├── compliance_service.py       # Servicio de análisis de riesgos (IA)
    ├── weather_service.py          # [LEGACY] Servicio de clima
    └── ml_service.py               # [LEGACY] Sentimiento de clima
```

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota**: La primera ejecución descargará el modelo BART Large (~1GB). Esto puede tomar varios minutos.

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
NEWS_API_KEY=tu_api_key_de_newsapi
OPENWEATHER_API_KEY=tu_api_key_de_openweather  # (opcional, para endpoint legacy)
```

Obtén tu API key gratuita en: https://newsapi.org/

### 3. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## 📡 Endpoints

### Compliance Check (Principal)

**GET** `/api/v1/compliance-check?client_name={nombre}`

Analiza riesgos de compliance de un cliente buscando noticias y clasificándolas con IA.

**Parámetros:**

- `client_name` (str): Nombre del cliente a consultar

**Respuesta exitosa (clear):**

```json
{
	"client": "Empresa ABC",
	"status": "clear",
	"risk_score": 0.0,
	"message": "No se encontraron registros adversos."
}
```

**Respuesta con alerta:**

```json
{
	"client": "Empresa XYZ",
	"status": "alert",
	"risk_score": 0.4523,
	"analysis": {
		"top_risk": "fraude financiero",
		"confidence": 0.4523,
		"evidence_snippet": "Empresa XYZ investigada por irregularidades contables"
	}
}
```

### Health Check

**GET** `/health`

Verifica el estado de la API.

### Documentación Interactiva

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Configuración Avanzada

En [app/config.py](app/config.py) puedes modificar:

```python
# Umbral de confianza para alertas (default: 0.35)
RISK_THRESHOLD: float = 0.35

# Etiquetas de riesgo evaluadas
RISK_LABELS: list = [
    "fraude financiero",
    "lavado de activos",
    "corrupción",
    "quiebra",
    "operación normal"
]
```

## 🧪 Ejemplos de Uso

### Con curl:

```bash
curl "http://localhost:8000/api/v1/compliance-check?client_name=Tesla"
```

### Con Python:

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/compliance-check",
    params={"client_name": "Tesla"}
)
print(response.json())
```

## 🎯 Lógica de Decisión

1. **Búsqueda**: Consulta noticias relacionadas al cliente en NewsAPI
2. **Sin resultados**: Retorna status "clear" (sin riesgos)
3. **Con resultados**: Analiza el artículo más relevante con modelo BART
4. **Clasificación**: Determina la categoría de riesgo más probable
5. **Decisión**:
   - Si la categoría es "fraude financiero", "lavado de activos" o "corrupción"
   - Y la confianza > 0.35 (umbral configurable)
   - Entonces: status "alert"
   - Sino: status "clear"

## 🔒 Consideraciones de Seguridad

- Nunca subas el archivo `.env` al repositorio
- Usa variables de entorno en producción
- Considera implementar rate limiting
- Implementa autenticación para endpoints sensibles

## 📊 Modelo de IA

- **Modelo**: `facebook/bart-large-mnli`
- **Tipo**: Zero-shot classification
- **Tamaño**: ~1.6GB
- **Idioma**: Multilingüe (optimizado para inglés, funciona en español)

## 🐛 Troubleshooting

### Error: "NEWS_API_KEY no está configurada"

- Verifica que el archivo `.env` existe y contiene `NEWS_API_KEY`

### Error al descargar el modelo

- Verifica tu conexión a internet
- El modelo se descarga en la primera ejecución (~1GB)
- Se cachea en `~/.cache/huggingface/`

### Límite de consultas excedido

- NewsAPI free tier: 100 consultas/día
- Considera upgrade o implementar caché

## 📝 Licencia

MIT
