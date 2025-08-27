from dataclasses import dataclass
from apac_core.domain.repositories.city_repository import CityRepository
from apac_core.domain.repositories.establishment_repository import EstablishmentRepository
from apac_core.domain.entities.establishment import Establishment
from apac_core.domain.exceptions import ValidationException
from pydantic import BaseModel


class CreateEstablishmentDto(BaseModel):
    name: str
    cnes: str
    cnpj: str
    acronym: str
    city_id: int

@dataclass
class CreateEstablishmentUseCase:
    repo_establishment: EstablishmentRepository
    repo_city: CityRepository

    def execute(self, data: CreateEstablishmentDto) -> Establishment:
        if len(data.name) < 4:
            raise ValidationException("O nome deve conter pelo menos 5 caracters!")
        if len(data.cnes) < 4:
            raise ValidationException("O cnes deve conter pelo menos 5 caracters!")
        city = self.repo_city.get_by_id(data.city_id)
        return self.repo_establishment.save(
            Establishment(
                name=data.name,
                cnes=data.cnes,
                cnpj=data.cnpj,
                acronym=data.acronym,
                city=city
            )
        )
