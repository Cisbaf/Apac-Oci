from dataclasses import dataclass
from apac_core.domain.repositories.city_repository import CityRepository
from apac_core.domain.entities.city import City
from apac_core.domain.exceptions import ValidationException
from pydantic import BaseModel


class CreateCityDto(BaseModel):
    name: str
    ibge_code: str
    agency_name: str

@dataclass
class CreateCityUseCase:
    repo: CityRepository

    def execute(self, data: CreateCityDto) -> City:
        if len(data.name) < 4:
            raise ValidationException("O nome deve conter pelo menos 5 caracters!")
        return self.repo.save(
            City(
                name=data.name,
                ibge_code=data.ibge_code,
                agency_name=data.agency_name
        ))
