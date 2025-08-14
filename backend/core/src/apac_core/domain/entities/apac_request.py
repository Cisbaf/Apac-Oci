from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.entities.establishment import Establishment
from apac_core.domain.entities.user import User
from apac_core.domain.entities.apac_data import ApacData
from apac_core.domain.exceptions import ValidationException

class ApacRequest(BaseModel):
    class Config:
        use_enum_values = True
        
    establishment: Establishment
    requester: User
    apac_data: Optional[ApacData] = None
    request_date: date
    status: Optional[ApacStatus] = ApacStatus.PENDING
    updated_at: datetime = Field(default_factory=datetime.now)
    authorizer: Optional[User] = None
    justification: Optional[str] = None
    review_date: Optional[datetime] = None
    id: Optional[int] = None

    def set_status(self, status: ApacStatus):
        self.status = status

    def set_authorizer(self, user: User):
        self.authorizer = user

    def set_justification(self, justification: str):
        if not justification or justification == "":
            raise ValidationException("A justificativa não pode ser vazia!")
        self.justification = justification

    def set_review_date(self, date: datetime = datetime.now()):
        self.review_date = date