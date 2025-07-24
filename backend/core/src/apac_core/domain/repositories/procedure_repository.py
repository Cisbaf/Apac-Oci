from abc import ABC, abstractmethod
from apac_core.domain.entities.procedure import Procedure

class ProcedureRepository(ABC):

    @abstractmethod
    def save(self, procedure: Procedure) -> Procedure:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Procedure:
        pass