from dataclasses import dataclass
from apac_core.domain.repositories.apac_request_repository import ApacRequestRepository
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.exceptions import PermissionDeniedException
from apac_core.domain.messages.apac_request_messages import APAC_REQUEST_NOT_PENDING

@dataclass
class GetApacRequestPedingUseCase:
    repo_apac_request: ApacRequestRepository

    def execute(self, apac_request_id: int):
        apac_request = self.repo_apac_request.get_by_id(apac_request_id)
        if apac_request.status != ApacStatus.PENDING:
            raise PermissionDeniedException(APAC_REQUEST_NOT_PENDING)
        return apac_request