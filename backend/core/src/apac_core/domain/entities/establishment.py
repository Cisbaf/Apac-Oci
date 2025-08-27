from pydantic import BaseModel
from typing import Optional
from apac_core.domain.entities.city import City


class Establishment(BaseModel):
    name: str
    cnes: str
    city: City
    cnpj: str
    acronym: str
    is_active: Optional[bool] = True
    id: Optional[int] = None  # ID opcional até ser salvo

