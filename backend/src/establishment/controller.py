from establishment.models import EstablishmentModel
from city.models import CityModel
from apac_core.domain.repositories.establishment_repository import EstablishmentRepository
from apac_core.domain.exceptions import NotFoundException


class EstablishmentController(EstablishmentRepository):
    
    def get_by_id(self, id):
        establishment = EstablishmentModel.objects.get(pk=id)
        if establishment:
            return establishment.to_entity()
        raise NotFoundException()
    
    def save(self, establishment):
        return EstablishmentModel.objects.create(
            name=establishment.name,
            cnes=establishment.cnes,
            city=CityModel.objects.get(pk=establishment.city.id),
            cnpj=establishment.cnpj,
            acronym=establishment.acronym,
            is_active=establishment.is_active
        ).to_entity()