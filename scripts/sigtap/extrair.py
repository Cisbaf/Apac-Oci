#!/usr/bin/env python3
"""Extrai o cadastro oficial de um procedimento (ou grupo) direto das tabelas SIGTAP.

As tabelas ficam no ambiente de competência montado pelo apac-magnetico-validador
(`ambientes/<competencia>/`). São a **mesma** fonte que o APAC Magnético usa para
criticar o arquivo — por isso valem como verdade: o que sai daqui é exatamente o
que o programa oficial vai aceitar.

Uso:
    python3 scripts/sigtap/extrair.py <dir-ambiente> --grupo 0907 0908
    python3 scripts/sigtap/extrair.py <dir-ambiente> --proc 090801001 090801002
    python3 scripts/sigtap/extrair.py <dir-ambiente> --grupo 0908 --json saida.json

Sem `--json`, imprime um relatório legível em português.

Tabelas lidas
-------------
S_PA      procedimento (valor, idade, sexo, quantidade máxima, exige CBO, SECOBRI)
S_PAPA    par principal × secundário — o campo PAPA_TRAT diz o papel:
            01 = secundário compatível
            95 = secundário OBRIGATÓRIO (só aparece quando S_PA.PA_SECOBRI = 'S')
            98/99 = conjuntos de exclusão mútua (procedimentos que não convivem);
                    não são secundários e por isso não entram no cadastro
S_PACID   par procedimento × CID — PACID_PRIN 'S' = CID principal aceito
S_PACBO   par procedimento × CBO permitido
S_PADET   atributos complementares do procedimento (043, 053, 064, 067...)
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dbf import read_dbf  # noqa: E402

# Papéis do campo PAPA_TRAT que representam um secundário de fato.
PAPEL_COMPATIVEL = "01"
PAPEL_OBRIGATORIO = "95"
PAPEIS_SECUNDARIOS = (PAPEL_COMPATIVEL, PAPEL_OBRIGATORIO)

# Atributos complementares relevantes para as OCIs (Portarias 4.304 e 4.306/2026).
ATRIBUTOS = {
    "043": "Exige CID de causas associadas",
    "053": "Procedimento PMAE (Agora Tem Especialistas)",
    "054": "Validade fixa de 2 competências",
    "057": "Exige autorização prévia",
    "058": "Obrigatório informar CPF do paciente",
    "059": "Componente Complementar Modalidade 2",
    "060": "Exige procedimento secundário de consulta",
    "064": "Exige procedimento diagnóstico e clínico-restaurador",
    "067": "Exige punção lombar e/ou tomografia de crânio",
    "068": "Exige procedimento dos subgrupos 02.02 e/ou 02.03",
    "069": "Exige procedimento dos subgrupos 02.06 e/ou 02.09",
    "070": "Exige tomografia e/ou biópsia",
    "071": "Exige procedimento reabilitador",
}


def carregar(ambiente):
    """Lê as cinco tabelas do ambiente e devolve um dicionário de índices."""
    def tabela(nome):
        caminho = os.path.join(ambiente, nome)
        if not os.path.exists(caminho):  # o ambiente mistura .DBF e .dbf
            caminho = os.path.join(ambiente, nome.lower())
        return read_dbf(caminho)[1]

    return {
        "pa": tabela("S_PA.DBF"),
        "papa": tabela("S_PAPA.DBF"),
        "pacid": tabela("S_PACID.DBF"),
        "pacbo": tabela("S_PACBO.DBF"),
        "padet": tabela("S_PADET.DBF"),
    }


def extrair(ambiente, codigos):
    """Monta o cadastro completo de cada procedimento pedido."""
    t = carregar(ambiente)
    por_id = {p["PA_ID"]: p for p in t["pa"]}
    nome = {p["PA_ID"]: p["PA_DC"] for p in t["pa"]}
    dv = {p["PA_ID"]: p["PA_DV"] for p in t["pa"]}

    resultado = {}
    for codigo in codigos:
        p = por_id.get(codigo)
        if p is None:
            print(f"AVISO: {codigo} não existe nesta competência", file=sys.stderr)
            continue

        secundarios = {"obrigatorios": [], "compativeis": []}
        for r in t["papa"]:
            if r["PAPA_PRINC"] != codigo or r["PAPA_TRAT"] not in PAPEIS_SECUNDARIOS:
                continue
            destino = ("obrigatorios" if r["PAPA_TRAT"] == PAPEL_OBRIGATORIO
                       else "compativeis")
            sec = r["PAPA_SECUN"]
            secundarios[destino].append({
                "codigo": sec,
                "codigo_dv": sec + dv.get(sec, ""),
                "nome": nome.get(sec, ""),
                "quantidade_maxima": int(r["PAPA_QTMAX"]),
            })
        for lista in secundarios.values():
            lista.sort(key=lambda s: s["codigo"])

        cids = sorted(r["PACID_CID"] for r in t["pacid"]
                      if r["PACID_PA"] == codigo and r["PACID_PRIN"] == "S")
        cbos = sorted(r["PACBO_CBO"] for r in t["pacbo"] if r["PACBO_PA"] == codigo)
        atributos = sorted(r["DET_COD"] for r in t["padet"] if r["DET_PA"] == codigo)

        resultado[codigo] = {
            "codigo": codigo,
            "codigo_dv": codigo + p["PA_DV"],
            "nome": p["PA_DC"],
            "valor": p["PA_TOTAL"],
            "idade_minima": p["PA_IDADEMN"],
            "idade_maxima": p["PA_IDADEMX"],
            "sexo": p["PA_SEXO"],
            "quantidade_maxima": p["PA_QTDMAX"],
            "exige_secundario_obrigatorio": p["PA_SECOBRI"] == "S",
            "exige_cpf": p["PA_CPFPCN"] == "S",
            "exige_cbo": p["PA_EXIGCBO"] == "S",
            "tipo_laudo": p["PA_LAUDO"],
            "atributos": [{"codigo": a, "descricao": ATRIBUTOS.get(a, "?")}
                          for a in atributos],
            "cbos_permitidos": cbos,
            "cids_principais": cids,
            "secundarios": secundarios,
        }
    return resultado


def imprimir(dados):
    for codigo, d in dados.items():
        print(f"\n{'=' * 78}")
        print(f"{d['codigo_dv']}  {d['nome']}")
        print(f"{'=' * 78}")
        print(f"  Valor R$ {d['valor']} | idade {d['idade_minima']}-{d['idade_maxima']} "
              f"| sexo {d['sexo']} | qtd máx {d['quantidade_maxima']} | laudo {d['tipo_laudo']}")
        print(f"  Exige CPF: {'sim' if d['exige_cpf'] else 'não'} | "
              f"Exige CBO: {'sim' if d['exige_cbo'] else 'não'} | "
              f"Exige secundário obrigatório: "
              f"{'sim' if d['exige_secundario_obrigatorio'] else 'não'}")

        print("\n  Atributos complementares:")
        for a in d["atributos"]:
            print(f"    {a['codigo']} — {a['descricao']}")

        print(f"\n  CIDs principais aceitos ({len(d['cids_principais'])}): "
              f"{', '.join(d['cids_principais'])}")
        print(f"  CBOs permitidos ({len(d['cbos_permitidos'])}): "
              f"{', '.join(d['cbos_permitidos'][:10])}"
              f"{' ...' if len(d['cbos_permitidos']) > 10 else ''}")

        obr = d["secundarios"]["obrigatorios"]
        if obr:
            print(f"\n  Secundários OBRIGATÓRIOS ({len(obr)}) — todos devem estar na APAC:")
            for s in obr:
                print(f"    {s['codigo_dv']}  qtd máx {s['quantidade_maxima']}  {s['nome'][:52]}")

        com = d["secundarios"]["compativeis"]
        print(f"\n  Secundários compatíveis ({len(com)}):")
        for s in com:
            print(f"    {s['codigo_dv']}  qtd máx {s['quantidade_maxima']}  {s['nome'][:52]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ambiente", help="diretório da competência (ex.: .../ambientes/202608a)")
    ap.add_argument("--grupo", nargs="*", default=[],
                    help="prefixos de código a extrair (ex.: 0907 0908)")
    ap.add_argument("--proc", nargs="*", default=[],
                    help="códigos de 9 dígitos, sem DV")
    ap.add_argument("--json", help="grava o resultado em JSON neste caminho")
    args = ap.parse_args()

    codigos = list(args.proc)
    if args.grupo:
        _, pa = read_dbf(os.path.join(args.ambiente, "S_PA.DBF"))
        for p in pa:
            # PA_TOTAL vazio marca as linhas de grupo/subgrupo, que não são
            # procedimentos cobráveis e não têm cadastro a extrair.
            if any(p["PA_ID"].startswith(g) for g in args.grupo) and p["PA_TOTAL"]:
                codigos.append(p["PA_ID"])
    if not codigos:
        ap.error("informe --grupo ou --proc")

    dados = extrair(args.ambiente, sorted(set(codigos)))
    if args.json:
        with open(args.json, "w") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"{len(dados)} procedimentos gravados em {args.json}", file=sys.stderr)
    else:
        imprimir(dados)


if __name__ == "__main__":
    main()
