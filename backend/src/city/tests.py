from django.test import TestCase
from apac_core.application.use_cases.create_city_case import CreateCityUseCase
from .models import CityModel
from .controller import CityController


class CityControllerTestCase(TestCase):

    def setUp(self):
        self.repo = CityController()
        CreateCityUseCase(self.repo).execute("Nova Iguaçu")

    def test_create_city_use_case_success(self):
        self.assertIsNotNone(CityModel.objects.get(name="Nova Iguaçu"))

    def test_get_city_by_id_with_use_case(self):
        self.assertIsNotNone(self.repo.get_by_id(1))

    def test_convert_model_to_entity_success(self):
        city_model = CityModel.objects.get(pk=1)
        city_entity = self.repo.get_by_id(1)
        self.assertEqual(city_entity, city_model.to_entity())