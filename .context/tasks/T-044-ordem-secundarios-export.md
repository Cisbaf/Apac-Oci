# T-044 — Ordem dos secundários no export (crítica nova do APAC Magnético 04.01)

- **Fase:** 0 · **Status:** done · **Depende de:** T-002
- **Branch:** `refactor/T-044-ordem-secundarios-export`

## Origem — relato do usuário

Consistência do arquivo `APCDRDM.AGO` (Duque de Caxias, competência 08/2026) no APAC
Magnético **04.01**, tabela `202608a`: 22 críticas, todas iguais e todas da OCI
`0901010057` (investigação diagnóstica de câncer de colo do útero):

```
202608 3326702930298 ERR 090101 000013 PROC.PRINC(0901010057) E PROC.SEC.(0201010666) EXIGE O 0203020081).
```

## Causa raiz

O `0203020081` (anatomopatológico do colo) **estava no arquivo** nas 22 APACs, mas na
linha "13" *antes* da biópsia `0201010666`. O 04.01 só reconhece o exame exigido
quando ele vem depois do secundário que o exige. SIGTAP não explica: os dois são
`PAPA_TRAT=01` (compatíveis) com a OCI, quantidade 1, CBO 225250 aceito nos dois.

Provado no `apac-magnetico-validador` (ambiente `202608-0401` = `202608a` com o
`APAC.exe` do `APACMAG_0401.exe`):

| Programa | Arquivo | Resultado |
|---|---|---|
| 04.00 | original | SEM ERROS |
| 04.00 | biópsia antes do anatomopatológico | SEM ERROS |
| 04.01 | original | as mesmas 22 críticas |
| 04.01 | biópsia antes do anatomopatológico | SEM ERROS (302 APAC) |
| 04.01 e 04.00 | todos os secundários em ordem de código | SEM ERROS (302 APAC) |

O export gerava as linhas na ordem de `apac_data.sub_procedures`, que vem de
`ApacDataModel.records` **sem `ordering`** — ordem do banco, não garantida.

## Correção

`ordered_sub_procedures()` em `apac_extract/controller.py`: os secundários saem em
ordem crescente de código SIGTAP. O principal continua sendo a primeira linha "13".
Na tabela SIGTAP a coleta/biópsia (02.01) vem antes do exame (02.03), então a
ordem por código põe o exigido depois de quem exige. Ordenar por código também
deixa o arquivo determinístico.

## Escopo

- [x] `controller.py`: ordena os secundários por código antes de montar as linhas "13".
- [x] `test_ordem_secundarios.py`: caso real (consulta, anatomopatológico, biópsia) sai
      com a biópsia antes; ordem gravada não influencia. Provado vermelho sem o fix.
- [x] Golden `apac_com_subprocedimentos.txt` atualizado **de propósito**: mesmas 5
      linhas "13", só a ordem dos 4 secundários mudou (cabeçalho e campo de controle
      inalterados).

## Fora do escopo

- Arquivos já exportados não são reescritos. O de Duque de Caxias 08/2026 foi
  corrigido à mão (linhas trocadas) e passou no 04.01.
- O rótulo `versao_layout` do cabeçalho continua `"Versao 04.00"` (T-029); o 04.01
  aceita o arquivo assim.
- `bin/montar-competencia.sh` do validador ainda usa o `APACMAG_0400.exe` por padrão —
  por isso a crítica não apareceu lá antes.

## Impacto no formato do export

Muda **só a ordem** das linhas "13" dos secundários dentro de cada APAC. Nenhum campo,
tamanho ou conteúdo muda.

## Verificação

- `cd backend/core && python -m pytest`
- `cd backend/src && python manage.py test`
- `bash scripts/verify.sh`

## Critério de aceite

- [x] APAC com biópsia `0201010666` e anatomopatológico `0203020081` exporta a biópsia antes.
- [x] Arquivo real ordenado por código passa no 04.01 e no 04.00.
- [x] Gates verdes (`verify.sh`: core 49, src 83, jest 48, lint).

## Ao concluir

- Marcar como `done` em `INDEX.md`.
