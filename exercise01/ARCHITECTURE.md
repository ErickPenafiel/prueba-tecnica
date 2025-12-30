# Weather Sentiment API - Nueva Arquitectura

## 📁 Estructura del Proyecto

```
app/
├── __init__.py                 # Inicialización del paquete
├── main.py                     # Aplicación FastAPI principal
├── config.py                   # Configuración centralizada
├── exceptions.py               # Excepciones personalizadas
├── models.py                   # Modelos Pydantic (schemas)
├── utils.py                    # Utilidades generales
│
├── api/                        # Capa de API
│   ├── __init__.py
│   └── routes.py              # Definición de endpoints
│
├── services/                   # Capa de servicios (lógica de negocio)
│   ├── __init__.py
│   ├── weather_service.py     # Servicio de consulta de clima
│   └── ml_service.py          # Servicio de ML/sentimiento
│
├── weather_service.py         # [LEGACY] Mantener compatibilidad
└── ml_model.py                # [LEGACY] Mantener compatibilidad
```

## 🏗️ Principios de Arquitectura

### 1. **Separación de Responsabilidades**

- **API Layer** (`api/`): Maneja requests/responses HTTP
- **Service Layer** (`services/`): Lógica de negocio
- **Models** (`models.py`): Definición de estructuras de datos
- **Config** (`config.py`): Configuración centralizada

### 2. **Arquitectura en Capas**

```
┌─────────────────────────────────┐
│     API Layer (routes.py)       │  ← Endpoints HTTP
├─────────────────────────────────┤
│   Service Layer (services/)     │  ← Lógica de negocio
├─────────────────────────────────┤
│   Models (models.py)            │  ← Validación de datos
├─────────────────────────────────┤
│   Config (config.py)            │  ← Configuración
└─────────────────────────────────┘
```

### 3. **Características Implementadas**

#### ✅ Configuración Centralizada

- Variables de entorno en un solo lugar
- Fácil de modificar y testear

#### ✅ Manejo de Errores Robusto

- Excepciones personalizadas por tipo de error
- Status codes HTTP apropiados
- Mensajes descriptivos en español

#### ✅ Estructura de Respuesta Estándar

```python
{
    "data": {...},          # Datos solicitados
    "message": "...",       # Mensaje descriptivo
    "status_code": 200      # Código HTTP
}
```

#### ✅ Código Limpio y Mantenible

- Separación clara de responsabilidades
- Métodos pequeños y enfocados
- Docstrings completos

#### ✅ Escalabilidad

- Fácil añadir nuevos servicios
- Fácil añadir nuevos endpoints
- Estructura preparada para crecimiento

## 🚀 Mejoras Implementadas

### Antes vs Después

**Antes:**

- Todo en 3 archivos
- Configuración mezclada con lógica
- Errores genéricos
- Difícil de mantener

**Después:**

- Arquitectura modular
- Configuración centralizada
- Manejo de errores específico
- Fácil de mantener y escalar

### Manejo de Errores Mejorado

| Error                | Status Code | Mensaje                |
| -------------------- | ----------- | ---------------------- |
| Ciudad vacía         | 400         | Parámetro requerido    |
| API key inválida     | 401         | No autorizado          |
| Ciudad no encontrada | 404         | No encontrada          |
| Rate limit           | 429         | Límite excedido        |
| Error interno        | 500         | Error del servidor     |
| Timeout              | 504         | Tiempo agotado         |
| Sin conexión         | 503         | Servicio no disponible |

## 📝 Uso

### Endpoint Principal

```http
GET /weather-sentiment?city=Madrid
```

**Respuesta:**

```json
{
	"city": "Madrid",
	"country": "ES",
	"description": "cielo claro",
	"temperature": 15.5,
	"feels_like": 14.2,
	"humidity": 65,
	"sentiment_label": "positivo",
	"sentiment_probability": 0.87
}
```

### Health Check

```http
GET /health
```

## 🔧 Ventajas de esta Arquitectura

1. **Testeable**: Cada capa se puede testear independientemente
2. **Mantenible**: Código organizado y documentado
3. **Escalable**: Fácil añadir funcionalidades
4. **Reutilizable**: Servicios pueden usarse en múltiples endpoints
5. **Clean Code**: Sigue principios SOLID

## 📚 Próximos Pasos Sugeridos

- [ ] Añadir tests unitarios
- [ ] Implementar logging estructurado
- [ ] Añadir caché para requests frecuentes
- [ ] Implementar rate limiting
- [ ] Dockerizar la aplicación
- [ ] Añadir CI/CD pipeline
