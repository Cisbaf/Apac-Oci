from apac_core.domain.entities.establishment import Establishment
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.services.apac_extract.apac_model import ApacModel
from datetime import datetime
from apac_core.domain.services.apac_extract.utils import get_end_of_next_month


def adaptar_oci(apac_model: ApacModel):

    # data_autorizacao == procedure_date de apac data (adaptando)
    procedure_date =  datetime.strptime(apac_model.data_autorizacao, "%Y%m%d")

    apac_model.data_inicio_validade = procedure_date.strftime("%Y%m%d")
    apac_model.data_fim_validade = get_end_of_next_month(procedure_date).strftime("%Y%m%d")

    return apac_model