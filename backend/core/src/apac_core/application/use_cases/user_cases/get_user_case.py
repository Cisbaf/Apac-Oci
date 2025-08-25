from dataclasses import dataclass
from apac_core.domain.repositories.user_repository import UserRepository
from apac_core.domain.entities.user_role import UserRole
from apac_core.domain.exceptions import PermissionDeniedException
from apac_core.domain.messages.apac_request_messages import(
    USER_IS_NOT_REQUESTER_OR_ADM,
    USER_IS_NOT_AUTHORIZER,
    USER_IS_NOT_REQUESTER,
    USER_IS_NOT_AUTHORIZER_OR_ADM
)

@dataclass
class GetUserAuthorizerUseCase:
    repo_user: UserRepository

    def execute(self, authorizer_id: int):
        user = self.repo_user.get_by_id(authorizer_id)
        if user.role != UserRole.AUTHORIZER:
            raise PermissionDeniedException(USER_IS_NOT_AUTHORIZER)
        return user
    
@dataclass
class GetUserRequesterUseCase:
    repo_user: UserRepository

    def execute(self, requester_id: int):
        user = self.repo_user.get_by_id(requester_id)
        if user.role != UserRole.REQUESTER:
            raise PermissionDeniedException(USER_IS_NOT_REQUESTER)
        return user
    
@dataclass
class GetUserRequesterOrAdministratorUseCase:
    repo_user: UserRepository

    def execute(self, requester_id: int):
        user = self.repo_user.get_by_id(requester_id)
        if user.role != UserRole.REQUESTER and user.role != UserRole.ADMIN:
            raise PermissionDeniedException(USER_IS_NOT_REQUESTER_OR_ADM)
        return user


@dataclass
class GetUserAuthorizerOrAdministratorUseCase:
    repo_user: UserRepository

    def execute(self, authorizer_id: int):
        user = self.repo_user.get_by_id(authorizer_id)
        if user.role != UserRole.AUTHORIZER and user.role != UserRole.ADMIN:
            raise PermissionDeniedException(USER_IS_NOT_AUTHORIZER_OR_ADM)
        return user