from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from apac_core.domain.entities.city import City
from apac_core.domain.value_objects.validity import Validity
from apac_core.domain.entities.apac_request import ApacRequest

class ApacBatch(BaseModel):
    batch_number: str
    city: City
    validity: Validity
    apac_request: Optional[ApacRequest] = None
    export_date: Optional[date] = None
    id: Optional[int] = None

    def is_available(self, now: datetime) -> bool:
        return self.apac_request is None and not self.validity.is_expired(now)

    def set_apac_request(self, apac_request: ApacRequest):
        self.apac_request = apac_request