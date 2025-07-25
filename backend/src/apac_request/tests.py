from datetime import date
from random import random
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from apac_request.models import ApacRequestModel
from apac_batch.models import ApacBatchModel
from city.models import CityModel
from customuser.models import CustomUser, UserRole
from establishment.models import EstablishmentModel
from procedure.models import ProcedureModel, CidModel
from apac_core.application.use_cases.apac_request_cases.create_apac_request_case import (
    CreateApacRequestDTO,
)
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.messages.apac_request_messages import (
    NO_BATCH_AVAILABLE,
    USER_IS_NOT_REQUESTER,
    SUCCESSFULLY_REGISTERED,
)

# Constantes para dados de teste
PATIENT_DATA = {
    "patient_name": "João da Silva",
    "patient_record_number": "2023100456",
    "patient_cns": "898001160651234",
    "patient_cpf": "123.456.789-00",
    "patient_birth_date": "12/03/1999",
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
    "medic_name": "Fernando Rodrigues",
    "medic_cns": "5667789",
    "medic_cbo": "20154786",
    "procedure_date": "12/03/1999"
}

def random_str():
    return str(int(random() * 1000000))


class BaseApacTest(APITestCase):
    """Classe base com setup comum para todos os testes de APAC"""

    def setUp(self):
        # Configuração básica
        self.city = CityModel.objects.create(name=random_str())
        self.authorizer = self.create_user(UserRole.AUTHORIZER, "auth_user")
        self.requester = self.create_user(UserRole.REQUESTER, "req_user")
        
        # Configuração de estabelecimento
        self.establishment = EstablishmentModel.objects.create(
            cnes=random_str(), 
            name="Test Hospital", 
            city=self.city
        )
        
        # Configuração de procedimentos
        self.procedure, self.sub_procedure = self.create_procedure_hierarchy()
        self.cid = CidModel.objects.create(
            code=random_str(), 
            name="A00", 
            procedure=self.procedure
        )
        
        # URLs e dados base
        self.base_data = self.build_apac_data()
        self.create_apac_url = reverse("apac_route")
        self.approve_url = reverse("approved")
        self.reject_url = reverse("reject")
    
    # Métodos auxiliares
    def create_user(self, role, username=None):
        return CustomUser.objects.create(
            city=self.city,
            role=role,
            username=username or random_str()
        )
    
    def create_batch(self, city):
        return ApacBatchModel.objects.create(
            batch_number=random_str(),
            city=city,
            expire_in=date.today()
        )
    
    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def create_procedure_hierarchy(self):
        procedure = ProcedureModel.objects.create(
            code=random_str(), 
            name="Main Procedure"
        )
        sub_procedure = ProcedureModel.objects.create(
            code=random_str(), 
            name="Sub Procedure", 
            parent=procedure, 
            mandatory=True
        )
        return procedure, sub_procedure
    
    def build_apac_data(self):
        return CreateApacRequestDTO(**{
            "requester_id": self.requester.pk,
            "establishment_id": self.establishment.pk,
            "apac_data": {
                **PATIENT_DATA,
                "cid_id": self.cid.pk,
                "main_procedure_id": self.procedure.pk,
                "sub_procedures": [{
                    "procedure_id": self.sub_procedure.pk,
                    "quantity": 3
                }]
            }
        })
    
    def create_apac_request(self):
        self.authenticate(self.requester)
        self.client.post(
            self.create_apac_url, 
            self.base_data.model_dump(),
            format='json'
        )
        return ApacRequestModel.objects.last()

    def assert_apac_status(self, apac_id, expected_status):
        apac = ApacRequestModel.objects.get(pk=apac_id)
        self.assertEqual(apac.status, expected_status)


class ApacCreationTests(BaseApacTest):
    """Testes para criação de APACs"""
    
    def setUp(self):
        super().setUp()
        self.authenticate(self.requester)
    
    def test_success_as_requester(self):
        response = self.client.post(
            self.create_apac_url, 
            self.base_data.model_dump(),
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), SUCCESSFULLY_REGISTERED)
        
        apac = ApacRequestModel.objects.first()
        self.assertEqual(apac.status, ApacStatus.PENDING)
        self.assertEqual(apac.requester, self.requester)
        self.assertEqual(apac.establishment, self.establishment)
    
    def test_fail_as_authorizer(self):
        self.authenticate(self.authorizer)
        self.base_data.requester_id = self.authorizer.pk
        
        response = self.client.post(
            self.create_apac_url, 
            self.base_data.model_dump(),
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), USER_IS_NOT_REQUESTER)
        self.assertEqual(ApacRequestModel.objects.count(), 0)


class ApacApprovalTests(BaseApacTest):
    """Testes para aprovação de APACs"""
    
    def setUp(self):
        super().setUp()
        self.apac = self.create_apac_request()
        self.create_batch(self.requester.city)
        self.authenticate(self.authorizer)
    
    def test_success_with_available_batch(self):
        response = self.client.post(
            self.approve_url,
            {
                "apac_request_id": self.apac.pk,
                "authorizer_id": self.authorizer.pk
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_apac_status(self.apac.pk, ApacStatus.APPROVED)
        
        apac = ApacRequestModel.objects.get(pk=self.apac.pk)
        self.assertEqual(apac.authorizer, self.authorizer)
        self.assertIsNotNone(apac.review_date)
    
    def test_fail_without_batch(self):
        ApacBatchModel.objects.all().delete()
        
        response = self.client.post(
            self.approve_url,
            {
                "apac_request_id": self.apac.pk,
                "authorizer_id": self.authorizer.pk
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("message"), NO_BATCH_AVAILABLE)
        self.assert_apac_status(self.apac.pk, ApacStatus.PENDING)
    
    def test_fail_as_requester(self):
        self.authenticate(self.requester)
        
        response = self.client.post(
            self.approve_url,
            {
                "apac_request_id": self.apac.pk,
                "authorizer_id": self.requester.pk
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_apac_status(self.apac.pk, ApacStatus.PENDING)


class ApacRejectionTests(BaseApacTest):
    """Testes para rejeição de APACs"""
    
    def setUp(self):
        super().setUp()
        self.apac = self.create_apac_request()
        self.create_batch(self.requester.city)
        self.authenticate(self.authorizer)
    
    def test_success_with_valid_reason(self):
        justification = "Procedimento não autorizado conforme protocolo"
        
        response = self.client.post(
            self.reject_url,
            {
                "apac_request_id": self.apac.pk,
                "authorizer_id": self.authorizer.pk,
                "justification": justification
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_apac_status(self.apac.pk, ApacStatus.REJECTED)
        
        apac = ApacRequestModel.objects.get(pk=self.apac.pk)
        self.assertEqual(apac.justification, justification)
        self.assertEqual(apac.authorizer, self.authorizer)
    
    def test_fail_with_empty_reason(self):
        response = self.client.post(
            self.reject_url,
            {
                "apac_request_id": self.apac.pk,
                "authorizer_id": self.authorizer.pk,
                "justification": ""
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_apac_status(self.apac.pk, ApacStatus.PENDING)
    
    def test_fail_as_requester(self):
        self.authenticate(self.requester)
        
        response = self.client.post(
            self.reject_url,
            {
                "apac_request_id": self.apac.pk,
                "authorizer_id": self.requester.pk,
                "justification": "Teste"
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_apac_status(self.apac.pk, ApacStatus.PENDING)


class EdgeCaseTests(BaseApacTest):
    """Testes para casos extremos e validações"""
    
    def setUp(self):
        super().setUp()
        self.authenticate(self.authorizer)
    
    def test_approve_nonexistent_apac(self):
        response = self.client.post(
            self.approve_url,
            {
                "apac_request_id": 9999,
                "authorizer_id": self.authorizer.pk
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_reject_with_long_justification(self):
        apac = self.create_apac_request()
        justification = "X" * 501  # Excede o limite de 500 caracteres
        
        response = self.client.post(
            self.reject_url,
            {
                "apac_request_id": apac.pk,
                "authorizer_id": self.authorizer.pk,
                "justification": justification
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_apac_status(apac.pk, ApacStatus.PENDING)
    
    def test_approve_already_approved_apac(self):
        apac = self.create_apac_request()
        apac.status = 'approved'
        apac.save()
        self.create_batch(self.requester.city)
        
        response = self.client.post(
            self.approve_url,
            {
                "apac_request_id": apac.pk,
                "authorizer_id": self.authorizer.pk
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_apac_status(apac.pk, ApacStatus.APPROVED)