from pydantic import Field, field_validator
from typing import Optional
from apac_core.domain.services.apac_extract.base import FixedWidthBaseModel
from apac_core.domain.services.apac_extract.utils import format_date_yyyymmdd, fix_length, only_digits
from datetime import date

class ApacInfo(FixedWidthBaseModel):
    __field_sizes__ = { # A quantidade de caracters que cada campo deverá ter
        "mes_fim_validate": 6,
        "o_que_e": 2,
        "numero_apac": 13,
        "cid": 4,
    }
    mes_fim_validate: str
    o_que_e: str # antigo "o_que_e"
    numero_apac: str
    cid: str

    @field_validator("*", mode="before")
    @classmethod
    def normalize_fields(cls, v, info):
        field = info.field_name
        sizes = cls.__field_sizes__

        if field.startswith("data_") and isinstance(v, (str, date)):
            return format_date_yyyymmdd(v)

        if "cns" in field or field == "cnes":
            return only_digits(v, sizes[field])

        return fix_length(str(v), sizes[field])
