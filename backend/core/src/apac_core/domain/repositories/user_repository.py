from abc import ABC, abstractmethod
from apac_core.domain.entities.user import User


class UserRepository(ABC):


    @abstractmethod
    def save(self, user: User):
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> User:
        pass