# T-301 — Namespace API v2 + infra de feature flag — STUB

- **Fase:** 3 · **Status:** todo · **Depende de:** Fase 2
- **Branch:** `refactor/T-301-api-v2-flags`

> Stub. Expandir com `/tarefa T-301` quando iniciar.

## Objetivo (rascunho)
Criar a base para a migração das ferramentas do admin para o React sem quebrar o legado: um namespace `/api/v2/` e um mecanismo de feature flag por rota/ambiente.

## Direção
- Definir convenção de URLs v2 e como convivem com as atuais.
- Infra de flag (env/config) que liga a superfície nova mantendo a antiga como fallback.
- Documentar em `architecture.md` (namespace de convivência).

## Aceite (rascunho)
- [ ] v2 responde; legado intacto; flag controla qual o frontend usa.
