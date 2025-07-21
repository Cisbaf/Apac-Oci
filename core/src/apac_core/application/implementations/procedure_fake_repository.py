from typing import List
from apac_core.domain.repositories.procedure_repository import ProcedureRepository
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.exceptions import NotFoundException

class ProcedureFakeRepository(ProcedureRepository):
    
    def __init__(self):
        super().__init__()
        self.increment_id = 1
        self.procedures: List[Procedure] = []
    
    def save(self, procedure):
        if not procedure.id:
            procedure.id = self.increment_id
            self.increment_id += 1
            self.procedures.append(procedure)
        else:
            for i, _procedure in enumerate(self.procedures):
                if _procedure.id == procedure.id:
                    self.procedures[i] = procedure
                    break
        return procedure

    def get_by_id(self, id):
        for procedure in self.procedures:
            if procedure.id == id:
                return procedure
        raise NotFoundException()