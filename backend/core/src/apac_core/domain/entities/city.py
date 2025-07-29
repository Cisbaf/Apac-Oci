from typing import Optional
from pydantic import BaseModel

class City(BaseModel):
    name: str
    ibge_code: Optional[str] = None
    agency_name: Optional[str] = None
    id: Optional[int] = None  # ID opcional até ser salvo
