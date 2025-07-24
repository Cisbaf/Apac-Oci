from dataclasses import dataclass
from apac_core.domain.repositories.establishment_repository import EstablishmentRepository
from apac_core.domain.repositories.user_repository import UserRepository
from apac_core.domain.exceptions import NotFoundException

@dataclass
class GetEstablishmentByUserId():
    repo_establishment: EstablishmentRepository
    repo_user: UserRepository

    def execute(self, user_id: int):
        user = self.repo_user.get_by_id(user_id)
        if not user.city:
            raise NotFoundException("O usuário está registrado em uma cidade!")
        