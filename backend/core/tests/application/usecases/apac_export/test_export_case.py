from apac_core.application.use_cases.apac_request_cases.create_apac_request_case import CreateApacRequestUseCase, CreateApacRequestDTO
from apac_core.application.use_cases.apac_export_case import ApacExportCase, ApacExportDto
from apac_core.domain.entities.user_role import UserRole
from apac_core.domain.entities.apac_batch import ApacBatch
from apac_core.domain.entities.establishment import Establishment
import datetime

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

def generate_apac_request_dto(user, establishment, apac_data, request_date):
    return CreateApacRequestDTO(
        requester_id=user.id,
        establishment_id=establishment.id,
        request_date=request_date,
        apac_data=apac_data
    )

def test_generate(repos):
    today = datetime.date.today()
    production = datetime.date(2025, 5, 1)
    repo_apac_batch = repos['apac_batch']
    repo_apac_batch.apac_batchs.append(ApacBatch(**batch_fake_data))
    repo_establishment = repos['establishment']
    repo_establishment.establishments.append(Establishment(**establishment_fake_data))
    export = ApacExportCase(
        repo_apac_batch=repo_apac_batch,
        repo_establishment=repo_establishment
    ).execute(ApacExportDto(
        production=production,
        establishment_id=4,
        apac_batchs=[2]
    ))
    assert export == f"""01#APAC2025050000011810POLICLINICA SHOPPING NOVA IGUAPOLSHG29138278000705SECRETARIA MUNICIPAL DE NOVA IGUACU     M{today.strftime("%Y%m%d")}Versao 03.15   
142025053325700278252334507940202505012025050120250630003EVANI BARBOSA DA SILVA        MARINETE BARBOSA DA SILVA     081 AMERICO DE JESUS          199  CASA 1    26271132330350019730105MDAVID DE BARROS VALENTE       09020100261220250512VINICIUS DOS SANTOS AUGUSTO   000000000000000700000138906208704602184313922              45079402025050120250508M33035000101000000000000003EVANI BARBOSA DA SILVA        010    081JARDIM PALMARES                                                                  70000013890620822022934776          N
062025{production.strftime("%m")}3325700278252Z848
1320250533257002782520902010026123456000001
1320250533257002782520301010072123456000001
1320250533257002782520211020036123456000001
1320250533257002782520204030153123456000001
1320250533257002782520205010032123456000001"""

batch_fake_data = {'batch_number': '3325700278252', 'city': {'name': 'Nova Iguaçu', 'ibge_code': '3303500', 'agency_name': 'SECRETARIA MUNICIPAL DE NOVA IGUACU', 'id': 1}, 'validity': {'expire_in': datetime.date(2025, 8, 11), 'created_in': datetime.date(2025, 8, 11)},
    'apac_request': 
        {'establishment': {
            'name': 'POLICLINICA SHOPPING NOVA IGUACU', 'cnes': '4507940', 'city': {'name': 'Nova Iguaçu', 'ibge_code': '3303500', 'agency_name': 'SECRETARIA MUNICIPAL DE NOVA IGUACU', 'id': 1}, 'cnpj': '29138278000705', 'acronym': 'POLSHG', 'is_active': True, 'id': 4}, 'requester': {'name': 'Usuario Solicitante', 'role': UserRole.REQUESTER, 'city': {'name': 'Nova Iguaçu', 'ibge_code': '3303500', 'agency_name': 'SECRETARIA MUNICIPAL DE NOVA IGUACU', 'id': 1}, 'id': 4}, 'apac_data': {'patient_data': {'name': 'EVANI BARBOSA DA SILVA', 'record_number': '', 'cns': {'value': '898005978123294'}, 'cpf': {'value': '22022934776'}, 'birth_date': datetime.date(1973, 1, 5), 'race_color': '03', 'gender': 'M', 'mother_name': 'MARINETE BARBOSA DA SILVA', 'address_street_type': '081', 'address_street_name': 'AMERICO DE JESUS', 'address_number': '199', 'address_complement': 'CASA 1', 'address_postal_code': {'value': '26271132'}, 'address_neighborhood': 'JARDIM PALMARES', 'address_city': 'Nova Iguaçu', 'address_state': 'RJ'}, 'supervising_physician_data': {'name': 'DAVID DE BARROS VALENTE', 'cns': {'value': '700000138906208'}, 'cbo': {'value': '123456'}}, 'authorizing_physician_data': {'name': 'VINICIUS DOS SANTOS AUGUSTO', 'cns': {'value': '704602184313922'}, 'cbo': {'value': '654321'}}, 'cid': {'code': 'Z848', 'name': 'História familiar de outras afecções especificadas', 'procedure': {'name': 'OCI AVALIAÇÃO CARDIOLÓGICA', 'code': '0902010026', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [{'name': 'CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA', 'code': '0301010072', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 673000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 673000, tzinfo=datetime.timezone.utc), 'id': 245}, {'name': 'ELETROCARDIOGRAMA', 'code': '0211020036', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 677000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 677000, tzinfo=datetime.timezone.utc), 'id': 246}, {'name': 'RADIOGRAFIA DE TÓRAX (PA E PERFIL)', 'code': '0204030153', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 680000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 680000, tzinfo=datetime.timezone.utc), 'id': 247}, {'name': 'ECOCARDIOGRAFIA TRANSTORÁCICA', 'code': '0205010032', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 684000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 684000, tzinfo=datetime.timezone.utc), 'id': 248}], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 669000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 669000, tzinfo=datetime.timezone.utc), 'id': 244}, 'id': 19}, 'procedure_date': datetime.date(2025, 5, 8), 'discharge_date': datetime.date(2025, 5, 12), 'main_procedure': {'name': 'OCI AVALIAÇÃO CARDIOLÓGICA', 'code': '0902010026', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [{'name': 'CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA', 'code': '0301010072', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 673000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 673000, tzinfo=datetime.timezone.utc), 'id': 245}, {'name': 'ELETROCARDIOGRAMA', 'code': '0211020036', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 677000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 677000, tzinfo=datetime.timezone.utc), 'id': 246}, {'name': 'RADIOGRAFIA DE TÓRAX (PA E PERFIL)', 'code': '0204030153', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 680000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 680000, tzinfo=datetime.timezone.utc), 'id': 247}, {'name': 'ECOCARDIOGRAFIA TRANSTORÁCICA', 'code': '0205010032', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 684000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 684000, tzinfo=datetime.timezone.utc), 'id': 248}], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 669000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 669000, tzinfo=datetime.timezone.utc), 'id': 244}, 'sub_procedures': [{'procedure': {'name': 'CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA', 'code': '0301010072', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 673000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 673000, tzinfo=datetime.timezone.utc), 'id': 245}, 'quantity': 1, 'id': 132}, {'procedure': {'name': 'ELETROCARDIOGRAMA', 'code': '0211020036', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 677000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 677000, tzinfo=datetime.timezone.utc), 'id': 246}, 'quantity': 1, 'id': 133}, {'procedure': {'name': 'RADIOGRAFIA DE TÓRAX (PA E PERFIL)', 'code': '0204030153', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 680000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 680000, tzinfo=datetime.timezone.utc), 'id': 247}, 'quantity': 1, 'id': 134}, {'procedure': {'name': 'ECOCARDIOGRAFIA TRANSTORÁCICA', 'code': '0205010032', 'description': None, 'is_active': True, 'parent': None, 'sub_procedures': [], 'created_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 684000, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2025, 6, 6, 15, 35, 32, 684000, tzinfo=datetime.timezone.utc), 'id': 248}, 'quantity': 1, 'id': 135}], 'id': 5}, 'request_date': datetime.date(2025, 5, 1), 'status': 'approved', 'updated_at': datetime.datetime(2025, 8, 11, 17, 42, 43, 721965, tzinfo=datetime.timezone.utc), 'authorizer': {'name': 'Usuario Autorizador', 'role': UserRole.AUTHORIZER, 'city': {'name': 'Nova Iguaçu', 'ibge_code': '3303500', 'agency_name': 'SECRETARIA MUNICIPAL DE NOVA IGUACU', 'id': 1}, 'id': 5}, 'justification': '', 'review_date': datetime.datetime(2025, 5, 11, 17, 46, 46, tzinfo=datetime.timezone.utc), 'id': 5}, 'export_date': None, 'id': 2}

establishment_fake_data = {
    'name': 'POLICLINICA SHOPPING NOVA IGUACU', 'cnes': '4507940', 'city': {'name': 'Nova Iguaçu', 'ibge_code': '3303500', 'agency_name': 'SECRETARIA MUNICIPAL DE NOVA IGUACU', 'id': 1}, 'cnpj': '29138278000705', 'acronym': 'POLSHG', 'is_active': True, 'id': 4}