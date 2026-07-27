# T-019 — Trava o vínculo faixa↔APAC na UI do admin

- **Fase:** 0 · **Status:** done · **Depende de:** T-006
- **Branch:** `refactor/T-019-admin-lock-vinculo-faixa`

## Objetivo
Fechar o vetor de orfanamento de APAC aprovada que sobrou na UI do admin, depois
que a T-018 fechou o vetor de corrida na aprovação. Mesmo sintoma
(APAC `approved` sem faixa ⇒ invisível ao export ⇒ risco de glosa), outro
caminho: edição direta do campo `apac_request` pela tela de faixas.

## Contexto / porquê
`ApacBatchModel.apac_request` é o vínculo entre a faixa e a APAC que a consumiu.
Ele só deve ser criado pelo `ApprovedApacRequestUseCase`, na aprovação. Com o
campo editável no admin, um superuser podia:

- **limpar** o vínculo → a APAC continua `approved` mas perde a faixa, e o export
  não a enxerga mais;
- **reapontar** para outra APAC → orfana a APAC anterior, mesmo efeito.

Isso é exatamente a regra de ouro da `architecture.md` sendo furada: mudança de
estado de negócio acontecendo pela tela, sem passar pela camada Application.

## O que a tarefa dizia × o que era verdade

A descrição original no `INDEX.md` apontava **dois** vetores (`ApacBatchAdmin` e
`ApacBatchInline`) e pedia `max_num=1` no inline. Investigando o comportamento
real do Django, só um dos dois existia:

| Superfície | Descrição original | Verificado |
|---|---|---|
| `ApacBatchAdmin` (tela avulsa "Lotes Apac") | vetor | ✅ **real** — `apac_request` era um `ModelChoiceField` editável para superuser, confirmado inspecionando `get_form().base_fields` |
| `ApacBatchInline` (dentro da tela da APAC) | vetor | ❌ **não era** — o Django troca a FK para o pai por um `InlineForeignKeyField` com `HiddenInput`, amarrado à APAC da tela; não é escolhível |
| `max_num=1` no inline | correção pedida | ❌ **no-op** — como `apac_request` é `OneToOneField` (unique), o `inlineformset_factory` já força `max_num=1`; confirmado: `formset.max_num == 1` antes de qualquer mudança |

Marcar `apac_request` como readonly no inline também foi testado e é inócuo (o
formset monta igual, o campo continua `InlineForeignKeyField`) — ou seja, seria
uma mudança que *parece* correção sem corrigir nada. Não foi feita.

## O que foi feito
`backend/src/apac_batch/admin.py` — `ApacBatchAdmin.get_readonly_fields` passa a
devolver `['apac_request']` para superuser, em vez de `[]`. Para não-superuser
nada muda (já era tudo readonly). Comentário no código explica o porquê e aponta
para T-018/T-020, para ninguém "destravar por conveniência" depois.

`backend/src/apac_request/admin.py` — `ApacBatchInline` ganha `max_num = 1`
**explícito** e um comentário registrando que a proteção do vínculo aqui vem do
próprio Django, não deste arquivo. É documentação da invariante, não correção:
serve para o próximo que olhar não repetir a investigação, e para o dia em que
alguém mudar o tipo do campo.

### Decisão de escopo: T-019 trava, T-020 repara
Travar o campo remove o único caminho de reparo manual de faixa órfã que existia
pela UI. Decisão tomada com o usuário: **fechar o vetor de dano agora** (é bug de
produção ativo) e deixar a reatribuição para a T-020, por caminho controlável
(management command / use case), coerente com a regra de ouro — e não por edição
livre de FK numa tela. Entre este PR e a T-020, reparo de órfã é via shell/DBA.

## Verificação
5 testes novos em `backend/src/apac_batch/tests.py`:

- `ApacBatchAdminLinkLockTests` (3) — superuser e admin comum não editam
  `apac_request`; e o efeito prático, que o campo não chega a aparecer em
  `get_form().base_fields`.
- `ApacBatchInlineLinkLockTests` (2) — fixam a invariante que o Django garante
  (`InlineForeignKeyField` oculto, `max_num == 1`), para que uma mudança futura
  no inline ou no tipo do campo não reabra o vetor em silêncio.

**Testes confirmados vermelhos sem o fix** (revertendo `get_readonly_fields`
temporariamente): `AssertionError: 'apac_request' not found in []` e
`'apac_request' unexpectedly found in {...}`. Os 2 testes do inline passam nos
dois estados — são guardas de invariante, e isso está dito na docstring deles em
vez de fingir cobertura.

`apac_batch`: 29/29 (24 anteriores + 5 novos). `bash scripts/verify.sh` 4/4 verde.

## Aceite
- [x] `apac_request` readonly para todos, inclusive superuser, na tela de faixas.
- [x] Efeito prático verificado (campo fora de `base_fields`), não só a lista de
      readonly.
- [x] Invariante do inline coberta por teste, com honestidade sobre o que o
      Django já garantia.
- [x] Testes provados vermelhos sem o fix.
- [x] Nenhuma mudança de comportamento para não-superuser.
- [x] Golden file do export inalterado (não toca export).

## Achado registrado, não corrigido
`batch_number` e `export_date` continuam editáveis por superuser nas duas
superfícies — e `batch_number` é o número da APAC que vai para o arquivo
exportado. Registrado como **T-031**, fora do escopo desta tarefa.
