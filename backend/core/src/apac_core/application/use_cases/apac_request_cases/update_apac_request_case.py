from dataclasses import dataclass
from apac_core.domain.repositories.apac_request_repository import ApacRequestRepository
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.exceptions import PermissionDeniedException
from apac_core.domain.messages.apac_request_messages import APAC_REQUEST_NOT_PENDING


@dataclass
class SetApacRequestToApprovedUseCase:
    repo_apac_request: ApacRequestRepository