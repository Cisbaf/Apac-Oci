import calendar
from datetime import date
from typing import Union

def fix_length(value: Union[str, int], size: int) -> str:
    """Trunca ou preenche à direita com espaço para garantir tamanho fixo."""
    value = str(value or "")
    return value[:size].ljust(size)

def only_digits(value: str, size: int) -> str:
    """Remove tudo que não é dígito e aplica tamanho fixo."""
    return fix_length(''.join(filter(str.isdigit, value)), size)

def format_date_yyyymmdd(value: Union[str, date]) -> str:
    """Converte string DD/MM/AAAA ou objeto date para AAAAMMDD"""
    if isinstance(value, date):
        return value.strftime("%Y%m%d")
    elif isinstance(value, str):
        parts = value.replace("-", "/").split("/")
        if len(parts) == 3:
            dd, mm, yyyy = parts
            return f"{yyyy}{mm}{dd}"
        return value  # já pode estar no formato certo
    return ""

def format_with_zeros(quantity: int, length: int) -> str:
    return str(quantity).zfill(length)

def get_end_of_next_month(d: date) -> date:
    """
    Retorna o último dia do mês seguinte à data fornecida, sem usar bibliotecas externas.
    
    :param d: Data de entrada (datetime.date)
    :return: Último dia do mês seguinte (datetime.date)
    """
    # Avança para o mês seguinte
    year = d.year
    month = d.month + 1
    if month > 12:
        month = 1
        year += 1

    # Descobre o último dia do mês seguinte
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)