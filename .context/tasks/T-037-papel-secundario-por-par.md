# T-037 — Papel e quantidade máxima do secundário são do par, não do procedimento

- **Fase:** 0
- **Status:** done
- **Depende de:** T-035
- **Branch:** `refactor/T-037-papel-secundario-por-par`

## Objetivo
Guardar "obrigatório" e "quantidade máxima" no vínculo principal×secundário, como
o SIGTAP faz, em vez de no procedimento.

## Contexto / porquê
`ProcedureModel.mandatory` é um booleano **do procedimento**. O SIGTAP guarda a
informação **do par**, em `S_PAPA` (`PAPA_TRAT`, `PAPA_QTMAX`). A diferença não é
teórica — nas 10 OCIs novas:

**6 secundários têm papel divergente** entre OCIs:

| Secundário | Obrigatório em | Compatível em |
|---|---|---|
| `020208003` | `090801002` | `090801001`, `090801003`, `090801005`, `090801007`, `090801008` |
| `020208011` | `090801002` | `090801003`, `090801005`, `090801007`, `090801008` |
| `020208013` | `090801002` | `090801001`, `090801003`, `090801005`, `090801007`, `090801008` |
| `020208025` | `090801002` | `090801005`, `090801007`, `090801008` |
| `020302003` | `090801008` | `090801002`, `090801005`, `090801006`, `090801007` |
| `020602003` | `090801001` | `090801006` |

**5 secundários têm quantidade máxima divergente** entre as duas OCIs de Saúde
Bucal (ex.: `030704011` aceita 2 em `090701001` e 1 em `090701002`).

Com um booleano por procedimento não há resposta certa: marcar `020208003` como
obrigatório passa a exigi-lo em 5 OCIs onde ele é só compatível; não marcar deixa
`090801002` incompleta. A crítica correspondente é
`PROC.PRINC(...) EXIGE PELO MENOS (00N) PROC. SECUNDARIO OBRIGATORIO`.

Hoje nada disso é validado no sistema — a crítica só aparece no APAC Magnético,
depois que o município já fechou a competência.

## Escopo (o que fazer)
- Trocar o M2M `ProcedureModel.parents` por um `through` explícito com
  `mandatory` e `max_quantity` (migration preservando os vínculos existentes).
- Estender `sigtap_auditar` para conferir também papel e quantidade do par.
- Avaliar (com o usuário) se o formulário passa a **validar** ou apenas **avisar**
  — validar muda o comportamento para o município e merece decisão explícita.

## Fora de escopo
- CID de causas associadas — T-036.
- Os atributos de grupo "ou" (064, 067, 068, 069, 070, 071), que não são
  expressáveis como par simples: pedem um grupo de alternativas. Registrar como
  tarefa própria se for necessário validá-los no sistema.

## Arquivos prováveis
- `backend/src/procedure/models.py` — through model + migration
- `backend/src/procedure/management/commands/sigtap_auditar.py` — conferir o par
- `backend/core/src/apac_core/domain/entities/procedure.py` — entidade

## Critério de aceite
- [x] `020208003` consta obrigatório em `090801002` e compatível nas outras 5
- [x] `030704011` consta com quantidade 2 em `090701001` e 1 em `090701002`
- [x] `sigtap_auditar` acusa divergência de papel e de quantidade
- [x] Golden file do export inalterado

## O que foi feito

Novo modelo `ProcedureSecondary` (`parent`, `child`, `mandatory`, `max_quantity`,
`unique_together`), substituindo o M2M simples `ProcedureModel.parents` e o
campo `ProcedureModel.mandatory`. Três migrações em sequência para não perder
dado:
1. `0027` — cria `ProcedureSecondary` (tabela nova, nada mexido ainda).
2. `0028` — `RunPython` copia cada par do M2M antigo para o modelo novo,
   herdando `mandatory` do antigo `ProcedureModel.mandatory` do filho (melhor
   sinal disponível até o `sigtap_auditar` corrigir por par) e `max_quantity`
   vazio (nunca existiu essa informação no cadastro manual). Reversível.
3. `0029` — remove `mandatory` e `parents` de `ProcedureModel` (dropa a tabela
   M2M antiga).

Todos os consumidores do M2M antigo foram migrados para o modelo novo:
`ProcedureModel.to_entity` (via `secondary_links`), `views.py` (lista de
principais = `parent_links__isnull=True`), `controller.py` (`save`, dead code
em produção — nenhuma view chama, confirmado por grep), `admin.py` (filtros +
`ProcedureSecondaryInline` no lugar do widget M2M, que **não** funciona com
through-model com campos extras — limitação conhecida do Django Admin),
`sigtap_auditar.py` e `apac_request/tests.py`.

`sigtap_auditar` estendido: além de ausência/sobra de secundário, agora compara
`mandatory` e `max_quantity` do par contra o SIGTAP e corrige com `--aplicar`.

`ProcedureSerializer.get_children` injeta `mandatory`/`max_quantity` do
`ProcedureSecondary` em cada filho — o formulário recebe o valor certo por
contexto de principal, sem mudar o formato do JSON que já consumia
(`mandatory: boolean` por item de `children`); `max_quantity` é aditivo.

**Decisão explicitamente NÃO tomada nesta tarefa:** o escopo original pedia
avaliar se o formulário passa a *validar* (bloquear envio sem os obrigatórios)
ou continua só *avisando*. Perguntei ao usuário, que confirmou manter o
comportamento atual — nenhuma validação nova no backend. Correção sobre o que
esse "atual" realmente é (só descoberto testando no navegador, ver abaixo): o
frontend **já bloqueia**, via `required` nativo do checkbox +
`validateSubProcedures.ts` ("O procedimento obrigatório ... não foi
selecionado!") — não é um aviso, é enforcement client-side. O que não existe é
validação no **backend**; isso continua assim, por decisão do usuário.

## Bug achado e corrigido testando em ambiente de dev real

O golden test (fixture sintética) não pegou isto porque não reflete uma
particularidade real do SIGTAP. Rodando o stack completo (`docker-dev`,
`docker-compose.dev.yml`) e testando a OCI `0908010028` no navegador, um dos 6
secundários obrigatórios (`020208025`, Exame Micológico Direto) apareceu como
`required: false` — 5 obrigatórios, não 6.

Causa raiz: `S_PAPA` às vezes lista o **mesmo par** (principal, secundário)
**duas vezes** — uma `TRAT=01`, outra `TRAT=95` (confirmado: `090801002` ×
`020208025`, mais dois pares em `090801008`). `extrair.py` tratava cada linha
isoladamente; `sigtap_auditar.py` indexava por `codigo_dv` num dict — quem
processasse "compativeis" por último apagava o "obrigatório" de "obrigatorios".
Corrigido em `extrair.py` (commit `43aeb0b`): agrupa por par antes de separar,
obrigatório vence. Teste de regressão em `scripts/sigtap/tests/test_extrair.py`
(commit `2f8052b`) trava os dois sentidos de ordenação.

Reaplicado no container de dev rodando: os 3 pares afetados corrigidos: agora
6/6 obrigatórios com `required: true`. Confirmado ponta a ponta — formulário
até o fim, POST 200, registro persistido com `secondary_cid=A162` e os 6
secundários corretos.

## Verificação
- Gates: `bash scripts/verify.sh` verde (72 testes `backend/core`, suite
  completa `backend/src`, 34 testes frontend, lint sem erros novos) — antes e
  depois da correção do bug do par duplicado.
- Migração preserva os 173 vínculos existentes (173 → 173, contado antes/depois
  numa cópia gravável do banco).
- `sigtap_auditar` nas 10 OCIs novas: 198 divergências de papel/quantidade
  (invisíveis antes desta tarefa) → 0, idempotente.
- Golden files do export **inalterados** (`git diff` vazio) — o export nunca
  leu `mandatory`, só `ProcedureRecord`/`ApacData.sub_procedures`.
- **Teste manual em ambiente real** (`docker-dev`, competência 202608):
  solicitação completa da OCI `0908010028` — 6 secundários obrigatórios
  corretos, CID de causas associadas exibido e persistido, POST 200,
  `ApacDataModel` conferido direto no banco do container.
