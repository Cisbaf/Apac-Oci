from typing import Optional
from pydantic import BaseModel


class City(BaseModel):
    name: str
    ibge_code: str
    agency_name: str
    id: Optional[int] = None  # ID opcional até ser salvo
