# T-015 — Teste de integração para o fluxo de solicitação de APAC

- **Fase:** 0 · **Status:** done · **Depende de:** T-009
- **Branch:** `refactor/T-015-integration-test-apac-request`

## Objetivo
Cobrir com teste de integração o caminho que faltava desde a T-009: a
submissão da APAC em `ApacRequestFinishForm` (`finishFormApacRequest.tsx`) —
adaptação dos dados do formulário, POST em `/api/proxy/apac_request/api`,
tratamento da resposta (`showResponseApi`) e redirecionamento
(`/visualizar?id=...`).

## Decisão de escopo
Entre as duas opções do rascunho (isolar `ApacRequestFinishForm` vs. montar o
fluxo completo via `page.tsx`), optei por **isolar o `ApacRequestFinishForm`**:
- `useFormRequest()` é mockado diretamente (mesmo padrão já usado em
  `ApacProgressStepper.test.tsx`), controlando `getValues()` para retornar um
  `RequestForm` válido — sem precisar montar o wizard completo de steps.
- As subforms renderizadas em modo `disabled` dentro do `ApacRequestFinishForm`
  (`IdentifyEstablishmentForm`, `IdentifyPatientForm` etc.) dependem de
  `useRequestData()`/CADSUS, que não são o alvo deste teste — substituídas por
  stubs nomeados (`jest.mock`) só para não precisarem desses contextos.
- `ConfirmButton` exige "pressione e segure" com temporizadores reais; vira um
  botão comum que chama `onConfirm` no clique, para não depender de timing de
  hold no teste.
- `GlobalComponentsProvider` real (não mockado) — mesma escolha já usada no
  teste do `ApacProgressStepper`, garante que `showResponseApi`/`showBackdrop`
  se comportam como em produção.

Montar o fluxo completo via `page.tsx` navegando pelos 5 steps teria mais valor
de realismo, mas exigiria mockar `ApacRequestFetchApi` (fetch inicial),
`useRequestData` com estabelecimentos/procedimentos reais e todos os
validadores de CEP/idade da `ApacProgressStepper` — custo bem mais alto para o
mesmo objetivo (caminho feliz do envio). Registrar como extensão futura se um
dia o resto do wizard (steps 1-4) precisar de cobertura própria.

## O que foi feito
Novo arquivo `frontend/src/app/solicitar/apacRequest/__tests__/ApacRequestFinishForm.test.tsx`,
3 testes:
1. **Submissão com sucesso** — confirma que o payload enviado ao
   `fetch('/api/proxy/apac_request/api', ...)` tem as datas convertidas
   (`procedure_date`/`discharge_date` de dd/mm/yyyy para yyyy-mm-dd) e os
   subprocedimentos adaptados para snake_case, só os marcados (`checked:
   true`); e que o redirecionamento (`router.push('/visualizar?id=...')`)
   acontece com o `apac_request_id` da resposta.
2. **Falha da API** — não redireciona; o erro (`json.message`) aparece via
   `showResponseApi`/`GlobalAlert`.
3. **`diagnosticDate` vazio** — vai como `null` no payload (comportamento
   deliberado do código, distinto do achado abaixo).

### Achado registrado, não corrigido: T-033
Caracterizando o comportamento real da submissão, `apacData.diagnosticDate`
**não** passa por `formatDateToISO` — a linha está comentada no código-fonte
(`finishFormApacRequest.tsx`) — diferente de `procedureDate`/`dischargeDate`/
`patientBirthDate`, que são convertidos. Quando preenchida, a API recebe a
data crua em dd/mm/yyyy. O teste 1 caracteriza esse comportamento real (não o
que "deveria ser"), com comentário explicando. Achado registrado como
**T-033**, fora do escopo desta tarefa (teste não corrige comportamento, só
descreve o que existe).

### Infra de teste corrigida no caminho
`structuredClone` (usado em `finishFormApacRequest.tsx` para clonar os valores
do form antes de adaptá-los) não existe no ambiente `jest-environment-jsdom`
mesmo com Node com suporte nativo — qualquer teste que exercitasse esse
caminho quebraria. Adicionado polyfill mínimo (JSON deep clone, suficiente
para dados de formulário) em `frontend/.jest/setup.ts`, compartilhado por
todos os testes.

### Achado registrado durante a sessão, não desta tarefa: T-032
Pedido do usuário no meio da sessão (botão de auto-preenchimento fake em modo
desenvolvimento) registrado como tarefa própria para não misturar com o
escopo de teste da T-015.

## Verificação
- `cd frontend && npm test`: 6 suítes, 34/34 (era 5 suítes/31 antes desta
  tarefa).
- `cd frontend && npm run lint`: sem novos erros (só os warnings
  pré-existentes de `react-hooks/exhaustive-deps`, fora de escopo desde
  T-010).
- `bash scripts/verify.sh`: 4/4 verde.
- Nenhuma mudança em código de produção do fluxo de solicitação além do
  polyfill de teste em `.jest/setup.ts`. Golden file do export inalterado
  (não toca export).

## Aceite
- [x] Teste de integração cobrindo o caminho feliz do envio de APAC.
- [x] Cobre também o caminho de falha da API (não estava no aceite mínimo do
      stub, adicionado por ser o par natural do caminho feliz).
- [x] `cd frontend && npm test` verde.
