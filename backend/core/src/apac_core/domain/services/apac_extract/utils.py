import calendar
from datetime import date
from typing import Union
import unicodedata

def sanitize_text(value: str) -> str:
    """
    Remove acentos, caracteres especiais e espaços invisíveis.
    Garante apenas caracteres ASCII básicos.
    """
    if not isinstance(value, str):
        value = str(value)

    # Normaliza e remove acentos (NFD separa base + acento)
    value = unicodedata.normalize("NFD", value)
    value = "".join(c for c in value if unicodedata.category(c) != "Mn")

    # Remove caracteres invisíveis e BOMs (\ufeff)
    value = value.replace("\ufeff", "").replace("\n", "").replace("\r", "").replace("\t", "")

    # Substitui caracteres fora do ASCII básico
    value = value.encode("ascii", "ignore").decode("ascii")

    return value

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

def get_end_of_month_offset(d: date, months_ahead: int) -> date:
    """
    Retorna o último dia do mês que fica `months_ahead` meses à frente do mês de `d`.

    months_ahead=1 replica o comportamento antigo de `get_end_of_next_month`
    (regra extinta do atributo complementar 054 — 2 competências).
    months_ahead=2 dá o último dia do 3º mês, ou seja, a validade normal de uma
    APAC (3 meses/competências) vigente desde a Portaria SAES/MS Nº 3.958/2026
    (competência 04/2026 em diante).
    """
    year = d.year
    month = d.month + months_ahead
    while month > 12:
        month -= 12
        year += 1

    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)