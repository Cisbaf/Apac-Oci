from typing import List
from apac_core.domain.exceptions import NotFoundException
from apac_core.domain.repositories.apac_data_repository import ApacDataRepository
from apac_core.domain.entities.apac_data import ApacData


class ApacDataFakeRepository(ApacDataRepository):

    def __init__(self):
        super().__init__()
        self.increment_id = 1
        self.apac_datas: List[ApacData] = []
    
    def save(self, apac_data):
        if not apac_data.id:
            apac_data.id = self.increment_id
            self.increment_id += 1
            self.apac_datas.append(apac_data)
        else:
            for i, _apac_data in enumerate(self.apac_datas):
                if _apac_data.id == apac_data.id:
                    self.apac_datas[i] = apac_data
                    break
        return apac_data

    def get_by_id(self, id):
        for apac_data in self.apac_datas:
            if apac_data.id == id:
                return apac_data
        raise NotFoundException()