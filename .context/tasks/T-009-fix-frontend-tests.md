# T-009 — Corrigir testes quebrados no frontend — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-001
- **Branch:** `refactor/T-009-fix-frontend-tests`

> Stub. Descoberto ao rodar `bash scripts/verify.sh` pela primeira vez (T-001). Expandir com `/tarefa T-009`.

## Objetivo (rascunho)
Destravar o gate `frontend (jest)`, hoje vermelho antes de qualquer mudança de comportamento intencional.

## Direção
- `ApacRequestService.test.tsx` falha ao carregar: importa `@/app/solicitar/apacRequest/components/ApacRequestService`, módulo que não existe no caminho atual — checar se foi movido/renomeado e ajustar o import do teste.
- `VerificationService.test.tsx` (`checkAgeProcedureAlert`) espera chamada para `/api/proxy/procedure/apac/check-age-alert/` (com barra final) mas o código chama sem a barra — decidir qual é o comportamento correto (código ou teste) sem alterar contrato de API sem necessidade.

## Aceite (rascunho)
- [ ] `cd frontend && npm test` verde.
- [ ] Nenhuma mudança de comportamento observável do app sem que a tarefa diga isso explicitamente.
