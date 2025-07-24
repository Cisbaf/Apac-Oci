from typing import List
from apac_core.domain.repositories.procedure_record_repository import ProcedureRecordRepository
from apac_core.domain.entities.procedure_record import ProcedureRecord
from apac_core.domain.exceptions import NotFoundException

class ProcedureRecordFakeRepository(ProcedureRecordRepository):
    
    def __init__(self):
        super().__init__()
        self.increment_id = 1
        self.procedures_record: List[ProcedureRecord] = []
    
    def save(self, procedure_record):
        if not procedure_record.id:
            procedure_record.id = self.increment_id
            self.increment_id += 1
            self.procedures_record.append(procedure_record)
        else:
            for i, _procedure_record in enumerate(self.procedures_record):
                if _procedure_record == procedure_record.id:
                    self.procedures_record[i] = procedure_record
                    break
        return procedure_record

    def get_by_id(self, id):
        for procedure_record in self.procedures_record:
            if procedure_record.id == id:
                return procedure_record
        raise NotFoundException()