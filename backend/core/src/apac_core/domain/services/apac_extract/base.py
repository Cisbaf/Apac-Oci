from pydantic import BaseModel
from typing import ClassVar

from apac_core.domain.services.apac_extract.utils import fix_length, sanitize_text


class FixedWidthBaseModel(BaseModel):
    __field_sizes__: ClassVar[dict] = {}

    def to_fixed_line(self) -> str:
        """
        Concatena os campos com tamanhos fixos conforme o mapa __field_sizes__.
        Se o campo não tiver tamanho definido, converte apenas para string limpa.
        """
        parts = []
        for field, value in self.model_dump().items():
            size = self.__field_sizes__.get(field)
            text = fix_length(sanitize_text(str(value)), size)
            parts.append(text)
        return "".join(parts)