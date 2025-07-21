from typing import List
from apac_core.domain.exceptions import NotFoundException
from apac_core.domain.repositories.city_repository import CityRepository
from apac_core.domain.entities.city import City


class CityFakeRepository(CityRepository):

    def __init__(self):
        super().__init__()
        self.increment_id = 1
        self.cities: List[City] = []
    
    def save(self, city):
        if not city.id:
            city.id = self.increment_id
            self.increment_id += 1
            self.cities.append(city)
        else:
            for i, _city in enumerate(self.cities):
                if _city.id == city.id:
                    self.cities[i] = city
                    break
        return city

    def get_by_id(self, id):
        for city in self.cities:
            if city.id == id:
                return city
        raise NotFoundException()