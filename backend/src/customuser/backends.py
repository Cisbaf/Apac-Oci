import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


def _cpf_variants(value):
    """Formas equivalentes de um mesmo CPF (com e sem pontuacao)."""
    digits = re.sub(r"\D", "", value)
    if len(digits) != 11:
        return []
    formatted = f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    return [formatted, digits]


class UsernameOrCpfBackend(ModelBackend):
    """
    Aceita login por username livre (ex: 'mesquita_adm') mantendo o login por
    CPF, digitado com ou sem pontuacao, para quem ja acessa desse jeito.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return None

        username = username.strip()
        candidates = list(dict.fromkeys([username, *_cpf_variants(username)]))

        for candidate in candidates:
            user = UserModel._default_manager.filter(
                username__iexact=candidate
            ).order_by('pk').first()
            if user is None:
                continue
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        # Mesmo custo de hashing quando nao ha usuario, evita timing attack
        UserModel().set_password(password)
        return None
