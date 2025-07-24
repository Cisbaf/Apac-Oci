from dataclasses import dataclass
from apac_core.domain.repositories.city_repository import CityRepository
from apac_core.domain.repositories.establishment_repository import EstablishmentRepository
from apac_core.domain.entities.establishment import Establishment
from apac_core.domain.exceptions import ValidationException

@dataclass
class CreateEstablishmentUseCase:
    repo_establishment: EstablishmentRepository
    repo_city: CityRepository

    def execute(self, name: str, cnes: str, city_id) -> Establishment:
        if len(name) < 4:
            raise ValidationException("O nome deve conter pelo menos 5 caracters!")
        if len(cnes) < 4:
            raise ValidationException("O cnes deve conter pelo menos 5 caracters!")
        city = self.repo_city.get_by_id(city_id)
        return self.repo_establishment.save(Establishment(name=name, cnes=cnes, city=city))
