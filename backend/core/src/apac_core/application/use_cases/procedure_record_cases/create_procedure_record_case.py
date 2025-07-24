
from dataclasses import dataclass
from pydantic import BaseModel
from apac_core.domain.repositories.procedure_repository import ProcedureRepository
from apac_core.domain.repositories.procedure_record_repository import ProcedureRecordRepository
from apac_core.domain.entities.procedure_record import ProcedureRecord
from apac_core.domain.exceptions import ValidationException


class CreateProcedureRecordDTO(BaseModel):
    procedure_id: int
    quantity: int

@dataclass
class CreateProcedureRecordUseCase:
    repo_procedure_record: ProcedureRecordRepository
    repo_procedure: ProcedureRepository

    def execute(self, data: CreateProcedureRecordDTO) -> ProcedureRecord:
        
        if data.quantity <= 0:
            raise ValidationException("A quantidade deve ser maior que 0")
        
        procedure = self.repo_procedure.get_by_id(data.procedure_id)

        return self.repo_procedure_record.save(ProcedureRecord(procedure=procedure, quantity=data.quantity))
