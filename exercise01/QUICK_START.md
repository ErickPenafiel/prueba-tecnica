# 🚀 Guía de Inicio Rápido - Ejercicio 01 (SafeBank AI API)

## 📋 Requisitos Previos

- ✅ Python 3.9 o superior
- ✅ pip (gestor de paquetes de Python)
- ✅ API Key de NewsAPI (gratis) → [Obtener aquí](https://newsapi.org/register)

---

## 🏃 Inicio Rápido (5 pasos)

### 1️⃣ Crear Entorno Virtual

```powershell
# Navegar al directorio del ejercicio 01
cd exercise01

# Crear entorno virtual
python -m venv venv
```

### 2️⃣ Activar Entorno Virtual

**En Windows (PowerShell):**

```powershell
.\venv\Scripts\activate
```

**En Windows (CMD):**

```cmd
venv\Scripts\activate.bat
```

Deberías ver `(venv)` al inicio de tu línea de comando.

### 3️⃣ Instalar Dependencias

```powershell
# Instalar todas las dependencias
pip install -r requirements.txt
```

**Nota:** La primera instalación descargará ~2GB de modelos de IA (BART). Esto puede tardar varios minutos.

### 4️⃣ Configurar API Key de NewsAPI

**Opción A - Editar directamente el archivo de configuración:**

Abre [app/config.py](app/config.py) y encuentra la línea:

```python
NEWS_API_KEY: str = "TU_API_KEY_AQUI"
```

Reemplaza `TU_API_KEY_AQUI` con tu API key real de NewsAPI.

**Opción B - Usar archivo .env (recomendado):**

Crea un archivo `.env` en la raíz del ejercicio 01:

```bash
NEWS_API_KEY=tu_api_key_de_newsapi_aqui
```

### 5️⃣ Ejecutar el API

```powershell
# Ejecutar con auto-reload (modo desarrollo)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Deberías ver:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## ✅ Verificar que Funciona

### Opción 1: Navegador

Abre tu navegador en:

- **Documentación interactiva:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health
- **Endpoint principal:** http://localhost:8000

### Opción 2: cURL (desde otra terminal)

```powershell
# Health check
curl http://localhost:8000/health

# Analizar Tesla
curl "http://localhost:8000/api/v1/risk-analysis?company_name=Tesla"

# Analizar Apple
curl "http://localhost:8000/api/v1/risk-analysis?company_name=Apple"
```

### Respuesta Esperada

```json
{
	"status_code": 200,
	"message": "Análisis completado exitosamente",
	"data": {
		"company_name": "Tesla",
		"overall_risk_status": "warning",
		"overall_risk_score": 0.4521,
		"market_sentiment": "neutral",
		"sentiment_confidence": 0.8934,
		"compliance_status": "clear",
		"compliance_risk_type": "operación normal",
		"compliance_confidence": 0.7234,
		"requires_manual_review": true,
		"source_news_title": "Tesla Reports Q4 Earnings...",
		"source_url": "https://...",
		"analysis_timestamp": "2025-12-30T10:30:00Z"
	}
}
```

---

## 📚 Documentación Interactiva (Swagger)

Una vez que el API esté corriendo, visita:

**http://localhost:8000/docs**

Aquí puedes:

- 📖 Ver todos los endpoints disponibles
- 🎮 Probar el API directamente desde el navegador
- 📋 Ver los schemas de request/response
- 💡 Entender los parámetros requeridos

### Ejemplo de Uso en Swagger:

1. Haz clic en **GET /api/v1/risk-analysis**
2. Haz clic en **Try it out**
3. Ingresa en `company_name`: `Tesla`
4. Haz clic en **Execute**
5. Ve la respuesta en tiempo real

---

## 🔍 Endpoints Disponibles

### 1. Health Check

```http
GET /health
```

**Respuesta:**

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

### 2. Análisis de Riesgo (Principal)

```http
GET /api/v1/risk-analysis?company_name=Tesla
```

**Parámetros:**

- `company_name` (string, requerido): Nombre de la empresa a analizar

**Respuesta:** Ver ejemplo completo arriba

### 3. Análisis de Compliance (Individual)

```http
POST /api/v1/compliance/analyze
Content-Type: application/json

{
  "text": "La empresa fue acusada de lavado de dinero"
}
```

**Respuesta:**

```json
{
	"status_code": 200,
	"message": "Análisis completado exitosamente",
	"data": {
		"is_risk": true,
		"risk_category": "lavado de activos",
		"confidence": 0.9234,
		"analysis_timestamp": "2025-12-30T10:30:00Z"
	}
}
```

---

## 🧪 Ejecutar Tests

```powershell
# Ejecutar todos los tests
pytest

# Con más detalles
pytest -v

# Con cobertura de código
pytest --cov=app tests/

# Solo tests de compliance
pytest tests/test_compliance.py

# Solo tests de análisis de riesgo
pytest tests/test_risk_analysis.py
```

---

## 🐛 Troubleshooting

### Problema 1: Error al instalar dependencias

**Error:**

```
ERROR: Could not install packages due to an EnvironmentError
```

**Solución:**

```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Intentar de nuevo
pip install -r requirements.txt
```

### Problema 2: ModuleNotFoundError

**Error:**

```
ModuleNotFoundError: No module named 'app'
```

**Solución:**

```powershell
# Asegúrate de estar en el directorio correcto
cd exercise01

# Verifica que el entorno virtual esté activado
# Deberías ver (venv) en tu prompt

# Si no está activado:
.\venv\Scripts\activate
```

### Problema 3: Error con NewsAPI

**Error:**

```
HTTP 426 Upgrade Required
```

**Causa:** API key inválida o límite de requests excedido

**Soluciones:**

1. Verifica que tu API key sea correcta
2. Revisa cuota diaria (100 requests/día en plan free)
3. Espera 24 horas si alcanzaste el límite

### Problema 4: Modelos de IA muy lentos

**Primera ejecución:**

- Los modelos BART se descargan la primera vez (~1.6GB cada uno)
- Puede tardar 5-10 minutos según tu conexión
- Los modelos se cachean en `~/.cache/huggingface/`

**Ejecuciones siguientes:**

- Deberían tomar 3-5 segundos por análisis
- Si sigue lento, verifica RAM disponible (necesita ~4GB)

### Problema 5: Puerto 8000 ya en uso

**Error:**

```
Address already in use
```

**Solución:**

**Opción A - Usar otro puerto:**

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Opción B - Matar el proceso:**

```powershell
# Encontrar el proceso
netstat -ano | findstr :8000

# Matar el proceso (reemplaza PID con el número que encontraste)
taskkill /PID <PID> /F
```

---

## ⚙️ Configuración Avanzada

### Cambiar Modelos de IA

Edita [app/config.py](app/config.py):

```python
class Settings(BaseSettings):
    # Cambiar modelos
    COMPLIANCE_MODEL: str = "facebook/bart-large-mnli"
    SENTIMENT_MODEL: str = "facebook/bart-large-mnli"

    # Puedes usar otros modelos compatibles de Hugging Face
    # Ejemplo: "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
```

### Variables de Entorno

Crea archivo `.env` en `exercise01/`:

```bash
# NewsAPI
NEWS_API_KEY=tu_api_key_aqui

# Modelos de IA (opcional)
COMPLIANCE_MODEL=facebook/bart-large-mnli
SENTIMENT_MODEL=facebook/bart-large-mnli

# API Configuration
APP_TITLE=SafeBank AI - Risk Intelligence Platform
APP_VERSION=2.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

---

## 📊 Métricas de Rendimiento

| Operación                           | Tiempo Promedio | Notas                 |
| ----------------------------------- | --------------- | --------------------- |
| Primera ejecución (descarga models) | 5-10 min        | Solo la primera vez   |
| Análisis completo (con noticias)    | 3-5 seg         | Incluye NewsAPI + ML  |
| Solo análisis ML (texto dado)       | 1-2 seg         | Sin llamada a NewsAPI |
| Health check                        | < 50ms          | Sin procesamiento     |

---

## 🔗 Próximos Pasos

1. ✅ **API funcionando** → Continuar con Ejercicio 02 (n8n)
2. ✅ **Leer documentación completa:** [README.md](README.md)
3. ✅ **Explorar arquitectura:** [ARCHITECTURE.md](ARCHITECTURE.md)
4. ✅ **Entender compliance:** [COMPLIANCE_README.md](COMPLIANCE_README.md)

---

## 📞 Soporte

- 📚 **README Principal:** [README.md](README.md)
- 🏗️ **Arquitectura:** [ARCHITECTURE.md](ARCHITECTURE.md)
- 📖 **Documentación Swagger:** http://localhost:8000/docs
- 🐛 **Issues:** GitHub Issues del proyecto

---

**¡Listo!** Tu API de SafeBank AI está corriendo. 🎉

Ahora puedes:

1. Probarlo con diferentes empresas
2. Integrarlo con el Ejercicio 02 (n8n)
3. Explorar la documentación completa

Para usar con n8n, **mantén este API corriendo** y ve al ejercicio 02.
