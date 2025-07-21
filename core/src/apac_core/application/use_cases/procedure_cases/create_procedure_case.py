
from dataclasses import dataclass
from apac_core.domain.repositories.procedure_repository import ProcedureRepository
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.exceptions import ValidationException

@dataclass
class CreateProcedureUseCase:
    repo: ProcedureRepository

    def execute(self, name: str, code: str, parent_id: int = None, description: str = None) -> Procedure:
        
        if len(name) < 5:
            raise ValidationException("O nome deve conter pelo menos 5 caracteres!")
        
        if len(code) < 5:
            raise ValidationException("O codigo sigtap deve conter pelo menos 5 caracteres!")

        parent = None
        if parent_id:
            parent = self.repo.get_by_id(parent_id)
        
        return self.repo.save(
            Procedure(
                name=name,
                code=code,
                description=description,
                parent=parent
            )
        )
