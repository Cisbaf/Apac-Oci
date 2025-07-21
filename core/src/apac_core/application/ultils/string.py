from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel


def sanitize_numeric(value: str) -> str:
    """Remove todos os caracteres não numéricos"""
    return ''.join(filter(str.isdigit, str(value)))

def format_field(value: Any, length: int, field_type: str) -> str:
    """Formata campo para o layout de texto fixo"""
    str_value = str(value) if value is not None else ""
    
    if field_type == "num":
        # Campos numéricos: zeros à esquerda, sem caracteres especiais
        clean_value = sanitize_numeric(str_value)
        return clean_value.zfill(length)[:length]
    else:  # alfa
        # Campos alfanuméricos: remove caracteres problemáticos e completa com espaços
        clean_value = str_value.translate(
            str.maketrans({
                '\n': ' ', '\r': ' ', '\t': ' ',
                '/': ' ', '-': ' ', '.': ' ', ',': ' '
            })
        ).strip()
        return clean_value.ljust(length)[:length]