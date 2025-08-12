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
from apac_core.domain.dto.patientData import PatientData
from apac_core.domain.dto.medicData import MedicData

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
    supervising_physician_name: str
    supervising_physician_cns: str
    supervising_physician_cbo: str
    authorizing_physician_name: str
    authorizing_physician_cns: str
    authorizing_physician_cbo: str
    cid_id: int
    procedure_date: str
    discharge_date: str
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
            patient_data=PatientData(
               name=data.patient_name,
               record_number=data.patient_record_number,
               cns=CnsField(value=data.patient_cns),
               cpf=CpfField(value=data.patient_cpf),
               birth_date=data.patient_birth_date,
               race_color=data.patient_race_color,
               gender=data.patient_gender,
               mother_name=data.patient_mother_name,
               address_street_type=data.patient_address_street_type,
               address_street_name=data.patient_address_street_name,
               address_number=data.patient_address_number,
               address_complement=data.patient_address_complement,
               address_postal_code=CepField(value=data.patient_address_postal_code),
               address_neighborhood=data.patient_address_neighborhood,
               address_city=data.patient_address_city,
               address_state=data.patient_address_state,
            ),
            supervising_physician_data=MedicData(
                name=data.supervising_physician_name,
                cns=CnsField(value=data.supervising_physician_cns),
                cbo=data.supervising_physician_cbo,
            ),
            authorizing_physician_data=MedicData(
                name=data.authorizing_physician_name,
                cns=CnsField(value=data.authorizing_physician_cns),
                cbo=data.authorizing_physician_cbo,
            ),
            cid=cid,
            procedure_date=data.procedure_date,
            discharge_date=data.discharge_date,
            main_procedure=main_procedure,
            sub_procedures=sub_procedures
        ))
        