import pytest
from apac_core.application.implementations.apac_data_fake_repository import ApacDataFakeRepository
from apac_core.application.implementations.apac_request_fake_repository import ApacRequestFakeRepository
from apac_core.application.implementations.establishment_fake_repository import EstablishmentFakeRepository
from apac_core.application.implementations.user_fake_repository import UserFakeRepository
from apac_core.application.implementations.city_fake_repository import CityFakeRepository
from apac_core.application.implementations.cid_fake_repository import CidFakeRepository
from apac_core.application.implementations.procedure_fake_repository import ProcedureFakeRepository
from apac_core.application.implementations.procedure_record_fake_repository import ProcedureRecordFakeRepository
from apac_core.application.implementations.apac_batch_fake_repository import ApacBatchFakeRepository
from apac_core.application.use_cases.procedure_cases.create_procedure_case import CreateProcedureUseCase
from apac_core.application.use_cases.procedure_record_cases.create_procedure_record_case import CreateProcedureRecordDTO
from apac_core.application.use_cases.cid_cases.create_cid_case import CreateCidUseCase
from apac_core.application.use_cases.user_cases.create_user_case import CreateUserUseCase
from apac_core.application.use_cases.create_city_case import CreateCityUseCase
from apac_core.application.use_cases.establishment_cases.create_establishment_case import CreateEstablishmentUseCase
from apac_core.domain.entities.user_role import UserRole

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
        "apac_batch": ApacBatchFakeRepository()
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

@pytest.fixture
def administrator(repos, city):
    """Fixture creating an authorizer user."""
    return CreateUserUseCase(repos["user"], repos["city"]).execute(
        "Authorizer User",
        UserRole.ADMIN,
        city.id
    )
