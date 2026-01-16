from .models import ProcedureModel, ProcedureRecordModel
from apac_core.domain.repositories.procedure_record_repository import ProcedureRecordRepository
from apac_core.domain.exceptions import NotFoundException


class ProcedureRecordController(ProcedureRecordRepository):

    def get_by_id(self, id):
        procedure_record = ProcedureRecordModel.objects.get(pk=id)
        if procedure_record:
            return procedure_record.to_entity()
        raise NotFoundException()
    
    def save(self, procedure_record):
        return ProcedureRecordModel.objects.create(
            procedure=ProcedureModel.objects.get(pk=procedure_record.procedure.id),
            quantity=procedure_record.quantity,
            cbo=procedure_record.cbo,
            cnes=procedure_record.cnes
        ).to_entity()