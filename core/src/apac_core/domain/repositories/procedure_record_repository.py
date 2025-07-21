from abc import ABC, abstractmethod
from apac_core.domain.entities.procedure_record import ProcedureRecord

class ProcedureRecordRepository(ABC):

    @abstractmethod
    def save(self, procedure_record: ProcedureRecord) -> ProcedureRecord:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> ProcedureRecord:
        pass