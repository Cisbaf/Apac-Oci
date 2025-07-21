from django.test import TestCase
from apac_core.application.use_cases.establishment_cases.create_establishment_case import CreateEstablishmentUseCase
from apac_core.application.use_cases.create_city_case import CreateCityUseCase
from city.controller import CityController
from .controller import EstablishmentController
from .models import EstablishmentModel

class EstablishmentControllerTestCase(TestCase):

    def setUp(self):
        self.repo = EstablishmentController()
        repo_city = CityController()
        self.city = CreateCityUseCase(repo_city).execute("Nova Iguaçu")
        CreateEstablishmentUseCase(self.repo, repo_city).execute(
            "HGNI",
            "7890380",
            self.city.id
        )

    def test_create_establishment_use_case_success(self):
        self.assertIsNotNone(EstablishmentModel.objects.get(name="HGNI"))

    def test_get_establishment_by_id_with_use_case(self):
        self.assertIsNotNone(self.repo.get_by_id(1))

    def test_convert_model_to_entity_success(self):
        establishment_model = EstablishmentModel.objects.get(pk=1)
        establishment_entity = self.repo.get_by_id(1)
        self.assertEqual(establishment_entity, establishment_model.to_entity())