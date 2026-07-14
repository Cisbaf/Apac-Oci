# T-008 — Corrigir teste quebrado em backend/src — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-001
- **Branch:** `refactor/T-008-fix-src-tests`

> Stub. Descoberto ao rodar `bash scripts/verify.sh` pela primeira vez (T-001). Expandir com `/tarefa T-008`.

## Objetivo (rascunho)
Destravar o gate `backend/src (manage.py test)`, hoje vermelho antes de qualquer mudança de comportamento intencional.

## Direção
- `apac_request.tests.ApacApprovalTests.test_success_with_available_batch` espera `200` e recebe `403` — investigar se é regressão de permissão/autenticação ou o teste está desatualizado em relação à regra atual.
- Observado nível de flakiness entre execuções (às vezes 1, às vezes 2 falhas no mesmo teste/variante `_for_adm`) — pode depender de data/competência corrente; investigar dependência de tempo.

## Aceite (rascunho)
- [ ] `cd backend/src && python manage.py test` verde e estável (rodar mais de uma vez).
- [ ] Nenhuma mudança de comportamento de negócio sem que a tarefa diga isso explicitamente.
