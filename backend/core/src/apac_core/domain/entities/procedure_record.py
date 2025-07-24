from pydantic import BaseModel
from apac_core.domain.entities.procedure import Procedure
from typing import Optional

class ProcedureRecord(BaseModel):
    procedure: Procedure
    quantity: int
    id: Optional[int] = None  # ID opcional até ser salvo
