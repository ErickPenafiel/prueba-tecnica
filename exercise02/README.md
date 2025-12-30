# 🚀 Ejercicio 02: Automatización con n8n - Integración con SafeBank AI

---

## ⚠️ PREREQUISITO OBLIGATORIO - LEE ESTO PRIMERO

> **🛑 ATENCIÓN**: Este ejercicio **NO FUNCIONARÁ** sin el Ejercicio 01 ejecutándose.

**ANTES DE CONTINUAR CON ESTE EJERCICIO, DEBES:**

### 1️⃣ Verificar que el Ejercicio 01 está configurado y funcionando

El **Ejercicio 01 (SafeBank AI API)** debe estar ejecutándose en el puerto 8000 ANTES de levantar n8n.

```powershell
# En una terminal separada, ve al directorio del ejercicio 01
cd .\exercise01

# Verifica que existe el entorno virtual
Get-ChildItem venv

# Si NO existe, créalo:
python -m venv venv

# Activa el entorno virtual
.\venv\Scripts\activate

# Instala dependencias (si no lo has hecho)
pip install -r requirements.txt

# Configura tu NEWSAPI_KEY en .env
# Copia .env.example a .env y agrega tu API key

# Ejecuta el API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2️⃣ Verifica que el API responde correctamente

**En otra terminal, prueba:**

```powershell
# Test de health check
curl http://localhost:8000/health

# Deberías ver:
# {"status":"healthy","service":"FinUp Risk Intelligence Platform",...}

# Test de análisis (requiere NewsAPI key configurada)
curl "http://localhost:8000/api/v1/risk-analysis?company_name=Tesla"
```

**Si los comandos anteriores NO funcionan:**

- ❌ NO continúes con este ejercicio
- ❌ El workflow de n8n fallará al intentar conectarse al API
- ✅ Revisa la documentación del Ejercicio 01: `../exercise01/README.md`
- ✅ Asegúrate de tener NewsAPI key configurada

**Si los comandos funcionan correctamente:**

- ✅ Mantén esa terminal abierta con el API ejecutándose
- ✅ Ahora sí puedes continuar con este ejercicio

---

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
┌────────────────────────────────────────────────────────────────────┐
│                       EJERCICIO 02 - n8n                           │
│                    (Docker Container: 5678)                        │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │         Workflow de Automatización (14 nodos)            │     │
│  │                                                           │     │
│  │  1. Schedule Trigger (8:00 AM diario)                    │     │
│  │  2. Google Drive: Buscar "monitoring_list"               │     │
│  │  3. If: ¿Existe monitoring_list?                         │     │
│  │     ├─ NO → Crear sheet + Poblar empresas (Tesla, etc.) │     │
│  │     └─ SI → Continuar                                    │     │
│  │  4. Google Sheets: Leer empresas del sheet               │     │
│  │  5. Loop: Para cada empresa                              │     │
│  │  6. HTTP Request → FastAPI (Exercise 01)                 │     │
│  │     URL: host.docker.internal:8000/api/v1/risk-analysis  │     │
│  │     Método: GET + Query Param: company_name              │     │
│  │  7. If: ¿Status 200?                                     │     │
│  │     ├─ NO → Email de error + Fin                         │     │
│  │     └─ SI → Continuar procesamiento                      │     │
│  │  8. Google Drive: Buscar "monitoring_register"           │     │
│  │  9. If: ¿Existe monitoring_register?                     │     │
│  │     ├─ NO → Crear sheet "registros"                      │     │
│  │     └─ SI → Continuar                                    │     │
│  │  10. JavaScript: Formatear datos del API                 │     │
│  │      (timestamp, risk_status, risk_score, sentiment,     │     │
│  │       compliance_type, evidence, URL, manual_review)     │     │
│  │  11. Google Sheets: Guardar análisis en "registros"      │     │
│  │  12. Email: Enviar reporte detallado con resultados      │     │
│  │                                                           │     │
│  └───────────────────────────────────────────────────────────┘     │
└────────────────────┬───────────────────────────────────────────────┘
                     │
           ┌─────────┴──────────┐
           │                    │
           ▼                    ▼
┌──────────────────────┐  ┌──────────────────────┐
│  EJERCICIO 01        │  │  Google Cloud APIs   │
│  SafeBank AI API     │  │  ──────────────────  │
│  (FastAPI)           │  │  • Drive API         │
│                      │  │  • Sheets API        │
│  host.docker         │  │  • SMTP (Gmail)      │
│  .internal:8000      │  │                      │
│                      │  └──────────────────────┘
│  GET /api/v1/        │
│    risk-analysis     │
│  ?company_name=      │
│                      │
│  Response:           │
│  ├─ status_code      │
│  ├─ message          │
│  └─ data:            │
│     ├─ company_name  │
│     ├─ risk_status   │
│     ├─ risk_score    │
│     ├─ sentiment     │
│     ├─ compliance    │
│     ├─ evidence      │
│     └─ timestamp     │
└──────────────────────┘
```

**Componentes:**

- **n8n (Docker)**: Motor de automatización ejecutándose en contenedor Docker
- **SafeBank AI API (Ejercicio 01)**: API FastAPI con análisis de riesgo usando ML (host.docker.internal:8000)
- **Google Workspace**: Suite de servicios (Gmail, Sheets, Drive) para almacenamiento y notificaciones
- **Docker Compose**: Orquestación de servicios

---

## 📦 Requisitos del Sistema

### 🐳 Docker y Docker Compose (OBLIGATORIO)

Este ejercicio se ejecuta completamente en Docker. **Docker Desktop es REQUISITO OBLIGATORIO**.

#### Instalación de Docker Desktop

**Windows 10/11:**

1. **Descargar Docker Desktop:**

   - [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Versión mínima: **20.10** o superior

2. **Instalar Docker Desktop:**

   - Ejecutar el instalador descargado
   - Reiniciar el sistema si es requerido
   - Iniciar Docker Desktop desde el menú de inicio

3. **Verificar instalación:**

   ```powershell
   # Verificar versión de Docker
   docker --version
   # Debe mostrar: Docker version 20.10.x o superior

   # Verificar Docker Compose (incluido en Docker Desktop)
   docker-compose --version
   # Debe mostrar: Docker Compose version v2.x.x o superior

   # Verificar que Docker está corriendo
   docker ps
   # Debe mostrar una tabla (puede estar vacía)
   ```

**Si `docker ps` muestra error:**

- ✅ Asegúrate de que Docker Desktop está ejecutándose (ícono en la bandeja del sistema)
- ✅ Abre Docker Desktop y espera a que inicie completamente
- ✅ Reinicia Docker Desktop: Settings → Restart

#### Configuración de Docker Desktop

**Para mejor rendimiento:**

1. Abre Docker Desktop
2. Ve a **Settings** (⚙️) → **Resources**
3. Configura:
   - **CPU**: Mínimo 2 cores (recomendado 4)
   - **Memory**: Mínimo 4 GB (recomendado 8 GB)
   - **Disk**: Asegúrate de tener al menos 10 GB libres
4. Click en **Apply & Restart**

### 📋 Software Adicional

- ✅ **Git** - Para clonar el repositorio
- ✅ **Terminal PowerShell** - Incluido en Windows
- ✅ **Editor de texto** - Para editar archivos `.env`

### 🔐 Cuentas y Credenciales (Para funcionalidad completa)

- 🌐 **Cuenta de Google Cloud Platform** (para envío de emails y Google Sheets)
- 🔑 **Credenciales OAuth 2.0** de Google Workspace

> **Nota**: El workflow puede importarse sin estas credenciales, pero requieren configuración para ejecutarse completamente.

### APIs de Google a Habilitar

1. **Gmail API** - Para envío de reportes
2. **Google Sheets API** - Para lectura/escritura de datos
3. **Google Drive API** - Para gestión de archivos

**📖 Guía completa con capturas de pantalla:**

👉 **[Ver GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md)** - Guía paso a paso con imágenes

Esta guía incluye:

- ✅ Cómo habilitar las APIs en Google Cloud Console
- ✅ Cómo crear credenciales OAuth 2.0
- ✅ Cómo configurar la pantalla de consentimiento
- ✅ Cómo conectar las credenciales en n8n
- ✅ Solución de problemas comunes con capturas

**Resumen rápido:**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Enable APIs
2. Habilita: Drive API, Sheets API, Gmail API
3. Crea credenciales OAuth 2.0 (Aplicación web)
4. URI de redirección: `http://localhost:5678/rest/oauth2-credential/callback`
5. Configura en n8n (ver [guía detallada](GOOGLE_CLOUD_SETUP.md))

---

## 🐳 Configuración y Levantamiento de Docker

### Entendiendo la Arquitectura Docker

Este ejercicio utiliza **Docker Compose** para orquestar el contenedor de n8n con todas las configuraciones necesarias.

**¿Por qué Docker?**

- ✅ Instalación simplificada (no requiere Node.js, npm, etc.)
- ✅ Aislamiento del sistema host
- ✅ Persistencia de datos mediante volúmenes
- ✅ Fácil escalabilidad y portabilidad
- ✅ Configuración reproducible

### Archivo docker-compose.yml

El proyecto incluye un archivo `docker-compose.yml` pre-configurado:

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

## 🚀 Guía de Instalación Paso a Paso

> **⚠️ RECORDATORIO**: Antes de ejecutar estos pasos, asegúrate de que el **Ejercicio 01** está ejecutándose en otra terminal. Si no lo has hecho, revisa la sección "PREREQUISITO OBLIGATORIO" al inicio de este documento.

---

### ✅ PASO 0: Verificación Final del Ejercicio 01

**En una terminal separada (déjala abierta):**

```powershell
# Terminal 1 - API SafeBank AI (Ejercicio 01)
cd ..\exercise01
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Salida esperada:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process...
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verificación rápida (en otra terminal):**

```powershell
curl http://localhost:8000/health
```

**Si obtienes respuesta JSON con "status": "healthy"** → ✅ Puedes continuar

**Si obtienes error de conexión** → ❌ Revisa el Ejercicio 01 primero

---

### 📁 PASO 1: Navegar al directorio del Ejercicio 02

```powershell
# Abre una NUEVA terminal (PowerShell)
# Navega al directorio del ejercicio 02
cd D:\PruebaTecnica\FinUp\exercise02

# Verifica que estás en el directorio correcto
Get-Location
# Debe mostrar: D:\PruebaTecnica\FinUp\exercise02

# Lista los archivos
dir
# Debes ver: docker-compose.yml, .env.example, etc.
```

### ⚙️ PASO 2: Configurar Variables de Entorno

```powershell
# En el directorio exercise02
cp .env.example .env
```

Edita el archivo `.env` y cambia la contraseña:

```bash
N8N_BASIC_AUTH_PASSWORD=tu_contraseña_segura_aqui
```

### 🐳 PASO 3: Levantar n8n con Docker Compose

#### 3.1 Iniciar el Contenedor

```powershell
# En el directorio exercise02
# Asegúrate de estar en: D:\PruebaTecnica\FinUp\exercise02

docker-compose up -d
```

**¿Qué hace este comando?**

- `docker-compose`: Herramienta de orquestación de Docker
- `up`: Crea e inicia los contenedores definidos en docker-compose.yml
- `-d`: Modo "detached" (segundo plano), libera la terminal

**Salida esperada:**

```
Creating network "exercise02_default" with the default driver
Pulling n8n (docker.n8n.io/n8nio/n8n:latest)...
latest: Pulling from n8nio/n8n
...
Status: Downloaded newer image for docker.n8n.io/n8nio/n8n:latest
Creating exercise02_n8n_1 ... done
```

> **Primera vez**: La descarga de la imagen puede tomar 5-10 minutos dependiendo de tu conexión a internet (aprox. 500MB).

#### 3.2 Verificar que el Contenedor está Corriendo

```powershell
# Ver contenedores activos
docker ps
```

**Salida esperada:**

```
CONTAINER ID   IMAGE                              COMMAND                  CREATED         STATUS         PORTS                    NAMES
a1b2c3d4e5f6   docker.n8n.io/n8nio/n8n:latest    "tini -- /docker-ent…"   2 minutes ago   Up 2 minutes   0.0.0.0:5678->5678/tcp   exercise02_n8n_1
```

**Campos importantes:**

- **STATUS**: Debe decir "Up X minutes" (si dice "Restarting" hay un problema)
- **PORTS**: Debe mostrar "0.0.0.0:5678->5678/tcp"
- **NAMES**: Nombre del contenedor (puede variar)

#### 3.3 Verificar los Logs del Contenedor

```powershell
# Ver logs en tiempo real
docker-compose logs -f

# O ver las últimas 50 líneas
docker-compose logs --tail=50
```

**Logs saludables deben mostrar:**

```
n8n_1  | Editor is now accessible via:
n8n_1  | http://localhost:5678/
n8n_1  |
n8n_1  | Version: X.X.X
```

**Para salir de los logs:** Presiona `Ctrl + C`

#### 3.4 Verificar Conectividad

```powershell
# Probar que n8n responde
curl http://localhost:5678

# Debe redirigir o mostrar HTML
```

**Si hay problemas:**

```powershell
# Ver estado detallado
docker-compose ps

# Reiniciar el contenedor
docker-compose restart

# Detener y volver a iniciar (si es necesario)
docker-compose down
docker-compose up -d

# Ver logs de errores
docker-compose logs --tail=100
```

### 🌐 PASO 4: Acceder a la Interfaz Web de n8n

#### 4.1 Abrir n8n en el Navegador

1. **Abre tu navegador preferido** (Chrome, Firefox, Edge)
2. **Navega a:** http://localhost:5678
3. **Espera unos segundos** mientras carga la interfaz

#### 4.2 Iniciar Sesión

En la pantalla de login, ingresa:

- **Usuario:** `admin`
- **Contraseña:** La que configuraste en el archivo `.env` (paso 2)

**Si olvidaste tu contraseña:**

```powershell
# Ver el archivo .env
Get-Content .env | Select-String "PASSWORD"

# O editarlo de nuevo
notepad .env
```

#### 4.3 Primera Vez en n8n

**Al entrar por primera vez verás:**

- 🏠 Dashboard principal vacío
- 📋 Menú lateral con opciones: Workflows, Credentials, Executions
- ➕ Botón "Create workflow" para crear nuevos workflows

**Felicidades! n8n está funcionando correctamente** 🎉

---

### 🔐 PASO 5: Configurar Credenciales de Google (Opcional)

> **📖 GUÍA COMPLETA:** Para instrucciones detalladas con capturas de pantalla, consulta:
> **[GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md)**

**Resumen rápido:**

1. En la interfaz de n8n, ve a **Menu Izquierdo, en el boton +** (⚙️) → **Credentials**
2. Haz clic en **Add Credential**
3. Busca y configura:
   - **Google Drive OAuth2 API** (para buscar sheets)
   - **Google Sheets OAuth2 API** (para leer/escribir datos)
   - **Gmail OAuth2** (opcional, para emails) o **Gmail SMTP** (alternativa)
4. Usa las credenciales OAuth 2.0 que creaste en Google Cloud
5. Sigue el flujo de autenticación

**📧 Alternativa SMTP para Emails:**

Si prefieres usar Gmail SMTP en lugar de OAuth 2.0 para enviar emails:

👉 **[Ver GMAIL_SMTP_SETUP.md](GMAIL_SMTP_SETUP.md)** - Guía completa de configuración SMTP

Esta guía incluye:

- ✅ Configuración de Verificación en Dos Pasos
- ✅ Generación de Contraseña de Aplicación
- ✅ Parámetros técnicos del servidor (smtp.gmail.com:465)
- ✅ Configuración de credenciales SMTP en n8n
- ✅ Solución de problemas comunes

**⚠️ Importante:**

- Necesitarás el **Client ID** y **Client Secret** de Google Cloud
- Si no los has creado, consulta la [guía completa](GOOGLE_CLOUD_SETUP.md)
- La URI de redirección debe ser: `http://localhost:5678/rest/oauth2-credential/callback`

### Paso 6: Importar el Workflow

#### Importar Workflow Pre-configurado (Recomendado) ⭐

El proyecto incluye un workflow completo listo para usar: **`workflow-riesgos.json`**

**Arquitectura del workflow (14 nodos interconectados):**

```
1. Schedule Trigger → 8:00 AM diario
2. Google Drive → Buscar "monitoring_list"
3. IF → ¿Existe monitoring_list?
   ├─ NO → 4. Crear sheet + 5. JS: Empresas (Tesla, Apple, Luis Arce) + 6. Append
   └─ SI → 7. Get rows: Leer empresas
8. HTTP Request → host.docker.internal:8000/api/v1/risk-analysis?company_name={{nombre}}
9. IF → ¿Status 200?
   ├─ NO → 16. Email ERROR
   └─ SI → 10. Drive: Buscar "monitoring_register"
          11. IF → ¿Existe?
              ├─ NO → 12. Crear sheet "registros"
              └─ SI → continuar
          13. JavaScript → Formatear 12 campos (timestamp, risk_status, etc.)
          14. Append → Guardar en "registros"
          15. Email → Reporte exitoso
```

**Características incluidas:**

- ✅ **Gestión automática de sheets**: Crea "monitoring_list" y "monitoring_register" si no existen
- ✅ **Lista de empresas inicial**: Tesla, Apple, Luis Arce (editable en nodo "Code in JavaScript1")
- ✅ **Schedule Trigger**: Ejecución diaria a las 8:00 AM (configurable)
- ✅ **Llamadas al API**: `http://host.docker.internal:8000/api/v1/risk-analysis` por cada empresa
- ✅ **Retry logic**: HTTP Request con `retryOnFail: true` y `onError: continueRegularOutput`
- ✅ **Validación de respuestas**: IF que verifica status_code == 200
- ✅ **Formateo inteligente**: JavaScript transforma JSON del API a 12 campos para Sheets
- ✅ **Emails detallados**:
  - Rama éxito: Reporte con risk_status, risk_score, sentiment, compliance_type, evidence, URL, etc.
  - Rama error: Alerta con detalles del fallo y timestamp
- ✅ **Credenciales configurables**: Google Sheets, Google Drive, SMTP

**Campos guardados en Google Sheets (12 campos):**

```
timestamp_analisis | status | message | company | registration_date |
risk_status | risk_score | sentiment | compliance_type | evidence |
url | manual_review
```

**Pasos para importar:**

1. En n8n, haz clic en el menú **Workflows** (parte superior izquierda)
2. Haz clic en **Import from File**
3. Selecciona el archivo: `workflows/workflow-riesgos.json`
4. El workflow se importará con **14 nodos** pre-configurados

5. **Configurar credenciales (obligatorio):**

   > **📖 ¿No tienes credenciales configuradas?** Consulta la guía completa:
   > **[GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md)**

   **a) Google Sheets OAuth2** (asignar en 3 nodos):

   - `Get row(s) in sheet`
   - `Create spreadsheet` / `Create spreadsheet1`
   - `Append row in sheet` / `Append row in sheet1`

   **b) Google Drive OAuth2** (asignar en 2 nodos):

   - `Search files and folders`
   - `Search files and folders1`

   **c) SMTP Gmail** (asignar en 2 nodos + actualizar emails):

   > **📧 ¿Cómo configurar Gmail SMTP?** Consulta la guía técnica completa:
   > **[GMAIL_SMTP_SETUP.md](GMAIL_SMTP_SETUP.md)**

   - `Send email` (errores)
   - `Send email1` (reportes exitosos)
   - **IMPORTANTE**: Editar cada nodo y actualizar:
     ```javascript
     fromEmail: "tu-email@gmail.com";
     toEmail: "destinatario@gmail.com";
     ```
   - **Requisitos previos:**
     - Verificación en Dos Pasos habilitada
     - Contraseña de Aplicación generada (ver guía)
     - Credencial SMTP configurada en n8n

6. **Ajustar configuración (opcional):**

   - **Horario**: Editar nodo "Schedule Trigger" para cambiar hora de ejecución
   - **Empresas**: Editar nodo "Code in JavaScript1" para modificar lista:
     ```javascript
     return [
     	{ nombre: "Tesla" },
     	{ nombre: "Apple" },
     	{ nombre: "Microsoft" },
     	{ nombre: "Amazon" },
     ];
     ```

7. **Ejecutar manualmente**:

   - Click en "Execute Workflow" (botón superior derecho)
   - Observar la ejecución nodo por nodo
   - Verificar que se crean los sheets en Google Drive
   - Revisar email recibido

8. **Activar para ejecución automática**:
   - Toggle "Active" (superior derecho) → ON
   - El workflow se ejecutará automáticamente a las 8 AM

**Documentación detallada del workflow:**
Ver [workflows/README.md](workflows/README.md) para descripción completa de cada nodo.

---

## 📤 Exportar e Importar Workflows

### Exportar un Workflow

Una vez que hayas creado tu workflow en n8n:

1. **Abrir el workflow** que deseas exportar
2. Hacer clic en el menú **⋯** (tres puntos) en la esquina superior derecha
3. Seleccionar **Download**
4. El archivo se descargará como `workflow-name.json`
5. Guardar el archivo en el directorio del proyecto (opcional):
   ```powershell
   # Mover el archivo a la carpeta workflows
   mkdir workflows
   mv ~/Downloads/workflow-name.json ./workflows/risk-analysis-workflow.json
   ```

### Importar un Workflow

Para importar un workflow existente:

1. En n8n, hacer clic en **Workflows** (menú superior)
2. Hacer clic en **Import from File**
3. Seleccionar el archivo `.json` del workflow
4. El workflow se importará automáticamente
5. **Importante:** Configurar las credenciales necesarias:
   - Google Sheets
   - Gmail
   - Cualquier otra integración que requiera autenticación

### Compartir Workflows

Los archivos de workflow exportados pueden:

- ✅ Ser compartidos con el equipo
- ✅ Versionarse en Git
- ✅ Usarse como plantillas
- ✅ Documentar la arquitectura de automatización

**Recomendación:** Crear un directorio `workflows/` en el proyecto para almacenar workflows exportados:

```
exercise02/
├── workflows/
│   ├── risk-analysis-workflow.json       # Workflow principal
│   ├── compliance-alerts-workflow.json   # Workflow de alertas
│   └── README.md                         # Documentación de workflows
├── docker-compose.yml
└── README.md
```

---

## 🔄 Detalles del workflow-riesgos.json

### Arquitectura del Workflow (14 Nodos)

El workflow implementa un sistema completo de monitoreo automatizado con gestión inteligente de sheets, validaciones y notificaciones.

**Flujo completo:**

```
1. Schedule Trigger (8 AM diario)
   ↓
2. Google Drive: Buscar "monitoring_list"
   ↓
3. IF: ¿Existe monitoring_list?
   ├─ NO → 4. Crear sheet
   │        5. JS: Empresas (Tesla, Apple, Luis Arce)
   │        6. Append: Escribir empresas
   │        ↓
   └─ SI → 7. Get rows: Leer todas las empresas
              ↓
         8. HTTP Request: API Exercise01
            host.docker.internal:8000/api/v1/risk-analysis
            Query: company_name={{ $json.nombre }}
            retryOnFail: true
            ↓
         9. IF: ¿Status 200?
            ├─ NO → 16. Email ERROR ❌
            │
            └─ SI → 10. Drive: Buscar "monitoring_register"
                    11. IF: ¿Existe?
                        ├─ NO → 12. Crear sheet "registros"
                        └─ SI → continuar
                    13. JavaScript: Formatear 12 campos
                        (timestamp, risk_status, risk_score,
                         sentiment, compliance_type, evidence,
                         url, manual_review, etc.)
                    14. Append: Guardar en "registros"
                    15. Email: Reporte exitoso ✅
```

### Configuraciones Clave del Workflow

#### HTTP Request Node (Nodo 8)

```json
{
	"url": "http://host.docker.internal:8000/api/v1/risk-analysis",
	"method": "GET",
	"queryParameters": {
		"company_name": "={{ $json.nombre }}"
	},
	"retryOnFail": true,
	"onError": "continueRegularOutput"
}
```

#### JavaScript Formatting (Nodo 13)

```javascript
const items = $("HTTP Request").all();
const fechaLegible = new Date().toLocaleString("es-ES", {
	day: "2-digit",
	month: "2-digit",
	year: "numeric",
	hour: "2-digit",
	minute: "2-digit",
	second: "2-digit",
});

return rawData.map((item) => ({
	json: {
		timestamp_analisis: item.data?.analysis_timestamp,
		status: item.status_code,
		company: item.data?.company_name,
		registration_date: fechaLegible,
		risk_status: item.data?.overall_risk_status,
		risk_score: item.data?.overall_risk_score,
		sentiment: item.data?.market_sentiment,
		compliance_type: item.data?.compliance_risk_type,
		evidence: item.data?.evidence_headline,
		url: item.data?.evidence_url,
		manual_review: item.data?.requires_manual_review ? "SI" : "NO",
	},
}));
```

#### Email Templates

**Email de Éxito (Nodo 15):**

```
Subject: 📊 Reporte de Riesgo: {{ company }} - [{{ risk_status }}]

🏢 Empresa: {{ company }}
🛡️ Estado de Riesgo: {{ risk_status }}
📉 Puntaje: {{ risk_score }}
🎭 Sentimiento: {{ sentiment }}
🔍 Compliance: {{ compliance_type }}
⚠️ Revisión Manual: {{ manual_review }}

📰 Evidencia: "{{ evidence }}"
🔗 URL: {{ url }}
```

**Email de Error (Nodo 16):**

```
Subject: ❌ ERROR: Análisis de Riesgo - {{ empresa }}

❌ Error: {{ message }}
📡 Status Code: {{ status_code }}

Posibles causas:
1. FastAPI no está corriendo
2. host.docker.internal no accesible
3. API error 500/404
```

### Google Sheets Gestionados

1. **monitoring_list** (sheet: "list")

   - Columnas: nombre
   - Contiene: Lista de empresas a monitorear
   - Creación: Automática si no existe
   - Población inicial: Tesla, Apple, Luis Arce

2. **monitoring_register** (sheet: "registros")
   - Columnas: timestamp_analisis, status, message, company, registration_date, risk_status, risk_score, sentiment, compliance_type, evidence, url, manual_review
   - Contiene: Histórico de todos los análisis
   - Creación: Automática si no existe

### Respuesta Esperada del API (Exercise01)

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
		"evidence_headline": "Tesla Reports Q4 Earnings...",
		"evidence_url": "https://newsapi.org/...",
		"analysis_timestamp": "2025-12-30T10:30:00Z"
	}
}
```

### Ventajas del Workflow

1. ✅ **Auto-configurable**: Crea sheets si no existen
2. ✅ **Resiliente**: Retry automático + manejo de errores
3. ✅ **Notificaciones duales**: Emails de éxito y error
4. ✅ **Extensible**: Agregar empresas editando el sheet
5. ✅ **Auditable**: Registro histórico completo
6. ✅ **Producción-ready**: Validaciones completas
   url: 'http://host.docker.internal:8000/api/v1/risk-analysis',
   queryParameters: {
   company_name: '={{ $json.company_name }}'
   },
   responseFormat: 'json',
   timeout: 30000
   }

````

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
````

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

## 🔑 Configuración de Credenciales

### Google Workspace (Drive, Sheets, Gmail)

Este proyecto requiere credenciales de Google Cloud para integrar con Google Drive, Google Sheets y Gmail. Para instrucciones detalladas de configuración:

📖 **Guías completas de configuración:**

| Servicio                  | Guía                                                                      | Descripción                                                                                         |
| ------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Google Cloud APIs**     | [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md)                            | Configuración de OAuth 2.0, habilitación de APIs (Drive, Sheets, Gmail), pantalla de consentimiento |
| **Gmail SMTP**            | [GMAIL_SMTP_SETUP.md](GMAIL_SMTP_SETUP.md)                                | Alternativa SMTP para envío de emails, verificación en 2 pasos, contraseña de aplicación            |
| **Documentación Oficial** | [Google Cloud Console Docs](https://cloud.google.com/docs/authentication) | Documentación oficial de Google sobre autenticación y APIs                                          |

**Resumen rápido de credenciales necesarias:**

- ✅ **Google Drive OAuth2** - Búsqueda y gestión de archivos
- ✅ **Google Sheets OAuth2** - Lectura/escritura de datos
- ✅ **Gmail OAuth2 o SMTP** - Envío de emails (elige una opción)

> **💡 Recomendación:** Sigue las guías paso a paso con capturas de pantalla para una configuración sin errores.

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

## 🔗 Enlaces Útiles

### Documentación del Proyecto

- 📖 [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md) - Configuración de APIs de Google Cloud
- 📧 [GMAIL_SMTP_SETUP.md](GMAIL_SMTP_SETUP.md) - Configuración de Gmail SMTP para envío de emails
- 📊 [workflows/README.md](workflows/README.md) - Documentación técnica del workflow

### Documentación Externa

- [Documentación oficial de n8n](https://docs.n8n.io/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)

---

**🎯 Desarrollado por:** Erick Peñafiel
**📅 Última actualización:** Diciembre 2025  
**⚙️ Versión:** 1.0.0
