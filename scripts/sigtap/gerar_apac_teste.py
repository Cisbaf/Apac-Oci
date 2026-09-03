#!/usr/bin/env python3
"""Gera um arquivo de remessa de teste a partir do cadastro extraído do SIGTAP.

Preenche cada APAC com o CID principal aceito, TODOS os secundários (obrigatórios
e compatíveis) e, quando o procedimento carregar o atributo 043 (T-036), o CID de
causas associadas — exatamente o que o cadastro "correto" deveria produzir. Serve
para provar no APAC Magnético real que um cadastro corrigido pelo `sigtap_auditar`
não toma mais crítica de conteúdo.

Não resolve dois problemas que são do gerador de teste, não do cadastro, e ficam
fora de propósito por design:

  - Dígito verificador do número da APAC: o algoritmo oficial não foi identificado
    (não é módulo 11 nas variações testadas). Por isso o número da APAC e o
    cabeçalho vêm de um arquivo-modelo já existente, em vez de gerados do zero —
    reaproveita números que o ambiente de teste já reconhece na importação.
  - CNS: só os campos cns_paciente/cns_responsavel/cns_diretor recebem um CNS
    válido (algoritmo módulo 11 real); cns_medico_executante fica com o valor do
    arquivo-modelo.

Uso:
    python3 scripts/sigtap/gerar_apac_teste.py \
        --sigtap-json /tmp/ocis.json \
        --cids-secundarios scripts/sigtap/cids_causas_associadas.json \
        --modelo caminho/para/arquivo_modelo.AGO \
        --competencia 202608 \
        --saida /tmp/teste.AGO

`--sigtap-json` é o extrato de `extrair.py` (--grupo/--proc) para os
procedimentos principais que aparecem no arquivo-modelo. `--modelo` fornece o
cabeçalho e os números de APAC (registros "01" e "14") — só os campos de CID,
CBO e CNS de cada APAC são reescritos.
"""
import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dbf import read_dbf  # noqa: E402

# Layout do registro "14" até o campo que interessa aqui (cid_causas_associadas).
# Ver apac_extract/apac_model.py para o layout completo.
CAMPOS_REGISTRO_14 = [
    ("identificador", 2), ("competencia", 6), ("numero_apac", 13), ("cod_uf", 2),
    ("cnes", 7), ("data_proc", 8), ("data_inicio_validade", 8), ("data_fim_validade", 8),
    ("tipo_atendimento", 2), ("tipo_apac", 1), ("nome_paciente", 30), ("nome_mae", 30),
    ("logradouro", 30), ("numero_endereco", 5), ("complemento", 10), ("cep", 8),
    ("cod_municipio", 7), ("data_nascimento", 8), ("sexo", 1),
    ("nome_medico_responsavel", 30), ("cod_procedimento", 10), ("motivo_saida", 2),
    ("data_saida", 8), ("nome_diretor", 30), ("cns_paciente", 15),
    ("cns_responsavel", 15), ("cns_diretor", 15), ("cid_causas_associadas", 4),
]
_OFFSETS = {}
_pos = 0
for _nome, _tam in CAMPOS_REGISTRO_14:
    _OFFSETS[_nome] = (_pos, _pos + _tam)
    _pos += _tam


def cns_valido(rnd):
    """CNS definitivo válido (inicia 1 ou 2), algoritmo oficial módulo 11."""
    while True:
        pis = str(rnd.choice([1, 2])) + "".join(str(rnd.randint(0, 9)) for _ in range(10))
        soma = sum(int(pis[i]) * (15 - i) for i in range(11))
        dv = 11 - (soma % 11)
        if dv == 11:
            dv = 0
        if dv == 10:
            soma += 2
            dv = 11 - (soma % 11)
            if dv in (10, 11):
                continue
            return pis + "001" + str(dv)
        return pis + "000" + str(dv)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sigtap-json", required=True, help="extrato de extrair.py")
    ap.add_argument("--cids-secundarios",
                    help="cids_causas_associadas.json (T-035); omitir se nenhum "
                         "procedimento do lote exigir CID de causas associadas")
    ap.add_argument("--modelo", required=True,
                    help="arquivo de remessa existente: fornece cabeçalho e números de APAC")
    ap.add_argument("--tabela-cbo", required=True,
                    help="S_PACBO.DBF do ambiente da competência (apac-magnetico-validador)")
    ap.add_argument("--competencia", required=True, help="ex.: 202608")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--seed", type=int, default=1, help="semente do gerador de CNS (determinismo)")
    args = ap.parse_args()

    sigtap = json.load(open(args.sigtap_json))
    cids_sec = json.load(open(args.cids_secundarios)) if args.cids_secundarios else {}

    _, pacbo = read_dbf(args.tabela_cbo)
    cbos_por_procedimento = {}
    for r in pacbo:
        cbos_por_procedimento.setdefault(r["PACBO_PA"], []).append(r["PACBO_CBO"])

    def cbo_de(codigo9, preferido=None):
        lista = cbos_por_procedimento.get(codigo9, [])
        if preferido and preferido in lista:
            return preferido
        return lista[0] if lista else "225125"

    linhas = Path(args.modelo).read_text(encoding="latin-1").splitlines()
    cabecalho = next(l for l in linhas if l.startswith("01"))
    registros_14 = [l for l in linhas if l.startswith("14")]

    rnd = random.Random(args.seed)
    saida = [cabecalho]

    for linha in registros_14:
        num = linha[_OFFSETS["numero_apac"][0]:_OFFSETS["numero_apac"][1]]
        proc10 = linha[_OFFSETS["cod_procedimento"][0]:_OFFSETS["cod_procedimento"][1]]
        proc9 = proc10[:9]
        if proc9 not in sigtap:
            print(f"AVISO: {proc10} sem entrada no extrato SIGTAP, pulando", file=sys.stderr)
            continue
        dados = sigtap[proc9]

        cid_principal = dados["cids_principais"][0]
        entrada_sec = cids_sec.get(proc10)
        cid_secundario = entrada_sec["cids_causas_associadas"][0]["codigo"] if entrada_sec else ""

        linha = list(linha)
        for campo in ("cns_paciente", "cns_responsavel", "cns_diretor"):
            a, b = _OFFSETS[campo]
            if "".join(linha[a:b]).strip("0").strip():
                linha[a:b] = list(cns_valido(rnd))
        a, b = _OFFSETS["cid_causas_associadas"]
        linha[a:b] = list(f"{cid_secundario:<4}")
        saida.append("".join(linha))

        saida.append(f"06{args.competencia}{num}{cid_principal:<4}{cid_secundario:<4}{'':<8}")

        cbo_principal = cbo_de(proc9)

        def registro_13(codigo10, codigo9, cbo):
            return (f"13{args.competencia}{num}{codigo10:<10}{cbo:<6}{'0000001'}"
                    f"{'':<14}{'':<6}{cid_principal:<4}{cid_secundario:<4}")

        saida.append(registro_13(proc10, proc9, cbo_principal))
        vistos = {proc9}
        for grupo in ("obrigatorios", "compativeis"):
            for s in dados["secundarios"][grupo]:
                if s["codigo"] in vistos:
                    continue
                vistos.add(s["codigo"])
                saida.append(registro_13(s["codigo_dv"], s["codigo"],
                                         cbo_de(s["codigo"], cbo_principal)))

    Path(args.saida).write_text("\r\n".join(saida) + "\r\n", encoding="latin-1")
    print(f"{args.saida}: {len(saida)} linhas, {len(registros_14)} APAC(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
