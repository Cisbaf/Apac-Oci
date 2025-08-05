import pytest
from apac_core.application.implementations.apac_data_fake_repository import ApacDataFakeRepository
from apac_core.application.implementations.apac_request_fake_repository import ApacRequestFakeRepository
from apac_core.application.implementations.establishment_fake_repository import EstablishmentFakeRepository
from apac_core.application.implementations.user_fake_repository import UserFakeRepository
from apac_core.application.implementations.city_fake_repository import CityFakeRepository
from apac_core.application.implementations.cid_fake_repository import CidFakeRepository
from apac_core.application.implementations.procedure_fake_repository import ProcedureFakeRepository
from apac_core.application.implementations.procedure_record_fake_repository import ProcedureRecordFakeRepository
from apac_core.application.use_cases.apac_request_cases.create_apac_request_case import CreateApacRequestUseCase, CreateApacRequestDTO
from apac_core.application.use_cases.user_cases.create_user_case import CreateUserUseCase
from apac_core.application.use_cases.create_apac_data_case import CreateApacDataDTO
from apac_core.application.use_cases.create_city_case import CreateCityUseCase
from apac_core.application.use_cases.establishment_cases.create_establishment_case import CreateEstablishmentUseCase
from apac_core.application.use_cases.procedure_cases.create_procedure_case import CreateProcedureUseCase
from apac_core.application.use_cases.procedure_record_cases.create_procedure_record_case import CreateProcedureRecordDTO
from apac_core.application.use_cases.cid_cases.create_cid_case import CreateCidUseCase
from apac_core.domain.entities.user_role import UserRole
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.exceptions import PermissionDeniedException, DomainException, NotFoundException
from datetime import date

@pytest.fixture
def repos():
    """Fixture providing all fake repositories needed for testing."""
    return {
        "user": UserFakeRepository(),
        "establishment": EstablishmentFakeRepository(),
        "city": CityFakeRepository(),
        "apac_request": ApacRequestFakeRepository(),
        "apac_data": ApacDataFakeRepository(),
        "cid": CidFakeRepository(),
        "procedure": ProcedureFakeRepository(),
        "procedure_record": ProcedureRecordFakeRepository(),
    }

@pytest.fixture
def city(repos):
    """Fixture creating a test city."""
    return CreateCityUseCase(repos["city"]).execute("Nova Iguaçu")

@pytest.fixture
def establishment(repos, city):
    """Fixture creating a test establishment."""
    return CreateEstablishmentUseCase(repos["establishment"], repos["city"]).execute("HGNI", "78999631", city.id)

@pytest.fixture
def medical_procedures(repos):
    """Fixture creating test medical procedures."""
    main_procedure = CreateProcedureUseCase(repos["procedure"]).execute(
        "OCI MUALAÇÃO INICIAL EM OFFICIALOLOGIA", 
        "0005010035"
    )
    sub_procedures = [
        CreateProcedureRecordDTO(procedure_id=main_procedure.id, quantity=3)
    ]
    return main_procedure, sub_procedures

@pytest.fixture
def cid(repos, medical_procedures):
    main_procedure, _ = medical_procedures
    """Fixture creating a test city."""
    return CreateCidUseCase(repos["cid"], repos["procedure"]).execute("I20", "Angina pectoris", main_procedure.id)

@pytest.fixture
def requester(repos, city):
    """Fixture creating a requester user."""
    return CreateUserUseCase(repos["user"], repos["city"]).execute(
        "Requester User",
        UserRole.REQUESTER,
        city.id
    )

@pytest.fixture
def authorizer(repos, city):
    """Fixture creating an authorizer user."""
    return CreateUserUseCase(repos["user"], repos["city"]).execute(
        "Authorizer User",
        UserRole.AUTHORIZER,
        city.id
    )

def create_apac_request(repos, data):
    """Helper function to create an APAC request."""
    return CreateApacRequestUseCase(
        repos["apac_request"],
        repos["user"],
        repos["establishment"],
        repos["apac_data"],
        repos["cid"],
        repos["procedure"],
        repos["procedure_record"]
    ).execute(data)

def generate_apac_request_dto(user, establishment, medical_procedures, cid):
    main_procedure, sub_procedures = medical_procedures

    return CreateApacRequestDTO(
        requester_id=user.id,
        establishment_id=establishment.id,
        apac_data= CreateApacDataDTO(
            patient_name="João da Silva",
            patient_record_number="99999", # OPCIONAL
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
            sub_procedures=sub_procedures
        )
    )

class TestCreateApacRequest:
    """Test suite for APAC request creation functionality."""

    def test_request_has_correct_initial_state(self, repos, requester, establishment, cid, medical_procedures):
        """Newly created APAC request should have correct initial state."""

        request = create_apac_request(
            repos,
            generate_apac_request_dto(
                requester,
                establishment,
                medical_procedures,
                cid
            )
        )
        
        assert request.status == ApacStatus.PENDING
        assert request.authorizer is None
        assert request.justification is None
        assert request.requester.id == requester.id
        assert request.establishment.id == establishment.id

    def test_requester_can_create_request(self, repos, requester, establishment, cid, medical_procedures):
        """Requester role should be able to create APAC requests."""
        request = create_apac_request(
            repos,
            generate_apac_request_dto(
                requester,
                establishment,
                medical_procedures,
                cid
            )
        )
        
        assert request.id == 1
        assert request.status == ApacStatus.PENDING
        assert request.requester.id == requester.id
        assert request.establishment.id == establishment.id
        assert request.authorizer is None
        assert request.justification is None
        
    def test_authorizer_cannot_create_request(self, repos, authorizer, establishment, cid, medical_procedures):
        """Authorizer role should not be able to create APAC requests."""

        with pytest.raises(PermissionDeniedException):
            create_apac_request(
                repos,
                generate_apac_request_dto(
                    authorizer,
                    establishment,
                    medical_procedures,
                    cid
                )
            )

    def test_request_rejection_from_out_of_city_requester(self, repos, requester, cid, medical_procedures):
        """A user without an active establishment will not be able to create APAC requests."""
        _city =  CreateCityUseCase(repos["city"]).execute("Engenho")
        _establishment = CreateEstablishmentUseCase(repos["establishment"], repos["city"]).execute("Mariana", "6987749", _city.id)
        apac_request_dto = generate_apac_request_dto(
            requester,
            _establishment,
            medical_procedures,
            cid
        )
        with pytest.raises(DomainException):
            create_apac_request(repos, apac_request_dto)