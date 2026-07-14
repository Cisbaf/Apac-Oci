"""
Cenários determinísticos para o teste de caracterização (golden file) do export.

Construídos direto pelos construtores das entidades de domínio (sem passar pelos
use cases/fake repositories da application), para não depender de peças de
infraestrutura de teste que não têm relação com o export (ex.: o fixture `repos`
de conftest.py, que hoje quebra por causa de um método abstrato não implementado
em `ApacRequestFakeRepository` — ver T-007, fora do escopo da T-002).
"""
from datetime import date, datetime

from apac_core.domain.entities.apac_batch import ApacBatch
from apac_core.domain.entities.apac_data import ApacData
from apac_core.domain.entities.apac_request import ApacRequest
from apac_core.domain.entities.apac_status import ApacStatus
from apac_core.domain.entities.cid import Cid
from apac_core.domain.entities.city import City
from apac_core.domain.entities.establishment import Establishment
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.entities.procedure_record import ProcedureRecord
from apac_core.domain.entities.user import User
from apac_core.domain.entities.user_role import UserRole
from apac_core.domain.dto.medicData import MedicData
from apac_core.domain.dto.patientData import PatientData
from apac_core.domain.value_objects.cbo import CboField
from apac_core.domain.value_objects.cep import CepField
from apac_core.domain.value_objects.cns import CnsField
from apac_core.domain.value_objects.cpf import CpfField
from apac_core.domain.value_objects.validity import Validity


def build_city(name="Nova Iguaçu", ibge_code="3303500", agency_name="SECRETARIA MUNICIPAL DE NOVA IGUACU", id=1):
    return City(name=name, ibge_code=ibge_code, agency_name=agency_name, id=id)


def build_establishment(city, id=4, cnes="4507940", cnpj="29138278000705"):
    return Establishment(
        name="POLICLINICA SHOPPING NOVA IGUACU",
        cnes=cnes,
        city=city,
        cnpj=cnpj,
        acronym="POLSHG",
        is_active=True,
        id=id,
    )


def build_patient_data():
    return PatientData(
        name="EVANI BARBOSA DA SILVA",
        record_number="",
        cns=CnsField(value="898005978123294"),
        cpf=CpfField(value="22022934776"),
        birth_date=date(1973, 1, 5),
        race_color="03",
        gender="M",
        mother_name="MARINETE BARBOSA DA SILVA",
        address_street_type="081",
        address_street_name="AMERICO DE JESUS",
        address_number="199",
        address_complement="CASA 1",
        address_postal_code=CepField(value="26271132"),
        address_neighborhood="JARDIM PALMARES",
        address_city="Nova Iguaçu",
        address_state="RJ",
    )


def build_supervising_physician():
    return MedicData(
        name="DAVID DE BARROS VALENTE",
        cns=CnsField(value="700000138906208"),
        cbo=CboField(value="123456"),
    )


def build_authorizing_physician():
    return MedicData(
        name="VINICIUS DOS SANTOS AUGUSTO",
        cns=CnsField(value="704602184313922"),
        cbo=CboField(value="654321"),
    )


def build_cid():
    return Cid(code="Z848", name="História familiar de outras afecções especificadas", id=19)


def build_main_procedure():
    return Procedure(name="OCI AVALIAÇÃO CARDIOLÓGICA", code="0902010026", id=244)


def build_sub_procedure_records():
    """4 subprocedimentos, sem CBO próprio (usa o do médico supervisor)."""
    subs = [
        Procedure(name="CONSULTA MEDICA EM ATENCAO ESPECIALIZADA", code="0301010072", id=245),
        Procedure(name="ELETROCARDIOGRAMA", code="0211020036", id=246),
        Procedure(name="RADIOGRAFIA DE TORAX (PA E PERFIL)", code="0204030153", id=247),
        Procedure(name="ECOCARDIOGRAFIA TRANSTORACICA", code="0205010032", id=248),
    ]
    return [ProcedureRecord(procedure=p, quantity=1, id=132 + i) for i, p in enumerate(subs)]


def build_apac_batch(
    batch_number: str,
    city: City,
    establishment: Establishment,
    production: date,
    sub_procedures=None,
):
    """Monta um ApacBatch aprovado (pronto para export) para um cenário de teste."""
    apac_data = ApacData(
        patient_data=build_patient_data(),
        supervising_physician_data=build_supervising_physician(),
        authorizing_physician_data=build_authorizing_physician(),
        cid=build_cid(),
        procedure_date=date(production.year, production.month, 8),
        discharge_date=date(production.year, production.month, 12),
        main_procedure=build_main_procedure(),
        sub_procedures=sub_procedures or [],
        id=5,
    )

    requester = User(name="Usuario Solicitante", role=UserRole.REQUESTER, city=city, id=4)
    authorizer = User(name="Usuario Autorizador", role=UserRole.AUTHORIZER, city=city, id=5)

    apac_request = ApacRequest(
        establishment=establishment,
        requester=requester,
        apac_data=apac_data,
        request_date=date(production.year, production.month, 1),
        status=ApacStatus.APPROVED,
        updated_at=datetime(2025, 8, 11, 17, 42, 43),
        authorizer=authorizer,
        justification="",
        review_date=datetime(2025, 5, 11, 17, 46, 46),
        id=5,
    )

    return ApacBatch(
        batch_number=batch_number,
        city=city,
        validity=Validity(expire_in=date(2025, 8, 11), created_in=datetime(2025, 8, 11, 0, 0)),
        apac_request=apac_request,
        export_date=None,
        id=2,
    )
