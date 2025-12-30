# 🚀 Ejercicio 02: Automatización con n8n - Integración con SafeBank AI

## 📋 Descripción del Proyecto

Sistema automatizado de análisis de riesgo corporativo que **se conecta directamente con el API de SafeBank AI (Ejercicio 01)** para evaluar empresas de forma continua. Este workflow de n8n orquesta el análisis automatizado de múltiples empresas, consultando el API FastAPI del Exercise 01, procesando resultados y generando reportes automatizados.

**Características principales:**

- ⏰ Ejecución programada con triggers configurables (diaria/horaria)
- 🔗 **Integración directa con el API de SafeBank AI del Ejercicio 01**
- 📊 Ingesta y procesamiento de datos en Google Sheets
- 🤖 Análisis automático de riesgo usando ML (Zero-Shot Classification + Sentiment Analysis)
- 📧 Envío automático de reportes por Gmail
- 🔄 Gestión dinámica de hojas de cálculo (creación automática si no existen)
- 🔍 Verificación automática de archivos en Google Drive

---

## 🏗️ Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────────┐
│                     EJERCICIO 02 - n8n                       │
│                  (Docker Container: 5678)                    │
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │           Workflow de Automatización              │      │
│  │  1. Schedule Trigger (diario/horario)            │      │
│  │  2. Google Sheets: Leer lista de empresas        │      │
│  │  3. Loop sobre cada empresa                      │      │
│  │  4. HTTP Request → FastAPI (Exercise 01)         │      │
│  │  5. Procesamiento de resultados                  │      │
│  │  6. Google Sheets: Guardar análisis              │      │
│  │  7. Gmail: Enviar reportes                       │      │
│  └──────────────────────────────────────────────────┘      │
└──────────────────┬───────────────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
┌────────────────────┐  ┌──────────────────────┐
│  EJERCICIO 01      │  │  Google Cloud APIs   │
│  SafeBank AI API   │  │  ─────────────────   │
│  (FastAPI)         │  │  • Gmail API         │
│                    │  │  • Sheets API        │
│  host.docker       │  │  • Drive API         │
│  .internal:8000    │  │                      │
│                    │  └──────────────────────┘
│  GET /api/v1/      │
│    risk-analysis   │
│                    │
└────────────────────┘
```

**Componentes:**

- **n8n (Docker)**: Motor de automatización ejecutándose en contenedor Docker
- **SafeBank AI API (Ejercicio 01)**: API FastAPI con análisis de riesgo usando ML (host.docker.internal:8000)
- **Google Workspace**: Suite de servicios (Gmail, Sheets, Drive) para almacenamiento y notificaciones
- **Docker Compose**: Orquestación de servicios

---

## 📦 Requisitos Previos

### Software Necesario

- 🐳 **Docker** (v20.10 o superior) - [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop)
- 🐙 **Docker Compose** (v2.0 o superior) - Incluido en Docker Desktop
- 🐍 **Python 3.9+** - Para ejecutar el API de SafeBank AI (Ejercicio 01)
- 🌐 **Cuenta de Google Cloud Platform** con APIs habilitadas
- 🔑 **Credenciales OAuth 2.0** de Google Workspace

### ⚠️ Dependencia Crítica: Ejercicio 01

**IMPORTANTE**: Este ejercicio requiere que el **Ejercicio 01 (SafeBank AI API)** esté ejecutándose antes de iniciar n8n.

1. **Primero ejecuta el Ejercicio 01:**

   ```powershell
   # Navegar al directorio del Ejercicio 01
   cd ..\exercise01

   # Crear entorno virtual
   python -m venv venv

   # Activar entorno virtual (Windows)
   .\venv\Scripts\activate

   # Instalar dependencias
   pip install -r requirements.txt

   # Ejecutar el API
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verificar que el API esté funcionando:**
   - Abre tu navegador en: [http://localhost:8000](http://localhost:8000)
   - Deberías ver: `{"service": "FinUp Risk Intelligence Platform", ...}`
   - Documentación interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)

### APIs de Google a Habilitar

1. **Gmail API** - Para envío de reportes
2. **Google Sheets API** - Para lectura/escritura de datos
3. **Google Drive API** - Para gestión de archivos

**Guía rápida:** Visita [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Enable APIs

**Configurar OAuth 2.0:**

1. Ve a APIs & Services → Credentials
2. Crea credenciales de tipo "OAuth 2.0 Client ID"
3. Tipo de aplicación: "Desktop app"
4. Descarga el JSON de credenciales
5. Configura las credenciales en n8n (ver sección de configuración)

---

## 🐳 Configuración de Docker

### docker-compose.yml

El proyecto utiliza la siguiente configuración de Docker Compose con soporte para comunicación con el API del Ejercicio 01:

```yaml
version: "3.8"

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: unless-stopped

    ports:
      - "${N8N_PORT:-5678}:5678"

    environment:
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=5678
      - N8N_PROTOCOL=${N8N_PROTOCOL}
      - WEBHOOK_URL=${WEBHOOK_URL}
      - GENERIC_TIMEZONE=${GENERIC_TIMEZONE}
      - TZ=${GENERIC_TIMEZONE}

      # Seguridad: auth básica
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD}

      - NODE_ENV=production

    volumes:
      # Datos persistentes de n8n
      - ./n8n_data:/home/node/.n8n
      # Carpeta para leer/escribir archivos desde los flujos
      - ./local-files:/files
```

### 🔌 Conexión con el API de SafeBank AI (Ejercicio 01)

Para conectar n8n con el API de FastAPI que corre en tu máquina host, utiliza la siguiente URL:

**URL del API para usar en n8n:**

```
http://host.docker.internal:8000
```

**Endpoints disponibles del Ejercicio 01:**

1. **Análisis de Riesgo (Principal):**

   ```
   GET http://host.docker.internal:8000/api/v1/risk-analysis?company_name=Tesla
   ```

2. **Health Check:**

   ```
   GET http://host.docker.internal:8000/health
   ```

3. **Documentación interactiva:**
   - Desde el host: http://localhost:8000/docs
   - Desde n8n: http://host.docker.internal:8000/docs

### 🔧 Configuración Alternativa (si host.docker.internal no funciona)

Si estás en una versión antigua de Docker, agrega esta configuración a `docker-compose.yml`:

```yaml
services:
  n8n:
    # ... configuración existente ...
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

**Opción 2 - Usar la IP del host (fallback):**

En Windows, encuentra tu IP local:

```powershell
ipconfig
# Busca la IPv4 Address de tu red activa (ej: 192.168.1.100)
```

Luego usa:

```
http://192.168.1.100:8000/api/v1/risk-analysis?company_name=Tesla
```

### 📁 Volúmenes Configurados

- **`./n8n_data:/home/node/.n8n`** - Persistencia de workflows, credenciales y base de datos de n8n
- **`./local-files:/files`** - Carpeta compartida para lectura/escritura de archivos desde workflows

---

## 🚀 Guía de Instalación y Ejecución

### Paso 1: Asegurarse de que el Ejercicio 01 está corriendo

```powershell
# Terminal 1 - Ejecutar el API de SafeBank AI
cd ..\exercise01
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verifica que esté funcionando:

```powershell
# Probar el endpoint
curl http://localhost:8000/health
```

### Paso 2: Configurar variables de entorno

```powershell
# En el directorio exercise02
cp .env.example .env
```

Edita el archivo `.env` y cambia la contraseña:

```bash
N8N_BASIC_AUTH_PASSWORD=tu_contraseña_segura_aqui
```

### Paso 3: Levantar n8n con Docker Compose

```powershell
# Terminal 2 - En el directorio exercise02
docker-compose up -d
```

Verificar que el contenedor está corriendo:

```powershell
docker ps
```

Deberías ver:

```
CONTAINER ID   IMAGE                              STATUS         PORTS
xxxxx          docker.n8n.io/n8nio/n8n:latest    Up 2 minutes   0.0.0.0:5678->5678/tcp
```

### Paso 4: Acceder a la interfaz de n8n

1. Abre tu navegador en: **http://localhost:5678**
2. Ingresa las credenciales (por defecto):
   - Usuario: `admin`
   - Contraseña: la que configuraste en `.env`

### Paso 5: Configurar credenciales de Google en n8n

1. En la interfaz de n8n, ve a **Settings** (⚙️) → **Credentials**
2. Haz clic en **Add Credential**
3. Busca y configura:
   - **Google Sheets API** (OAuth2)
   - **Gmail API** (OAuth2)
   - **Google Drive API** (OAuth2)
4. Sigue el flujo de autenticación OAuth

### Paso 6: Importar/Crear el workflow

**Estructura del workflow de ejemplo:**

```
1. Schedule Trigger (cada hora)
   ↓
2. Google Sheets (Leer lista de empresas)
   ↓
3. Loop/Split In Batches
   ↓
4. HTTP Request → GET http://host.docker.internal:8000/api/v1/risk-analysis?company_name={{$json.company}}
   ↓
5. Code (Formatear resultados)
   ↓
6. Google Sheets (Escribir resultados)
   ↓
7. IF (¿Alertas detectadas?)
   ↓
8. Gmail (Enviar reporte)
```

---

## 🔄 Ejemplo de Workflow - Integración Completa

### Nodo 1: Schedule Trigger

```javascript
// Ejecutar cada hora
Schedule: 0 * * * *
```

### Nodo 2: Google Sheets - Leer Empresas

```javascript
// Configuración
Spreadsheet: "Análisis de Riesgo Empresas";
Sheet: "Empresas a Monitorear";
Range: "A2:B"; // Columna A: Nombre, B: Ticker
```

### Nodo 3: HTTP Request - Llamar al API de SafeBank AI

```javascript
// Configuración del nodo HTTP Request
{
  method: 'GET',
  url: 'http://host.docker.internal:8000/api/v1/risk-analysis',
  queryParameters: {
    company_name: '={{ $json.company_name }}'
  },
  responseFormat: 'json',
  timeout: 30000
}
```

**Respuesta esperada del API (Ejercicio 01):**

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

### Nodo 4: Code - Formatear Resultados

```javascript
// Procesar la respuesta del API
const items = $input.all();

return items.map((item) => {
	const data = item.json.data; // Acceder al objeto 'data' de la respuesta

	// Determinar emoji según el estado de riesgo
	let statusEmoji = "🟢";
	if (data.overall_risk_status === "alert") statusEmoji = "🔴";
	else if (data.overall_risk_status === "warning") statusEmoji = "🟡";

	return {
		json: {
			empresa: data.company_name,
			estado_riesgo: `${statusEmoji} ${data.overall_risk_status.toUpperCase()}`,
			score_riesgo: (data.overall_risk_score * 100).toFixed(2) + "%",
			sentimiento_mercado: data.market_sentiment,
			confianza_sentimiento: (data.sentiment_confidence * 100).toFixed(2) + "%",
			estado_compliance: data.compliance_status,
			tipo_riesgo_compliance: data.compliance_risk_type,
			requiere_revision: data.requires_manual_review ? "⚠️ SÍ" : "✅ NO",
			fecha_analisis: data.analysis_timestamp,
			fuente_noticia: data.source_news_title,
			url_noticia: data.source_url,
		},
	};
});
```

### Nodo 5: Google Sheets - Guardar Resultados

```javascript
// Configuración
Spreadsheet: "Análisis de Riesgo Empresas"
Sheet: "Resultados Análisis"
Operation: "Append"
Columns: empresa, estado_riesgo, score_riesgo, sentimiento_mercado, etc.
```

### Nodo 6: IF - Detectar Alertas

```javascript
// Condición
{
	{
		$json.requiere_revision === "⚠️ SÍ";
	}
}
```

### Nodo 7: Gmail - Enviar Reporte (solo si hay alertas)

```javascript
// Configuración
To: "compliance@empresa.com";
Subject: "⚠️ ALERTA: Análisis de Riesgo - {{ $json.empresa }}";
Body: `
<h2>Alerta de Riesgo Detectada</h2>
<p><strong>Empresa:</strong> {{ $json.empresa }}</p>
<p><strong>Estado:</strong> {{ $json.estado_riesgo }}</p>
<p><strong>Score de Riesgo:</strong> {{ $json.score_riesgo }}</p>
<p><strong>Sentimiento de Mercado:</strong> {{ $json.sentimiento_mercado }}</p>
<p><strong>Compliance:</strong> {{ $json.tipo_riesgo_compliance }}</p>
<p><strong>Fuente:</strong> <a href="{{ $json.url_noticia }}">{{ $json.fuente_noticia }}</a></p>
<p><em>Análisis realizado: {{ $json.fecha_analisis }}</em></p>
`;
```

---

## 🔐 Variables de Entorno

El proyecto incluye un archivo `.env.example` que puedes copiar para crear tu configuración:

```bash
# Copiar el archivo de ejemplo
cp .env.example .env
```

### Configuración Recomendada (.env)

```bash
# === n8n Configuration ===
# Host y puerto donde correrá n8n
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http

# URL pública (si estás en local, deja localhost)
WEBHOOK_URL=http://localhost:5678/

# Zona horaria
GENERIC_TIMEZONE=America/La_Paz

# Auth básica para proteger la UI
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=cambia_esta_contraseña_AHORA

# === SafeBank AI API (Ejercicio 01) ===
FASTAPI_HOST=host.docker.internal
FASTAPI_PORT=8000
FASTAPI_BASE_URL=http://host.docker.internal:8000

# === Google Workspace (Opcional - para usar en workflows) ===
# IDs de recursos de Google (obtener después de crear)
GOOGLE_SHEETS_ID=
GOOGLE_DRIVE_FOLDER_ID=
```

### 📋 Variables Explicadas

| Variable                  | Descripción                   | Valor por defecto                  |
| ------------------------- | ----------------------------- | ---------------------------------- |
| `N8N_HOST`                | Host donde se ejecuta n8n     | `localhost`                        |
| `N8N_PORT`                | Puerto de la interfaz web     | `5678`                             |
| `N8N_PROTOCOL`            | Protocolo (http/https)        | `http`                             |
| `WEBHOOK_URL`             | URL para webhooks externos    | `http://localhost:5678/`           |
| `GENERIC_TIMEZONE`        | Zona horaria del servidor     | `America/La_Paz`                   |
| `N8N_BASIC_AUTH_USER`     | Usuario para autenticación    | `admin`                            |
| `N8N_BASIC_AUTH_PASSWORD` | ⚠️ Contraseña (CÁMBIALA)      | -                                  |
| `FASTAPI_HOST`            | Host del API del Ejercicio 01 | `host.docker.internal`             |
| `FASTAPI_PORT`            | Puerto del API                | `8000`                             |
| `FASTAPI_BASE_URL`        | URL completa del API          | `http://host.docker.internal:8000` |

> **⚠️ Importante:** El archivo `.env` contiene credenciales sensibles. Asegúrate de que esté en tu `.gitignore`

---

## 🔄 Flujo de Trabajo - Descripción Técnica

### 1️⃣ **Trigger Programado (Schedule Trigger)**

- Ejecución diaria/horaria configurable
- Inicia el proceso de análisis de riesgo
- Configurable vía CRON expression

### 2️⃣ **Verificación de Archivos (Google Drive)**

- Comprueba existencia de archivos de entrada
- Valida estructura de carpetas
- Gestiona errores si archivos no existen

### 3️⃣ **Ingesta Inicial (Google Sheets)**

- Lee datos de empresas desde hoja de cálculo maestra
- Extrae información: nombre, ticker, sector, etc.
- Prepara datos para análisis

### 4️⃣ **Nodo IF - Control de Flujo**

```javascript
// Ejemplo de lógica condicional
if ($json.company_data && $json.company_data.length > 0) {
	return [true]; // Continuar procesamiento
} else {
	return [false]; // Enviar notificación de error
}
```

### 5️⃣ **Consulta API FastAPI (HTTP Request)**

```javascript
// Configuración del nodo
{
  url: 'http://host.docker.internal:8000/api/analyze',
  method: 'POST',
  body: {
    company: '{{ $json.company_name }}',
    ticker: '{{ $json.ticker }}'
  }
}
```

### 6️⃣ **Nodo Code - Procesamiento JavaScript**

```javascript
// Formateo de resultados de análisis
const items = $input.all();

return items.map((item) => {
	const riskData = item.json;

	return {
		json: {
			company: riskData.company,
			risk_score: parseFloat(riskData.risk_score).toFixed(2),
			sentiment: riskData.sentiment.toUpperCase(),
			compliance_status: riskData.compliance ? "✅ Cumple" : "❌ No Cumple",
			risk_level:
				riskData.risk_score > 7
					? "🔴 ALTO"
					: riskData.risk_score > 4
					? "🟡 MEDIO"
					: "🟢 BAJO",
			analysis_date: new Date().toISOString().split("T")[0],
			recommendations: riskData.recommendations || [],
		},
	};
});
```

### 7️⃣ **Nodo Merge - Combinación de Datos**

- Combina resultados de múltiples fuentes
- Estrategias: merge, append, concat
- Gestiona datos de múltiples empresas simultáneamente

### 8️⃣ **Inserción Dinámica (Google Sheets)**

- Crea hoja nueva si no existe
- Formato automático de columnas
- Inserción de datos procesados

### 9️⃣ **Envío de Reportes (Gmail)**

- Genera email con formato HTML
- Adjunta resumen de análisis
- Personalización por destinatario

---

## 🔑 Guía de Configuración de Credenciales

### Google Workspace OAuth 2.0

#### Paso 1: Crear Proyecto en Google Cloud

1. Accede a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea nuevo proyecto: **"n8n-risk-automation"**
3. Habilita las siguientes APIs:
   - Gmail API
   - Google Sheets API
   - Google Drive API

#### Paso 2: Configurar Pantalla de Consentimiento

1. **OAuth consent screen** → External
2. Completa información del proyecto
3. Agrega scopes necesarios:
   ```
   https://www.googleapis.com/auth/gmail.send
   https://www.googleapis.com/auth/spreadsheets
   https://www.googleapis.com/auth/drive
   ```

#### Paso 3: Crear Credenciales OAuth 2.0

1. **Credentials** → **Create Credentials** → **OAuth client ID**
2. Application type: **Web application**
3. Authorized redirect URIs:
   ```
   http://localhost:5678/rest/oauth2-credential/callback
   ```
4. Guarda **Client ID** y **Client Secret**

#### Paso 4: Configurar en n8n

##### 📧 Gmail API

```yaml
Credential Type: Gmail OAuth2 API
Client ID: <tu-client-id>
Client Secret: <tu-client-secret>
Auth URI: https://accounts.google.com/o/oauth2/v2/auth
Token URI: https://oauth2.googleapis.com/token
Scopes: https://www.googleapis.com/auth/gmail.send
```

**Pasos detallados en n8n:**

1. Ve a **Credentials** en el menú lateral
2. Click en **Add Credential**
3. Busca y selecciona **Gmail OAuth2 API**
4. Completa los campos:
   - **Credential Name**: Gmail - Risk Automation
   - **Client ID**: Pega el ID de Google Cloud Console
   - **Client Secret**: Pega el Secret de Google Cloud Console
5. Click en **Connect my account**
6. Autoriza en el navegador con tu cuenta de Google
7. Guarda la credencial

##### 📊 Google Sheets API

```yaml
Credential Type: Google Sheets OAuth2 API
Client ID: <tu-client-id>
Client Secret: <tu-client-secret>
Auth URI: https://accounts.google.com/o/oauth2/v2/auth
Token URI: https://oauth2.googleapis.com/token
Scopes: https://www.googleapis.com/auth/spreadsheets
```

**Pasos detallados en n8n:**

1. Ve a **Credentials** → **Add Credential**
2. Selecciona **Google Sheets OAuth2 API**
3. Completa:
   - **Credential Name**: Google Sheets - Risk Data
   - **Client ID**: Mismo que Gmail
   - **Client Secret**: Mismo que Gmail
4. Click en **Connect my account** y autoriza
5. Guarda la credencial

**Configuración en nodos Google Sheets:**

- **Operation**: Append, Update, Create, Read
- **Document ID**: Obtén el ID de la URL de tu hoja:
  ```
  https://docs.google.com/spreadsheets/d/[DOCUMENT_ID]/edit
  ```
- **Sheet Name**: Nombre de la pestaña (ej: "Risk Analysis")
- **Range**: Rango de celdas (ej: "A1:F100")

##### 📁 Google Drive API

```yaml
Credential Type: Google Drive OAuth2 API
Client ID: <tu-client-id>
Client Secret: <tu-client-secret>
Auth URI: https://accounts.google.com/o/oauth2/v2/auth
Token URI: https://oauth2.googleapis.com/token
Scopes: https://www.googleapis.com/auth/drive
```

**Pasos detallados en n8n:**

1. Ve a **Credentials** → **Add Credential**
2. Selecciona **Google Drive OAuth2 API**
3. Completa:
   - **Credential Name**: Google Drive - Input Files
   - **Client ID**: Mismo Client ID de GCP
   - **Client Secret**: Mismo Secret de GCP
4. **Important**: Asegúrate de usar el mismo proyecto de GCP
5. Click en **Connect my account** y autoriza con Google
6. Guarda la credencial

**Configuración en nodos Google Drive:**

- **Operation**: List, Upload, Download, Delete
- **Folder ID**: Obtén de la URL de tu carpeta:
  ```
  https://drive.google.com/drive/folders/[FOLDER_ID]
  ```
- **Search Query**: Usa sintaxis de Drive para filtrar:
  ```
  name contains 'risk_data' and mimeType='text/csv'
  ```

#### Paso 5: Autorizar Acceso

1. En cada nodo de Google (Gmail, Sheets, Drive)
2. Selecciona la credencial configurada
3. Click en **Connect my account**
4. Completa el flujo OAuth en el navegador
5. Autoriza permisos solicitados

### 🔒 Mejores Prácticas de Seguridad

- ✅ Usa Service Accounts para producción
- ✅ Rotación periódica de credenciales
- ✅ Principio de mínimo privilegio en scopes
- ✅ No commitees credenciales al repositorio
- ✅ Usa variables de entorno para datos sensibles

### 🔐 Service Accounts (Alternativa para Producción)

Para entornos de producción, considera usar Service Accounts:

1. En GCP Console → **Service Accounts** → **Create Service Account**
2. Otorga roles necesarios:
   - **Gmail**: Gmail API User
   - **Sheets**: Google Sheets Editor
   - **Drive**: Drive File Access
3. Crea clave JSON
4. En n8n, usa **Service Account** en lugar de OAuth2
5. Carga el archivo JSON de credenciales

**Ventajas:**

- No requiere interacción humana para autorizar
- Ideal para CI/CD y automatizaciones desatendidas
- Mayor control granular de permisos

---

## 🚀 Instalación y Ejecución

### Inicio Rápido

```bash
# 1. Clonar o navegar al proyecto
cd exercise02

# 2. Crear archivo .env
cp .env.example .env
# Editar con tus credenciales

# 3. Levantar servicios
docker-compose up -d

# 4. Verificar estado
docker-compose ps

# 5. Acceder a n8n
# Navegador: http://localhost:5678
```

### Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f n8n

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Eliminar volúmenes (⚠️ borra datos)
docker-compose down -v

# Backup de datos de n8n
tar -czf n8n_backup_$(date +%Y%m%d).tar.gz n8n_data/
```

---

## 📊 Estructura del Proyecto

```
exercise02/
├── docker-compose.yml          # Configuración de Docker
├── README.md                   # Esta documentación
├── .env                        # Variables de entorno (no commitear)
├── .env.example                # Template de variables
├── n8n_data/                   # Datos persistentes de n8n
│   ├── config                  # Configuración de n8n
│   ├── database.sqlite         # Base de datos local
│   ├── database.sqlite-shm     # Shared memory
│   ├── database.sqlite-wal     # Write-Ahead Log
│   ├── binaryData/             # Archivos binarios
│   ├── git/                    # Workflows versionados
│   ├── nodes/                  # Nodos personalizados
│   │   └── package.json
│   └── ssh/                    # Claves SSH
└── local-files/                # Archivos compartidos con host
```

---

## 🛠️ Solución de Problemas

### ❌ Error: No se puede conectar a FastAPI

**Síntoma:**

```
Error: connect ECONNREFUSED
```

**Solución:**

1. Verifica que FastAPI esté ejecutándose en el host
2. Usa `host.docker.internal` en lugar de `localhost`
3. Confirma el puerto correcto (por defecto: 8000)
4. Verifica configuración de `extra_hosts` en docker-compose.yml

```bash
# Verificar que FastAPI está corriendo
curl http://localhost:8000/health

# Desde dentro del contenedor n8n
docker exec -it n8n_automation curl http://host.docker.internal:8000/health
```

### ❌ Error: Credenciales de Google inválidas

**Síntoma:**

```
Invalid grant / Token expired
```

**Solución:**

1. Re-autoriza la conexión OAuth en n8n
2. Verifica que las APIs estén habilitadas en GCP
3. Comprueba las URIs de redirección autorizadas
4. Revisa los scopes configurados

### ❌ Error: Cannot find module en nodo Code

**Solución:**

- n8n no permite imports externos en nodos Code
- Usa funciones nativas de JavaScript
- Para librerías externas, crea un nodo personalizado

### ❌ Error: Google Sheets - Document not found

**Solución:**

1. Verifica que el Document ID sea correcto
2. Asegúrate de que la cuenta autorizada tenga acceso
3. Comparte la hoja con la cuenta de servicio (si usas Service Account)

### ❌ Error: Gmail - Insufficient Permission

**Solución:**

1. Revisa que el scope `https://www.googleapis.com/auth/gmail.send` esté incluido
2. Re-autoriza la credencial en n8n
3. Verifica que Gmail API esté habilitada en GCP

---

## 📈 Optimizaciones y Mejores Prácticas

### Performance

- ⚡ Usa nodos de lote para procesar múltiples items
- ⚡ Implementa caching en nodos HTTP Request
- ⚡ Limita concurrencia con "Batch Size"
- ⚡ Usa "Split In Batches" para grandes volúmenes de datos

### Monitoreo

- 📊 Activa "Execution Data" para debug
- 📊 Implementa notificaciones de error por Slack/Discord
- 📊 Usa el nodo "Error Trigger" para recuperación automática
- 📊 Configura alertas en Google Cloud Monitoring

### Mantenimiento

- 🔄 Versionado de workflows con Git integration
- 🔄 Backups automáticos de la base de datos
- 🔄 Documentación inline en nodos "Sticky Note"
- 🔄 Revisa logs periódicamente: `docker-compose logs`

### Seguridad

- 🔐 Usa HTTPS en producción (configurar reverse proxy)
- 🔐 Implementa autenticación de dos factores
- 🔐 Limita acceso por IP usando firewall
- 🔐 Audita permisos de Service Accounts regularmente

---

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork del repositorio
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 📞 Soporte

- 📧 Email: soporte@empresa.com
- 📚 Documentación n8n: https://docs.n8n.io/
- 💬 Community: https://community.n8n.io/
- 🐛 Issues: GitHub Issues del proyecto

---

## 🔗 Enlaces Útiles

- [Documentación oficial de n8n](https://docs.n8n.io/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)

---

**🎯 Desarrollado por:** Equipo de Automatización  
**📅 Última actualización:** Diciembre 2025  
**⚙️ Versión:** 1.0.0
