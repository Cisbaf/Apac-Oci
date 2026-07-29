from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import Optional, List



class Procedure(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    # Atributo complementar SIGTAP 054 — APAC com validade fixa de 2 competências.
    # A validade normal (3 competências) é o default desde a Portaria SAES/MS
    # Nº 3.958/2026 (T-024); alguns procedimentos ainda mantêm o atributo (T-034).
    fixed_validity_two_competences: bool = False
    parent: Optional['Procedure'] = None
    sub_procedures: List['Procedure'] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    id: Optional[int] = None  # ID opcional até ser salvo
