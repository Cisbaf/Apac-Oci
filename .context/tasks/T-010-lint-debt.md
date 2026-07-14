# T-010 — Débito de lint do frontend — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-001
- **Branch:** `refactor/T-010-lint-debt`

> Stub. O frontend nunca teve ESLint configurado; a T-001 adicionou `eslint.config.mjs` (`next/core-web-vitals` + `next/typescript`) para o gate de lint funcionar, e isso revelou ~81 erros pré-existentes (variáveis/imports não usados, `any` explícito, `display-name` em componentes anônimos). Expandir com `/tarefa T-010`.

## Objetivo (rascunho)
Zerar o débito de lint acumulado para que `npm run lint` fique verde sem exceções amplas, sem mudar comportamento do app.

## Direção
- Rodar `cd frontend && npm run lint` para a lista atual.
- Considerar corrigir em lotes por diretório (menor risco de PR gigante) em vez de um PR só.
- Não usar `eslint-disable` em massa como atalho — corrigir a causa (remover import morto, tipar em vez de `any`, etc.), exceto onde for justificável caso a caso.

## Aceite (rascunho)
- [ ] `cd frontend && npm run lint` sem erros (warnings podem ser tratados à parte, ex.: `react-hooks/exhaustive-deps`).
- [ ] Nenhuma mudança de comportamento do app.
