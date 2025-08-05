from dataclasses import dataclass
from pydantic import BaseModel
from typing import List
from datetime import date
from apac_core.domain.repositories.apac_data_repository import ApacDataRepository
from apac_core.domain.repositories.cid_repository import CidRepository
from apac_core.domain.repositories.procedure_repository import ProcedureRepository
from apac_core.domain.repositories.procedure_record_repository import ProcedureRecordRepository
from apac_core.domain.entities.apac_data import ApacData
from apac_core.application.use_cases.procedure_record_cases.create_procedure_record_case import (
    CreateProcedureRecordDTO, CreateProcedureRecordUseCase
)
from apac_core.domain.value_objects.cns import CnsField
from apac_core.domain.value_objects.cpf import CpfField
from apac_core.domain.value_objects.cep import CepField

class CreateApacDataDTO(BaseModel):
    patient_name: str
    patient_record_number: str
    patient_cns: str
    patient_cpf: str
    patient_birth_date: str
    patient_race_color: str
    patient_gender: str
    patient_mother_name: str
    patient_address_street_type: str
    patient_address_street_name: str
    patient_address_number: str
    patient_address_complement: str
    patient_address_postal_code: str
    patient_address_neighborhood: str
    patient_address_city: str
    patient_address_state: str
    medic_name: str
    medic_cns: str
    medic_cbo: str
    cid_id: int
    procedure_date: str
    main_procedure_id: int
    sub_procedures: List[CreateProcedureRecordDTO]


@dataclass
class CreateApacDataUseCase:
    repo_apac_data: ApacDataRepository
    repo_cid: CidRepository
    repo_procedure: ProcedureRepository
    repo_procedure_record: ProcedureRecordRepository

    def execute(
        self,
        data: CreateApacDataDTO
    ):
        # Obtém o procedimento principal pelo ID
        main_procedure = self.repo_procedure.get_by_id(data.main_procedure_id)

        # Obtém o CID pelo ID
        cid = self.repo_cid.get_by_id(data.cid_id)
        
        # Registra todos os sub procedimentos usando o Use Case de ProcedureRecrod
        sub_procedures = [
            CreateProcedureRecordUseCase(
                self.repo_procedure_record,
                self.repo_procedure
            ).execute(dto) for dto in data.sub_procedures
        ]

        # Registrando e retornando ApacData
        return self.repo_apac_data.save(ApacData(
            patient_name=data.patient_name,
            patient_record_number=data.patient_record_number,
            patient_cns=CnsField(value=data.patient_cns),
            patient_cpf=CpfField(value=data.patient_cpf),
            patient_birth_date=data.patient_birth_date,
            patient_race_color=data.patient_race_color,
            patient_gender=data.patient_gender,
            patient_mother_name=data.patient_mother_name,
            patient_address_street_type=data.patient_address_street_type,
            patient_address_street_name=data.patient_address_street_name,
            patient_address_number=data.patient_address_number,
            patient_address_complement=data.patient_address_complement,
            patient_address_postal_code=CepField(value=data.patient_address_postal_code),
            patient_address_neighborhood=data.patient_address_neighborhood,
            patient_address_city=data.patient_address_city,
            patient_address_state=data.patient_address_state,
            medic_name=data.medic_name,
            medic_cns=CnsField(value=data.medic_cns),
            medic_cbo=data.medic_cbo,
            cid=cid,
            procedure_date=data.procedure_date,
            main_procedure=main_procedure,
            sub_procedures=sub_procedures
        ))
        