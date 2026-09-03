# Ferramenta de cadastro a partir do SIGTAP

Cadastrar uma OCI nova no sistema é transcrever regra de portaria para dentro do
banco. Transcrever à mão erra — e o erro só aparece semanas depois, quando o
município tenta faturar e o SIA rejeita. Esta ferramenta troca a transcrição por
extração: lê as **mesmas tabelas** que o APAC Magnético usa para criticar o
arquivo e compara com o que está cadastrado.

## Por que estas tabelas valem como verdade

O `apac-magnetico-validador` monta, por competência, o ambiente do programa
oficial em `ambientes/<competencia>/`. Lá ficam as tabelas DBF do SIGTAP daquela
competência. Quando o APAC Magnético critica uma APAC com
`PROC.(...) INCOMPATIVEL COM CID (...)`, é nestas tabelas que ele olhou. Cadastro
que bate com elas não toma crítica; cadastro que diverge, toma.

## Uso

```bash
# 1. Extrair a verdade oficial da competência (grupo 09.07 e 09.08)
python3 scripts/sigtap/extrair.py \
    ../apac-magnetico-validador/ambientes/202608a \
    --grupo 0907 0908 --json /tmp/ocis.json

# 2. Conferir o cadastro do sistema (não escreve nada)
cd backend/src && python manage.py sigtap_auditar --json /tmp/ocis.json

# 3. Corrigir
cd backend/src && python manage.py sigtap_auditar --json /tmp/ocis.json --aplicar
```

Sem `--json`, o `extrair.py` imprime um relatório legível — útil para conferir
uma OCI antes de cadastrar, ou para responder "quais secundários esta OCI
aceita?" sem abrir o SIGTAP.

O `--aplicar` **não apaga procedimento nem CID**: ele só desfaz o vínculo com a
OCI. Um procedimento desvinculado de uma OCI continua existindo e pode ser
secundário legítimo de outra.

## O que cada tabela responde

| Tabela | Responde |
|---|---|
| `S_PA` | valor, faixa etária, sexo, quantidade máxima, exige CBO, exige secundário obrigatório |
| `S_PAPA` | quais secundários a OCI aceita, o papel de cada um e a quantidade máxima do par |
| `S_PACID` | quais CIDs a OCI aceita como **principal** (`PACID_PRIN = 'S'`) |
| `S_PACBO` | quais CBOs podem executar o procedimento |
| `S_PADET` | atributos complementares (043, 053, 064, 067...) |

### O campo `PAPA_TRAT`, que decide o papel do secundário

| Valor | Significado |
|---|---|
| `01` | secundário **compatível** — pode entrar na APAC |
| `95` | secundário **obrigatório** — todos devem entrar. Só aparece quando `S_PA.PA_SECOBRI = 'S'`; a correspondência é exata nas 3.262 linhas da competência 202608 |
| `98` / `99` | conjuntos de **exclusão mútua** (procedimentos que não convivem na mesma APAC). Não são secundários e por isso a ferramenta os ignora |

Confundir `95` com `01` é o que produz a crítica
`PROC.PRINC(...) EXIGE PELO MENOS (00N) PROC. SECUNDARIO OBRIGATORIO` — o `N` da
mensagem é exatamente a contagem de linhas `TRAT=95` daquele principal.

## CID de causas associadas (atributo 043) — resolvido na T-036

O SIGTAP não lista quais CIDs valem como segundo CID — só marca, em `S_PADET`,
que o procedimento exige um. A lista em si (128 CIDs, para as 8 OCIs de
Infectologia) veio do texto da Portaria SAES/MS Nº 4.306/2026 e está preservada
em `cids_causas_associadas.json`, indexado pelo código de **10 dígitos** (com
DV). Para semear:

```bash
cd backend/src && python manage.py sigtap_semear_cid_secundario \
    --json ../../scripts/sigtap/cids_causas_associadas.json --aplicar
```

Mesmo padrão do `sigtap_auditar`: sem `--aplicar` só relata.

## Reteste no APAC Magnético

`gerar_apac_teste.py` monta um arquivo de remessa a partir do extrato do
SIGTAP — CID principal, todos os secundários (obrigatórios e compatíveis) e,
quando o atributo 043 se aplicar, o CID de causas associadas — para provar num
arquivo real que um cadastro corrigido não toma mais crítica de conteúdo.

```bash
python3 scripts/sigtap/gerar_apac_teste.py \
    --sigtap-json /tmp/ocis.json \
    --cids-secundarios scripts/sigtap/cids_causas_associadas.json \
    --modelo caminho/para/arquivo_modelo.AGO \
    --tabela-cbo ../apac-magnetico-validador/ambientes/202608a/S_PACBO.DBF \
    --competencia 202608 \
    --saida /tmp/teste.AGO
```

`--modelo` é necessário porque o gerador não resolve dois problemas que são do
arquivo de teste, não do cadastro: o dígito verificador do número da APAC
(algoritmo oficial não identificado) e o CNS do médico executante (só
paciente/responsável/diretor recebem CNS válido). O `--modelo` fornece
cabeçalho e números de APAC de um arquivo que o ambiente de teste já
reconhece; o gerador reescreve os campos de CID, CBO e CNS.

Rodar o arquivo gerado: `apac-magnetico-validador/bin/validar.sh <saida>`.

## Limite conhecido do cadastro atual

**Papel e quantidade máxima são do par, não do procedimento.**
`ProcedureModel.mandatory` é um booleano do procedimento, mas `020208003` é
compatível em `090801001` e obrigatório em `090801002`. São 6 secundários com
papel divergente e 5 com quantidade divergente entre as 10 OCIs novas. O
`sigtap_auditar` não confere isso ainda — ver `T-037`.
