from pydantic import BaseModel
from apac_core.domain.entities.procedure import Procedure
from typing import Optional


class ProcedureRecord(BaseModel):
    procedure: Procedure
    quantity: int
    cbo: Optional[str] = None # Cbo do médico executante
    cnes: Optional[str] = None # Cnes do estabelecimento executante
    id: Optional[int] = None  # ID opcional até ser salvo
