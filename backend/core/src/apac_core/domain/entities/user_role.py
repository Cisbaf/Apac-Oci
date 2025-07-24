from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    REQUESTER = "requester"
    AUTHORIZER = "authorizer"
    
    @classmethod
    def get(cls, role: str, default=None):
        """Retorna o membro da enumeração correspondente ao valor inteiro."""
        for member in cls:
            if member.value == role:
                return member
        return default