from pydantic import BaseModel, field_validator
import re

class CnsField(BaseModel):
    value: str

    # Remove máscara (espaços, traços, pontos)
    @field_validator('value', mode='before')
    @classmethod
    def clean(cls, v):
        if isinstance(v, str):
            return re.sub(r'\D', '', v)
        raise TypeError('CNS deve ser uma string')

    # Valida se o CNS é válido
    @field_validator('value', mode='after')
    @classmethod
    def validate(cls, v):
        if not cls._is_valid_cns(v):
            raise ValueError('CNS inválido')
        return v

    @staticmethod
    def _is_valid_cns(cns: str) -> bool:
        if len(cns) != 15:
            return False

        if cns[0] not in '123456789':
            return False

        soma = sum(int(digito) * peso for digito, peso in zip(cns, range(15, 0, -1)))
        return soma % 11 == 0
