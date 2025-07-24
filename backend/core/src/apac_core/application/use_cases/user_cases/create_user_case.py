from dataclasses import dataclass
from apac_core.domain.repositories.city_repository import CityRepository
from apac_core.domain.repositories.user_repository import UserRepository
from apac_core.domain.entities.user import User
from apac_core.domain.entities.user_role import UserRole
from apac_core.domain.exceptions import ValidationException


@dataclass
class CreateUserUseCase:
    repo_user: UserRepository
    repo_city: CityRepository

    def execute(self, name: str, role: UserRole, city_id: int) -> User:
        if len(name) < 4:
            raise ValidationException("O nome deve conter pelo menos 5 caracters!")
        city = self.repo_city.get_by_id(city_id)
        return self.repo_user.save(User(name=name, role=role, city=city))
