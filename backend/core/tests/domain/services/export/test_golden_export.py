"""
Teste de caracterização (golden file) do export APAC (layout posicional v03.15).

Congela o comportamento ATUAL do export byte a byte, inclusive os débitos
conhecidos (`cns_paciente` sempre "000000000000000", `cod_uf` fixo em "33") e a
adaptação `adaptar_oci` (hoje aplicada incondicionalmente a qualquer município,
não só Duque de Caxias — ver `.context/glossary.md`). Nenhum desses pontos deve
ser corrigido aqui: esta tarefa só fixa o que já existe, para que qualquer
mudança futura no export seja deliberada.

Se este teste quebrar depois de uma mudança de código, pare e pergunte:
"essa mudança no arquivo exportado era intencional?" Se sim, atualize o golden
na mesma tarefa que motivou a mudança e explique por quê no PR. Nunca
atualize o golden só para fazer o teste passar.
"""
from datetime import date
from pathlib import Path

import pytest

from apac_core.application.use_cases.apac_export_case import ApacExportCase, ApacExportDto
from apac_core.application.implementations.apac_batch_fake_repository import ApacBatchFakeRepository
from apac_core.application.implementations.establishment_fake_repository import EstablishmentFakeRepository

from fixtures import build_apac_batch, build_city, build_establishment, build_sub_procedure_records

GOLDEN_DIR = Path(__file__).parent / "golden"
FIXED_TODAY = date(2025, 6, 10)
PRODUCTION = date(2025, 5, 1)


class _FixedDate(date):
    """Substitui `date` no módulo do controller para congelar `date.today()`."""

    @classmethod
    def today(cls):
        return FIXED_TODAY


@pytest.fixture(autouse=True)
def freeze_today(monkeypatch):
    monkeypatch.setattr(
        "apac_core.domain.services.apac_extract.controller.date", _FixedDate
    )


def _export(city, establishment, batch):
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


def _assert_matches_golden(output: str, golden_filename: str):
    golden_path = GOLDEN_DIR / golden_filename
    expected = golden_path.read_text(encoding="utf-8")
    assert output == expected, (
        f"Saída do export divergiu do golden file '{golden_filename}'. "
        "Se a mudança foi intencional, atualize o golden na mesma tarefa "
        "que a motivou e explique por quê no PR — nunca só para 'fazer passar'."
    )


def test_golden_apac_simples():
    """1 APAC com apenas o procedimento principal, sem subprocedimentos."""
    city = build_city()
    establishment = build_establishment(city)
    batch = build_apac_batch(
        batch_number="3325700278201",
        city=city,
        establishment=establishment,
        production=PRODUCTION,
        sub_procedures=[],
    )

    output = _export(city, establishment, batch)

    _assert_matches_golden(output, "apac_simples.txt")


def test_golden_apac_com_subprocedimentos():
    """1 APAC com o procedimento principal + 4 subprocedimentos."""
    city = build_city()
    establishment = build_establishment(city)
    batch = build_apac_batch(
        batch_number="3325700278252",
        city=city,
        establishment=establishment,
        production=PRODUCTION,
        sub_procedures=build_sub_procedure_records(),
    )

    output = _export(city, establishment, batch)

    _assert_matches_golden(output, "apac_com_subprocedimentos.txt")


def test_golden_apac_duque_de_caxias():
    """
    Estabelecimento em Duque de Caxias (ibge 3301702). `adaptar_oci` hoje é
    aplicada a qualquer município (não checa a cidade) — este golden fixa o
    comportamento atual para esse município específico, para servir de
    referência quando a T-202 isolar essa regra por `MunicipalityExportProfile`.
    """
    city = build_city(name="Duque de Caxias", ibge_code="3301702", agency_name="SECRETARIA MUNICIPAL DE DUQUE DE CAXIAS", id=2)
    establishment = build_establishment(city, id=7, cnes="2280396", cnpj="42498600000171")
    batch = build_apac_batch(
        batch_number="3325700278301",
        city=city,
        establishment=establishment,
        production=PRODUCTION,
        sub_procedures=[],
    )

    output = _export(city, establishment, batch)

    _assert_matches_golden(output, "apac_duque_de_caxias.txt")


def test_determinismo_roda_duas_vezes_com_mesmo_resultado():
    """Regra do critério de aceite: rodar 2x tem que dar o mesmo resultado."""
    city = build_city()
    establishment = build_establishment(city)
    batch = build_apac_batch(
        batch_number="3325700278201",
        city=city,
        establishment=establishment,
        production=PRODUCTION,
        sub_procedures=[],
    )

    first = _export(city, establishment, batch)

    city2 = build_city()
    establishment2 = build_establishment(city2)
    batch2 = build_apac_batch(
        batch_number="3325700278201",
        city=city2,
        establishment=establishment2,
        production=PRODUCTION,
        sub_procedures=[],
    )
    second = _export(city2, establishment2, batch2)

    assert first == second
