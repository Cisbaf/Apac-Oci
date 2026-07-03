from abc import ABC, abstractmethod
from apac_core.domain.entities.apac_request import ApacRequest
from apac_core.domain.entities.apac_status import ApacStatus
from datetime import datetime

class ApacRequestRepository(ABC):

    @abstractmethod
    def save(self, apac_request: ApacRequest) -> ApacRequest:
        pass

    @abstractmethod
    def check_duplicates(self, establishment_id: int, patient_cpf: str, main_procedure: int, request_date: datetime):
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> ApacRequest:
        pass
