from dataclasses import dataclass
from apac_core.domain.entities.apac_batch import ApacBatch
from apac_core.domain.entities.establishment import Establishment
from apac_core.domain.repositories.apac_batch_repository import ApacBatchRepository
from apac_core.domain.repositories.establishment_repository import EstablishmentRepository
from apac_core.application.use_cases.apac_batch_cases.get_finished_apac_batch_case import GetFinishedApacBatchUseCase
from apac_core.domain.services.apac_extract.controller import ExportApacBatchController
from pydantic import BaseModel
from datetime import date
from typing import List


class ApacExportDto(BaseModel):
    production: date
    establishment_id: int
    apac_batchs: List[int]


@dataclass
class ApacExportCase:
    repo_apac_batch: ApacBatchRepository
    repo_establishment: EstablishmentRepository

    def execute(self, data: ApacExportDto) -> str:
        establishment = self.repo_establishment.get_by_id(data.establishment_id)
        if not establishment:
            raise Exception("Estabelecimento não encontrado!")
        
        apac_batchs: List[ApacBatch] = []

        for batch_id in data.apac_batchs:
            apac_batch = GetFinishedApacBatchUseCase(self.repo_apac_batch).execute(batch_id)
            if not apac_batch.apac_request.establishment.id == establishment.id:
                raise Exception("Os estabelecimentos não batem!!")
            
            if not (apac_batch.apac_request.request_date.year == data.production.year and
                    apac_batch.apac_request.request_date.month == data.production.month):
                raise Exception("Não são da mesma competencia!")
            
            apac_batchs.append(apac_batch)

        controller = ExportApacBatchController(
            establishment=establishment,
            apac_batchs=apac_batchs,
            date_production=data.production
        )

        lines = []
        lines.append(controller.header().to_fixed_line())
        for body in controller.body():
            lines.append(body.apac_model.to_fixed_line())
            lines.append(body.apac_info.to_fixed_line())
            for procedure in body.apac_procedures:
                lines.append(procedure.to_fixed_line())

        output_string = "\n".join(lines)

        return output_string