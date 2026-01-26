from pydantic import BaseModel
from apac_core.domain.services.apac_extract.apac_model import ApacModel
from apac_core.domain.services.apac_extract.apac_procedure import ApacProcedure
# from apac_core.domain.services.apac_extract.apac_info import ApacInfo
from apac_core.domain.services.apac_extract.apac_variavel import ApacVariavel

from typing import List

class ApacBody(BaseModel):
    apac_model: ApacModel
    apac_info: ApacVariavel
    apac_procedures: List[ApacProcedure]