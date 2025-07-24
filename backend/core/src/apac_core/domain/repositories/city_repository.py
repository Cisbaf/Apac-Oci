from abc import ABC, abstractmethod
from apac_core.domain.entities.city import City

class CityRepository(ABC):

    @abstractmethod
    def save(self, city: City) -> City:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> City:
        pass