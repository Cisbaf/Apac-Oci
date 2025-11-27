from pydantic import BaseModel
from typing import Optional, List
from apac_core.domain.entities.procedure import Procedure


class Cid(BaseModel):
    code: str
    name: str
    procedure: Optional[List[Procedure]] = []
    id: Optional[int] = None  # ID opcional até ser salvo
