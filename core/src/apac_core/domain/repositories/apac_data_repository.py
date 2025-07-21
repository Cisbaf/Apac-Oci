from abc import ABC, abstractmethod
from apac_core.domain.entities.apac_data import ApacData

class ApacDataRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> ApacData:
        pass

    @abstractmethod
    def save(self, apac_data: ApacData) -> ApacData:
        pass