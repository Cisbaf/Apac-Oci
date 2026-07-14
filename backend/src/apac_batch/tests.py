from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework import status
from city.models import CityModel
from customuser.models import CustomUser, UserRole
from .models import ApacBatchModel
from .forms import parse_faixas, ImportFaixasForm


def random_str(prefix="x"):
    import random
    return f"{prefix}{random.randint(1, 10**9)}"


class ParseFaixasTests(TestCase):

    def test_parse_single_line(self):
        raw = '"332670197467-3 | 332670197468-4 | 332670197469-5'
        self.assertEqual(
            parse_faixas(raw),
            ["3326701974673", "3326701974684", "3326701974695"]
        )

    def test_parse_multiple_lines(self):
        raw = (
            '"332670197467-3 | 332670197468-4\n'
            '"332670197471-7 | 332670197472-8'
        )
        self.assertEqual(
            parse_faixas(raw),
            ["3326701974673", "3326701974684", "3326701974717", "3326701974728"]
        )

    def test_parse_ignores_empty_lines_and_parts(self):
        raw = '"332670197467-3 |  \n\n"332670197468-4'
        self.assertEqual(
            parse_faixas(raw),
            ["3326701974673", "3326701974684"]
        )

    def test_parse_empty_string_returns_empty_list(self):
        self.assertEqual(parse_faixas(""), [])
        self.assertEqual(parse_faixas("   \n  \n  "), [])


class ImportFaixasFormTests(TestCase):

    def setUp(self):
        self.city = CityModel.objects.create(
            name=random_str("city"),
            ibge_code=random_str(),
            agency_name=random_str()
        )

    def valid_data(self, **overrides):
        data = {
            "city": self.city.pk,
            "quantidade_esperada": 2,
            "faixas_raw": '"332670197467-3 | 332670197468-4',
        }
        data.update(overrides)
        return data

    def test_valid_form_parses_and_is_valid(self):
        form = ImportFaixasForm(data=self.valid_data())
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data["numeros_parseados"],
            ["3326701974673", "3326701974684"]
        )

    def test_quantidade_diferente_gera_erro(self):
        form = ImportFaixasForm(data=self.valid_data(quantidade_esperada=5))
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Quantidade não confere",
            " ".join(form.non_field_errors())
        )

    def test_faixa_ja_existente_no_banco_gera_erro(self):
        ApacBatchModel.objects.create(
            batch_number="3326701974673",
            city=self.city,
            expire_in=date.today()
        )
        form = ImportFaixasForm(data=self.valid_data())
        self.assertFalse(form.is_valid())
        self.assertIn(
            "já estão registradas",
            " ".join(form.non_field_errors())
        )

    def test_faixa_duplicada_no_input_gera_erro(self):
        data = self.valid_data(
            quantidade_esperada=2,
            faixas_raw='"332670197467-3 | 332670197467-3'
        )
        form = ImportFaixasForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "mais de uma vez",
            " ".join(form.non_field_errors())
        )

    def test_salvar_insere_faixas_no_banco(self):
        form = ImportFaixasForm(data=self.valid_data())
        self.assertTrue(form.is_valid(), form.errors)
        total = form.salvar()

        self.assertEqual(total, 2)
        self.assertEqual(ApacBatchModel.objects.count(), 2)

        batch = ApacBatchModel.objects.get(batch_number="3326701974673")
        self.assertEqual(batch.city, self.city)
        self.assertEqual(batch.expire_in, date(date.today().year, 12, 31))

    def test_erro_nao_insere_nenhuma_faixa(self):
        ApacBatchModel.objects.create(
            batch_number="3326701974673",
            city=self.city,
            expire_in=date.today()
        )
        form = ImportFaixasForm(data=self.valid_data())
        self.assertFalse(form.is_valid())

        # Apenas a faixa criada no setUp deve existir
        self.assertEqual(ApacBatchModel.objects.count(), 1)

    def test_usuario_admin_nao_superuser_nao_escolhe_cidade(self):
        admin_user = CustomUser.objects.create(
            username=random_str("admin"),
            role=UserRole.ADMIN,
            city=self.city,
            is_staff=True
        )
        data = self.valid_data()
        del data["city"]

        form = ImportFaixasForm(data=data, user=admin_user)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.get_city(), self.city)

        total = form.salvar()
        self.assertEqual(total, 2)
        batch = ApacBatchModel.objects.get(batch_number="3326701974673")
        self.assertEqual(batch.city, self.city)

    def test_usuario_admin_ignora_cidade_enviada_no_post(self):
        outra_cidade = CityModel.objects.create(
            name=random_str("city"),
            ibge_code=random_str(),
            agency_name=random_str()
        )
        admin_user = CustomUser.objects.create(
            username=random_str("admin"),
            role=UserRole.ADMIN,
            city=self.city,
            is_staff=True
        )
        data = self.valid_data(city=outra_cidade.pk)

        form = ImportFaixasForm(data=data, user=admin_user)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.get_city(), self.city)

    def test_usuario_admin_sem_cidade_associada_gera_erro(self):
        admin_user = CustomUser.objects.create(
            username=random_str("admin"),
            role=UserRole.ADMIN,
            city=None,
            is_staff=True
        )
        data = self.valid_data()
        del data["city"]

        form = ImportFaixasForm(data=data, user=admin_user)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "não possui uma cidade associada",
            " ".join(form.non_field_errors())
        )


class ImportarFaixasViewTests(TestCase):

    def setUp(self):
        self.city = CityModel.objects.create(
            name=random_str("city"),
            ibge_code=random_str(),
            agency_name=random_str()
        )
        self.superuser = CustomUser.objects.create_superuser(
            username=random_str("super"),
            email=None,
            password="pass1234",
            city=self.city
        )
        self.regular_user = CustomUser.objects.create(
            username=random_str("user"),
            role=UserRole.REQUESTER,
            city=self.city,
            is_staff=True
        )
        self.regular_user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="apac_batch",
                codename="view_apacbatchmodel"
            )
        )
        self.admin_user = CustomUser.objects.create(
            username=random_str("admin"),
            role=UserRole.ADMIN,
            city=self.city,
            is_staff=True
        )
        self.admin_user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="apac_batch",
                codename="view_apacbatchmodel"
            )
        )
        self.url = reverse("admin:apac_batch_importar_faixas")
        self.client = Client()

    def test_anonimo_eh_redirecionado_para_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_usuario_sem_role_admin_recebe_403(self):
        self.client.force_login(self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_superuser_acessa_formulario(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Importar Faixas APAC")
        self.assertContains(response, 'name="city"')

    def test_admin_nao_superuser_acessa_formulario_sem_campo_cidade(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Importar Faixas APAC")
        self.assertNotContains(response, 'name="city"')
        self.assertContains(response, self.city.name)

    def test_admin_nao_superuser_submete_sem_campo_cidade(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.url, data={
            "quantidade_esperada": 2,
            "faixas_raw": '"332670197467-3 | 332670197468-4',
        })

        self.assertRedirects(
            response,
            reverse("admin:apac_batch_apacbatchmodel_changelist")
        )
        self.assertEqual(ApacBatchModel.objects.count(), 2)
        batch = ApacBatchModel.objects.get(batch_number="3326701974673")
        self.assertEqual(batch.city, self.city)

    def test_submissao_valida_cria_faixas_e_redireciona(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, data={
            "city": self.city.pk,
            "quantidade_esperada": 2,
            "faixas_raw": '"332670197467-3 | 332670197468-4',
        })

        self.assertRedirects(
            response,
            reverse("admin:apac_batch_apacbatchmodel_changelist")
        )
        self.assertEqual(ApacBatchModel.objects.count(), 2)

    def test_submissao_invalida_nao_cria_faixas_e_reexibe_erros(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, data={
            "city": self.city.pk,
            "quantidade_esperada": 5,
            "faixas_raw": '"332670197467-3 | 332670197468-4',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ApacBatchModel.objects.count(), 0)
        self.assertContains(response, "Quantidade não confere")

    def test_botao_importar_visivel_para_superuser_e_admin(self):
        changelist_url = reverse("admin:apac_batch_apacbatchmodel_changelist")

        self.client.force_login(self.superuser)
        response = self.client.get(changelist_url)
        self.assertContains(response, "Importar Faixas")

        self.client.force_login(self.admin_user)
        response = self.client.get(changelist_url)
        self.assertContains(response, "Importar Faixas")

        self.client.force_login(self.regular_user)
        response = self.client.get(changelist_url)
        self.assertNotContains(response, "Importar Faixas")


class ExportApacBatchAuthTests(APITestCase):
    """T-003: o endpoint de export não pode aceitar requisição sem autenticação."""

    def setUp(self):
        self.url = reverse("extract_batch")

    def test_post_sem_autenticacao_e_rejeitado(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )
