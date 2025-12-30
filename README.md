# 🏆 Prueba Técnica FinUp - Sistema Integral de Análisis de Riesgos

## 📋 Descripción General

Este repositorio contiene la solución completa para la prueba técnica de FinUp, que consiste en un **sistema integral de inteligencia de riesgos empresariales** compuesto por dos ejercicios complementarios:

1. **Ejercicio 01 - SafeBank AI**: API de análisis de riesgos con Inteligencia Artificial
2. **Ejercicio 02 - Automatización n8n**: Orquestador de workflows que integra y automatiza el análisis

---

## 🎯 Objetivo del Proyecto

Crear un sistema automatizado que permita a instituciones financieras:

- ✅ **Monitorear riesgos reputacionales** mediante análisis de noticias en tiempo real
- ✅ **Detectar riesgos de compliance** (fraude, lavado de activos, corrupción)
- ✅ **Analizar sentimiento de mercado** usando modelos de IA avanzados
- ✅ **Automatizar reportes** con integración a Google Workspace
- ✅ **Reducir tiempo de respuesta** de días a minutos

---

## 🏗️ Arquitectura Global del Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SISTEMA INTEGRAL FINUP                           │
└─────────────────────────────────────────────────────────────────────┘

                               ┌─────────────────────┐
                               │   EJERCICIO 02      │
                               │   n8n Automation    │
                               │   (Port: 5678)      │
                               │                     │
                               │  • Schedule Trigger │
                               │  • Google Sheets    │
                               │  • Gmail Reports    │
                               │  • Workflow Engine  │
                               └──────────┬──────────┘
                                          │
                            HTTP Request  │  GET /api/v1/risk-analysis
                                          │
                                          ▼
                               ┌─────────────────────┐
                               │   EJERCICIO 01      │
                               │   SafeBank AI API   │
                               │   (Port: 8000)      │
                               │                     │
                               │  • FastAPI          │
                               │  • Zero-Shot ML     │
                               │  • Sentiment AI     │
                               │  • NewsAPI          │
                               └──────────┬──────────┘
                                          │
                         ┌────────────────┼────────────────┐
                         │                │                │
                         ▼                ▼                ▼
              ┌──────────────┐  ┌─────────────┐  ┌──────────────┐
              │   NewsAPI    │  │ Zero-Shot   │  │  Sentiment   │
              │   (Noticias) │  │ Classifier  │  │  Analyzer    │
              │              │  │ BART-MNLI   │  │  BART-MNLI   │
              └──────────────┘  └─────────────┘  └──────────────┘
```

### Flujo de Datos

1. **n8n** (Ejercicio 02) lee lista de empresas desde Google Sheets
2. Para cada empresa, envía request a **SafeBank AI API** (Ejercicio 01)
3. **SafeBank AI** busca noticias recientes de la empresa vía NewsAPI
4. Ejecuta análisis de IA:
   - **Zero-Shot Classification**: Detecta riesgos de compliance
   - **Sentiment Analysis**: Evalúa sentimiento de mercado
5. Retorna resultado estructurado a n8n
6. **n8n** procesa resultados, guarda en Google Sheets y envía reportes por Gmail

---

## 📁 Estructura del Repositorio

```
FinUp/
├── README.md                          # ← Este archivo (documentación general)
│
├── exercise01/                        # Ejercicio 1: SafeBank AI API
│   ├── README.md                      # Documentación detallada del API
│   ├── ARCHITECTURE.md                # Decisiones de arquitectura
│   ├── COMPLIANCE_README.md           # Análisis de compliance
│   ├── README_RISK_INTELLIGENCE.md    # Motor de inteligencia de riesgos
│   ├── REFACTORING_SUMMARY.md         # Mejoras implementadas
│   ├── requirements.txt               # Dependencias Python
│   ├── app/
│   │   ├── main.py                    # Entry point FastAPI
│   │   ├── config.py                  # Configuración
│   │   ├── models.py                  # Modelos Pydantic
│   │   ├── ml_model.py                # Carga de modelos IA
│   │   ├── api/
│   │   │   └── routes.py              # Endpoints del API
│   │   └── services/
│   │       ├── compliance_service.py  # Zero-Shot Classification
│   │       ├── sentiment_service.py   # Sentiment Analysis
│   │       ├── news_service.py        # Integración NewsAPI
│   │       └── ml_service.py          # Orquestador ML
│   └── tests/
│       ├── test_compliance.py
│       └── test_risk_analysis.py
│
└── exercise02/                        # Ejercicio 2: Automatización n8n
    ├── README.md                      # Documentación detallada de n8n
    ├── QUICK_START.md                 # Guía de inicio rápido
    ├── docker-compose.yml             # Configuración Docker
    ├── .env.example                   # Plantilla de variables de entorno
    ├── workflows/                     # ⭐ Workflows exportados de n8n
    │   ├── README.md                  # Documentación del workflow
    │   └── workflow-riesgos.json      # Workflow completo (importable)
    ├── n8n_data/                      # Datos persistentes de n8n (generado)
    └── local-files/                   # Archivos compartidos con workflows
```

---

## 🚀 Guía de Instalación Rápida

### 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- ✅ **Python 3.9+** → [Descargar](https://www.python.org/downloads/)
- ✅ **Docker Desktop** → [Descargar](https://www.docker.com/products/docker-desktop)
- ✅ **Git** → [Descargar](https://git-scm.com/downloads)
- ✅ **Cuenta NewsAPI** (gratis) → [Registrarse](https://newsapi.org/register)
- ✅ **Cuenta Google Cloud** (para Gmail/Sheets - opcional) → [Registrarse](https://console.cloud.google.com/)

---

## ⚡ Inicio Rápido en 5 Minutos

### Opción 1: Guías de Inicio Rápido (Recomendado)

Cada ejercicio tiene su propia guía de inicio rápido con instrucciones paso a paso:

1. **📘 [Ejercicio 01 - QUICK_START.md](exercise01/QUICK_START.md)**

   - Setup del API de SafeBank AI
   - Instalación de dependencias y modelos de IA
   - ~5 minutos (primera vez incluye descarga de modelos)

2. **📗 [Ejercicio 02 - QUICK_START.md](exercise02/QUICK_START.md)**
   - Setup de n8n y automatización
   - Importación de workflows
   - ~3 minutos

### Opción 2: Setup Manual Completo

### Paso 1: Clonar el Repositorio

```powershell
git clone <url-del-repositorio>
cd FinUp
```

### Paso 2: Configurar y Ejecutar Ejercicio 01 (SafeBank AI API)

```powershell
# Navegar al directorio del ejercicio 01
cd exercise01

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API Key de NewsAPI
# Editar app/config.py y agregar tu API key
# O crear archivo .env con: NEWS_API_KEY=tu_api_key_aqui

# Ejecutar el API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verificar funcionamiento:**

- Abrir navegador en: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Paso 3: Configurar y Ejecutar Ejercicio 02 (n8n)

**En una nueva terminal:**

```powershell
# Navegar al directorio del ejercicio 02
cd ..\exercise02

# Crear archivo de configuración
cp .env.example .env

# Editar .env y cambiar la contraseña
# N8N_BASIC_AUTH_PASSWORD=tu_contraseña_segura

# Levantar n8n con Docker
docker-compose up -d

# Verificar que está corriendo
docker ps
```

**Acceder a n8n:**

- URL: http://localhost:5678
- Usuario: `admin`
- Contraseña: la que configuraste en `.env`

### Paso 4: Configurar Google Cloud (Opcional para notificaciones)

1. Crear proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar APIs: Gmail, Google Sheets, Google Drive
3. Crear credenciales OAuth 2.0
4. Configurar en n8n (ver documentación del Ejercicio 02)

---

## 🎮 Uso del Sistema

### Ejemplo 1: Consulta Directa al API (Ejercicio 01)

```powershell
# Analizar riesgo de Tesla
curl "http://localhost:8000/api/v1/risk-analysis?company_name=Tesla"
```

**Respuesta esperada:**

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

### Ejemplo 2: Workflow Automatizado (Ejercicio 02)

1. **Acceder a n8n:** http://localhost:5678

2. **Importar workflow pre-configurado:**

   - Ir a **Workflows** → **Import from File**
   - Seleccionar: `exercise02/workflows/workflow-riesgos.json`

3. **El workflow incluye 14 nodos interconectados:**

   **Flujo automático completo:**

   ```
   Schedule (8 AM) → Drive: Buscar "monitoring_list"
   → IF: ¿Existe? → NO: Crear + Poblar empresas
                  → SI: Leer empresas
   → HTTP Request: API Exercise01 (por cada empresa)
   → IF: ¿Status 200? → NO: Email de error
                       → SI: Drive: Buscar "monitoring_register"
                             → IF: ¿Existe? → NO: Crear sheet
                                            → SI: Continuar
                             → JS: Formatear datos
                             → Sheets: Guardar análisis
                             → Email: Reporte exitoso
   ```

   **Características integradas:**

   - ✅ Gestión automática de Google Sheets (creación si no existen)
   - ✅ Lista de empresas: Tesla, Apple, Luis Arce (editable)
   - ✅ Llamadas al API: `http://host.docker.internal:8000/api/v1/risk-analysis`
   - ✅ Formateo de 12 campos: timestamp, company, risk_status, risk_score, sentiment, compliance_type, evidence, URL, manual_review, etc.
   - ✅ Manejo de errores: Rama alternativa con email de alerta
   - ✅ Retry logic: HTTP Request configurado con reintentos automáticos
   - ✅ Emails detallados: Templates con todos los detalles del análisis

4. **Configurar credenciales necesarias:**

   - Google Sheets OAuth2 (3 nodos)
   - Google Drive OAuth2 (2 nodos)
   - SMTP para emails (2 nodos - actualizar direcciones)

5. **Activar workflow** (toggle superior derecho)
   - Se ejecutará automáticamente todos los días a las 8:00 AM
   - Monitorear ejecuciones en la pestaña "Executions"

**Ver documentación completa del workflow:**

- [exercise02/workflows/README.md](exercise02/workflows/README.md) - Arquitectura detallada
- [exercise02/README.md](exercise02/README.md) - Guía completa de configuración
- [exercise02/QUICK_START.md](exercise02/QUICK_START.md) - Inicio rápido

---

## 📊 Características Principales

### Ejercicio 01 - SafeBank AI API

| Característica               | Descripción                                                | Tecnología              |
| ---------------------------- | ---------------------------------------------------------- | ----------------------- |
| **Zero-Shot Classification** | Detecta riesgos sin datos etiquetados previos              | BART-Large-MNLI (1.6GB) |
| **Sentiment Analysis**       | Analiza sentimiento de mercado (positivo/neutral/negativo) | BART-Large-MNLI         |
| **News Integration**         | Ingesta automática de noticias recientes                   | NewsAPI                 |
| **Risk Scoring**             | Cálculo de score de riesgo global (0-1)                    | Algoritmo propietario   |
| **API Documentation**        | Swagger/OpenAPI interactivo                                | FastAPI                 |
| **Asynchronous Processing**  | Procesamiento no bloqueante                                | async/await Python      |
| **Error Handling**           | Manejo robusto de errores y timeouts                       | Custom exceptions       |

**Categorías de Riesgo Detectadas:**

- 🚨 Fraude financiero
- 💰 Lavado de activos (AML)
- 🤝 Corrupción
- 📉 Quiebra/Insolvencia
- ✅ Operación normal

### Ejercicio 02 - Automatización n8n

| Característica                | Descripción                                       | Integración/Tecnología |
| ----------------------------- | ------------------------------------------------- | ---------------------- |
| **Scheduled Execution**       | Ejecución diaria automática a las 8:00 AM         | Schedule Trigger       |
| **Google Drive Integration**  | Búsqueda y verificación de sheets existentes      | Google Drive API       |
| **Google Sheets Integration** | Lectura/escritura automática de datos             | Google Sheets API      |
| **Dynamic Sheet Creation**    | Crea sheets automáticamente si no existen         | Conditional Logic + IF |
| **Gmail Automation**          | Emails de éxito y error con templates detallados  | SMTP (Gmail)           |
| **API Orchestration**         | Llamadas HTTP al API del Ejercicio 01 por empresa | HTTP Request Node      |
| **Data Transformation**       | Formateo de 12 campos del API a formato Sheets    | Code Node (JavaScript) |
| **Conditional Logic**         | 3 validaciones IF (sheets, status, errores)       | IF Nodes               |
| **Error Recovery**            | Rama alternativa con email de alerta + retry      | Error Handling + Retry |
| **Persistent Storage**        | Workflows, credenciales y datos persistentes      | SQLite + Docker Volume |
| **Default Companies**         | Lista inicial: Tesla, Apple, Luis Arce            | JavaScript Code        |
| **14-Node Architecture**      | Workflow completo con gestión end-to-end          | n8n Workflow Engine    |
| **Retry Logic**               | HTTP Request con reintentos automáticos           | retryOnFail: true      |
| **Detailed Reporting**        | Emails con timestamp, risk_status, evidence, etc. | Email Templates        |

**Google Sheets Gestionados Automáticamente:**

- 📊 **monitoring_list**: Lista de empresas a monitorear (sheet: "list")
- 📊 **monitoring_register**: Registro histórico de análisis (sheet: "registros")

**Datos Capturados (12 campos):**
timestamp_analisis, status, message, company, registration_date, risk_status, risk_score, sentiment, compliance_type, evidence, url, manual_review

---

## 🧪 Testing

### Ejercicio 01 - Unit Tests

```powershell
cd exercise01

# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app tests/

# Tests específicos
pytest tests/test_compliance.py
pytest tests/test_risk_analysis.py
```

### Ejercicio 02 - Manual Testing

```powershell
# Verificar conectividad desde n8n
docker exec -it $(docker ps -qf "name=n8n") /bin/sh
curl http://host.docker.internal:8000/health

# Ver logs de n8n
docker-compose logs -f
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno - Ejercicio 01

Crear archivo `exercise01/.env`:

```bash
# NewsAPI Configuration
NEWS_API_KEY=tu_api_key_de_newsapi

# API Configuration
APP_TITLE=SafeBank AI - Risk Intelligence Platform
APP_VERSION=2.0.0
API_PORT=8000

# ML Models (opcional - usa defaults si no se especifica)
COMPLIANCE_MODEL=facebook/bart-large-mnli
SENTIMENT_MODEL=facebook/bart-large-mnli
```

### Variables de Entorno - Ejercicio 02

Editar `exercise02/.env`:

```bash
# n8n Configuration
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
WEBHOOK_URL=http://localhost:5678/
GENERIC_TIMEZONE=America/La_Paz

# Autenticación
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=TU_CONTRASEÑA_SEGURA

# SafeBank AI API (Ejercicio 01)
FASTAPI_HOST=host.docker.internal
FASTAPI_PORT=8000
FASTAPI_BASE_URL=http://host.docker.internal:8000
```

---

## 📈 Casos de Uso

### 1. Monitoreo de Cartera de Inversiones

**Escenario:** Hedge fund monitorea 100 empresas diariamente

**Implementación:**

```
Google Sheets (100 empresas)
→ Loop en n8n
→ API Risk Analysis para cada una
→ Guardar resultados
→ Email diario con resumen
```

### 2. Alertas de Compliance en Tiempo Real

**Escenario:** Detección inmediata de riesgos AML/KYC

**Implementación:**

```
n8n Schedule (cada 2 horas)
→ API Risk Analysis
→ IF (compliance_status === "alert")
→ SMS urgente + Email + Ticket Jira
```

### 3. Due Diligence Automatizado

**Escenario:** Análisis previo a inversión en startup

**Implementación:**

```
Webhook trigger (nuevo deal en CRM)
→ API Risk Analysis
→ Guardar en base de datos
→ Notificar equipo de inversiones
```

---

## 🐛 Troubleshooting Común

### Problema: n8n no puede conectarse al API

**Error:**

```
connect ECONNREFUSED host.docker.internal:8000
```

**Soluciones:**

1. Verificar que el API está corriendo: `curl http://localhost:8000/health`
2. Verificar puerto: `netstat -ano | findstr :8000`
3. Usar IP del host en lugar de `host.docker.internal`
4. Actualizar Docker Desktop a última versión

### Problema: Modelos de IA muy lentos en primera ejecución

**Causa:** Descarga inicial de modelos (1.6GB cada uno)

**Solución:**

- Esperar a que descarguen completamente
- Los modelos se cachean en `~/.cache/huggingface/`
- Ejecuciones subsecuentes serán más rápidas (2-5 segundos)

### Problema: NewsAPI devuelve error 426

**Error:**

```
HTTP 426 Upgrade Required
```

**Causa:** Plan gratuito de NewsAPI con límites

**Solución:**

1. Verificar cuota diaria (100 requests/día en plan free)
2. Implementar caché de resultados en n8n
3. Reducir frecuencia de ejecución del workflow

---

## 📚 Documentación Adicional

### Documentos por Ejercicio

**Ejercicio 01:**

- [README.md](exercise01/README.md) - Guía completa del API
- [ARCHITECTURE.md](exercise01/ARCHITECTURE.md) - Decisiones de diseño
- [COMPLIANCE_README.md](exercise01/COMPLIANCE_README.md) - Sistema de compliance
- [README_RISK_INTELLIGENCE.md](exercise01/README_RISK_INTELLIGENCE.md) - Motor de IA

**Ejercicio 02:**

- [README.md](exercise02/README.md) - Guía completa de n8n
- [docker-compose.yml](exercise02/docker-compose.yml) - Configuración de Docker

### Enlaces Externos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [n8n Documentation](https://docs.n8n.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [Google Cloud APIs](https://cloud.google.com/apis/docs)

---

## 🎯 Tecnologías Utilizadas

### Backend (Ejercicio 01)

| Tecnología   | Versión | Propósito                    |
| ------------ | ------- | ---------------------------- |
| Python       | 3.9+    | Lenguaje base                |
| FastAPI      | 0.115+  | Framework API REST           |
| Transformers | 4.37+   | Modelos de IA (Hugging Face) |
| PyTorch      | 2.0+    | Framework de Deep Learning   |
| Pydantic     | 2.0+    | Validación de datos          |
| Uvicorn      | 0.27+   | ASGI Server                  |
| Requests     | 2.31+   | Cliente HTTP para NewsAPI    |

### Automatización (Ejercicio 02)

| Tecnología     | Versión | Propósito                 |
| -------------- | ------- | ------------------------- |
| n8n            | latest  | Motor de automatización   |
| Docker         | 20.10+  | Containerización          |
| Docker Compose | 2.0+    | Orquestación de servicios |
| Google APIs    | -       | Gmail, Sheets, Drive      |

### Modelos de IA

| Modelo                   | Tamaño | Uso                      |
| ------------------------ | ------ | ------------------------ |
| facebook/bart-large-mnli | 1.6GB  | Zero-Shot Classification |
| facebook/bart-large-mnli | 1.6GB  | Sentiment Analysis       |

---

## 🏆 Decisiones de Diseño Destacadas

### 1. Zero-Shot Learning vs Supervised Learning

**Decisión:** Usar Zero-Shot Classification

**Justificación:**

- ✅ No requiere datasets etiquetados históricos
- ✅ Adaptable a nuevas categorías sin reentrenamiento
- ✅ Reduce time-to-market
- ✅ Evita sesgos de datos históricos

### 2. FastAPI vs Flask/Django

**Decisión:** FastAPI

**Justificación:**

- ✅ Alto rendimiento (comparable a Node.js/Go)
- ✅ Asíncrono nativo (ideal para llamadas a APIs externas)
- ✅ Validación automática con Pydantic
- ✅ Documentación OpenAPI auto-generada
- ✅ Type hints nativos (mejor mantenibilidad)

### 3. n8n vs Airflow/Prefect

**Decisión:** n8n

**Justificación:**

- ✅ UI visual intuitiva (no requiere código)
- ✅ Integraciones pre-construidas (Gmail, Sheets, etc.)
- ✅ Deployment simple con Docker
- ✅ Ideal para automatizaciones de negocio
- ✅ Community edition gratuita

### 4. Arquitectura en Capas

**Decisión:** Separación API Layer / Service Layer / ML Layer

**Justificación:**

- ✅ Testabilidad independiente
- ✅ Escalabilidad por capas
- ✅ Mantenibilidad (cambios aislados)
- ✅ Reusabilidad de servicios

---

## 📊 Métricas de Rendimiento

### Ejercicio 01 - API Performance

| Operación                           | Tiempo Promedio | Notas                 |
| ----------------------------------- | --------------- | --------------------- |
| Primera ejecución (descarga models) | 5-10 min        | Solo primera vez      |
| Análisis completo (con noticias)    | 3-5 seg         | Incluye NewsAPI + ML  |
| Solo análisis ML (texto dado)       | 1-2 seg         | Sin llamada a NewsAPI |
| Health check                        | < 50ms          | Sin procesamiento     |

### Ejercicio 02 - Workflow Performance

| Operación                | Tiempo Promedio | Notas                             |
| ------------------------ | --------------- | --------------------------------- |
| Análisis de 1 empresa    | 5-7 seg         | API call + formateo + sheet write |
| Análisis de 10 empresas  | 50-70 seg       | Secuencial (sin paralelización)   |
| Análisis de 100 empresas | ~10 min         | Con batching de 5 empresas        |
| Envío de email           | 1-2 seg         | Con Gmail API                     |

**Optimizaciones posibles:**

- Implementar paralelización en n8n (procesamiento simultáneo)
- Cachear resultados de empresas por N horas
- Usar queue system (RabbitMQ/Redis) para análisis masivos

---

## 🔐 Seguridad y Mejores Prácticas

### Implementadas

- ✅ Autenticación básica en n8n
- ✅ Variables de entorno para secretos
- ✅ Validación de inputs con Pydantic
- ✅ Manejo de errores personalizado
- ✅ Rate limiting consideration (NewsAPI)
- ✅ CORS configuration en FastAPI

### Recomendadas para Producción

- 🔒 Implementar OAuth 2.0 / JWT en el API
- 🔒 HTTPS con certificados SSL/TLS
- 🔒 API Keys con rate limiting por cliente
- 🔒 Secrets management (AWS Secrets Manager, Azure Key Vault)
- 🔒 Logging estructurado (ELK Stack)
- 🔒 Monitoring y alertas (Prometheus + Grafana)
- 🔒 Database persistence para resultados
- 🔒 Kubernetes para escalabilidad

---

## 📞 Soporte y Contacto

### Recursos

- 📧 **Email:** [tu-email@ejemplo.com]
- 🐛 **Issues:** GitHub Issues del repositorio
- 📚 **Wiki:** Documentación extendida en Wiki del repo

### Preguntas Frecuentes

**¿Puedo usar otros modelos de IA?**

- Sí, el código está diseñado para ser modular. Puedes cambiar los modelos en `app/config.py`

**¿Funciona con otras fuentes de noticias?**

- Actualmente solo NewsAPI, pero puedes agregar servicios en `app/services/news_service.py`

**¿Puedo desplegar en la nube?**

- Sí, ambos ejercicios son cloud-ready. Ver sección de deployment en cada README.

**¿Qué pasa si supero el límite de NewsAPI?**

- Plan Free: 100 requests/día. Solución: cachear resultados o upgrade a plan Developer

---

## 🚀 Próximos Pasos y Roadmap

### Mejoras Planificadas

- [ ] **Persistencia de datos:** PostgreSQL/MongoDB para histórico de análisis
- [ ] **Dashboard interactivo:** Frontend con React/Vue para visualización
- [ ] **Análisis multi-idioma:** Soporte para noticias en inglés, español, etc.
- [ ] **Machine Learning avanzado:** Fine-tuning de modelos con datos específicos de fintech
- [ ] **Alertas en tiempo real:** WebSockets para notificaciones push
- [ ] **Integración con Bloomberg/Reuters:** Fuentes de datos premium
- [ ] **API pública:** Rate limiting, API keys, planes de pricing
- [ ] **Mobile app:** Aplicación móvil para alertas

---

## 📄 Licencia

Este proyecto fue desarrollado como parte de una **prueba técnica para FinUp**.

**Uso:** Educativo y demostrativo  
**Autor:** [Tu Nombre]  
**Fecha:** Diciembre 2025

---

## ✨ Agradecimientos

- **Hugging Face** por los modelos pre-entrenados
- **FastAPI** por el excelente framework
- **n8n** por la plataforma de automatización
- **NewsAPI** por el acceso a noticias globales
- **FinUp** por la oportunidad de desarrollar este proyecto

---

## 🎓 Conclusión

Este proyecto demuestra la integración completa de:

1. ✅ **APIs modernas** con FastAPI y documentación interactiva
2. ✅ **Inteligencia Artificial** con modelos state-of-the-art (BART)
3. ✅ **Automatización de workflows** con n8n
4. ✅ **Integración cloud** con Google Workspace
5. ✅ **DevOps** con Docker y Docker Compose
6. ✅ **Buenas prácticas** de arquitectura y clean code

El sistema está listo para ser extendido y desplegado en producción con las mejoras de seguridad y escalabilidad mencionadas.

---

**🎯 Desarrollado con 💙 para FinUp**  
**📅 Diciembre 2025**
