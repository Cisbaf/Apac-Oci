from .models import ProcedureModel, CidModel
from apac_core.domain.repositories.procedure_repository import ProcedureRepository
from apac_core.domain.repositories.cid_repository import CidRepository
from apac_core.domain.exceptions import NotFoundException


class ProcedureController(ProcedureRepository):

    def get_by_id(self, id):
        procedure = ProcedureModel.objects.get(pk=id)
        if procedure:
            return procedure.to_entity()
        raise NotFoundException()
    
    def save(self, procedure):
        registered = ProcedureModel.objects.create(
            name=procedure.name,
            code=procedure.code,
            description=procedure.description,
            is_active=procedure.is_active,
            created_at=procedure.created_at,
            updated_at=procedure.updated_at
        )
        # registrando 
        if procedure.parent:
            registered.parents.add(ProcedureModel.objects.get(pk=procedure.parent.id))
            registered.save()

        return registered.to_entity()
    

class CidController(CidRepository):

    def get_by_id(self, id):
        cid = CidModel.objects.get(pk=id)
        if cid:
            return cid.to_entity()
        raise NotFoundException()
    
    def save(self, cid):
        return CidModel.objects.create(
            code=cid.code,
            name=cid.name,
            procedure=ProcedureModel.objects.get(pk=cid.procedure.id)
        ).to_entity()