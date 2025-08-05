from .models import ApacDataModel
from procedure.models import ProcedureModel, CidModel
from procedure_record.models import ProcedureRecordModel
from apac_core.domain.repositories.apac_data_repository import ApacDataRepository
from apac_core.domain.exceptions import NotFoundException


class ApacDataController(ApacDataRepository):

    def get_by_id(self, id):
        apac_data = ApacDataModel.objects.get(pk=id)
        if apac_data:
            return apac_data.to_entity()
        raise NotFoundException()
    
    def save(self, apac_data):
        created_apac_data = ApacDataModel.objects.create(
            patient_name = apac_data.patient_name,
            patient_record_number = apac_data.patient_record_number,
            patient_cns = apac_data.patient_cns.value,
            patient_cpf = apac_data.patient_cpf.value,
            patient_birth_date = apac_data.patient_birth_date,
            patient_race_color = apac_data.patient_race_color,
            patient_gender = apac_data.patient_gender,
            patient_mother_name = apac_data.patient_mother_name,
            patient_address_street_type = apac_data.patient_address_street_type,
            patient_address_street_name = apac_data.patient_address_street_name,
            patient_address_number = apac_data.patient_address_number,
            patient_address_complement = apac_data.patient_address_complement,
            patient_address_postal_code = apac_data.patient_address_postal_code.value,
            patient_address_neighborhood = apac_data.patient_address_neighborhood,
            patient_address_city = apac_data.patient_address_city,
            patient_address_state = apac_data.patient_address_state,
            medic_name = apac_data.medic_name,
            medic_cns = apac_data.medic_cns.value,
            medic_cbo = apac_data.medic_cbo,
            cid=CidModel.objects.get(pk=apac_data.cid.id),
            procedure_date=apac_data.procedure_date,
            main_procedure=ProcedureModel.objects.get(pk=apac_data.main_procedure.id)
        )
        for sub in apac_data.sub_procedures:
            sub_procedure = ProcedureRecordModel.objects.get(pk=sub.id)
            sub_procedure.apac_data = created_apac_data
            sub_procedure.save()
        return created_apac_data.to_entity()