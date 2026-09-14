import json
import os
import tempfile
from datetime import date
from io import StringIO
from pathlib import Path
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ProcedureModel, ProcedureRequirementGroup, ProcedureSecondary


class ProcedureAgeAlertApiViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("apac_procedure_age_alert")
        self.procedure = ProcedureModel.objects.create(
            code="0301010064",
            name="Procedimento de teste",
        )

    def test_missing_fields_returns_400(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_birth_date_format_returns_400(self):
        response = self.client.post(
            self.url,
            {"procedure_id": self.procedure.id, "birth_date": "12/03/1999"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unknown_procedure_returns_404(self):
        response = self.client.post(
            self.url,
            {"procedure_id": 999999, "birth_date": "1999-03-12"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_rule_registered_returns_no_alert(self):
        response = self.client.post(
            self.url,
            {"procedure_id": self.procedure.id, "birth_date": "1999-03-12"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["alert"])

    @mock.patch.dict(
        "procedure.views.PROCEDURE_AGE_ALERT_RULES",
        {"0301010064": {"min_age": 18, "max_age": None, "message": "Procedimento restrito a maiores de idade."}},
        clear=True,
    )
    def test_age_outside_rule_range_returns_alert(self):
        response = self.client.post(
            self.url,
            {"procedure_id": self.procedure.id, "birth_date": "2015-01-01"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["alert"])
        self.assertEqual(response.data["message"], "Procedimento restrito a maiores de idade.")

    @mock.patch.dict(
        "procedure.views.PROCEDURE_AGE_ALERT_RULES",
        {"0301010064": {"min_age": 18, "max_age": None}},
        clear=True,
    )
    def test_age_inside_rule_range_returns_no_alert(self):
        response = self.client.post(
            self.url,
            {"procedure_id": self.procedure.id, "birth_date": "1999-03-12"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["alert"])


class ProcedureFixedValidityFlagTests(APITestCase):
    """
    T-034 — a flag do atributo SIGTAP 054 precisa atravessar o `to_entity`, senão o
    export continua calculando 3 competências e o APAC Magnético rejeita com 010087.
    """

    def test_default_is_false(self):
        procedure = ProcedureModel.objects.create(code="0902010026", name="OCI sem 054")

        self.assertFalse(procedure.fixed_validity_two_competences)
        self.assertFalse(procedure.to_entity().fixed_validity_two_competences)

    def test_flag_is_propagated_to_entity(self):
        procedure = ProcedureModel.objects.create(
            code="0902010034",
            name="OCI com 054",
            fixed_validity_two_competences=True,
        )

        self.assertTrue(procedure.to_entity().fixed_validity_two_competences)


class SemearGrupoConsultaPmaeTests(TestCase):
    """
    T-042 — o grupo da consulta (atributo PMAE 053) é o que impede a APAC de OCI
    de sair sem consulta nem teleconsulta e tomar a crítica
    "PMAE EXIGE PELO MENOS 2 PROC.SEC. SENDO UM OBRIG.(030101007 OU 030101030)".
    """

    JSON_OFICIAL = (Path(__file__).resolve().parents[3]
                    / "scripts" / "sigtap" / "grupos_exigencia.json")

    def setUp(self):
        self.oci = ProcedureModel.objects.create(code="0908010010", name="OCI de teste")
        self.consulta = ProcedureModel.objects.create(code="0301010072", name="Consulta")
        self.tele = ProcedureModel.objects.create(code="0301010307", name="Teleconsulta")
        for filho in (self.consulta, self.tele):
            ProcedureSecondary.objects.create(parent=self.oci, child=filho, mandatory=False)

    def _semear(self, aplicar=True, members=("0301010072", "0301010307")):
        conteudo = {
            "0908010010_OCI": {
                "codigo_dv": "0908010010",
                "nome": "OCI de teste",
                "attribute_code": "OCI",
                "description": "Consulta ou teleconsulta",
                "minimum": 1,
                "members": list(members),
            }
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(conteudo, f)
            caminho = f.name
        try:
            saida = StringIO()
            call_command("sigtap_semear_grupos_exigencia", "--json", caminho,
                         *(["--aplicar"] if aplicar else []), stdout=saida)
            return saida.getvalue()
        finally:
            os.unlink(caminho)

    def test_cria_grupo_com_consulta_e_teleconsulta(self):
        self._semear()

        grupo = ProcedureRequirementGroup.objects.get(principal=self.oci, attribute_code="OCI")
        self.assertEqual(grupo.minimum, 1)
        self.assertCountEqual(
            grupo.members.values_list("code", flat=True),
            ["0301010072", "0301010307"],
        )

    def test_sem_aplicar_nao_grava(self):
        saida = self._semear(aplicar=False)

        self.assertFalse(ProcedureRequirementGroup.objects.exists())
        self.assertIn("pendente", saida)

    def test_codigo_duplicado_fora_do_principal_nao_vira_membro(self):
        """A produção tem `0301010307` em dois ids; só o que é secundário desta
        OCI pode entrar no grupo, senão sobra membro pendurado (achado do GIN3)."""
        pendurado = ProcedureModel.objects.create(
            code="0301010307", name="Teleconsulta (duplicata sem vínculo)")

        self._semear()

        grupo = ProcedureRequirementGroup.objects.get(principal=self.oci, attribute_code="OCI")
        self.assertEqual(grupo.members.count(), 2)
        self.assertNotIn(pendurado.id, grupo.members.values_list("id", flat=True))

    def test_json_oficial_cobre_as_oito_ocis_de_infectologia(self):
        """Guarda do dado: sem entrada no JSON, o semeador não cria o grupo e a
        regra da consulta some sem ninguém perceber."""
        dados = json.loads(self.JSON_OFICIAL.read_text(encoding="utf-8"))
        com_grupo_oci = {
            info["codigo_dv"] for chave, info in dados.items()
            if not chave.startswith("_") and info["attribute_code"] == "OCI"
        }

        esperadas = {
            "0908010010", "0908010028", "0908010036", "0908010044",
            "0908010052", "0908010060", "0908010079", "0908010087",
        }
        self.assertTrue(esperadas.issubset(com_grupo_oci))
