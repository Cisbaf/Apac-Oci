from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.entities.procedure_record import ProcedureRecord
from apac_core.domain.entities.cid import Cid
from apac_core.domain.exceptions import ValidationException

class ApacData(BaseModel):
    patient_name: str
    patient_record_number: str
    patient_cns: str
    patient_cpf: str
    patient_birth_date: str
    patient_race_color: str
    patient_gender: str
    patient_mother_name: str
    patient_address_street_type: str
    patient_address_street_name: str
    patient_address_number: str
    patient_address_complement: str
    patient_address_postal_code: str
    patient_address_neighborhood: str
    patient_address_city: str
    patient_address_state: str
    medic_name: str
    medic_cns: str
    medic_cbo: str
    cid: Cid
    procedure_date: str
    main_procedure: Procedure
    sub_procedures: List[ProcedureRecord]
    id: Optional[int] = None

    @field_validator(
        'patient_name', 'patient_record_number', 'patient_cns', 'patient_cpf',
        'patient_birth_date', 'patient_race_color', 'patient_gender', 'patient_mother_name',
        'patient_address_street_type', 'patient_address_street_name', 'patient_address_number',
        'patient_address_postal_code', 'patient_address_neighborhood',
        'patient_address_city', 'patient_address_state', 'medic_name', 'medic_cns', 'medic_cbo', 'procedure_date',
        mode='before'
    )
    @classmethod
    def validate_non_empty(cls, value: str, info):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationException(f"O campo '{info.field_name}' não pode ser vazio ou None.")
        return value
