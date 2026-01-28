from abc import ABC, abstractmethod
from apac_core.domain.entities.apac_batch import ApacBatch
from datetime import date

class ApacBatchRepository(ABC):

    @abstractmethod
    def search_for_available_batch(self, city_id: int, competence: date) -> ApacBatch:
        pass

    @abstractmethod
    def save(self, apac_batch: ApacBatch) -> ApacBatch:
        pass

    @abstractmethod
    def get_by_id(self, batch_id: int) -> ApacBatch:
        pass

