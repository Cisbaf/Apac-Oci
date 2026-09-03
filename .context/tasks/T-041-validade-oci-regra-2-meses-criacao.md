# T-041 — Validação de criação da OCI ainda usa a regra extinta de 2 meses

- **Fase:** 0 · **Status:** done · **Depende de:** T-024, T-034
- **Branch:** `refactor/T-041-validade-oci-regra-2-meses-criacao`

## Origem — relato do usuário

Usuário tentou registrar uma OCI com data do procedimento `07/07/2026` e data de alta
`02/09/2026` e recebeu o erro:

```
A data de alta excede o limite de 2 meses da APAC.
```

## Causa raiz

`CreateApacRequestUseCase` (`create_apac_request_case.py:50-54`) tinha uma validação de
"2 meses" própria, escrita antes da T-024, que calculava o limite como o **fim do mês
seguinte** ao procedimento (`(procedure_date + relativedelta(months=2)).replace(day=1) -
1 dia`) — matematicamente a mesma regra extinta do atributo SIGTAP 054.

A T-024 trocou essa conta para 3 competências no *export* (`controller.py`/`adapter.py`,
via `get_end_of_month_offset`), apoiada na Portaria SAES/MS Nº 3.958/2026. A T-034 refinou
para condicional por procedimento (`fixed_validity_two_competences`). Nenhuma das duas
tocou `create_apac_request_case.py` — a validação de *criação* ficou presa na regra velha
enquanto o *export* já usa a regra nova, então a tela bloqueava solicitações que o próprio
sistema aceitaria exportar sem erro.

No caso relatado: procedimento em julho, sem o atributo 054 (a maioria) → limite real é
30/09/2026 (3ª competência). A alta em 02/09/2026 estava dentro do prazo; o sistema
rejeitou por engano.

## Correção

`create_apac_request_case.py` passou a buscar o procedimento principal (`repo_procedure`,
já injetado no use case) e usar a mesma lógica do export: `months_ahead = 1` se
`fixed_validity_two_competences`, senão `2`, com `get_end_of_month_offset` (reaproveitado
de `apac_extract/utils.py`, não duplicado). Mensagem de erro atualizada para citar a
competência calculada (2 ou 3), em vez do "2 meses" fixo que não refletia a regra real.

## Escopo

- [x] `create_apac_request_case.py`: busca `main_procedure` antes da checagem, deriva
      `months_ahead` da flag, usa `get_end_of_month_offset`.
- [x] 3 testes novos em `test_create_apac_request.py`: caso relatado pelo usuário (3ª
      competência dentro do limite → aceita), alta além da 3ª competência (bloqueia),
      procedimento com o atributo 054 (mantém limite de 2 competências).
- [x] Caso relatado provado vermelho sem o fix (mesma mensagem de erro do usuário).

## Impacto no formato do export

Nenhum — esta tarefa não toca `apac_extract/` nem `ApacModel`. Golden files inalterados
(`git diff` vazio em `backend/core/tests/domain/services/export/golden/`).

## Verificação

- `cd backend/core && python -m pytest` — 36/36 (era 33/33).
- `cd backend/src && python manage.py test` — 74/74.
- `bash scripts/verify.sh` — 4/4 gates verdes.
- `git diff` nos golden files: vazio.

## Critério de aceite

- [x] Caso do usuário (procedimento 07/07/2026, alta 02/09/2026, procedimento sem o
      atributo 054) não é mais bloqueado.
- [x] Procedimento com `fixed_validity_two_competences=True` continua bloqueando alta
      além de 2 competências (regressão evitada).
- [x] Gates verdes, golden file inalterado.

## Ao concluir

- Marcar como `done` em `INDEX.md`.
