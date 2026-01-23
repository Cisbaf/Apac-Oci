from pydantic import BaseModel, field_validator
from typing import List, Optional
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.entities.procedure_record import ProcedureRecord
from apac_core.domain.entities.cid import Cid
from apac_core.domain.exceptions import ValidationException
from apac_core.domain.dto.patientData import PatientData
from apac_core.domain.dto.medicData import MedicData
from datetime import date


class ApacData(BaseModel):
    patient_data: PatientData
    supervising_physician_data: MedicData
    authorizing_physician_data: MedicData
    cid: Cid
    procedure_date: date
    discharge_date: date
    main_procedure: Procedure
    sub_procedures: List[ProcedureRecord]
    id: Optional[int] = None

    @field_validator('procedure_date', 'discharge_date', mode='after')
    @classmethod
    def validate_discharge_date(cls, v, info):
        procedure_date = info.data.get('procedure_date')
        if procedure_date and v < procedure_date:
            raise ValueError("A data da alta não pode ser anterior à data do procedimento.")
        return v
    
    @field_validator('procedure_date', 'discharge_date', mode='before')
    @classmethod
    def validate_non_empty(cls, value: str, info):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationException(f"O campo '{info.field_name}' não pode ser vazio ou None.")
        return value
