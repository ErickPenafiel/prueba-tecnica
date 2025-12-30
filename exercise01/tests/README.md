# Tests para Weather Sentiment API

## Configuración de Tests (Futuro)

```bash
pip install pytest pytest-asyncio httpx
```

## Estructura de Tests Sugerida

```
tests/
├── __init__.py
├── conftest.py                 # Configuración de fixtures
├── test_config.py             # Tests de configuración
├── test_weather_service.py    # Tests del servicio de clima
├── test_ml_service.py         # Tests del servicio ML
└── test_routes.py             # Tests de endpoints
```

## Ejemplo de Test

```python
# tests/test_weather_service.py
import pytest
from app.services import WeatherService

def test_weather_service_invalid_city():
    result = WeatherService.get_weather("")
    assert result["status_code"] == 400
    assert result["data"] is None

def test_weather_service_valid_city():
    result = WeatherService.get_weather("Madrid")
    if result["status_code"] == 200:
        assert result["data"] is not None
        assert "city" in result["data"].columns
```
