from .models import CustomUser
from apac_core.domain.repositories.user_repository import UserRepository
from apac_core.domain.exceptions import NotFoundException


class UserController(UserRepository):

    def get_by_id(self, id):
        user = CustomUser.objects.get(pk=id)
        if user:
            return user.to_entity()
        raise NotFoundException()
    
    def save(self, user):
        return super().save(user)