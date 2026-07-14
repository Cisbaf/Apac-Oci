# T-201 — Transições de estado via use case (admin incluso) — STUB

- **Fase:** 2 · **Status:** todo · **Depende de:** T-006, T-103
- **Branch:** `refactor/T-201-state-usecases`

> Stub. Expandir com `/tarefa T-201` quando a Fase 1 estiver concluída, lendo o código já refatorado.

## Objetivo (rascunho)
Garantir que **toda** transição de estado de negócio (aprovar, rejeitar, mudar status, atribuir/trocar faixa) passe por use case — admin e React usando os mesmos.

## Direção
- Auditar todos os pontos que mudam `status` ou `apac_batch` e roteá-los para use cases.
- Onde faltar use case (ex.: troca manual de faixa), criar.
- Consolidar o que T-006 começou no admin.

## Aceite (rascunho)
- [ ] Nenhuma mutação de estado de negócio fora da camada Application.
- [ ] Golden file inalterado; testes verdes.
