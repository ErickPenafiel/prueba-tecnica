"""
Utilidades generales de la aplicación.
"""
from datetime import datetime


def timestamp_to_datetime(timestamp: int) -> str:
    """
    Convierte un timestamp Unix a formato datetime legible.
    
    Args:
        timestamp: Timestamp Unix (segundos desde 1970)
        
    Returns:
        Fecha y hora en formato string
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def validate_non_empty_string(value: str, field_name: str) -> str:
    """
    Valida que una cadena no esté vacía.
    
    Args:
        value: Valor a validar
        field_name: Nombre del campo (para mensajes de error)
        
    Returns:
        El valor si es válido
        
    Raises:
        ValueError: Si el valor es vacío
    """
    if not value or not value.strip():
        raise ValueError(f"El campo '{field_name}' no puede estar vacío")
    return value.strip()
