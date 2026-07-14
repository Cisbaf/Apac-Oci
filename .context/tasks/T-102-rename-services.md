# T-102 — Renomear `controllers/` → `services/` (frontend)

- **Fase:** 1
- **Status:** todo
- **Depende de:** Fase 0 concluída
- **Branch:** `refactor/T-102-rename-services`

## Objetivo
Remover a segunda colisão da palavra "controller": no frontend, `extracao/controllers/` são wrappers de `fetch`, não controllers.

## Contexto / porquê
Ver `../conventions.md`. Padroniza a camada de acesso à API do frontend com um nome coerente (`services/` ou `api/`).

## Escopo
- Renomear `frontend/src/app/extracao/controllers/` → `services/` (ou `api/`, escolher e padronizar com o resto do frontend — `solicitar` já usa `services/`, então **use `services/`**).
- Atualizar imports.
- Renome mecânico, sem mudança de comportamento.

## Fora de escopo
- Refatorar a lógica dos serviços.

## Arquivos prováveis
- `frontend/src/app/extracao/controllers/*` → `services/*`
- `frontend/src/app/extracao/**` (imports), `hooks`, `page.tsx`

## Critério de aceite
- [ ] Não há mais pasta `controllers/` no frontend.
- [ ] Testes/lint verdes; comportamento idêntico.

## Verificação
- `bash scripts/verify.sh` verde.

## Ao concluir
- Atualizar `conventions.md`.
