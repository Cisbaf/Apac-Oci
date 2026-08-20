from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class LoginPorCpfOuUsernameTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cpf_user = CustomUser.objects.create_user(
            username='004.701.667-11', password='senha123'
        )
        cls.named_user = CustomUser.objects.create_user(
            username='mesquita_adm', password='senha123'
        )

    def test_cpf_com_pontuacao_continua_entrando(self):
        self.assertEqual(
            authenticate(username='004.701.667-11', password='senha123'),
            self.cpf_user,
        )

    def test_cpf_sem_pontuacao_entra(self):
        self.assertEqual(
            authenticate(username='00470166711', password='senha123'),
            self.cpf_user,
        )

    def test_username_livre_entra(self):
        self.assertEqual(
            authenticate(username='mesquita_adm', password='senha123'),
            self.named_user,
        )

    def test_username_livre_ignora_maiusculas_e_espacos(self):
        self.assertEqual(
            authenticate(username='  Mesquita_ADM ', password='senha123'),
            self.named_user,
        )

    def test_senha_errada_nao_entra(self):
        self.assertIsNone(authenticate(username='mesquita_adm', password='errada'))

    def test_usuario_inexistente_nao_entra(self):
        self.assertIsNone(authenticate(username='nao_existe', password='senha123'))

    def test_usuario_inativo_nao_entra(self):
        self.named_user.is_active = False
        self.named_user.save()
        self.assertIsNone(authenticate(username='mesquita_adm', password='senha123'))


class LoginAdminPorCpfOuUsernameTest(TestCase):
    """O admin usa AdminAuthenticationForm, que alem da senha exige is_staff."""

    @classmethod
    def setUpTestData(cls):
        cls.staff = CustomUser.objects.create_user(
            username='mesquita_adm', password='senha123', is_staff=True
        )
        cls.staff_cpf = CustomUser.objects.create_user(
            username='004.701.667-11', password='senha123', is_staff=True
        )

    def _login(self, username):
        return self.client.post(
            reverse('admin:login'),
            {'username': username, 'password': 'senha123', 'next': '/admin/'},
        )

    def test_admin_aceita_username_livre(self):
        self.assertRedirects(
            self._login('mesquita_adm'), '/admin/', fetch_redirect_response=False
        )

    def test_admin_aceita_cpf_com_pontuacao(self):
        self.assertRedirects(
            self._login('004.701.667-11'), '/admin/', fetch_redirect_response=False
        )

    def test_admin_aceita_cpf_sem_pontuacao(self):
        self.assertRedirects(
            self._login('00470166711'), '/admin/', fetch_redirect_response=False
        )

    def test_admin_recusa_usuario_sem_is_staff(self):
        CustomUser.objects.create_user(username='comum_adm', password='senha123')
        self.assertEqual(self._login('comum_adm').status_code, 200)
