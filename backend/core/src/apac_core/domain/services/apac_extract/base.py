from pydantic import BaseModel
from typing import ClassVar

from apac_core.domain.services.apac_extract.utils import fix_length

class FixedWidthBaseModel(BaseModel):
    __field_sizes__: ClassVar[dict] = {}

    def to_fixed_line(self) -> str:
        """Concatena os campos com tamanhos fixos, conforme __field_sizes__"""
        parts = []
        for field, value in self.model_dump().items():
            size = self.__field_sizes__.get(field)
            parts.append(fix_length(value, size) if size else str(value))
        return ''.join(parts)
