from pydantic import BaseModel
from apac_core.domain.entities.city import City
from apac_core.domain.entities.establishment import Establishment
from apac_core.domain.entities.user_role import UserRole
from typing import Optional


class User(BaseModel):
    name: str
    role: UserRole
    city: City
    id: Optional[int] = None  # ID opcional até ser salvo
    