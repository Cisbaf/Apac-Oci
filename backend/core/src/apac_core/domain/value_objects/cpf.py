from pydantic import BaseModel, field_validator
import re

class CpfField(BaseModel):
    value: str

    # Remove máscara: pontos e traço
    @field_validator('value', mode='before')
    @classmethod
    def clean(cls, v):
        if isinstance(v, str):
            return re.sub(r'\D', '', v)  # Remove tudo que não for número
        raise TypeError('CPF deve ser uma string')

    # Valida o CPF
    @field_validator('value', mode='after')
    @classmethod
    def validate(cls, v):
        if not cls._is_valid_cpf(v):
            raise ValueError('CPF inválido')
        return v

    @staticmethod
    def _is_valid_cpf(cpf: str) -> bool:
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        for i in [9, 10]:
            soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(i))
            digito = ((soma * 10) % 11) % 10
            if int(cpf[i]) != digito:
                return False
        return True
