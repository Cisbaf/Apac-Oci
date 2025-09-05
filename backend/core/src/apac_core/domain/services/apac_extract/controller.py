from dataclasses import dataclass
from typing import List
from datetime import date
from apac_core.domain.entities.apac_batch import ApacBatch
from apac_core.domain.entities.establishment import Establishment
from apac_core.domain.services.apac_extract.header_model import HeaderModel
from apac_core.domain.services.apac_extract.apac_model import ApacModel
from apac_core.domain.services.apac_extract.apac_body import ApacBody
from apac_core.domain.services.apac_extract.apac_procedure import ApacProcedure
from apac_core.domain.services.apac_extract.apac_info import ApacInfo
from apac_core.domain.services.apac_extract.utils import (
    format_with_zeros, get_end_of_next_month
)

@dataclass
class ExportApacBatchController:
    establishment: Establishment
    apac_batchs: List[ApacBatch]
    date_production: date

    def header(self) -> HeaderModel:
        return HeaderModel(
            competencia=self.date_production.strftime("%Y%m"),
            qtd_apacs=format_with_zeros(len(self.apac_batchs), 6),
            campo_controle="1810",
            nome_orgao_origem=self.establishment.name,
            sigla_origem=self.establishment.acronym,
            cnpj_prestador=self.establishment.cnpj,
            nome_destino=self.establishment.city.agency_name,
            indicador_destino="M",
            data_geracao=date.today().strftime("%Y%m%d"),
            versao_layout="Versao 03.15"
        )
    
    def body(self) -> List[ApacBody]:
        bodys = []
        for apac_batch in self.apac_batchs:
            apac_request = apac_batch.apac_request
            apac_data = apac_request.apac_data
            data_fim = get_end_of_next_month(self.date_production)
            bodys.append(ApacBody(
                apac_model=ApacModel(
                    competencia=self.date_production.strftime("%Y%m"),
                    numero_apac=apac_batch.batch_number,
                    cod_uf="33",
                    cnes=self.establishment.cnes,
                    data_proc=self.date_production.strftime("%Y%m%d"),
                    data_inicio_validade=self.date_production.strftime("%Y%m%d"),
                    data_fim_validade=data_fim.strftime("%Y%m%d"),
                    tipo_atendimento="00",
                    tipo_apac="3",
                    nome_paciente=apac_data.patient_data.name,
                    nome_mae=apac_data.patient_data.mother_name,
                    logradouro=f"{apac_data.patient_data.address_street_type} {apac_data.patient_data.address_street_name}",
                    numero_endereco=apac_data.patient_data.address_number,
                    complemento=apac_data.patient_data.address_complement,
                    cep=apac_data.patient_data.address_postal_code.value,
                    cod_municipio=apac_batch.city.ibge_code,
                    data_nascimento=apac_data.patient_data.birth_date.strftime("%Y%m%d"),
                    sexo=apac_data.patient_data.gender,
                    nome_medico_responsavel=apac_data.supervising_physician_data.name,
                    cod_procedimento=apac_data.main_procedure.code,
                    motivo_saida="12",
                    data_saida=apac_data.discharge_date.strftime("%Y%m%d"),
                    nome_diretor=apac_data.authorizing_physician_data.name,
                    cns_paciente="000000000000000",
                    cns_responsavel=apac_data.supervising_physician_data.cns.value,
                    cns_diretor=apac_data.authorizing_physician_data.cns.value,
                    cid_causas_associadas="",
                    numero_pronturario="",
                    cnes_solicitate=self.establishment.cnes,
                    data_solicitacao=self.date_production.strftime("%Y%m%d"), # Data da solicitação deverá ser igual a data de inicio da validade da APAC - Hoje a data de solicitação está replicando a data do procedimento   apac_request.apac_data.procedure_date.strftime("%Y%m%d")
                    data_autorizacao=apac_request.apac_data.procedure_date.strftime("%Y%m%d"), # por enquanto fixo
                    codigo_emissor=f"M{apac_batch.city.ibge_code}01",
                    caracter_atendimento="01",
                    apac_anterior="0000000000000",
                    raca_paciente=apac_data.patient_data.race_color,
                    responsavel_paciente=apac_data.patient_data.name,
                    codigo_nacionalidade="010",
                    etinia_paciente="",
                    cod_logradouro=apac_data.patient_data.address_street_type,
                    bairro_paciente=apac_data.patient_data.address_neighborhood,
                    ddd_tel_paciente="",
                    tel_paciente="",
                    email_paciente="",
                    cns_medico_executante=apac_data.supervising_physician_data.cns.value,
                    cpf_paciente=apac_data.patient_data.cpf.value,
                    id_nacional_equipe="",
                    situacao_rua="N"
                ),
                apac_info=ApacInfo(
                    mes_fim_validate=data_fim.strftime("%m%Y"),
                    o_que_e="05",
                    numero_apac=apac_batch.batch_number,
                    cid=apac_data.cid.code,
                ),
                apac_procedures=[
                    ApacProcedure(
                        identificador="13",
                        competencia=self.date_production.strftime("%Y%m"),
                        numero_apac_seq=apac_batch.batch_number,
                        cod_procedimento=apac_data.main_procedure.code,
                        cbo=apac_data.supervising_physician_data.cbo,
                        quantity=format_with_zeros(1, 6),
                    )
                ] + [
                    ApacProcedure(
                        identificador="13",
                        competencia=self.date_production.strftime("%Y%m"),
                        numero_apac_seq=apac_batch.batch_number,
                        cod_procedimento=sub_procedure.procedure.code,
                        cbo=apac_data.supervising_physician_data.cbo,
                        quantity=format_with_zeros(sub_procedure.quantity, 6),
                    ) for sub_procedure in apac_data.sub_procedures
                ]
            ))
        return bodys
    