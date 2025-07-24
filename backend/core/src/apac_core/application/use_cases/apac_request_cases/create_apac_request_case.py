from pydantic import BaseModel
from apac_core.application.use_cases.create_apac_data_case import CreateApacDataDTO, CreateApacDataUseCase
from apac_core.application.use_cases.user_cases.get_user_case import GetUserRequesterUseCase
from apac_core.domain.entities.apac_request import ApacRequest
from apac_core.domain.repositories.apac_request_repository import ApacRequestRepository
from apac_core.domain.repositories.user_repository import UserRepository
from apac_core.domain.repositories.establishment_repository import EstablishmentRepository
from apac_core.domain.repositories.apac_data_repository import ApacDataRepository
from apac_core.domain.repositories.cid_repository import CidRepository
from apac_core.domain.repositories.procedure_repository import ProcedureRepository
from apac_core.domain.repositories.procedure_record_repository import ProcedureRecordRepository
from apac_core.domain.exceptions import DomainException
from dataclasses import dataclass

class CreateApacRequestDTO(BaseModel):
    requester_id: int
    establishment_id: int
    apac_data: CreateApacDataDTO

@dataclass
class CreateApacRequestUseCase:
    repo_apac_request: ApacRequestRepository
    repo_user: UserRepository
    repo_establishment: EstablishmentRepository
    repo_apac_data: ApacDataRepository
    repo_cid: CidRepository
    repo_procedure: ProcedureRepository
    repo_procedure_record: ProcedureRecordRepository

    def execute(self, data: CreateApacRequestDTO) -> ApacRequest:
        # Obtém o requester pelo ID 
        requester = GetUserRequesterUseCase(self.repo_user).execute(data.requester_id)

        # Obtém o estabelecimento pelo ID
        establishment = self.repo_establishment.get_by_id(data.establishment_id)
        if establishment.city.id != requester.city.id:
            raise DomainException(f"O requester pertence a cidade {requester.city.name} e está tentando registrar apac na cidade {establishment.city.name}")

        # Registra o Apac Data via Use Case Apac Dara
        apac_data = CreateApacDataUseCase(
            self.repo_apac_data,
            self.repo_cid,
            self.repo_procedure,
            self.repo_procedure_record
        ).execute(data.apac_data)

        # Cria o apac request
        created_apac_request = self.repo_apac_request.save(ApacRequest(
            requester=requester,
            establishment=establishment,
            apac_data=apac_data
        ))

        return created_apac_request