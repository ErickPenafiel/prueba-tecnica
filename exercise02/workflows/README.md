# 📁 Workflows de n8n

Este directorio contiene workflows exportados de n8n que pueden ser importados directamente en tu instancia.

## 📋 Workflow Disponible

### `workflow-riesgos.json` ⭐

**Descripción:** Workflow completo de análisis de riesgo con integración a Google Sheets y ejecución programada.

**Componentes:**

- Schedule Trigger (ejecución diaria a las 8 AM)
- Google Sheets (lectura de lista de empresas)
- HTTP Request al API del Ejercicio 01 (SafeBank AI)
- Procesamiento y formateo de resultados
- Google Sheets (escritura de resultados)
- Lógica condicional para alertas

**Requisitos:**

- ✅ Google Sheets API configurado en n8n
- ✅ Spreadsheet de Google Sheets con lista de empresas
- ✅ API del Ejercicio 01 ejecutándose en puerto 8000

**Configuración requerida después de importar:**

1. Asignar credenciales de Google Sheets
2. Configurar el ID del Google Spreadsheet en los nodos de Sheets
3. Ajustar el horario del Schedule Trigger si es necesario
4. Verificar la URL del API: `http://host.docker.internal:8000/api/v1/risk-analysis`

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
