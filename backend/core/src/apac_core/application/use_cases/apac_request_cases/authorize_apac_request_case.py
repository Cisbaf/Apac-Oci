from dataclasses import dataclass
from apac_core.application.use_cases.user_cases.get_user_case import GetUserAuthorizerUseCase, GetUserAuthorizerOrAdministratorUseCase
from apac_core.application.use_cases.apac_request_cases.get_apac_request_case import GetApacRequestPedingUseCase
from apac_core.domain.repositories.apac_request_repository import ApacRequestRepository
from apac_core.domain.repositories.user_repository import UserRepository
from apac_core.domain.repositories.apac_batch_repository import ApacBatchRepository
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.exceptions import DomainException
from apac_core.domain.messages.apac_request_messages import NO_BATCH_AVAILABLE
from datetime import date
from pydantic import BaseModel


class ApprovedApacRequestDTO(BaseModel):
    apac_request_id: int
    authorizer_id: int

@dataclass
class ApprovedApacRequestUseCase:
    repo_apac_request: ApacRequestRepository
    repo_user: UserRepository
    repo_apac_batch: ApacBatchRepository

    def execute(self, data: ApprovedApacRequestDTO, today: date = None):
        today = today or date.today()

        apac_request = GetApacRequestPedingUseCase(self.repo_apac_request).execute(data.apac_request_id)
        
        authorizer = GetUserAuthorizerOrAdministratorUseCase(self.repo_user).execute(data.authorizer_id)

        apac_batch = self.repo_apac_batch.search_for_available_batch(authorizer.city.id, apac_request.request_date)
        if not apac_batch.is_available(today):
            raise DomainException(NO_BATCH_AVAILABLE)
        
        apac_request.set_status(ApacStatus.APPROVED)
        apac_request.set_authorizer(authorizer)
        apac_request.set_review_date()
        # atribuindo apac request a Faixa Apac
        apac_batch.set_apac_request(apac_request)
        # atualizando a Faixa Apac
        self.repo_apac_batch.save(apac_batch)

        return self.repo_apac_request.save(apac_request)


class RejectApacRequestDTO(BaseModel):
    apac_request_id: int
    authorizer_id: int
    justification: str

@dataclass
class RejectApacRequestUseCase:
    repo_apac_request: ApacRequestRepository
    repo_user: UserRepository

    def execute(self, data: RejectApacRequestDTO, today: date = None):
        today = today or date.today()

        apac_request = GetApacRequestPedingUseCase(self.repo_apac_request).execute(data.apac_request_id)
        authorizer = GetUserAuthorizerOrAdministratorUseCase(self.repo_user).execute(data.authorizer_id)

        apac_request.set_justification(data.justification)
        apac_request.set_status(ApacStatus.REJECTED)
        apac_request.set_authorizer(authorizer)
        apac_request.set_review_date()
        
        return self.repo_apac_request.save(apac_request)
