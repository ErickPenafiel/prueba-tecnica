# 📁 Workflows de n8n

Este directorio contiene workflows exportados de n8n que pueden ser importados directamente en tu instancia.

## 📋 Workflow Disponible

### `workflow-riesgos.json` ⭐

**Descripción:** Workflow completo de análisis de riesgo automatizado con 14 nodos interconectados, gestión automática de Google Sheets, notificaciones por email, y manejo robusto de errores.

**Arquitectura del Workflow (14 Nodos):**

```
┌─────────────────────┐
│ 1. Schedule Trigger │ → Ejecuta diariamente a las 8 AM
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│ 2. Search files (Drive)     │ → Busca "monitoring_list"
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 3. If (¿existe sheet?)      │ → Verifica si existe
└────┬─────────────────┬──────┘
     │NO               │SI
     ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│ 4. Create    │  │ 7. Get rows      │
│    Sheet     │  │    from sheet    │
└───┬──────────┘  └────┬─────────────┘
    │                  │
    ▼                  │
┌──────────────┐       │
│ 5. Code JS   │       │
│ (Empresas)   │       │
└───┬──────────┘       │
    │                  │
    ▼                  │
┌──────────────┐       │
│ 6. Append    │       │
│    rows      │       │
└───┬──────────┘       │
    └──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 8. HTTP Request (FastAPI)   │ → POST a Exercise01 API
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 9. If (¿status 200?)        │ → Valida respuesta
└────┬─────────────────┬──────┘
     │SI               │NO
     ▼                 ▼
┌──────────────┐  ┌─────────────┐
│ 10. Search   │  │ 14. Send    │
│     Drive    │  │     Email   │
│ (register)   │  │  (ERROR)    │
└───┬──────────┘  └─────────────┘
    │
    ▼
┌──────────────┐
│ 11. If       │
│ (¿existe?)   │
└─┬───────┬────┘
  │NO     │SI
  ▼       ▼
┌──────┐┌──────┐
│ 12.  ││      │
│Create││      │
│Sheet ││      │
└─┬────┘│      │
  └──────┘      │
     │          │
     ▼          │
┌──────────────┐│
│ 13. Code JS  ││
│  (Format)    ││
└──┬───────────┘│
   └─────────────┘
        │
        ▼
┌─────────────────┐
│ 14. Append row  │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ 15. Send Email  │ → Notificación de éxito
└─────────────────┘
```

**Nodos Principales (14 en total):**

1. **Schedule Trigger** - Ejecuta workflow diariamente a las 8:00 AM
2. **Search files and folders1** (Drive) - Busca sheet "monitoring_list" en Google Drive
3. **If2** - Verifica si existe el sheet "monitoring_list"
4. **Create spreadsheet1** - Crea "monitoring_list" si no existe
5. **Code in JavaScript1** - Genera lista inicial de empresas (Tesla, Apple, Luis Arce)
6. **Append row in sheet1** - Escribe empresas en "monitoring_list"
7. **Get row(s) in sheet** - Lee lista completa de empresas del sheet
8. **HTTP Request** - Llama al API del Exercise01: `http://host.docker.internal:8000/api/v1/risk-analysis?company_name={{nombre}}`
9. **If** - Valida que status_code == 200
10. **Search files and folders** (Drive) - Busca sheet "monitoring_register" para resultados
11. **If1** - Verifica si existe el sheet de registros
12. **Create spreadsheet** - Crea "monitoring_register" con hoja "registros" si no existe
13. **Code in JavaScript** - Formatea datos del API para Google Sheets (timestamp, status, company, risk_status, etc.)
14. **Append row in sheet** - Guarda análisis en "monitoring_register"
15. **Send email1** - Envía reporte exitoso con todos los detalles del análisis
16. **Send email** (error branch) - Envía alerta de error si API falla

**Características Avanzadas:**

✅ **Gestión Automática de Sheets**: Crea automáticamente los Google Sheets si no existen
✅ **Manejo de Errores**: Rama alternativa con email de error si API falla (status ≠ 200)
✅ **Retry Logic**: HTTP Request configurado con `retryOnFail: true` y `onError: continueRegularOutput`
✅ **Formateo Inteligente**: JavaScript transforma respuesta JSON del API a formato legible para Sheets
✅ **Emails Detallados**: Incluyen timestamp, risk_status, risk_score, sentiment, compliance_type, evidence, URL, etc.
✅ **IDs Dinámicos**: Usa lógica condicional para referenciar el spreadsheet correcto (creado vs existente)

**Campos Procesados del API:**

```javascript
{
  timestamp_analisis: item.data?.analysis_timestamp,
  status: item.status_code,
  message: item.message,
  company: item.data?.company_name,
  registration_date: fechaLegible, // Formato: DD/MM/YYYY HH:mm:ss
  risk_status: item.data?.overall_risk_status,
  risk_score: item.data?.overall_risk_score,
  sentiment: item.data?.market_sentiment,
  compliance_type: item.data?.compliance_risk_type,
  evidence: item.data?.evidence_headline,
  url: item.data?.evidence_url,
  manual_review: item.data?.requires_manual_review ? "SI" : "NO"
}
```

**Requisitos:**

- ✅ Google Sheets API configurado en n8n (credencial: "Google Sheets account")
- ✅ Google Drive API configurado en n8n (credencial: "Google Drive account")
- ✅ SMTP configurado para envío de emails (credencial: "SMTP account")
- ✅ API del Ejercicio 01 ejecutándose en `http://host.docker.internal:8000`
- ✅ NewsAPI Key configurada en el API del Exercise01

**Configuración requerida después de importar:**

1. **Credenciales de Google Sheets**: Asignar OAuth2 credentials en nodos:

   - `Get row(s) in sheet`
   - `Create spreadsheet` / `Create spreadsheet1`
   - `Append row in sheet` / `Append row in sheet1`

2. **Credenciales de Google Drive**: Asignar OAuth2 credentials en nodos:

   - `Search files and folders`
   - `Search files and folders1`

3. **Credenciales SMTP**: Configurar servidor SMTP en nodos:

   - `Send email` (errores)
   - `Send email1` (reportes exitosos)
   - **Importante**: Actualizar `fromEmail` y `toEmail` con tus direcciones

4. **Ajustar Schedule Trigger**: Modificar horario si no deseas ejecución a las 8 AM

5. **Verificar URL del API**: Confirmar que `http://host.docker.internal:8000/api/v1/risk-analysis` es accesible desde el contenedor

6. **Configurar empresas iniciales**: Editar nodo "Code in JavaScript1" para modificar lista de empresas por defecto:
   ```javascript
   return [{ nombre: "Tesla" }, { nombre: "Apple" }, { nombre: "Luis Arce" }];
   ```

---

## 🔄 Cómo Importar Workflows

### Método 1: Desde la UI de n8n

1. Acceder a n8n: http://localhost:5678
2. Hacer clic en **Workflows** (menú superior)
3. Hacer clic en **Import from File**
4. Seleccionar el archivo `.json` desde este directorio
5. Configurar credenciales según sea necesario
6. Guardar y activar el workflow

### Método 2: Usando la API de n8n

```bash
# Importar workflow via API
curl -X POST http://localhost:5678/api/v1/workflows/import \
  -H "Content-Type: application/json" \
  -u admin:tu_contraseña \
  --data @./workflows/workflow-riesgos.json
```

---

## 📤 Cómo Exportar tus Workflows

1. Abrir el workflow en n8n
2. Hacer clic en el menú **⋯** (tres puntos) en la esquina superior derecha
3. Seleccionar **Download**
4. Guardar el archivo en este directorio
5. (Opcional) Renombrar con un nombre descriptivo
6. (Opcional) Agregar documentación en este README

---

## 🔐 Seguridad

**⚠️ IMPORTANTE:**

Los workflows exportados **NO contienen credenciales** por razones de seguridad. Las credenciales deben ser configuradas manualmente después de importar.

Sin embargo, los workflows pueden contener:

- URLs de APIs
- IDs de recursos (Spreadsheet IDs, etc.)
- Lógica de negocio
- Configuraciones de nodos

**Recomendaciones:**

- ✅ Revisar el archivo JSON antes de compartir
- ✅ Remover IDs sensibles si es necesario
- ✅ Documentar las credenciales requeridas
- ✅ Usar variables de entorno para configuraciones

---

## 📝 Estructura de un Workflow JSON

```json
{
	"name": "Risk Analysis Workflow",
	"nodes": [
		{
			"id": "...",
			"name": "HTTP Request",
			"type": "n8n-nodes-base.httpRequest",
			"position": [250, 300],
			"parameters": {
				"url": "http://host.docker.internal:8000/api/v1/risk-analysis",
				"method": "GET",
				"queryParameters": {
					"parameters": [
						{
							"name": "company_name",
							"value": "={{ $json.company_name }}"
						}
					]
				}
			}
		}
		// ... más nodos
	],
	"connections": {
		// ... conexiones entre nodos
	},
	"settings": {
		// ... configuración del workflow
	}
}
```

---

## 🎯 Mejores Prácticas

1. **Nombrar workflows descriptivamente:**

   - ✅ `risk-analysis-daily-report.json`
   - ❌ `workflow-1.json`

2. **Documentar cada workflow:**

   - Propósito
   - Dependencias
   - Credenciales requeridas
   - Frecuencia de ejecución

3. **Versionar workflows:**

   - Usar Git para trackear cambios
   - Incluir fecha en el nombre: `risk-analysis-v2-2025-12.json`

4. **Probar antes de compartir:**
   - Verificar que funciona correctamente
   - Probar la importación en una instancia limpia

---

## 🆘 Solución de Problemas

### Error al importar workflow

**Problema:** "Invalid workflow file"

**Soluciones:**

- Verificar que el archivo sea un JSON válido
- Verificar que contenga la estructura correcta de n8n
- Verificar la versión de n8n (workflows de versiones más nuevas pueden no ser compatibles con versiones antiguas)

### Workflow importado no funciona

**Problema:** Nodos muestran errores después de importar

**Soluciones:**

- Configurar todas las credenciales requeridas
- Verificar que las URLs y endpoints sean correctos
- Verificar que los servicios externos (APIs, Google, etc.) estén accesibles
- Revisar los parámetros de cada nodo

---

## 📚 Referencias

- [Documentación de n8n sobre Workflows](https://docs.n8n.io/workflows/)
- [Exportar e Importar Workflows](https://docs.n8n.io/workflows/export-import/)
- [Compartir Workflows](https://docs.n8n.io/workflows/share/)

---

**Última actualización:** Diciembre 2025
