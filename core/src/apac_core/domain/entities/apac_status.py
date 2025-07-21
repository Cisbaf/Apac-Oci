from enum import Enum


class ApacStatus(str, Enum):  # herdar de str também garante compatibilidade com JSON
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    @classmethod
    def get(cls, status: str, default=None):
        """Retorna o membro da enumeração correspondente ao valor inteiro."""
        for member in cls:
            if member.value == status:
                return member
        return default