"""Testes do extrator SIGTAP. Rodar com `python3 -m pytest scripts/sigtap/tests`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from extrair import resolver_secundarios  # noqa: E402


def _linha(principal, secun, trat, qtmax="0002"):
    return {"PAPA_PRINC": principal, "PAPA_SECUN": secun, "PAPA_TRAT": trat, "PAPA_QTMAX": qtmax}


def test_par_simples_obrigatorio():
    linhas = [_linha("090801002", "020102001", "95")]
    r = resolver_secundarios(linhas, "090801002", dv={}, nome={})
    assert [s["codigo"] for s in r["obrigatorios"]] == ["020102001"]
    assert r["compativeis"] == []


def test_par_simples_compativel():
    linhas = [_linha("090801002", "030101007", "01")]
    r = resolver_secundarios(linhas, "090801002", dv={}, nome={})
    assert [s["codigo"] for s in r["compativeis"]] == ["030101007"]
    assert r["obrigatorios"] == []


def test_par_duplicado_obrigatorio_vence_independente_da_ordem():
    """Regressão: S_PAPA pode listar o mesmo par com TRAT=01 e TRAT=95 (achado
    real em 090801002 x 020208025, competência 202608). O extrator não deve
    deixar o código cair em "compatível" só porque essa linha veio depois."""
    ordem_95_depois = [
        _linha("090801002", "020208025", "01", qtmax="0002"),
        _linha("090801002", "020208025", "95", qtmax="0002"),
    ]
    ordem_01_depois = [
        _linha("090801002", "020208025", "95", qtmax="0002"),
        _linha("090801002", "020208025", "01", qtmax="0002"),
    ]
    for linhas in (ordem_95_depois, ordem_01_depois):
        r = resolver_secundarios(linhas, "090801002", dv={}, nome={})
        assert [s["codigo"] for s in r["obrigatorios"]] == ["020208025"]
        assert r["compativeis"] == []


def test_ignora_trat_exclusao_mutua():
    linhas = [_linha("090801002", "030305004", "98"), _linha("090801002", "030305005", "99")]
    r = resolver_secundarios(linhas, "090801002", dv={}, nome={})
    assert r["obrigatorios"] == []
    assert r["compativeis"] == []


def test_ignora_linhas_de_outro_principal():
    linhas = [_linha("090801001", "020102001", "95")]
    r = resolver_secundarios(linhas, "090801002", dv={}, nome={})
    assert r["obrigatorios"] == []
    assert r["compativeis"] == []
