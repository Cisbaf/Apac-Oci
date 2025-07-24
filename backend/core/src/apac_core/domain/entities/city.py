from typing import Optional
from pydantic import BaseModel

class City(BaseModel):
    name: str
    ibge_code: Optional[str] = None
    state_type: Optional[str] = "M"
    id: Optional[int] = None  # ID opcional até ser salvo
