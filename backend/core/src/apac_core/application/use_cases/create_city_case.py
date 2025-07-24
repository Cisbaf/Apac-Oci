
from dataclasses import dataclass
from apac_core.domain.repositories.city_repository import CityRepository
from apac_core.domain.entities.city import City
from apac_core.domain.exceptions import ValidationException

@dataclass
class CreateCityUseCase:
    repo: CityRepository

    def execute(self, name: str) -> City:
        if len(name) < 4:
            raise ValidationException("O nome deve conter pelo menos 5 caracters!")
        return self.repo.save(City(name=name))
