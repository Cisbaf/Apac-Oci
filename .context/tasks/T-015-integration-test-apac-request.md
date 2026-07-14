# T-015 — Teste de integração para o fluxo de solicitação de APAC — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-009
- **Branch:** `refactor/T-015-integration-test-apac-request`

> Stub. Descoberto na T-009 ao investigar `ApacRequestService.test.tsx` (removido nessa tarefa).

## Objetivo (rascunho)
O fluxo de solicitação de APAC no frontend (`ApacRequestFormProvider` + `ApacRequestFillingData` + `StepForm`/`ApacProgressStepper` + `ApacRequestFinishForm`, ver `frontend/src/app/solicitar/page.tsx`) hoje não tem nenhum teste de integração cobrindo o caminho feliz completo (preencher os steps → confirmar → `fetch('/api/proxy/apac_request/api', ...)` → redirecionar).

## Contexto (da T-009)
Existia `ApacRequestService.test.tsx`, mas testava um componente (`components/ApacRequestService`) que **nunca existiu no histórico do git** — não foi renomeado, nunca chegou a existir. O teste também assumia um contrato (`handleComplete`/`getDataRequest` como props de um componente único) incompatível com a arquitetura atual, que faz fetch direto dentro de `ApacRequestFinishForm` (`finishFormApacRequest.tsx`) usando `useFormRequest()`, `useGlobalComponents()` (backdrop/resposta) e `useRouter()`. Foi removido por ser teste morto, sem cobertura real perdida.

## Direção (rascunho)
- Escrever um teste de integração novo, mockando `fetch`, `next/navigation` (`useRouter`) e o contexto `GlobalUIContext`, cobrindo pelo menos: submissão com sucesso (redireciona para `/visualizar?id=...`) e falha da API (não redireciona, mostra erro via `showResponseApi`).
- Decidir se cobre só `ApacRequestFinishForm` isolado (mais simples, mocka `useFormRequest`) ou o fluxo completo via `page.tsx` (mais realista, mais custoso de montar).

## Aceite (rascunho)
- [ ] Teste de integração cobrindo o caminho feliz do envio de APAC.
- [ ] `cd frontend && npm test` verde.
