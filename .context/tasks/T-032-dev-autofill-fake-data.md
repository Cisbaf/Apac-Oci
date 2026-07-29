# T-032 — Botão de auto-preenchimento fake em desenvolvimento — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** —
- **Branch:** `refactor/T-032-dev-autofill-fake-data`

> Stub. Pedido pelo usuário durante a T-015, registrado para não misturar com o
> escopo de teste da T-015.

## Objetivo (rascunho)
Botão visível **só em desenvolvimento** na tela `/solicitar` que preenche todo o
formulário (`RequestForm`, todos os steps) com dados fake, para acelerar teste
manual e demonstrações — sempre no formato correto (mesmas validações que um
preenchimento manual passaria).

## Contexto
Já existe `frontend/src/app/solicitar/apacRequest/utils/dataFakes.ts`
(`fakeRequestForm`/`fakeDataRequestFillingPart`) com um `RequestForm` fake
completo, mas:
- usa **IDs fixos** (`mainProcedureId: 231`, `establishmentId: 2`, `cidId: 6`)
  que só existem se o banco do ambiente tiver exatamente esses registros —
  não é portável entre ambientes (dev local × outro banco de teste);
- está listado na T-401 como candidato a **remoção** (código morto, não usado
  em produção hoje).

Não reaproveitar como está. O botão precisa montar os dados a partir do que
está realmente carregado em `useRequestData()` (`procedures`/`establishments`
reais do ambiente), sorteando entre as opções disponíveis, e gerando
CPF/CNS com dígito verificador válido (ver `CpfField`/`CnsField` em
`apac_core` para a regra de validação, e os validadores espelhados no
frontend em `schemas/`).

## Decisão de escopo (com o usuário)
- Botão **global**, não um por `StepForm`: preenche o `RequestForm` inteiro de
  uma vez (não step a step).
- Só aparece em modo desenvolvimento (avaliar `process.env.NODE_ENV !==
  'production'` ou flag equivalente já usada no projeto).

## Direção (rascunho, a refinar em `/tarefa T-032`)
- Onde plugar: `ApacProgressStepper` (topo) ou `page.tsx`, com acesso a
  `useFormRequest()` (para `setValue`/`reset`) e `useRequestData()` (para
  sortear estabelecimento/procedimento/CID reais).
- Sub-procedimentos: sortear a partir de `procedure.children` do procedimento
  principal sorteado (mesma lógica que `FormApacRequest.tsx` já usa ao trocar
  de procedimento principal).
- CPF/CNS: gerar com dígito verificador válido, não reaproveitar string fixa.
- Decidir se usa uma lib de dados fake (ex. `@faker-js/faker`, que ainda não é
  dependência do projeto — avaliar necessidade antes de adicionar) ou gerador
  próprio, dado que nome/dados de paciente não precisam ser realistas, só os
  campos com validação de formato (CPF/CNS/CBO/CEP) precisam ser válidos.

## Aceite (rascunho)
- [ ] Botão só visível fora de produção.
- [ ] Preenche todos os steps com um clique, usando dados reais carregados
      (não IDs fixos).
- [ ] Dados gerados passam nas mesmas validações que preenchimento manual.
- [ ] Não introduz nenhum caminho nesse botão que rode em produção.
