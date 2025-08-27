from dataclasses import dataclass
from apac_core.domain.repositories.apac_batch_repository import ApacBatchRepository
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.entities.apac_batch import ApacBatch

@dataclass
class GetFinishedApacBatchUseCase:
    repo_apac_batch: ApacBatchRepository

    def execute(self, batch_id: int) -> ApacBatch:
        apac_batch = self.repo_apac_batch.get_by_id(batch_id)
        if not apac_batch:
            raise Exception("Faixa não encontrada!")
        
        if not apac_batch.apac_request:
            raise Exception("Essa faixa não está atribuida a uma solicitação!")
        
        if not apac_batch.apac_request.status == ApacStatus.APPROVED:
            raise Exception("Essa solicitação não foi aprovada!")

        return apac_batch



