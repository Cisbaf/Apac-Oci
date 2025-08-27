from pydantic import Field, field_validator
from datetime import date
from typing import Optional
from apac_core.domain.services.apac_extract.base import FixedWidthBaseModel
from apac_core.domain.services.apac_extract.utils import (
    only_digits, fix_length, format_date_yyyymmdd
)

class ApacModel(FixedWidthBaseModel):
    __field_sizes__ = {
        "identificador": 2,
        "competencia": 6,
        "numero_apac": 13,
        "cod_uf": 2,
        "cnes": 7,
        "data_proc": 8,
        "data_inicio_validade": 8,
        "data_fim_validade": 8,
        "tipo_atendimento": 2,
        "tipo_apac": 1,
        "nome_paciente": 30,
        "nome_mae": 30,
        "logradouro": 30,
        "numero_endereco": 5,
        "complemento": 10,
        "cep": 8,
        "cod_municipio": 7,
        "data_nascimento": 8,
        "sexo": 1,
        "nome_medico_responsavel": 30,
        "cod_procedimento": 10,
        "motivo_saida": 2,
        "data_saida": 8,
        "nome_diretor": 30,
        "cns_paciente": 15,
        "cns_responsavel": 15,
        "cns_diretor": 15,
        "cid_causas_associadas": 4,
        "numero_pronturario": 10,
        "cnes_solicitate": 7,
        "data_solicitacao": 8,
        "data_autorizacao": 8,
        "codigo_emissor": 10,
        "caracter_atendimento": 2,
        "apac_anterior": 13,
        "raca_paciente": 2,
        "responsavel_paciente": 30,
        "codigo_nacionalidade": 3,
        "etinia_paciente": 4,
        "cod_logradouro": 3,
        "bairro_paciente": 30,
        "ddd_tel_paciente": 2,
        "tel_paciente": 9,
        "email_paciente": 40,
        "cns_medico_executante": 15,
        "cpf_paciente": 11,
        "id_nacional_equipe": 10,
        "situacao_rua": 1,
    }

    identificador: Optional[str] = Field(default="14")
    competencia: str
    numero_apac: str
    cod_uf: str
    cnes: str
    data_proc: str
    data_inicio_validade: str
    data_fim_validade: str
    tipo_atendimento: str
    tipo_apac: str
    nome_paciente: str
    nome_mae: str
    logradouro: str
    numero_endereco: str
    complemento: str
    cep: str
    cod_municipio: str
    data_nascimento: str
    sexo: str
    nome_medico_responsavel: str
    cod_procedimento: str
    motivo_saida: Optional[str] = ""
    data_saida: Optional[str] = ""
    nome_diretor: str
    cns_paciente: str
    cns_responsavel: str
    cns_diretor: str
    cid_causas_associadas: Optional[str] = ""
    numero_pronturario: Optional[str] = ""
    cnes_solicitate: Optional[str] = ""
    data_solicitacao: str
    data_autorizacao: str
    codigo_emissor: str
    caracter_atendimento: str
    apac_anterior: Optional[str] = Field(default="0000000000000")
    raca_paciente: str
    responsavel_paciente: str
    codigo_nacionalidade: str
    etinia_paciente: str
    cod_logradouro: str
    bairro_paciente: str
    ddd_tel_paciente: Optional[str] = ""
    tel_paciente: Optional[str] = ""
    email_paciente: Optional[str] = ""
    cns_medico_executante: str
    cpf_paciente: Optional[str] = ""
    id_nacional_equipe: Optional[str] = ""
    situacao_rua: Optional[str] = Field(default="N")

    @field_validator("*", mode="before")
    @classmethod
    def normalize_fields(cls, v, info):
        field = info.field_name
        sizes = cls.__field_sizes__

        if field.startswith("data_") and isinstance(v, (str, date)):
            return format_date_yyyymmdd(v)

        if "cns" in field or field == "cnes":
            return only_digits(v, sizes[field])

        return fix_length(str(v), sizes[field])
