from abc import ABC, abstractmethod
from apac_core.domain.entities.cid import Cid

class CidRepository(ABC):

    @abstractmethod
    def save(self, cid: Cid) -> Cid:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Cid:
        pass