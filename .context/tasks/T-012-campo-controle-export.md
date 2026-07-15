# T-012 — Campo de controle do export hardcoded (`cbc-smt-vrf`)

- **Fase:** 0 · **Status:** doing · **Depende de:** T-002
- **Branch:** `refactor/T-012-campo-controle-export`

## Contexto / porquê
O documento oficial do layout (seção final, "OBS - Calculo do campo de
controle") define uma fórmula para `campo_controle` (`HeaderModel`, posições
020-023):
1. Somar o código de todos os procedimentos + quantidade + número da APAC.
2. Obter o resto da divisão do resultado por 1111.
3. Somar 1111 ao resto (domínio final: [1111..2221]).

O código atual (`controller.py`, método `header()`) sempre envia o literal
`"1810"`, independente do conteúdo real do lote exportado.

## Decisão do usuário (confirmada em sessão)
O campo é **recalculado automaticamente pelo próprio APAC Magnético** depois da
importação — por isso nunca causou problema do jeito que está hoje (`"1810"`
fixo). Não é crítico para o SIA aceitar o arquivo.

**Escopo desta tarefa:** desenvolver o cálculo da fórmula oficial como função
pura, isolada, **sem ligar ao fluxo real de export ainda** — fica disponível
para uso futuro, quando o usuário decidir ativá-la. O golden file (T-002) e o
`controller.py` **não são alterados** nesta tarefa.

## O que foi feito
- Nova função pura `calculate_control_field(procedures, apac_numbers)` em
  `backend/core/src/apac_core/domain/services/apac_extract/control_field.py`
  — recebe `[(código_procedimento, quantidade), ...]` e `[número_apac, ...]`,
  aplica a fórmula do spec (soma → resto mod 1111 → +1111) e retorna o
  `campo_controle` como string. Zero dependência de Django, testável isolada.
- Testes em
  `backend/core/tests/domain/services/apac_extract/test_control_field.py`
  (6 casos): soma zero, resto zero, resto máximo (limites do domínio
  [1111..2221]), soma com código+quantidade+número da APAC, múltiplos
  procedimentos/múltiplas APACs, e um cenário com dados reais dos fixtures do
  golden file da T-002 (só para validar a fórmula com dados realistas — não é
  o valor que o export de produção emite hoje).
- `controller.py` (`header()`) **não foi tocado** — `campo_controle` continua
  `"1810"` fixo no fluxo real de export.
- Golden file (T-002) **inalterado** — confirmado via `git diff` vazio nos
  arquivos de `tests/domain/services/export/golden/`.

## Como ativar no futuro (não faz parte desta tarefa)
Quando o usuário quiser usar o cálculo de verdade: chamar
`calculate_control_field` dentro de `ExportApacBatchController.header()`,
passando os pares `(cod_procedimento, quantidade)` de todos os procedimentos
(principal + subprocedimentos) de todos os `apac_batchs` do lote, e os
`batch_number` de cada `ApacBatch`. Isso muda o conteúdo do arquivo exportado
— exige atualizar o golden file **de propósito**, com justificativa explícita
no PR, conforme a regra de ouro do `CLAUDE.md`.

## Aceite
- [x] Fórmula oficial implementada como função pura, testável isoladamente.
- [x] Não ligada ao fluxo real de export — `campo_controle` continua `"1810"`.
- [x] Golden file inalterado.
- [x] `bash scripts/verify.sh` — todos os 4 gates verdes.
