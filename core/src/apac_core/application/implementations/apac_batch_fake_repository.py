from apac_core.domain.repositories.apac_batch_repository import ApacBatchRepository
from apac_core.domain.entities.apac_batch import ApacBatch
from apac_core.domain.exceptions import NotFoundException
from typing import List
from datetime import date

class ApacBatchFakeRepository(ApacBatchRepository):

    def __init__(self):
        self.increment_id = 1
        self.apac_batchs: List[ApacBatch] = []

    def get_by_id(self, id):
        for batch in self.apac_batchs:
            if batch.id == id:
                return batch
        raise NotFoundException("A Faixa Apac não foi encontrada!")


    def search_for_available_batch(self, city_id) -> ApacBatch:
        for batch in self.apac_batchs:
            if (
                batch.city.id == city_id
                and batch.is_available(date.today())
            ):
                return batch
        raise NotFoundException("Nenhuma Faixa Apac disponível encontrado!")

    def save(self, apac_batch):
        if not apac_batch.id:
            apac_batch.id = self.increment_id
            self.increment_id += 1
            self.apac_batchs.append(apac_batch)
        else:
            for i, _apac_batch in enumerate(self.apac_batchs):
                if _apac_batch.id == apac_batch.id:
                    self.apac_batchs[i] = apac_batch
                    break
        return apac_batch
    
    def delete_by_id(self, batch_id):
        for i, batch in enumerate(self.apac_batchs):
            if batch.id == batch_id:
                del self.apac_batchs[i]
                return
        raise NotFoundException(f"Faixa Apac com id {batch_id} não encontrada para exclusão.")
