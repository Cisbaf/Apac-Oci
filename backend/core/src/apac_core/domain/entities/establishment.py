from pydantic import BaseModel
from typing import Optional
from apac_core.domain.entities.city import City


class Establishment(BaseModel):
    name: str
    cnes: str
    city: City
    cnpj: Optional[str] = None
    acronym: Optional[str] = None
    is_active: Optional[bool] = True
    id: Optional[int] = None  # ID opcional até ser salvo

