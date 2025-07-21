from abc import ABC, abstractmethod
from apac_core.domain.entities.establishment import Establishment

class EstablishmentRepository(ABC):

    @abstractmethod
    def save(self, establishment: Establishment) -> Establishment:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Establishment:
        pass

