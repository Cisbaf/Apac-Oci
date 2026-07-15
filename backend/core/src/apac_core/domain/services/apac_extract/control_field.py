from typing import Sequence, Tuple

CONTROL_FIELD_MODULUS = 1111


def calculate_control_field(
    procedures: Sequence[Tuple[str, int]],
    apac_numbers: Sequence[str],
) -> str:
    """Fórmula do cbc-smt-vrf (layout_Exportacao_APAC_v20250513.pdf, seção final):
    soma os códigos de procedimento + quantidades + números de APAC do lote,
    tira o resto da divisão por 1111 e soma 1111 ao resto (domínio [1111..2221]).
    Não é usada no fluxo real de export ainda (T-012) — cbc-smt-vrf segue fixo em "1810".
    """
    total = sum(int(code) for code, _quantity in procedures)
    total += sum(quantity for _code, quantity in procedures)
    total += sum(int(numero_apac) for numero_apac in apac_numbers)
    remainder = total % CONTROL_FIELD_MODULUS
    return str(remainder + CONTROL_FIELD_MODULUS)
