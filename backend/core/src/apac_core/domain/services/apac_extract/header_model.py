from datetime import date, datetime
from typing import ClassVar
from pydantic import Field, field_validator

from apac_core.domain.services.apac_extract.base import FixedWidthBaseModel
from apac_core.domain.services.apac_extract.utils import (
    only_digits, fix_length, format_date_yyyymmdd
)


class HeaderModel(FixedWidthBaseModel):
    __field_sizes__: ClassVar[dict] = {
        "identificador": 2,
        "literal_apac": 5,
        "competencia": 6,
        "qtd_apacs": 6,
        "campo_controle": 4,
        "nome_orgao_origem": 30,
        "sigla_origem": 6,
        "cnpj_prestador": 14,
        "nome_destino": 40,
        "indicador_destino": 1,
        "data_geracao": 8,
        "versao_layout": 15,
    }

    identificador: str = Field(default="01")  # 001–002
    literal_apac: str = Field(default="#APAC")  # 003–007
    competencia: str  # 008–013
    qtd_apacs: str  # 014–019
    campo_controle: str  # 020–023
    nome_orgao_origem: str  # 024–053
    sigla_origem: str  # 054–059
    cnpj_prestador: str  # 060–073
    nome_destino: str  # 074–113
    indicador_destino: str  # 114
    data_geracao: str  # 115–122
    versao_layout: str  # 123–137

    @field_validator("*", mode="before")
    @classmethod
    def normalize_fields(cls, v, info):
        field = info.field_name
        sizes = cls.__field_sizes__

        if field.startswith("data_") and isinstance(v, (str, date, datetime)):
            return format_date_yyyymmdd(v)

        if "cnpj" in field:
            return only_digits(v, sizes[field])
        
        return fix_length(str(v), sizes[field])
