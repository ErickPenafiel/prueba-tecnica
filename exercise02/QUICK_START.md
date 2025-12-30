# 🚀 Guía de Inicio Rápido - Ejercicio 02

## ⚠️ Requisito Previo Crítico

**ANTES DE CONTINUAR:** Asegúrate de que el **Ejercicio 01 (SafeBank AI API)** está ejecutándose.

```powershell
# En otra terminal, navega al ejercicio 01
cd ..\exercise01

# Activa el entorno virtual
.\venv\Scripts\activate

# Ejecuta el API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verifica que funciona:

```powershell
curl http://localhost:8000/health
```

---

## 🏃 Inicio Rápido (3 pasos)

### 1️⃣ Configurar Variables de Entorno

```powershell
# Copiar el archivo de ejemplo
cp .env.example .env
```

**Edita `.env` y cambia la contraseña:**

```bash
N8N_BASIC_AUTH_PASSWORD=tu_contraseña_segura_aqui
```

### 2️⃣ Levantar n8n con Docker

```powershell
# Iniciar n8n
docker-compose up -d

# Verificar que está corriendo
docker ps
```

Deberías ver algo como:

```
CONTAINER ID   IMAGE                              STATUS         PORTS
xxxxx          docker.n8n.io/n8nio/n8n:latest    Up 5 seconds   0.0.0.0:5678->5678/tcp
```

### 3️⃣ Acceder a n8n

1. Abre tu navegador en: **http://localhost:5678**
2. Ingresa credenciales:
   - **Usuario:** `admin`
   - **Contraseña:** la que configuraste en `.env`

---

## ✅ Verificar Conectividad con el API

### Desde tu navegador (fuera de Docker)

```powershell
# Probar el API directamente
curl http://localhost:8000/api/v1/risk-analysis?company_name=Tesla
```

### Desde dentro de n8n

1. Crea un nuevo workflow
2. Agrega nodo **HTTP Request**
3. Configura:
   - **Method:** GET
   - **URL:** `http://host.docker.internal:8000/health`
4. Ejecuta el nodo

**Respuesta esperada:**

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

## 🎮 Importar el Workflow

### Importar Workflow Pre-configurado ⚡

El workflow `workflow-riesgos.json` incluye 14 nodos interconectados con lógica completa:

**Funcionalidades integradas:**

- ✅ Gestión automática de Google Sheets (creación si no existen)
- ✅ Schedule trigger (ejecución diaria a las 8 AM)
- ✅ Lectura de lista de empresas desde "monitoring_list"
- ✅ Llamadas al API del Exercise01 por cada empresa
- ✅ Validación de respuestas (status 200)
- ✅ Escritura de resultados en "monitoring_register"
- ✅ Formateo de datos con JavaScript
- ✅ Emails de éxito y error
- ✅ Manejo robusto de errores

**Pasos para importar:**

1. **En n8n, haz clic en "Workflows"** (menú superior izquierdo)
2. **Haz clic en "Import from File"**
3. **Selecciona el archivo:** `workflows/workflow-riesgos.json`
4. **El workflow aparecerá con 14 nodos ya configurados**

**Configuraciones necesarias:**

5. **Google Sheets Credentials** (3 nodos):

   - `Get row(s) in sheet`
   - `Create spreadsheet` / `Create spreadsheet1`
   - `Append row in sheet` / `Append row in sheet1`
   - **Acción:** Asignar "Google Sheets account" OAuth2

6. **Google Drive Credentials** (2 nodos):

   - `Search files and folders`
   - `Search files and folders1`
   - **Acción:** Asignar "Google Drive account" OAuth2

7. **SMTP Credentials** (2 nodos):

   - `Send email` (errores)
   - `Send email1` (reportes exitosos)
   - **Acción:** Configurar servidor SMTP
   - **IMPORTANTE:** Actualizar emails en los nodos:
     ```javascript
     fromEmail: "tu-email@gmail.com";
     toEmail: "destinatario@gmail.com";
     ```

8. **Empresas iniciales** (opcional):

   - Editar nodo `Code in JavaScript1`
   - Modificar lista por defecto:
     ```javascript
     return [
     	{ nombre: "Tesla" },
     	{ nombre: "Apple" },
     	{ nombre: "Microsoft" },
     	{ nombre: "Amazon" },
     ];
     ```

9. **¡Listo!** Haz clic en **"Execute Workflow"**

**Qué sucederá:**

- Si no existe "monitoring_list": Se crea y puebla con empresas por defecto
- Si existe: Lee empresas del sheet
- Llama al API por cada empresa
- Si API responde OK: Guarda en "monitoring_register" + Envía email exitoso
- Si API falla: Envía email de error

**Activación automática:**

- Activa el workflow (toggle superior derecho)
- Se ejecutará automáticamente todos los días a las 8:00 AM

### Estructura del Workflow Importado

**Flujo completo (14 nodos):**

```
1. Schedule Trigger (8 AM diario)
   ↓
2. Google Drive: Buscar "monitoring_list"
   ↓
3. IF: ¿Existe monitoring_list?
   ├─ NO → 4. Crear sheet
   │         ↓
   │      5. JS: Generar empresas (Tesla, Apple, Luis Arce)
   │         ↓
   │      6. Append: Escribir empresas
   │         ↓
   └─ SI → 7. Get rows: Leer empresas del sheet
              ↓
         8. HTTP Request: POST a Exercise01 API
            URL: host.docker.internal:8000/api/v1/risk-analysis
            Param: company_name={{ $json.nombre }}
            ↓
         9. IF: ¿Status 200?
            ├─ NO → 16. Send Email (ERROR)
            │
            └─ SI → 10. Google Drive: Buscar "monitoring_register"
                      ↓
                   11. IF: ¿Existe monitoring_register?
                      ├─ NO → 12. Crear sheet "registros"
                      │         ↓
                      └─ SI → 13. JS: Formatear datos API
                                ↓
                             14. Append: Guardar en "registros"
                                ↓
                             15. Send Email (SUCCESS)
```

**Nodos Clave:**

- **HTTP Request**: `retryOnFail: true`, `onError: continueRegularOutput`
- **Code in JavaScript**: Transforma respuesta JSON a formato Sheets
- **If conditions**: Validación de existencia de sheets y status codes
- **Send email**: Dos ramas (exitoso vs error) con templates HTML/texto

**Datos guardados en Sheets:**

```
timestamp_analisis | status | message | company | registration_date |
risk_status | risk_score | sentiment | compliance_type | evidence |
url | manual_review
```

---

## � Exportar tu Workflow (Para Compartir)

Una vez que hayas creado o modificado un workflow:

1. **Abrir el workflow** en n8n
2. **Hacer clic en el menú ⋯** (tres puntos, esquina superior derecha)
3. **Seleccionar "Download"**
4. **Guardar el archivo** en `./workflows/mi-workflow.json`

```powershell
# Mover el workflow descargado a la carpeta del proyecto
mv ~/Downloads/workflow-name.json ./workflows/mi-workflow-personalizado.json
```

**Esto te permite:**

- ✅ Hacer backup de tus workflows
- ✅ Compartir workflows con el equipo
- ✅ Versionar workflows en Git
- ✅ Migrar workflows entre instancias de n8n

---

## �🔧 Comandos Útiles

### Gestión de Docker

```powershell
# Ver logs en tiempo real
docker-compose logs -f

# Detener n8n
docker-compose down

# Reiniciar n8n
docker-compose restart

# Ver estado
docker ps

# Acceder al contenedor (debug)
docker exec -it $(docker ps -qf "name=n8n") /bin/sh
```

### Troubleshooting

```powershell
# Verificar que el API está accesible desde Docker
docker exec -it $(docker ps -qf "name=n8n") /bin/sh
curl http://host.docker.internal:8000/health
exit

# Si no funciona, obtén tu IP local:
ipconfig | findstr IPv4
# Usa: http://192.168.X.X:8000/api/v1/risk-analysis
```

---

## 📊 Ejemplo de Respuesta del API

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

## 🎯 Próximos Pasos

1. ✅ **Configurar Google Cloud:**

   - Crear proyecto en Google Cloud Console
   - Habilitar APIs: Gmail, Sheets, Drive
   - Crear credenciales OAuth 2.0

2. ✅ **Configurar credenciales en n8n:**

   - Settings → Credentials → Add Credential
   - Configurar Gmail OAuth2
   - Configurar Google Sheets OAuth2

3. ✅ **Crear workflow completo:**

   - Implementar el workflow avanzado descrito arriba
   - Programar ejecución automática
   - Probar con lista de empresas real

4. ✅ **Leer documentación completa:**
   - [README.md](README.md) - Guía detallada
   - [../README.md](../README.md) - Documentación general del proyecto

---

## ❓ Preguntas Frecuentes

**¿Por qué "connection refused" al llamar al API?**

- Verifica que el API del Ejercicio 01 está corriendo
- Usa `host.docker.internal` en lugar de `localhost`
- Verifica el puerto: 8000

**¿Dónde se guardan los workflows?**

- En el volumen `./n8n_data/database.sqlite`
- Se persisten automáticamente

**¿Cómo hacer backup?**

```powershell
# Backup completo de n8n
cp -r ./n8n_data ./n8n_data_backup_$(Get-Date -Format "yyyyMMdd")
```

**¿Puedo usar otro puerto?**

- Sí, edita `N8N_PORT` en `.env`
- Luego: `docker-compose down && docker-compose up -d`

---

## 🆘 Soporte

Si tienes problemas:

1. Revisa la sección [Troubleshooting](README.md#troubleshooting) del README principal
2. Verifica los logs: `docker-compose logs -f`
3. Consulta la [documentación oficial de n8n](https://docs.n8n.io/)

---

**¡Listo!** Ya tienes n8n integrado con SafeBank AI. 🎉

Para información más detallada, consulta el [README.md](README.md) completo.
