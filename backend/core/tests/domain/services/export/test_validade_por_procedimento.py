"""
Validade da APAC exportada, condicionada ao procedimento principal (T-034).

Contexto: a T-024 trocou a validade de 2 para 3 competências para *toda* APAC,
apoiada no changelog v03.22 (Portaria SAES/MS Nº 3.958/2026 exclui o atributo
complementar "054 — APAC com validade fixa de 2 competências"). Um arquivo real
da competência 06/2026 foi rejeitado em produção com

    ERR CORPO 010087 PROCEDIMENTO EXIGE VALIDADE FIXA DE 2 COMPETENCIAS

provando que a exclusão não é geral: alguns procedimentos ainda carregam o 054.
A regra passou a ser por procedimento, e estes testes travam as duas pontas.
"""
from datetime import date

import pytest

from apac_core.application.use_cases.apac_export_case import ApacExportCase, ApacExportDto
from apac_core.application.implementations.apac_batch_fake_repository import ApacBatchFakeRepository
from apac_core.application.implementations.establishment_fake_repository import EstablishmentFakeRepository
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.services.apac_extract.apac_model import ApacModel

from fixtures import build_apac_batch, build_city, build_establishment

PRODUCTION = date(2025, 5, 1)


def _slice_of(field_name: str) -> slice:
    """Recorte posicional de um campo do registro "14", derivado do próprio model."""
    start = 0
    for name, size in ApacModel.__field_sizes__.items():
        if name == field_name:
            return slice(start, start + size)
        start += size
    raise AssertionError(f"campo inexistente em ApacModel: {field_name}")


def _export_com_procedimento(main_procedure: Procedure) -> str:
    city = build_city()
    establishment = build_establishment(city)
    batch = build_apac_batch(
        batch_number="3325700278201",
        city=city,
        establishment=establishment,
        production=PRODUCTION,
        sub_procedures=[],
    )
    batch.apac_request.apac_data.main_procedure = main_procedure

    repo_apac_batch = ApacBatchFakeRepository()
    repo_apac_batch.apac_batchs.append(batch)
    repo_establishment = EstablishmentFakeRepository()
    repo_establishment.establishments.append(establishment)

    return ApacExportCase(
        repo_apac_batch=repo_apac_batch,
        repo_establishment=repo_establishment,
    ).execute(ApacExportDto(
        production=PRODUCTION,
        establishment_id=establishment.id,
        apac_batchs=[batch.id],
    ))


def _datas_de_validade(output: str) -> tuple[str, str]:
    linha = next(l for l in output.splitlines() if l.startswith("14"))
    return linha[_slice_of("data_inicio_validade")], linha[_slice_of("data_fim_validade")]


def test_validade_padrao_e_de_3_competencias():
    """Sem o atributo 054: fim do 3º mês (regra vigente desde 04/2026, T-024)."""
    procedimento = Procedure(name="OCI AVALIAÇÃO CARDIOLÓGICA", code="0902010026", id=244)
    assert procedimento.fixed_validity_two_competences is False

    inicio, fim = _datas_de_validade(_export_com_procedimento(procedimento))

    assert inicio == "20250501"
    assert fim == "20250731"


def test_procedimento_com_atributo_054_exporta_2_competencias():
    """
    Com o atributo 054: fim do mês seguinte. É o caso que gerava o erro 010087 em
    produção (competência 06/2026 saía com 20260831 em vez de 20260731).
    """
    procedimento = Procedure(
        name="OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE CÂNCER DE PRÓSTATA",
        code="0902010034",
        id=249,
        fixed_validity_two_competences=True,
    )

    inicio, fim = _datas_de_validade(_export_com_procedimento(procedimento))

    assert inicio == "20250501"
    assert fim == "20250630"


@pytest.mark.parametrize(
    "producao, esperado",
    [
        (date(2026, 6, 1), "20260731"),   # o caso real que quebrou em produção
        (date(2026, 11, 1), "20261231"),  # virada de ano
        (date(2026, 12, 1), "20270131"),  # virada de ano com carry
    ],
)
def test_validade_054_atravessa_virada_de_ano(producao, esperado):
    """`get_end_of_month_offset` com offset 1 tem que atravessar dezembro sem erro."""
    from apac_core.domain.services.apac_extract.utils import get_end_of_month_offset

    assert get_end_of_month_offset(producao, 1).strftime("%Y%m%d") == esperado
