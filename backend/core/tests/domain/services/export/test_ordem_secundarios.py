"""
Ordem das linhas "13" dos secundários no arquivo exportado (T-044).

Contexto: o arquivo de Duque de Caxias da competência 08/2026 tomou 22 críticas no
APAC Magnético 04.01, todas da OCI 0901010057 (colo do útero):

    PROC.PRINC(0901010057) E PROC.SEC.(0201010666) EXIGE O 0203020081).

O `0203020081` estava no arquivo em todas elas, mas numa linha *antes* da biópsia
`0201010666`. Trocadas as duas linhas, o 04.01 aceitou as 302 APACs. O 04.00 aceita
as duas ordens, e a ordem que saía era a do banco, que não é garantida.
"""
from datetime import date

from apac_core.application.use_cases.apac_export_case import ApacExportCase, ApacExportDto
from apac_core.application.implementations.apac_batch_fake_repository import ApacBatchFakeRepository
from apac_core.application.implementations.establishment_fake_repository import EstablishmentFakeRepository
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.entities.procedure_record import ProcedureRecord

from fixtures import build_apac_batch, build_city, build_establishment

PRODUCTION = date(2026, 8, 1)


def _codigos_das_linhas_13(sub_procedures) -> list[str]:
    city = build_city()
    establishment = build_establishment(city)
    batch = build_apac_batch(
        batch_number="3326702930298",
        city=city,
        establishment=establishment,
        production=PRODUCTION,
        sub_procedures=sub_procedures,
    )
    batch.apac_request.apac_data.main_procedure = Procedure(
        name="OCI INVESTIGACAO DIAGNOSTICA DE CANCER DE COLO DO UTERO", code="0901010057", id=900
    )

    repo_apac_batch = ApacBatchFakeRepository()
    repo_apac_batch.apac_batchs.append(batch)
    repo_establishment = EstablishmentFakeRepository()
    repo_establishment.establishments.append(establishment)

    output = ApacExportCase(
        repo_apac_batch=repo_apac_batch,
        repo_establishment=repo_establishment,
    ).execute(ApacExportDto(
        production=PRODUCTION,
        establishment_id=establishment.id,
        apac_batchs=[batch.id],
    ))
    return [linha[21:31] for linha in output.splitlines() if linha.startswith("13")]


def _registro(code: str, id: int) -> ProcedureRecord:
    return ProcedureRecord(procedure=Procedure(name=code, code=code, id=id), quantity=1, id=id)


def test_biopsia_sai_antes_do_anatomopatologico_que_ela_exige():
    """A ordem gravada no caso real (consulta, anatomopatológico, biópsia) sai corrigida."""
    gravados = [
        _registro("0301010072", 1),  # consulta
        _registro("0203020081", 2),  # anatomopatológico do colo
        _registro("0201010666", 3),  # biópsia do colo
    ]

    codigos = _codigos_das_linhas_13(gravados)

    assert codigos[0] == "0901010057"  # o principal continua sendo a primeira linha
    assert codigos.index("0201010666") < codigos.index("0203020081")


def test_secundarios_saem_em_ordem_de_codigo_seja_qual_for_a_ordem_gravada():
    gravados = [_registro("0301010072", 1), _registro("0203020081", 2), _registro("0201010666", 3)]

    assert _codigos_das_linhas_13(gravados) == _codigos_das_linhas_13(list(reversed(gravados)))
    assert _codigos_das_linhas_13(gravados)[1:] == ["0201010666", "0203020081", "0301010072"]
