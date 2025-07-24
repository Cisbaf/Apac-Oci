from dataclasses import dataclass
from apac_core.domain.repositories.city_repository import CityRepository
from apac_core.domain.repositories.apac_batch_repository import ApacBatchRepository
from apac_core.domain.entities.apac_batch import ApacBatch
from apac_core.domain.value_objects.validity import Validity
from datetime import date

@dataclass
class CreateApacBatchUseCase:
    repo_apac_batch: ApacBatchRepository
    repo_city: CityRepository

    def execute(self, batch_number: str, expire_in: date, city_id: int):
        city = self.repo_city.get_by_id(city_id)

        apac_batch = ApacBatch(
            batch_number=batch_number,
            city=city,
            validity=Validity(expire_in)
        )

        created_apac_batch = self.repo_apac_batch.save(apac_batch)
        return created_apac_batch


