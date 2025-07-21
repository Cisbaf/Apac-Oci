from .models import CityModel
from apac_core.domain.repositories.city_repository import CityRepository
from apac_core.domain.exceptions import NotFoundException


class CityController(CityRepository):

    def get_by_id(self, id):
        city = CityModel.objects.get(pk=id)
        if city:
            return city.to_entity()
        raise NotFoundException()
    
    def save(self, city):
        return CityModel.objects.create(
            name=city.name
        ).to_entity()