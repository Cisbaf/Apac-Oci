from pydantic import BaseModel
from apac_core.domain.value_objects.cns import CnsField
from apac_core.domain.value_objects.cpf import CpfField
from apac_core.domain.value_objects.cep import CepField
from datetime import date
from pydantic import BaseModel, field_validator, field_serializer
from apac_core.domain.exceptions import ValidationException

class PatientData(BaseModel):
    name: str
    record_number: str
    cns: CnsField
    cpf: CpfField
    birth_date: date
    race_color: str
    gender: str
    mother_name: str
    address_street_type: str
    address_street_name: str
    address_number: str
    address_complement: str
    address_postal_code: CepField
    address_neighborhood: str
    address_city: str
    address_state: str

    @field_validator(
        'name', 'cns', 'cpf',
        'birth_date', 'race_color', 'gender', 'mother_name',
        'address_street_type', 'address_street_name', 'address_number',
        'address_postal_code', 'address_neighborhood',
        'address_city', 'address_state',
        mode='before'
    )
    @classmethod
    def validate_non_empty(cls, value: str, info):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationException(f"O campo '{info.field_name}' não pode ser vazio ou None.")
        return value
    
    @field_serializer("cpf", return_type=str)
    def serialize_cpf(self, cpf: CpfField, _info):
        return cpf.value
    
    @field_serializer("cns", return_type=str)
    def serialize_cns(self, cns: CnsField, _info):
        return cns.value

    @field_serializer("address_postal_code", return_type=str)
    def serialize_patient_address_postal_code(self, cep: CepField, _info):
        return cep.value
