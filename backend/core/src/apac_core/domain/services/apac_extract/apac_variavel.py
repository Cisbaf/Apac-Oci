from pydantic import Field, field_validator
from typing import Optional
from apac_core.domain.services.apac_extract.base import FixedWidthBaseModel
from apac_core.domain.services.apac_extract.utils import format_date_yyyymmdd, fix_length, only_digits
from datetime import date

class ApacVariavel(FixedWidthBaseModel):
    __field_sizes__ = { # A quantidade de caracters que cada campo deverá ter
        "apa_varia": 2,
        "apa_cmp": 6,  # competencia
        "apa_num": 13, # faixa apac
        "apa_cidpri": 4, # cid principal
        "apa_cidsec": 4, # cid secundario
        "apa_dtiden": 8 # data da identificacao
    }
    apa_varia: Optional[str] = Field(default="06")
    apa_cmp: str
    apa_num: str
    apa_cidpri: str
    apa_cidsec: Optional[str] = ""
    apa_dtiden: Optional[str] = ""