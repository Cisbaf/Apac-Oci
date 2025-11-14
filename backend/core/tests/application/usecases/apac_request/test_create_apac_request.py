import pytest
from apac_core.application.use_cases.apac_request_cases.create_apac_request_case import CreateApacRequestUseCase, CreateApacRequestDTO
from apac_core.application.use_cases.create_apac_data_case import CreateApacDataDTO
from apac_core.application.use_cases.create_city_case import CreateCityUseCase
from apac_core.application.use_cases.establishment_cases.create_establishment_case import CreateEstablishmentUseCase
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.exceptions import PermissionDeniedException, DomainException
from apac_core.application.use_cases.create_city_case import CreateCityUseCase, CreateCityDto
from apac_core.application.use_cases.establishment_cases.create_establishment_case import CreateEstablishmentUseCase, CreateEstablishmentDto
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.exceptions import PermissionDeniedException, DomainException

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
        request_date="2025-07-01",
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
            supervising_physician_name="Fernando Rodrigues",
            supervising_physician_cns="706000343458946",
            supervising_physician_cbo="654321",
            authorizing_physician_name="Fernando Rodrigues",
            authorizing_physician_cns="706000343458946",
            authorizing_physician_cbo="123456",
            cid_id=cid.id,
            procedure_date="2025-07-30",
            discharge_date="2025-07-31",
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
        _city =  CreateCityUseCase(
            repos["city"]
        ).execute(CreateCityDto(
            name="xxxxx",
            ibge_code="yyyyy",
            agency_name="zzzzzz"
        ))
        _establishment = CreateEstablishmentUseCase(
            repos["establishment"],
            repos["city"]
            ).execute(CreateEstablishmentDto(
                name="xxxxxx",
                cnes="zzzzzz",
                cnpj="yyyyyy",
                acronym="@@@@@",
                city_id=_city.id
            ))
        apac_request_dto = generate_apac_request_dto(
            requester,
            _establishment,
            medical_procedures,
            cid
        )
        with pytest.raises(DomainException):
            create_apac_request(repos, apac_request_dto)

    def test_adm_can_create_request(self, repos, administrator, establishment, cid, medical_procedures):
        """Requester role should be able to create APAC requests."""
        request = create_apac_request(
            repos,
            generate_apac_request_dto(
                administrator,
                establishment,
                medical_procedures,
                cid
            )
        )
        
        assert request.id == 1
        assert request.status == ApacStatus.PENDING
        assert request.requester.id == administrator.id
        assert request.establishment.id == establishment.id
        assert request.authorizer is None
        assert request.justification is None


def test_procedure_date_not_in_same_competency_month(repos, requester, establishment, cid, medical_procedures):
    """
    Deve lançar erro quando a data do procedimento NÃO estiver
    no mesmo ano e mês da request_date.
    """
    
    dto = generate_apac_request_dto(
        requester,
        establishment,
        medical_procedures,
        cid
    )

    # request_date = 2025-07-01 (fixo no helper)
    # Vamos colocar procedure_date em outro mês
    dto.apac_data.procedure_date = "2025-08-05"

    with pytest.raises(DomainException):
        create_apac_request(repos, dto)

def test_discharge_date_cannot_be_before_procedure_date(repos, requester, establishment, cid, medical_procedures):
    """
    Deve lançar erro quando a data de alta for menor que a data do procedimento.
    """

    dto = generate_apac_request_dto(
        requester,
        establishment,
        medical_procedures,
        cid
    )

    # procedure_date = 2025-07-30 (fixo no helper)
    # Vamos colocar discharge_date antes disso
    dto.apac_data.discharge_date = "2025-07-20"

    with pytest.raises(DomainException):
        create_apac_request(repos, dto)
