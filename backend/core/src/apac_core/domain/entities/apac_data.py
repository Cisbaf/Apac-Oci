from pydantic import BaseModel, field_validator, field_serializer
from typing import List, Optional
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.entities.procedure_record import ProcedureRecord
from apac_core.domain.entities.cid import Cid
from apac_core.domain.exceptions import ValidationException
from apac_core.domain.value_objects.cns import CnsField
from apac_core.domain.value_objects.cpf import CpfField
from apac_core.domain.value_objects.cep import CepField
from apac_core.domain.dto.patientData import PatientData
from apac_core.domain.dto.medicData import MedicData
from datetime import date


class ApacData(BaseModel):
    patient_data: PatientData
    supervising_physician_data: MedicData
    authorizing_physician_data: MedicData
    cid: Cid
    procedure_date: date
    main_procedure: Procedure
    sub_procedures: List[ProcedureRecord]
    id: Optional[int] = None

    @field_validator('procedure_date', mode='before')
    @classmethod
    def validate_non_empty(cls, value: str, info):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationException(f"O campo '{info.field_name}' não pode ser vazio ou None.")
        return value
    
    # @field_serializer("patient_cpf", return_type=str)
    # def serialize_patient_cpf(self, cpf: CpfField, _info):
    #     return cpf.value
    
    # @field_serializer("patient_cns", return_type=str)
    # def serialize_patient_cns(self, cns: CnsField, _info):
    #     return cns.value

    # @field_serializer("patient_address_postal_code", return_type=str)
    # def serialize_patient_address_postal_code(self, cep: CepField, _info):
    #     return cep.value

    # @field_serializer("medic_cns", return_type=str)
    # def serialize_medic_cns(self, cns: CnsField, _info):
    #     return cns.value