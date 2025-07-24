from typing import List
from apac_core.domain.exceptions import NotFoundException
from apac_core.domain.repositories.establishment_repository import EstablishmentRepository
from apac_core.domain.entities.establishment import Establishment


class EstablishmentFakeRepository(EstablishmentRepository):

    def __init__(self):
        super().__init__()
        self.increment_id = 1
        self.establishments: List[Establishment] = []
    
    def save(self, establishment):
        if not establishment.id:
            establishment.id = self.increment_id
            self.increment_id += 1
            self.establishments.append(establishment)
        else:
            for i, _establishment in enumerate(self.establishments):
                if _establishment.id == establishment.id:
                    self.establishments[i] = establishment
                    break
        return establishment

    def get_by_id(self, id):
        for establishment in self.establishments:
            if establishment.id == id:
                return establishment
        raise NotFoundException()