from pydantic import BaseModel, Field, conlist, field_validator # Importar field_validator
from datetime import datetime, date, timedelta # Importar timedelta
from typing import Optional, List, Dict
import re

# --- Constantes e Mapeamentos ---
# Mapeamento de Sexo
GENDER_MAP = {"M": "M", "F": "F", "m": "M", "f": "F", "Masculino": "M", "Feminino": "F"}

# Mapeamento de Raça/Cor (simplificado, idealmente uma tabela completa)
RACE_MAP = {
    "BRANCA": "01",
    "PRETA": "02",
    "PARDA": "03",
    "AMARELA": "04",
    "INDIGENA": "05",
    "NAO INFORMADA": "99", # Assumindo um código para não informada
    None: "99" # Default para quando não houver
}

# Códigos IBGE (Exemplos para RJ e Nova Iguaçu)
UF_RJ_IBGE = "33"
MUN_NOVA_IGUACU_IBGE = "3303500" # Código IBGE para Nova Iguaçu

# Tipo de Atendimento (Assumindo um padrão para risco cirúrgico ambulatorial)
# 01 = Ambulatorial, 02 = Internação, 03 = SADT, etc.
# Usaremos 01 (Ambulatorial) como um valor padrão razoável para avaliação de risco.
DEFAULT_APA_TIPATE = "01"

# Tipo de APAC
# 1 = Inicial, 2 = Continuidade, 3 = Única
DEFAULT_APA_TIPAPAC = "1" # Assumindo que a maioria será inicial para risco cirúrgico

# --- Funções Auxiliares para Formatação ---
def format_field(value, length: int, align: str = 'left', pad_char: str = ' '):
    """Formata um valor para uma string de tamanho fixo com preenchimento."""
    if value is None:
        value = ""
    s_value = str(value)
    if len(s_value) > length:
        return s_value[:length]
    if align == 'left':
        return s_value.ljust(length, pad_char)
    else:  # right align, typically for numbers with '0' padding
        return s_value.rjust(length, pad_char)


def calculate_competence(dt: date) -> str:
    """Calcula a competência (AAAAMM) de uma data."""
    return dt.strftime("%Y%m")

def get_last_day_of_month(year: int, month: int) -> date:
    """Retorna o último dia do mês para um dado ano e mês."""
    if month == 12:
        return date(year, month, 31)
    return date(year, month + 1, 1) - timedelta(days=1)


# --- DTOs para o Layout APAC ---

class Procedimento(BaseModel):
    code: str
    cbo: str
    quantity: int
    cid_principal: Optional[str] = None # pap_CIDP (065–068)
    cid_secundario: Optional[str] = None # pap_CIDS (069-072)
    cgc: Optional[str] = None # pap_CGC (045-058)
    nf: Optional[str] = None # pap_NF (059-064)
    clf: Optional[str] = None # pap_CLF (073)
    srv: Optional[str] = None # pap_SRV (074)
    equipe_seq: Optional[str] = None # pap_equipe_Seq (075-076)
    equipe_area: Optional[str] = None # pap_equipe_Area (077-078)
    cnes_terciario: Optional[str] = None # pap_cnes_terc (079-085)
    # Outros campos pap_ conforme PDF, muitos são opcionais ou ficam em branco

class ApaVariavel06LaudoGeral(BaseModel):
    """
    Parte Variável para Laudo Geral (Identificador '06')
    Campos específicos para o laudo médico geral.
    """
    identificador: str = Field("06", pattern=r"^06$")
    cod_apresentacao: str # Ex: '001' (003-005)
    dt_emissao_laudo: date # (006-013) AAAAMMDD
    identificador_laudo: str # Ex: 'z136' do exemplo (014-018)
    texto_laudo: Optional[str] = None # (019-368)
    # ... outros campos do registro 06 conforme layout completo

    def to_apac_string(self, competence: str, apac_number: str, cnes_prestador: str) -> str:
        s = ""
        s += format_field(self.identificador, 2, 'left', ' ')
        s += format_field(competence, 6, 'left', ' ')
        s += format_field(cnes_prestador, 7, 'right', '0') # Ajustar conforme o CNES do prestador
        s += format_field(apac_number, 13, 'left', ' ')
        s += format_field(self.identificador_laudo, 5, 'left', ' ') # 'z136' no exemplo
        s += format_field(self.dt_emissao_laudo.strftime("%Y%m%d"), 8, 'left', ' ')

        # Adaptando para o tamanho total do registro do exemplo (522 posições)
        # O exemplo fornecido para 06 é muito curto, não segue as 522 posições do layout completo.
        # "062025053325700278241z136     20250509" -> 41 caracteres.
        # No layout oficial, o registro 06 (Laudo Geral) tem 522 posições.
        # Vou preencher com espaços o restante para atingir 522 posições, como se fosse um registro completo.
        return format_field(s, 522, 'left', ' ')


class ApaVariavel17PreBariatrica(BaseModel):
    """
    Parte Variável para Acompanhamento PRÉ CIRURGIA BARIATRICA (Identificador '17')
    Contém o campo apa_risco_cir (Avaliação do risco cirúrgico).
    """
    identificador: str = Field("17", pattern=r"^17$")
    apa_risco_cir: str = Field(..., max_length=1) # Risco cirúrgico (A, B, C, D)
    # ... outros campos do registro 17 conforme layout completo

    def to_apac_string(self, competence: str, apac_number: str, cnes_prestador: str) -> str:
        s = ""
        s += format_field(self.identificador, 2, 'left', ' ')
        s += format_field(competence, 6, 'left', ' ')
        s += format_field(cnes_prestador, 7, 'right', '0')
        s += format_field(apac_number, 13, 'left', ' ')
        s += format_field(self.apa_risco_cir, 1, 'left', ' ')
        # No layout real, o registro 17 tem mais campos. O exemplo não mostra 17.
        # Preencher o restante com espaços até o comprimento total do registro 17 (522 posições, igual ao 06)
        return format_field(s, 522, 'left', ' ')


class ApacBody(BaseModel):
    """Corpo principal da APAC (Registro '14')."""
    identificador: str = Field("14", pattern=r"^14$")
    patient_name: str = Field(..., max_length=30)
    patient_mother_name: str = Field(..., max_length=30)
    patient_address_street_type: str = Field(..., max_length=15) # Tipo logradouro, ex: RUA, AV.
    patient_address_street_name: str = Field(..., max_length=15) # Nome logradouro
    patient_address_number: str = Field(..., max_length=5)
    patient_address_complement: Optional[str] = Field(None, max_length=10)
    patient_address_postal_code: str = Field(..., min_length=8, max_length=8)
    patient_address_city: str # Usado para derivar o código IBGE
    patient_birth_date: date # Será convertida para AAAAMMDD
    patient_gender: str = Field(..., max_length=1) # M/F
    medic_name: str = Field(..., max_length=30) # Nome do médico responsável (apa_nomeresp)
    main_procedure_code: str = Field(..., max_length=10) # apa_codprinc
    authorizer_name: str = Field(..., max_length=30) # apa_nomediretor
    patient_cns: str = Field(..., min_length=15, max_length=15)
    medic_cns: str = Field(..., min_length=15, max_length=15)
    authorizer_cns: str = Field(..., min_length=15, max_length=15) # CNS do autorizador (apa_cnsdir)
    patient_chart_number: Optional[str] = Field(None, max_length=15) # apa_npront
    request_date: Optional[date] = None # apa_datsol
    authorization_date: Optional[date] = None # apa_dataut
    issuer_code: Optional[str] = Field(None, max_length=5) # apa_codemis
    # apa_carate (Caráter de Atendimento): 'E' Eletivo, 'U' Urgência/Emergência
    # Portaria 719/2007 - Art 2, I, c. Usar 'E' para risco cirurgico eletivo.
    character_of_service: str = Field('E', max_length=1)
    patient_race: Optional[str] = None # apa_raca (código)
    # Outros CNSs, como apa_cnsexec (CNS do Executante)
    executing_medic_cns: Optional[str] = Field(None, min_length=15, max_length=15) # apa_cnsexec
    patient_cpf: Optional[str] = Field(None, min_length=11, max_length=14) # apa_cpfpcnte, pode ser 11 (CPF) ou 14 (CNPJ)
    patient_ethnic_group: Optional[str] = Field(None, max_length=4) # apa_etnia
    patient_birth_place: Optional[str] = Field(None, max_length=7) # apa_nascpcnte (código IBGE)
    # Dados de contato
    patient_ddd: Optional[str] = Field(None, max_length=3) # apa_dddtelcontato
    patient_phone: Optional[str] = Field(None, max_length=10) # apa_telcontato
    patient_email: Optional[str] = Field(None, max_length=50) # apa_email
    # Endereço Bairro e Código do Logradouro
    patient_address_neighborhood: Optional[str] = Field(None, max_length=30) # apa_bairro
    patient_address_code_street: Optional[str] = Field(None, max_length=5) # apa_cdlogr

    # CID Principal da APAC (para o laudo)
    cid_principal_diag: Optional[str] = Field(None, max_length=4) # apa_CID_A
    cid_causa_associada: Optional[str] = Field(None, max_length=4) # apa_CID_C_A

    # Motivo de Saída (Portaria 719/2007)
    # Valores: 01=Cura, 02=Melhora, 03=Óbito, 04=Óbito com AP, 05=Transferência, 06=Ausência, 07=Evasão, 08=Piora, 09=Outros
    # Para risco cirúrgico sem "saída", pode-se usar branco ou um código específico para "não aplicável" se houver.
    # Assumindo que para um risco cirúrgico que não resultou em "saída" explícita, o campo pode ficar em branco.
    exit_reason: Optional[str] = Field(None, max_length=2)
    exit_date: Optional[date] = None # apa_dtobitoalta (condicional)

    # Campos de controle internos/sequenciais da APAC
    apac_number: Optional[str] = None # Definido na função de exportação

    # Partes variáveis (opcionais, serão geradas se presentes)
    laudo_geral: Optional[ApaVariavel06LaudoGeral] = None
    pre_bariatrica: Optional[ApaVariavel17PreBariatrica] = None

    @field_validator('patient_gender', mode='before')
    @classmethod
    def validate_gender(cls, v):
        if v is None:
            return "M" # Default para Masculino se não informado
        gender_code = GENDER_MAP.get(str(v).upper(), "M") # Default para M se não mapeado
        return gender_code

    @field_validator('patient_race', mode='before')
    @classmethod
    def validate_race(cls, v):
        return RACE_MAP.get(str(v).upper() if v else None, "99")

    @property
    def full_patient_address(self):
        """Combina tipo e nome do logradouro para uso no campo apa_logpcnte."""
        type_part = format_field(self.patient_address_street_type, 15, 'left', ' ')
        name_part = format_field(self.patient_address_street_name, 15, 'left', ' ')
        return (type_part + name_part)[:30] # Limita a 30 caracteres para o campo apa_logpcnte

    @property
    def apa_dtiinval(self) -> date:
        # Data inicial de validade: 1º dia do mês da competência de geração
        # Ajustado para usar a data de processamento como base, ou a data atual se não definida
        # Para APACs, a validade inicial geralmente é a competência do procedimento
        return datetime.now().replace(day=1).date()

    @property
    def apa_dtfimval(self) -> date:
        # Data final de validade: Último dia do mês, 3 competências após a inicial
        initial_date = self.apa_dtiinval
        year = initial_date.year
        month = initial_date.month + 3
        if month > 12:
            year += (month - 1) // 12
            month = (month - 1) % 12 + 1
        return get_last_day_of_month(year, month)

    def to_apac_string(self, competence: str, apac_number: str, cnes_prestador: str) -> str:
        s = ""
        s += format_field(self.identificador, 2, 'left', ' ')
        s += format_field(competence, 6, 'left', ' ')
        s += format_field(apac_number, 13, 'left', ' ')
        s += format_field(UF_RJ_IBGE, 2, 'left', ' ') # apa_coduf
        s += format_field(cnes_prestador, 7, 'right', '0') # apa_codcnes
        s += format_field(datetime.now().strftime("%Y%m%d"), 8, 'left', ' ') # apa_pr (Data de processamento)
        s += format_field(self.apa_dtiinval.strftime("%Y%m%d"), 8, 'left', ' ') # apa_dtiinval
        s += format_field(self.apa_dtfimval.strftime("%Y%m%d"), 8, 'left', ' ') # apa_dtfimval
        s += format_field(DEFAULT_APA_TIPATE, 2, 'left', ' ') # apa_tipate
        s += format_field(DEFAULT_APA_TIPAPAC, 1, 'left', ' ') # apa_tipapac
        s += format_field(self.patient_name, 30, 'left', ' ') # apa_nomepcnte
        s += format_field(self.patient_mother_name, 30, 'left', ' ') # apa_nomemae
        s += format_field(self.full_patient_address, 30, 'left', ' ') # apa_logpcnte
        s += format_field(self.patient_address_number, 5, 'left', ' ') # apa_numpcnte
        s += format_field(self.patient_address_complement or "", 10, 'left', ' ') # apa_cplpcnte
        s += format_field(self.patient_address_postal_code, 8, 'left', ' ') # apa_ceppcnte
        s += format_field(MUN_NOVA_IGUACU_IBGE, 7, 'left', ' ') # apa_munpcnte (Nova Iguaçu)
        s += format_field(self.patient_birth_date.strftime("%Y%m%d"), 8, 'left', ' ') # apa_datanascim
        s += format_field(self.patient_gender, 1, 'left', ' ') # apa_sexopcnte
        s += format_field(self.medic_name, 30, 'left', ' ') # apa_nomeresp
        s += format_field(self.main_procedure_code, 10, 'left', ' ') # apa_codprinc
        s += format_field(self.exit_reason or "", 2, 'left', ' ') # apa_motsaida
        s += format_field(self.exit_date.strftime("%Y%m%d") if self.exit_date else "", 8, 'left', ' ') # apa_dtobitoalta
        s += format_field(self.authorizer_name, 30, 'left', ' ') # apa_nomediretor
        s += format_field(self.patient_cns, 15, 'left', ' ') # apa_cnspct
        s += format_field(self.medic_cns, 15, 'left', ' ') # apa_cnsres
        s += format_field(self.authorizer_cns, 15, 'left', ' ') # apa_cnsdir

        # Outros campos até 522
        # apa_CID_A (267-270) -> Posições 424-427 (na verdade é 425-428 no PDF, contando de 1)
        # Vamos seguir a ordem do PDF para evitar erros de mapeamento de posição
        # O campo 267 do PDF corresponde à 266 no índice 0
        s += format_field(self.patient_chart_number or "", 15, 'left', ' ') # apa_npront (312-326)
        s += format_field(self.request_date.strftime("%Y%m%d") if self.request_date else "", 8, 'left', ' ') # apa_datsol (327-334)
        s += format_field(self.authorization_date.strftime("%Y%m%d") if self.authorization_date else "", 8, 'left', ' ') # apa_dataut (335-342)
        s += format_field(self.issuer_code or "", 5, 'left', ' ') # apa_codemis (343-347)
        s += format_field(self.character_of_service, 1, 'left', ' ') # apa_carate (348)
        s += format_field(self.patient_race, 2, 'left', ' ') # apa_raca (349-350)
        s += format_field(self.executing_medic_cns or "", 15, 'left', ' ') # apa_cnsexec (351-365)
        s += format_field(self.patient_cpf or "", 14, 'left', ' ') # apa_cpfpcnte (366-379)
        s += format_field(self.patient_ethnic_group or "", 4, 'left', ' ') # apa_etnia (380-383)
        s += format_field(self.patient_birth_place or "", 7, 'left', ' ') # apa_nascpcnte (384-390)
        s += format_field(self.patient_address_code_street or "", 5, 'left', ' ') # apa_cdlogr (391-395)
        s += format_field(self.patient_address_neighborhood or "", 30, 'left', ' ') # apa_bairro (396-425)
        s += format_field(self.cid_principal_diag or "", 4, 'left', ' ') # apa_CID_A (426-429)
        s += format_field(self.cid_causa_associada or "", 4, 'left', ' ') # apa_CID_C_A (430-433)
        s += format_field(self.patient_ddd or "", 3, 'left', ' ') # apa_dddtelcontato (434-436)
        s += format_field(self.patient_phone or "", 10, 'left', ' ') # apa_telcontato (437-446)
        s += format_field(self.patient_email or "", 50, 'left', ' ') # apa_email (447-496)

        # Preencher o restante com espaços até 522 posições
        # A partir da posição 497, até 522, são campos opcionais ou reservados,
        # como apa_apacant, apa_versao, apa_coduf2. No exemplo, ficam em branco.
        s += " " * (522 - len(s)) # Preenche com espaços até o final do registro

        return s

class ApacProcedimentoRecord(BaseModel):
    """Registro de Procedimentos (Registro '13')."""
    identificador: str = Field("13", pattern=r"^13$")
    procedure_code: str = Field(..., max_length=10) # pap_codproc
    cbo_executing: str = Field(..., max_length=6) # pap_cbo
    quantity_produced: int = Field(..., ge=0) # pap_qtdprod
    # Demais campos são opcionais e preenchidos com espaços/zeros se não informados
    pap_cgc: Optional[str] = Field(None, max_length=14)
    pap_nf: Optional[str] = Field(None, max_length=6)
    pap_cidp: Optional[str] = Field(None, max_length=4) # Principal (somente medicamentos)
    pap_cids: Optional[str] = Field(None, max_length=4) # Secundário
    pap_clf: Optional[str] = Field(None, max_length=1)
    pap_srv: Optional[str] = Field(None, max_length=1)
    pap_equipe_seq: Optional[str] = Field(None, max_length=2)
    pap_equipe_area: Optional[str] = Field(None, max_length=2)
    pap_cnes_terc: Optional[str] = Field(None, max_length=7)

    def to_apac_string(self, competence: str, apac_number: str, cnes_prestador: str) -> str:
        s = ""
        s += format_field(self.identificador, 2, 'left', ' ')
        s += format_field(competence, 6, 'left', ' ')
        s += format_field(cnes_prestador, 7, 'right', '0') # Adicionado cnes_prestador para consistência
        s += format_field(apac_number, 13, 'left', ' ')
        s += format_field(self.procedure_code, 10, 'left', ' ') # pap_codproc
        s += format_field(self.cbo_executing, 6, 'left', ' ') # pap_cbo
        s += format_field(self.quantity_produced, 7, 'right', '0') # pap_qtdprod
        s += format_field(self.pap_cgc or "", 14, 'left', ' ') # pap_CGC
        s += format_field(self.pap_nf or "", 6, 'left', ' ') # pap_NF
        s += format_field(self.pap_cidp or "", 4, 'left', ' ') # pap_CIDP
        s += format_field(self.pap_cids or "", 4, 'left', ' ') # pap_CIDS
        s += format_field(self.pap_clf or "", 1, 'left', ' ') # pap_CLF
        s += format_field(self.pap_srv or "", 1, 'left', ' ') # pap_SRV
        s += format_field(self.pap_equipe_seq or "", 2, 'left', ' ') # pap_equipe_Seq
        s += format_field(self.pap_equipe_area or "", 2, 'left', ' ') # pap_equipe_Area
        s += format_field(self.pap_cnes_terc or "", 7, 'left', ' ') # pap_cnes_terc
        # Preencher o restante com espaços até 522 posições (comprimento total do registro 13)
        # O registro 13 tem 522 posições no layout oficial.
        s += " " * (522 - len(s)) # Preenche com espaços até o final do registro
        return s
    
class ApacHeader:
    """Cabeçalho do arquivo APAC (Registro '01')."""
    def __init__(
        self,
        origin_organization_name: str,
        origin_organization_acronym: str,
        provider_cnpj_cpf: str,
        destination_organization_name: str,
        destination_indicator: str,
        layout_version: str,
        competence: Optional[str] = '',  # AAAAMM
        apac_count: int = 0,  # quantidade de APACs
        control_field: str = '',  # campo de controle
        generation_date: Optional[date] = None,  # AAAAMMDD
    ):
        # fixed fields
        self.header_indicator = '01'
        self.file_identifier = '#APAC'
        # dynamic
        self.origin_organization_name = origin_organization_name
        self.origin_organization_acronym = origin_organization_acronym
        self.provider_cnpj_cpf = provider_cnpj_cpf
        self.destination_organization_name = destination_organization_name
        self.destination_indicator = destination_indicator
        self.layout_version = layout_version
        self.competence = competence or ''
        self.apac_count = apac_count
        self.control_field = control_field or ''
        self.generation_date = generation_date
        self._validate()

    def _validate(self):
        assert re.fullmatch(r"01" , self.header_indicator)
        assert re.fullmatch(r"#APAC", self.file_identifier)
        assert re.fullmatch(r"[ME]", self.destination_indicator)
        assert len(self.origin_organization_name) <= 30
        assert len(self.origin_organization_acronym) <= 6
        assert len(self.provider_cnpj_cpf) <= 14
        assert len(self.destination_organization_name) <= 40
        assert len(self.layout_version) <= 15
        if self.competence:
            assert re.fullmatch(r"\d{6}", self.competence)
        if self.generation_date:
            # date instance ok
            pass

    def to_apac_string(self) -> str:
        s = ''
        s += format_field(self.header_indicator, 2)
        s += format_field(self.file_identifier, 5)
        s += format_field(self.competence, 6)
        s += format_field(self.apac_count, 6, 'right', '0')
        s += format_field(self.control_field, 4)
        s += format_field(self.origin_organization_name, 30)
        s += format_field(self.origin_organization_acronym, 6)
        s += format_field(self.provider_cnpj_cpf, 14, 'right', '0')
        s += format_field(self.destination_organization_name, 40)
        s += format_field(self.destination_indicator, 1)
        s += format_field(
            self.generation_date.strftime("%Y%m%d") if self.generation_date else '',
            8
        )
        s += format_field(self.layout_version, 15)
        # CRLF at end
        s += '\r\n'
        return s


class ApacRecord(BaseModel):
    """Representa uma APAC completa, incluindo corpo e procedimentos associados."""
    body: ApacBody
    procedures: List[ApacProcedimentoRecord] = Field(default_factory=list)

    # Note: Variable parts (06, 17) are part of ApacBody for simplicity in this structure.
    # The export function will check for their presence.

class ApacExportData(BaseModel):
    """Modelo de entrada do JSON (simplificado com campos essenciais)."""
    # Dados do estabelecimento
    establishment_name: str
    establishment_cnes: str # 8 dígitos no JSON, 7 no APAC
    
    # Dados do paciente
    patient_name: str
    patient_mother_name: str
    patient_birth_date: date # <<-- ALTERADO PARA 'date'
    patient_gender: str
    patient_cns: str
    patient_cpf: Optional[str] = None
    patient_race: Optional[str] = None
    
    # Endereço do paciente
    patient_address_street_type: str
    patient_address_street_name: str
    patient_address_number: str
    patient_address_complement: Optional[str] = None
    patient_address_postal_code: str
    patient_address_city: str
    patient_address_neighborhood: Optional[str] = None
    patient_address_code_street: Optional[str] = None

    # Dados do médico
    medic_name: str
    medic_cns: str
    medic_cbo: str
    executing_medic_cns: Optional[str] = None # Para pap_cnsexec

    # Dados do autorizador
    authorizer_name: str
    authorizer_cns: str

    # Procedimento principal da APAC
    main_procedure: Dict[str, str] # {"code": "0902010026"}

    # Sub-procedimentos (listagem de procedimentos executados)
    sub_procedures: List[Dict] # Cada dict deve ter "code", "quantity", etc.

    # Data do procedimento (para competência)
    procedure_date: str # YYYYMMDD, ex: 20250611

    # Campos específicos para as partes variáveis, se aplicável
    # Exemplo para Laudo Geral (06)
    laudo_geral_id: Optional[str] = None # Ex: 'z136'
    laudo_geral_data_emissao: Optional[date] = None # <<-- ALTERADO PARA 'date'
    # Exemplo para Pré-Bariátrica (17)
    risco_cirurgico: Optional[str] = None # 'A', 'B', 'C', 'D'

    # Campos opcionais para o corpo da APAC
    patient_chart_number: Optional[str] = None
    request_date: Optional[date] = None # <<-- ALTERADO PARA 'date'
    authorization_date: Optional[date] = None # <<-- ALTERADO PARA 'date'
    issuer_code: Optional[str] = None
    character_of_service: Optional[str] = None # 'E' ou 'U'
    cid_principal_diag: Optional[str] = None
    cid_causa_associada: Optional[str] = None
    patient_ethnic_group: Optional[str] = None
    patient_birth_place: Optional[str] = None
    patient_ddd: Optional[str] = None
    patient_phone: Optional[str] = None
    patient_email: Optional[str] = None
    exit_reason: Optional[str] = None
    exit_date: Optional[date] = None # <<-- ALTERADO PARA 'date'


    # Usar field_validator e passar 'field_name' para que Pydantic saiba qual campo está sendo validado.
    @field_validator('patient_birth_date', 'request_date', 'authorization_date', 'laudo_geral_data_emissao', 'exit_date', mode='before')
    @classmethod
    def parse_date_strings(cls, v):
        if isinstance(v, date):
            return v
        if isinstance(v, str) and v:
            if len(v) == 8 and v.isdigit(): # YYYYMMDD
                return datetime.strptime(v, "%Y%m%d").date()
            elif len(v) == 10 and (v[2] == '/' and v[5] == '/'): # DD/MM/AAAA
                return datetime.strptime(v, "%d/%m/%Y").date()
        return None # Retorna None se o formato não for reconhecido ou vazio

    @field_validator('patient_address_postal_code', mode='before')
    @classmethod
    def validate_postal_code(cls, v):
        if v and isinstance(v, str) and '-' in v:
            return v.replace('-', '')
        return v
    
    @field_validator('patient_cns', 'medic_cns', 'authorizer_cns', 'executing_medic_cns', mode='before')
    @classmethod
    def clean_cns(cls, v):
        if v and isinstance(v, str):
            return v.replace(' ', '').replace('-', '') # Remove espaços e hífens
        return v

    @field_validator('patient_cpf', mode='before')
    @classmethod
    def clean_cpf(cls, v):
        if v and isinstance(v, str):
            return v.replace('.', '').replace('-', '').replace('/', '')
        return v

    @field_validator('establishment_cnes', mode='before')
    @classmethod
    def truncate_cnes(cls, v):
        if v and isinstance(v, str) and len(v) > 7:
            return v[:7] # Trunca para 7 dígitos se tiver 8 ou mais
        return v


# --- Função de Exportação para APAC Magnético ---
import os

def generate_apac_magnetico_file(
    data: ApacExportData,
    config: dict,
    output_filepath: str,
    apac_sequence_start: int = 1
) -> List[str]:
    """
    Gera um arquivo APAC Magnético (.txt) a partir dos dados fornecidos.

    Args:
        data (ApacExportData): DTO com os dados extraídos do JSON.
        config (dict): Dicionário de configurações para campos constantes/personalizados, como:
                       - 'origin_organization_acronym': Sigla do órgão de origem (cbc-sgl)
                       - 'provider_cnpj_cpf': CNPJ/CPF do prestador (cbc-cgccpf)
                       - 'destination_organization_name': Nome do órgão de destino (cbc-dst)
                       - 'destination_indicator': Indicador de destino 'M' ou 'E' (cbc-dst-in)
                       - 'layout_version': Versão do layout (cbc_versao, ex: "02.37")
        output_filepath (str): Caminho completo para o arquivo de saída (.txt).
        apac_sequence_start (int): Número inicial para a sequência das APACs no lote.

    Returns:
        List[str]: Lista de strings representando as linhas do arquivo gerado.
    """
    lines = []
    current_date = datetime.now().date()
    # A competência deve vir da data do procedimento, conforme o JSON
    competence_str = data.parse_date_strings(data.procedure_date).strftime("%Y%m") # Comp. do procedimento

    apac_number_counter = apac_sequence_start

    # --- 1. Preparar ApacBody ---
    apac_body_data = ApacBody(
        patient_name=data.patient_name,
        patient_mother_name=data.patient_mother_name,
        patient_address_street_type=data.patient_address_street_type,
        patient_address_street_name=data.patient_address_street_name,
        patient_address_number=data.patient_address_number,
        patient_address_complement=data.patient_address_complement,
        patient_address_postal_code=data.patient_address_postal_code,
        patient_address_city=data.patient_address_city,
        patient_birth_date=data.patient_birth_date,
        patient_gender=data.patient_gender,
        medic_name=data.medic_name,
        main_procedure_code=data.main_procedure["code"],
        authorizer_name=data.authorizer_name,
        patient_cns=data.patient_cns,
        medic_cns=data.medic_cns,
        authorizer_cns=data.authorizer_cns,
        patient_chart_number=data.patient_chart_number,
        request_date=data.request_date,
        authorization_date=data.authorization_date,
        issuer_code=data.issuer_code,
        character_of_service=data.character_of_service or 'E', # Default para Eletivo
        patient_race=data.patient_race,
        executing_medic_cns=data.executing_medic_cns,
        patient_cpf=data.patient_cpf,
        patient_ethnic_group=data.patient_ethnic_group,
        patient_birth_place=data.patient_birth_place,
        patient_ddd=data.patient_ddd,
        patient_phone=data.patient_phone,
        patient_email=data.patient_email,
        patient_address_neighborhood=data.patient_address_neighborhood,
        patient_address_code_street=data.patient_address_code_street,
        cid_principal_diag=data.cid_principal_diag,
        cid_causa_associada=data.cid_causa_associada,
        exit_reason=data.exit_reason,
        exit_date=data.exit_date
    )
    
    # Adicionar partes variáveis se os dados existirem
    if data.laudo_geral_id and data.laudo_geral_data_emissao:
        apac_body_data.laudo_geral = ApaVariavel06LaudoGeral(
            cod_apresentacao="001", # Exemplo de código
            dt_emissao_laudo=data.laudo_geral_data_emissao,
            identificador_laudo=data.laudo_geral_id
        )
    if data.risco_cirurgico:
        apac_body_data.pre_bariatrica = ApaVariavel17PreBariatrica(
            apa_risco_cir=data.risco_cirurgico
        )

    # --- 2. Preparar ApacProcedimentoRecord(s) ---
    procedure_records = []
    total_procedures_sum = 0
    # Adicionando o código do procedimento principal para o cálculo do campo de controle
    # O campo de controle soma 'código de *todos* os procedimentos + quantidade + número da APAC.'
    # Então o main_procedure_code do corpo da APAC também deve ser incluído.
    total_procedures_sum += int(data.main_procedure["code"])

    for i, sub_proc in enumerate(data.sub_procedures):
        proc_record = ApacProcedimentoRecord(
            procedure_code=sub_proc.get("code", ""),
            cbo_executing=data.medic_cbo, # Usar CBO do médico executante
            quantity_produced=sub_proc.get("quantity", 0),
            pap_cidp=sub_proc.get("pap_cidp"),
            pap_cids=sub_proc.get("pap_cids"),
            pap_cgc=sub_proc.get("pap_cgc"),
            pap_nf=sub_proc.get("pap_nf"),
            pap_clf=sub_proc.get("pap_clf"),
            pap_srv=sub_proc.get("pap_srv"),
            pap_equipe_seq=sub_proc.get("pap_equipe_seq"),
            pap_equipe_area=sub_proc.get("pap_equipe_area"),
            pap_cnes_terc=sub_proc.get("pap_cnes_terc")
        )
        procedure_records.append(proc_record)
        total_procedures_sum += int(proc_record.procedure_code) + proc_record.quantity_produced # Para cálculo do campo de controle

    # --- Iterar sobre cada APAC para gerar os registros ---
    apac_strings = []
    # O número da APAC no exemplo de saída tem 13 dígitos.
    # O formato "0000000000011" (12 digitos + 1 verificador).
    # Vamos assumir que o último dígito é o verificador para a soma de controle.
    # No exemplo de saída, o número da APAC é '278241' (parte final). Ele vem depois do CNES.
    # '3325700278241' onde '3325700' é o CNES e '278241' é parte da APAC.
    # Isso indica que o apa_num (009–021) é o número da APAC, 13 dígitos.
    # Ex: '0000000000011'
    # Vamos usar apac_number_counter para gerar os 12 primeiros e adicionar um '1' simples como verificador.
    # Ou, para ser mais fiel ao exemplo '278241', vamos criar um número fictício de 13 dígitos para o teste.
    
    # Para o exemplo, vamos gerar um número de APAC de 13 dígitos, onde os últimos 6 são o contador
    # e os primeiros 7 são um prefixo fixo (ex: para o prestador/unidade).
    # O exemplo tem '278241' para o primeiro, '278340' para o segundo e '278252' para o terceiro.
    # Isso sugere um número de APAC que é gerado internamente e não é apenas um contador simples.
    # Para simplicidade, vou criar um APAC_NUMBER fixo para este exemplo,
    # mas em produção, isso viria de uma sequência.

    # Usando um valor fixo para apac_number_base para simular o exemplo fornecido
    # A base '278241' aparece no exemplo, vamos simular isso para um apac_number de 13 dígitos.
    # Um número mais realista seria algo como '3303500000001', onde 3303500 é o IBGE de Nova Iguaçu
    # e 000001 é um sequencial.
    # Mas como o exemplo usa '278241' no campo apa_num (009-021), vamos replicar.
    # No formato, apa_num é 13 posições.
    # O seu exemplo de saída usa '278241' (6 dígitos) no meio do campo apa_num.
    # `142025053325700278241...` onde 3325700 é o CNES.
    # No PDF, apa_num é (009-021), 13 dígitos.
    # Isso significa que o '278241' do exemplo é uma parte do apa_num,
    # não o apa_num completo. O que está no exemplo parece ser o "número interno da APAC".
    # O mais provável é que o número da APAC seja uma concatenação ou um ID maior.
    # Seguindo o PDF, apa_num é de 13 posições.
    # O exemplo mostra: `142025053325700278241`.
    # 14 (id), 202505 (comp), 3325700 (CNES), 278241 (o que ele chama de apa_num?)
    # Posições do apa_num são (009-021). Se competência é 003-008 (6 pos), então 009 é o 9o caractere.
    # "14" + "202505" = 8 chars. O 9o char seria o início de apa_num.
    # No exemplo '142025053325700278241', '3325700278241' é o que está no campo apa_num.
    # Isso significa que o CNES (7 dígitos) está *dentro* do campo apa_num, o que não faz sentido com o PDF.
    # Vamos seguir o PDF estritamente: apa_num (13 dígitos) é um campo *separado* do CNES (7 dígitos).
    # O campo apa_codcnes é (024-030) e apa_num é (009-021).
    # A saída de exemplo parece ter uma anomalia ou uma interpretação diferente.

    # Para ser consistente com o layout oficial:
    # apa_num (009-021) = 13 posições
    # apa_coduf (022-023) = 2 posições
    # apa_codcnes (024-030) = 7 posições
    # Total de 13+2+7 = 22 caracteres.
    # `14` (2 chars) + `AAAAMM` (6 chars) + `apa_num` (13 chars) + `apa_coduf` (2 chars) + `apa_codcnes` (7 chars)
    # Exemplo: '14' + '202505' + 'NNNNNNNNNNNNN' + '33' + 'XXXXXXX'
    # Onde 'NNNNNNNNNNNNN' é o número da APAC de 13 dígitos.
    # A saída de exemplo '142025053325700278241' não segue isso para apa_num e CNES.
    # '3325700' é o CNES. '278241' (6 dígitos) está colado.
    # Se '3325700278241' é o apa_num, ele tem 13 dígitos.
    # Vamos assumir que o "número da APAC" que você quer usar é `data.establishment_cnes + contador` ou similar.
    # Mas o PDF diz que apa_num é um número de APAC de 13 dígitos.
    # Para o exemplo, vou usar um apa_num de 13 dígitos que comece com '33' (UF) + '03500' (Mun) + sequencial.
    # Este é um padrão comum para APACs em alguns estados.
    current_apac_number = f"{UF_RJ_IBGE}{MUN_NOVA_IGUACU_IBGE[2:]}{apac_number_counter:06d}" # Ex: 330350000001
    # Garante que tenha 13 dígitos. Se faltar, completa com zeros à esquerda.
    current_apac_number = format_field(current_apac_number, 13, 'right', '0')

    # Re-calcula total_procedures_sum usando o apa_num *correto* para o cálculo.
    apac_num_for_control = int(current_apac_number) # Usa o número completo da APAC (13 dígitos)
    control_sum = total_procedures_sum + apac_num_for_control
    control_field_val = (control_sum % 1111) + 1111
    
    # Define o número da APAC no corpo para uso interno
    apac_body_data.apac_number = current_apac_number

    # Linha do Corpo da APAC (Registro 14)
    lines.append(apac_body_data.to_apac_string(competence_str, current_apac_number, data.establishment_cnes))
    
    # Linhas das Partes Variáveis
    if apac_body_data.laudo_geral:
        lines.append(apac_body_data.laudo_geral.to_apac_string(competence_str, current_apac_number, data.establishment_cnes))
    if apac_body_data.pre_bariatrica:
        lines.append(apac_body_data.pre_bariatrica.to_apac_string(competence_str, current_apac_number, data.establishment_cnes))

    # Linhas dos Procedimentos (Registro 13)
    for proc_rec in procedure_records:
        lines.append(proc_rec.to_apac_string(competence_str, current_apac_number, data.establishment_cnes))
    
    # --- 3. Preparar o Cabeçalho ---
    header = ApacHeader(
        origin_organization_name=config['origin_organization_name'],
        origin_organization_acronym=config['origin_organization_acronym'],
        provider_cnpj_cpf=config['provider_cnpj_cpf'],
        destination_organization_name=config['destination_organization_name'],
        destination_indicator=config['destination_indicator'],
        layout_version=config['layout_version'],
        competence=competence_str,
        apac_count=1, # Para um único lote de APACs, é 1. Se fosse um arquivo com múltiplas APACs, seria a contagem.
        control_field=str(control_field_val),
        generation_date=current_date
    )
    
    # Inserir o cabeçalho no início da lista de linhas
    lines.insert(0, header.to_apac_string())
    
    # Adicionar CR+LF no final de cada linha para o arquivo TXT
    final_lines = [line + '\r\n' for line in lines]

    # Salvar no arquivo
    with open(output_filepath, 'w', encoding='latin-1') as f: # Geralmente usa latin-1 ou cp1252 para arquivos APAC
        f.writelines(final_lines)

    print(f"Arquivo APAC Magnético gerado com sucesso em: {output_filepath}")
    return final_lines

# --- Exemplo de Uso ---
if __name__ == "__main__":
    import json

    # Exemplo de JSON de entrada (adaptado do seu contexto)
    example_json_data = {
        "establishment_name": "POL SHOPPING NI",
        "establishment_cnes": "2570027", # Ajustado para 7 dígitos ou truncado pelo validador
        "patient_name": "ANA CELIA MENESES LIMA DE ASEV",
        "patient_mother_name": "MARIA MENESES LIMA",
        "patient_birth_date": "13/03/1961", # Continua como string para o input
        "patient_gender": "Feminino",
        "patient_cns": "700000138906208",
        "patient_cpf": None,
        "patient_race": "PARDA",
        "patient_address_street_type": "JOSE ARCAS", # Assumindo que aqui vem o tipo/prefixo do logradouro
        "patient_address_street_name": "RUA DA ALDEIA", # Nome completo da rua
        "patient_address_number": "390",
        "patient_address_complement": "CASA 1",
        "patient_address_postal_code": "26250300",
        "patient_address_city": "Nova Iguaçu",
        "patient_address_neighborhood": "CENTRO",
        "patient_address_code_street": "00011", # Exemplo
        "medic_name": "DAVID DE BARROS VALENTE",
        "medic_cns": "700000138906208",
        "medic_cbo": "225120", # Exemplo CBO para Cardiologista
        "executing_medic_cns": "700000138906208",
        "authorizer_name": "VINICIUS DOS SANTOS AUGUSTO",
        "authorizer_cns": "700000138906208", # Exemplo, deve ser o CNS real do autorizador
        "main_procedure": {"code": "0902010026"}, # Principal do corpo da APAC
        "sub_procedures": [ # Procedimentos executados
            {"code": "0902010026", "quantity": 1},
            {"code": "0204030153", "quantity": 1},
            {"code": "0211020036", "quantity": 1},
            {"code": "0301010072", "quantity": 1}
        ],
        "procedure_date": "20250501", # Data da competência
        "laudo_geral_id": "z136",
        "laudo_geral_data_emissao": "20250509", # Continua como string para o input
        "risco_cirurgico": "A", # Exemplo de risco A para a parte bariátrica
        "request_date": "01/05/2025", # Continua como string para o input
        "authorization_date": "09/05/2025", # Continua como string para o input
        "issuer_code": "081",
        "character_of_service": "E",
        "exit_reason": None, # Exemplo de campo opcional não preenchido
        "exit_date": None # Exemplo de campo opcional não preenchido
    }

    # Configurações para o cabeçalho (precisam ser definidas pelo sistema)
    # Estes são valores hipotéticos baseados no seu exemplo e no CISBAF.
    export_config = {
        'origin_organization_name': 'CISBAF - Consorcio Intermunicipal Saude ', # <--- ADD THIS LINE!
        'origin_organization_acronym': 'UNT   ', # Exemplo baseado no seu output "UNT" - Ajustado para 6 posições
        'provider_cnpj_cpf': '00000004565465', # Exemplo: CNPJ com 14 dígitos (zeros à esquerda)
        'destination_organization_name': 'SECRETARIA DE SAUDE                     ', # Nome destino, ex: SECRETARIA DE SAUDE - Ajustado para 40 posições
        'destination_indicator': 'E', # 'M' para Municipal, 'E' para Estadual
        'layout_version': '02.37' # Versão do layout, pode ser uma constante
    }

    # Criar DTO a partir dos dados JSON
    # A Pydantic agora esperará strings para as datas no input, e o validador as converterá para `date`
    apac_data_dto = ApacExportData(**example_json_data)

    # Caminho do arquivo de saída
    output_dir = "apac_export"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "APAC_MAGNETICO_EXEMPLO.txt")

    # Gerar o arquivo
    generated_lines = generate_apac_magnetico_file(apac_data_dto, export_config, f"/home/daniel/Documentos/exportacoes/APAC_MAGNETICO-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.txt")

    # Imprimir as primeiras linhas para verificação
    print("\n--- Conteúdo do arquivo gerado (primeiras linhas) ---")
    for i, line in enumerate(generated_lines):
        print(line.strip()) # .strip() para remover CR+LF para exibição
        if i >= 10: # Imprime as primeiras 10 linhas para não lotar o console
            break
    print("...")