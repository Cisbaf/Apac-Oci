from typing import List
from apac_core.domain.exceptions import NotFoundException
from apac_core.domain.repositories.cid_repository import CidRepository
from apac_core.domain.entities.cid import Cid


class CidFakeRepository(CidRepository):

    def __init__(self):
        super().__init__()
        self.increment_id = 1
        self.cidies: List[Cid] = []
    
    def save(self, cid):
        if not cid.id:
            cid.id = self.increment_id
            self.increment_id += 1
            self.cidies.append(cid)
        else:
            for i, _cid in enumerate(self.cidies):
                if _cid.id == cid.id:
                    self.cidies[i] = cid
                    break
        return cid

    def get_by_id(self, id):
        for cid in self.cidies:
            if cid.id == id:
                return cid
        raise NotFoundException()