
from dataclasses import dataclass
from apac_core.domain.repositories.cid_repository import CidRepository
from apac_core.domain.repositories.procedure_repository import ProcedureRepository
from apac_core.domain.entities.cid import Cid
from apac_core.domain.exceptions import ValidationException

@dataclass
class CreateCidUseCase:
    repo_cid: CidRepository
    repo_procedure: ProcedureRepository

    def execute(self, code: str, name: str, procedure_id: int) -> Cid:
        if len(name) < 4:
            raise ValidationException("O nome deve conter pelo menos 5 caracters!")
        
        # Obtém o procedimento pelo ID
        procedure = self.repo_procedure.get_by_id(procedure_id)

        return self.repo_cid.save(Cid(
            code=code,
            name=name,
            procedure=[procedure]
        ))
