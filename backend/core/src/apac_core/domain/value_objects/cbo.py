from pydantic import BaseModel, field_validator
import re

class CboField(BaseModel):
    value: str

    # Remove máscara
    @field_validator('value', mode='before')
    @classmethod
    def clean(cls, v):
        if isinstance(v, str):
            return re.sub(r'\D', '', v)
        raise TypeError('CBO deve ser uma string')

    # Valida formato (6 dígitos numéricos)
    @field_validator('value', mode='after')
    @classmethod
    def validate(cls, v):
        if not re.fullmatch(r'\d{6}', v):
            raise ValueError('CBO inválido (deve conter 6 dígitos)')
        return v
