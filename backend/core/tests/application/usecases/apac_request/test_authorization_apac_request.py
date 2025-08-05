import pytest
from apac_core.application.use_cases.apac_request_cases.authorize_apac_request_case import ApprovedApacRequestUseCase, RejectApacRequestUseCase, ApprovedApacRequestDTO, RejectApacRequestDTO
from apac_core.application.implementations.apac_data_fake_repository import ApacDataFakeRepository
from apac_core.application.implementations.apac_request_fake_repository import ApacRequestFakeRepository
from apac_core.application.implementations.establishment_fake_repository import EstablishmentFakeRepository
from apac_core.application.implementations.user_fake_repository import UserFakeRepository
from apac_core.application.implementations.city_fake_repository import CityFakeRepository
from apac_core.application.implementations.procedure_fake_repository import ProcedureFakeRepository
from apac_core.application.implementations.procedure_record_fake_repository import ProcedureRecordFakeRepository
from apac_core.application.implementations.apac_batch_fake_repository import ApacBatchFakeRepository
from apac_core.application.implementations.cid_fake_repository import CidFakeRepository
from apac_core.application.use_cases.apac_request_cases.create_apac_request_case import CreateApacRequestUseCase, CreateApacRequestDTO
from apac_core.application.use_cases.create_apac_data_case import CreateApacDataDTO, CreateProcedureRecordDTO
from apac_core.application.use_cases.user_cases.create_user_case import CreateUserUseCase
from apac_core.application.use_cases.create_city_case import CreateCityUseCase
from apac_core.application.use_cases.establishment_cases.create_establishment_case import CreateEstablishmentUseCase
from apac_core.application.use_cases.procedure_cases.create_procedure_case import CreateProcedureUseCase
from apac_core.application.use_cases.apac_batch_cases.create_apac_batch_case import CreateApacBatchUseCase
from apac_core.application.use_cases.cid_cases.create_cid_case import CreateCidUseCase
from apac_core.domain.entities.user_role import UserRole
from apac_core.domain.exceptions import PermissionDeniedException, ValidationException, DomainException
from apac_core.domain.entities.apac_status import ApacStatus
from datetime import date
from utils import get_date_for_token


@pytest.fixture
def repos():
    return {
        "user": UserFakeRepository(),
        "establishment": EstablishmentFakeRepository(),
        "city": CityFakeRepository(),
        "apac_request": ApacRequestFakeRepository(),
        "apac_data": ApacDataFakeRepository(),
        "cid": CidFakeRepository(),
        "procedure": ProcedureFakeRepository(),
        "procedure_record": ProcedureRecordFakeRepository(),
        "apac_batch": ApacBatchFakeRepository()
    }


@pytest.fixture
def common_entities(repos):
    """Fixture that creates and returns common test entities."""
    city = CreateCityUseCase(repos["city"]).execute("Nova Iguaçu")
    CreateApacBatchUseCase(repos["apac_batch"], repos["city"]).execute("7894", get_date_for_token(), city.id)
    establishment = CreateEstablishmentUseCase(repos["establishment"], repos["city"]).execute("HGNI", "7569944", city.id)
    main_procedure = CreateProcedureUseCase(repos["procedure"]).execute(
        "OCI MUALAÇÃO INICIAL EM OFFICIALOLOGIA", 
        "0005010035"
    )
    sub_procedure = CreateProcedureUseCase(repos["procedure"]).execute(
        "CONSULTA IMEDICA EM ATENÇÃO ESPECIALIZADA", 
        "02010100072", 
        main_procedure.id
    )

    cid = CreateCidUseCase(repos["cid"], repos["procedure"]).execute("xxxxx", "xxxxx", main_procedure.id)
    
    apac_data = CreateApacDataDTO(
        patient_name="João da Silva",
        patient_record_number="2023100456",
        patient_cns="706000343458946",
        patient_cpf="187.149.337-48",
        patient_birth_date="1999-03-12",
        patient_race_color="parda",
        patient_gender="Masculino",
        patient_mother_name="Maria Aparecida da Silva",
        patient_address_street_type="Avenida",
        patient_address_street_name="Abilio Augusto Tavora",
        patient_address_number="2789",
        patient_address_complement="Apartamento 201", # OPCIONAL
        patient_address_postal_code="26265-090",
        patient_address_neighborhood="Jardim Alvorada",
        patient_address_city="Nova Iguaçu",
        patient_address_state="RJ",
        medic_name="Fernando Rodrigues",
        medic_cns="706000343458946",
        medic_cbo="20154786",
        cid_id=cid.id,
        procedure_date="2025-07-30",
        main_procedure_id=main_procedure.id,
        sub_procedures=[CreateProcedureRecordDTO(procedure_id=sub_procedure.id, quantity=3)]
    )
    return establishment, apac_data


@pytest.fixture
def authorizer(repos, common_entities):
    """Fixture that creates an authorizer user."""
    establishment, _ = common_entities
    return CreateUserUseCase(repos["user"], repos["city"]).execute(
        "Mariana",
        UserRole.AUTHORIZER,
        establishment.city.id
    )

@pytest.fixture
def requester(repos, common_entities):
    """Fixture that creates an authorizer user."""
    establishment, _ = common_entities
    return CreateUserUseCase(repos["user"], repos["city"]).execute(
        "Requester",
        UserRole.REQUESTER,
        establishment.city.id
    )

@pytest.fixture
def apac_request(repos, common_entities, requester):
    """Fixture that creates a basic APAC request."""
    establishment, apac_data = common_entities
    return CreateApacRequestUseCase(
        repos["apac_request"],
        repos["user"],
        repos["establishment"],
        repos["apac_data"],
        repos["cid"],
        repos["procedure"],
        repos["procedure_record"]
    ).execute(CreateApacRequestDTO(
        requester_id=requester.id,
        establishment_id=establishment.id,
        apac_data=apac_data
    ))

def create_apac_request(repos, requester_id: int, establishment_id: int, apac_data: CreateApacDataDTO):
    return CreateApacRequestUseCase(
        repos["apac_request"],
        repos["user"],
        repos["establishment"],
        repos["apac_data"],
        repos["cid"],
        repos["procedure"],
        repos["procedure_record"]
    ).execute(CreateApacRequestDTO(
        requester_id=requester_id,
        establishment_id=establishment_id,
        apac_data=apac_data
    ))

def test_validate_by_authorizer_success(repos, common_entities, requester, authorizer):
    """Test that authorizer can successfully approve an APAC request."""
    establishment, apac_data = common_entities
    apac_request = create_apac_request(
        repos=repos,
        requester_id=requester.id,
        establishment_id=establishment.id,
        apac_data=apac_data
    )
    
    assert apac_request.status == ApacStatus.PENDING
    
    approved_request = ApprovedApacRequestUseCase(
        repos["apac_request"],
        repos["user"],
        repos["apac_batch"]
    ).execute(ApprovedApacRequestDTO(apac_request_id=apac_request.id, authorizer_id=authorizer.id))
    
    assert approved_request.status == ApacStatus.APPROVED


def test_validate_by_requester_fails(repos, common_entities, requester):
    """Test that requester cannot approve an APAC request."""
    establishment, apac_data = common_entities
    
    apac_request = create_apac_request(
        repos=repos,
        requester_id=requester.id,
        establishment_id=establishment.id,
        apac_data=apac_data
    )
    
    with pytest.raises(PermissionDeniedException):
        ApprovedApacRequestUseCase(
            repos["apac_request"],
            repos["user"],
            repos["apac_batch"]
        ).execute(ApprovedApacRequestDTO(apac_request_id=apac_request.id, authorizer_id=requester.id))


def test_reject_by_authorizer_success(repos, apac_request, authorizer):
    """Test that authorizer can reject an APAC request with valid reason."""
    rejected_request = RejectApacRequestUseCase(
        repos["apac_request"],
        repos["user"],
        repos["apac_batch"]
    ).execute(RejectApacRequestDTO(apac_request_id=apac_request.id, authorizer_id=authorizer.id, justification="Invalid procedure"))

    assert rejected_request.status == ApacStatus.REJECTED
    assert rejected_request.justification == "Invalid procedure"

def test_reject_by_requester_fails(repos, common_entities, requester):
    """Test that requester cannot reject an APAC request."""
    establishment, apac_data = common_entities

    apac_request = create_apac_request(
        repos=repos,
        requester_id=requester.id,
        establishment_id=establishment.id,
        apac_data=apac_data
    )
    
    with pytest.raises(PermissionDeniedException):
        RejectApacRequestUseCase(
            repos["apac_request"],
            repos["user"],
            repos["apac_batch"]
        ).execute(RejectApacRequestDTO(
            apac_request_id=apac_request.id,
            authorizer_id=requester.id,
            justification="Reason"
        ))


def test_reject_with_empty_reason_fails(repos, apac_request, authorizer):
    """Test that rejection requires a non-empty reason."""
    with pytest.raises(ValidationException):
        RejectApacRequestUseCase(
            repos["apac_request"],
            repos["user"],
            repos["apac_batch"]
        ).execute(RejectApacRequestDTO(
            apac_request_id=apac_request.id,
            authorizer_id=authorizer.id,
            justification=""
        ))

def test_no_apac_band_available_for_authorize(repos, apac_request, authorizer):
    repo_apac_batch = repos["apac_batch"]
    apac_batch = repo_apac_batch.search_for_available_batch(authorizer.city.id)
    repo_apac_batch.delete_by_id(apac_batch.id)
    with pytest.raises(DomainException):
        ApprovedApacRequestUseCase(
            repos["apac_request"],
            repos["user"],
            repos["apac_batch"]
        ).execute(ApprovedApacRequestDTO(
            apac_request_id=apac_request.id,
            authorizer_id=authorizer.id,
        ))