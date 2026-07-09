from datetime import date
from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ProcedureModel


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
