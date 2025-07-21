from abc import ABC, abstractmethod
from apac_core.domain.entities.apac_request import ApacRequest
from apac_core.domain.entities.apac_status import ApacStatus

class ApacRequestRepository(ABC):

    @abstractmethod
    def save(self, apac_request: ApacRequest) -> ApacRequest:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> ApacRequest:
        pass
