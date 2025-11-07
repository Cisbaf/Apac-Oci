from pydantic import BaseModel
from apac_core.domain.value_objects.cns import CnsField
from apac_core.domain.value_objects.cbo import CboField
from pydantic import BaseModel, field_validator, field_serializer
from apac_core.domain.exceptions import ValidationException

class MedicData(BaseModel):
    name: str
    cns: CnsField
    cbo: CboField

    @field_validator('*', mode="before")
    @classmethod
    def validate_non_empty(cls, value: str, info):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationException(f"O campo '{info.field_name}' não pode ser vazio ou None.")
        return value

    @field_serializer("cns", return_type=str)
    def serialize_medic_cns(self, cns: CnsField, _info):
        return cns.value
    
    @field_serializer("cbo", return_type=str)
    def serialize_medic_cbo(self, cbo: CboField, _info):
        return cbo.value