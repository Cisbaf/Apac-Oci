from unittest.mock import Mock

from django.contrib import admin
from django.test import TestCase

from apac_core.application.use_cases.create_apac_data_case import CreateApacDataDTO
from apac_data.forms import ApacDataInlineForm
from apac_data.models import ApacDataModel
from apac_request.admin import ApacDataInline
from procedure.models import CidModel, ProcedureModel

PATIENT_DATA = {
    "patient_name": "João da Silva",
    "patient_record_number": "",
    "patient_cns": "706000343458946",
    "patient_cpf": "187.149.337-48",
    "patient_birth_date": "1999-03-12",
    "patient_race_color": "parda",
    "patient_gender": "Masculino",
    "patient_mother_name": "Maria Aparecida da Silva",
    "patient_address_street_type": "Avenida",
    "patient_address_street_name": "Abilio Augusto Tavora",
    "patient_address_number": "2789",
    "patient_address_complement": "Apartamento 201", # opcional
    "patient_address_postal_code": "26265-090",
    "patient_address_neighborhood": "Jardim Alvorada",
    "patient_address_city": "Nova Iguaçu",
    "patient_address_state": "RJ",
    "supervising_physician_name": "Fernando Rodrigues",
    "supervising_physician_cns": "706000343458946",
    "supervising_physician_cbo": "20154786",
    "authorizing_physician_name": "Fernando Rodrigues",
    "authorizing_physician_cns": "706000343458946",
    "authorizing_physician_cbo": "20154786",
    "procedure_date": "2025-07-30",
    "discharge_date": "2025-07-29",
    "cid_id": 1,
    "main_procedure_id": 1,
    "sub_procedures": []
}



class BaseApacTest(TestCase):

    def test_create_entity(self):
        CreateApacDataDTO(**PATIENT_DATA)


class ApacDataInlineFormStreetTypeTests(TestCase):
    """Cobre o select de `patient_address_street_type` no Django Admin
    (choices oficiais + fallback de valor legado)."""

    def setUp(self):
        self.procedure = ProcedureModel.objects.create(code="1", name="Procedimento Teste")
        self.cid = CidModel.objects.create(code="A00", name="Cid Teste")

    def build_instance(self, street_type):
        instance = ApacDataModel(
            patient_name="João da Silva",
            patient_cns="706000343458946",
            patient_cpf="18714933748",
            patient_birth_date="1999-03-12",
            patient_race_color="03",
            patient_gender="Masculino",
            patient_mother_name="Maria Aparecida da Silva",
            patient_address_street_type=street_type,
            patient_address_street_name="Abilio Augusto Tavora",
            patient_address_number="2789",
            patient_address_postal_code="26265090",
            patient_address_neighborhood="Jardim Alvorada",
            patient_address_city="Nova Iguaçu",
            patient_address_state="RJ",
            supervising_physician_name="Fernando Rodrigues",
            supervising_physician_cns="706000343458946",
            supervising_physician_cbo="20154786",
            authorizing_physician_name="Fernando Rodrigues",
            authorizing_physician_cns="706000343458946",
            authorizing_physician_cbo="20154786",
            main_procedure=self.procedure,
            procedure_date="2025-07-30",
            discharge_date="2025-07-29",
            cid=self.cid,
        )
        instance.save()
        return instance

    def test_valid_code_is_selectable(self):
        instance = self.build_instance("081")

        form = ApacDataInlineForm(instance=instance)
        field = form.fields["patient_address_street_type"]

        self.assertIn(("081", "081 - Rua"), field.choices)
        self.assertTrue(field.valid_value("081"))

    def test_legacy_value_is_injected_as_extra_choice_and_stays_valid(self):
        instance = self.build_instance("Avenida Legada")

        form = ApacDataInlineForm(instance=instance)
        field = form.fields["patient_address_street_type"]

        self.assertTrue(field.valid_value("Avenida Legada"))
        self.assertTrue(
            any(value == "Avenida Legada" for value, _ in field.choices)
        )

    def test_official_choices_are_not_polluted_by_legacy_value(self):
        instance = self.build_instance("081")

        form = ApacDataInlineForm(instance=instance)
        field = form.fields["patient_address_street_type"]

        legado_labels = [label for _, label in field.choices if "legado" in label]
        self.assertEqual(legado_labels, [])


class ApacDataInlinePermissionTests(TestCase):
    """Garante que este plano não alterou `get_readonly_fields`.

    NOTA: `get_readonly_fields` tem um bug preexistente (não introduzido aqui,
    fora do escopo deste plano): para não-superuser, `base_fields` filtra
    `field.name in editable_fields` em vez de `not in`, então os campos
    listados em `editable_fields` ficam BLOQUEADOS e todos os demais campos
    (incluindo os de endereço, `patient_address_street_type` entre eles)
    ficam editáveis. Este teste documenta o comportamento atual (para pegar
    qualquer regressão futura), não o comportamento pretendido.
    """

    def build_request(self, is_superuser):
        return Mock(user=Mock(is_superuser=is_superuser))

    def get_inline(self):
        return ApacDataInline(ApacDataModel, admin.site)

    def test_non_superuser_current_readonly_fields_unchanged(self):
        inline = self.get_inline()
        readonly_fields = inline.get_readonly_fields(self.build_request(is_superuser=False))

        self.assertIn("patient_name", readonly_fields)
        self.assertNotIn("patient_address_street_type", readonly_fields)

    def test_superuser_can_edit_street_type(self):
        inline = self.get_inline()
        readonly_fields = inline.get_readonly_fields(self.build_request(is_superuser=True))

        self.assertNotIn("patient_address_street_type", readonly_fields)