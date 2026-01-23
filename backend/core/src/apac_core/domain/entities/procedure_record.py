from pydantic import BaseModel, Field, field_serializer
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.value_objects.cbo import CboField
from typing import Optional


class ProcedureRecord(BaseModel):
    procedure: Procedure
    quantity: int
    cbo: Optional[CboField] = Field(default=None)
    cnes: Optional[str] = None # Cnes do estabelecimento executante
    id: Optional[int] = None  # ID opcional até ser salvo

    @field_serializer("cbo", return_type=str)
    def serialize_medic_cbo(self, cbo: CboField, _info):
        if cbo:
            return cbo.value