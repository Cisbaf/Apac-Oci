"""T-043 — a regra PMAE vale na criação da APAC, não só no formulário.

Antes desta tarefa a exigência da consulta era um `ProcedureRequirementGroup`
lido pelo React: quem chamasse a API direto criava a APAC que o APAC Magnético
recusa depois, já com número de faixa consumido.
"""
import pytest
from apac_core.application.use_cases.apac_request_cases.create_apac_request_case import (
    CreateApacRequestDTO, CreateApacRequestUseCase,
)
from apac_core.application.use_cases.create_apac_data_case import CreateApacDataDTO
from apac_core.application.use_cases.procedure_record_cases.create_procedure_record_case import (
    CreateProcedureRecordDTO,
)
from apac_core.application.use_cases.cid_cases.create_cid_case import CreateCidUseCase
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.exceptions import DomainException
from apac_core.domain.services import pmae

TOMOGRAFIA = "0206020031"
BACILOSCOPIA = "0202080048"


@pytest.fixture
def oci_pmae(repos):
    """OCI de Infectologia com o atributo 053 e três secundários possíveis."""
    secundarios = [
        repos["procedure"].save(Procedure(name=nome, code=code))
        for code, nome in (
            (TOMOGRAFIA, "Tomografia Computadorizada de Tórax"),
            (BACILOSCOPIA, "Baciloscopia Direta para BAAR"),
            (pmae.CONSULTA, "Consulta Médica em Atenção Especializada"),
        )
    ]
    principal = repos["procedure"].save(Procedure(
        name="OCI Avaliação Diagnóstica Inicial de Síndromes Respiratórias",
        code="0908010010", pmae=True, sub_procedures=secundarios,
    ))
    return principal, {p.code: p for p in secundarios}


def dto(requester, establishment, cid, principal, marcados):
    return CreateApacRequestDTO(
        requester_id=requester.id,
        establishment_id=establishment.id,
        request_date="2025-07-01",
        apac_data=CreateApacDataDTO(
            patient_name="João da Silva",
            patient_record_number="99999",
            patient_cns="706000343458946",
            patient_cpf="187.149.337-48",
            patient_birth_date="1999-03-12",
            patient_race_color="parda",
            patient_gender="Masculino",
            patient_mother_name="Maria Aparecida da Silva",
            patient_address_street_type="Avenida",
            patient_address_street_name="Abilio Augusto Tavora",
            patient_address_number="2789",
            patient_address_complement="Apartamento 201",
            patient_address_postal_code="26265-090",
            patient_address_neighborhood="Jardim Alvorada",
            patient_address_city="Nova Iguaçu",
            patient_address_state="RJ",
            supervising_physician_name="Fernando Rodrigues",
            supervising_physician_cns="706000343458946",
            supervising_physician_cbo="654321",
            authorizing_physician_name="Fernando Rodrigues",
            authorizing_physician_cns="706000343458946",
            authorizing_physician_cbo="123456",
            cid_id=cid.id,
            procedure_date="2025-07-30",
            discharge_date="2025-07-31",
            main_procedure_id=principal.id,
            sub_procedures=[
                CreateProcedureRecordDTO(procedure_id=p.id, quantity=1) for p in marcados
            ],
        ),
    )


def criar(repos, data):
    return CreateApacRequestUseCase(
        repos["apac_request"], repos["user"], repos["establishment"],
        repos["apac_data"], repos["cid"], repos["procedure"],
        repos["procedure_record"],
    ).execute(data)


@pytest.fixture
def cid_da_oci(repos, oci_pmae):
    principal, _ = oci_pmae
    return CreateCidUseCase(repos["cid"], repos["procedure"]).execute(
        "B20", "Doença pelo HIV", principal.id)


class TestPmaeNaCriacao:

    def test_recusa_apac_com_um_secundario_so(self, repos, requester, establishment,
                                              cid_da_oci, oci_pmae):
        principal, secundarios = oci_pmae

        with pytest.raises(DomainException) as erro:
            criar(repos, dto(requester, establishment, cid_da_oci, principal,
                             [secundarios[TOMOGRAFIA]]))

        assert "pelo menos 2" in str(erro.value)

    def test_recusa_dois_secundarios_sem_consulta(self, repos, requester, establishment,
                                                  cid_da_oci, oci_pmae):
        principal, secundarios = oci_pmae

        with pytest.raises(DomainException) as erro:
            criar(repos, dto(requester, establishment, cid_da_oci, principal,
                             [secundarios[TOMOGRAFIA], secundarios[BACILOSCOPIA]]))

        assert pmae.CONSULTA in str(erro.value)

    def test_aceita_com_consulta(self, repos, requester, establishment,
                                 cid_da_oci, oci_pmae):
        principal, secundarios = oci_pmae

        request = criar(repos, dto(requester, establishment, cid_da_oci, principal,
                                   [secundarios[TOMOGRAFIA], secundarios[pmae.CONSULTA]]))

        assert request.id is not None
