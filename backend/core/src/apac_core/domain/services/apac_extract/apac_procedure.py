from pydantic import Field, field_validator
from typing import Optional
from apac_core.domain.services.apac_extract.base import FixedWidthBaseModel
from apac_core.domain.services.apac_extract.utils import format_date_yyyymmdd, fix_length, only_digits
from datetime import date

class ApacProcedure(FixedWidthBaseModel):
    __field_sizes__ = {
        "identificador": 2,
        "competencia": 6,
        "numero_apac_seq": 13,
        "cod_procedimento": 10,
        "cbo": 6,
        "quantity": 7,
        "cnpj": 14,
        "n_fiscal": 6,
        "cid_principal": 4,
        "cid_secundario": 4
    }
    identificador: Optional[str] = Field(default="13")
    competencia: str
    numero_apac_seq: str
    cod_procedimento: str
    cbo: str
    quantity: str
    cnpj: Optional[str] = ""
    n_fiscal: Optional[str] = ""
    cid_principal: str
    cid_secundario: Optional[str] = ""

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
