from typing import List
from apac_core.domain.repositories.user_repository import UserRepository
from apac_core.domain.entities.user import User
from apac_core.domain.exceptions import NotFoundException

class UserFakeRepository(UserRepository):
    
    def __init__(self):
        super().__init__()
        self.increment_id = 1
        self.users: List[User] = []
    
    def save(self, user):
        if not user.id:
            user.id = self.increment_id
            self.increment_id += 1
            self.users.append(user)
        else:
            for i, _user in enumerate(self.users):
                if _user.id == user.id:
                    self.users[i] = user
                    break
        return user

    def get_by_id(self, id):
        for user in self.users:
            if user.id == id:
                return user
        raise NotFoundException()