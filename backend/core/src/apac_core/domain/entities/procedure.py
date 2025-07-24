from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import Optional, List



class Procedure(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    parent: Optional['Procedure'] = None
    sub_procedures: List['Procedure'] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    id: Optional[int] = None  # ID opcional até ser salvo
