from pydantic import BaseModel, field_validator
import re

class CepField(BaseModel):
    value: str

    # Remove máscara
    @field_validator('value', mode='before')
    @classmethod
    def clean(cls, v):
        if isinstance(v, str):
            return re.sub(r'\D', '', v)
        raise TypeError('CEP deve ser uma string')

    # Valida formato (8 dígitos numéricos)
    @field_validator('value', mode='after')
    @classmethod
    def validate(cls, v):
        if not re.fullmatch(r'\d{8}', v):
            raise ValueError('CEP inválido (deve conter 8 dígitos)')
        return v
