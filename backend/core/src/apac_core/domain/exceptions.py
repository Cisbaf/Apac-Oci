# domain/exceptions.py

class DomainException(Exception):
    """Exceção base para erros de domínio."""
    pass


class NotFoundException(DomainException):
    """Erro para entidades não encontradas."""
    def __init__(self, message="Recurso não encontrado"):
        super().__init__(message)


class PermissionDeniedException(DomainException):
    """Erro para ações não permitidas por permissão."""
    def __init__(self, message="Permissão negada"):
        super().__init__(message)


class ValidationException(DomainException):
    """Erro de validação de dados de entrada ou regras de negócio."""
    def __init__(self, message="Dados inválidos"):
        super().__init__(message)
