# T-043 — Regra PMAE derivada do atributo 053, nas duas camadas

- **Fase:** 0
- **Status:** doing
- **Depende de:** T-042
- **Branch:** `refactor/T-043-regra-pmae-derivada`

## Objetivo
Trocar o cadastro manual da consulta obrigatória, OCI por OCI, por uma regra
derivada do atributo SIGTAP 053 — que também cobra o mínimo de dois
secundários, e que vale na API, não só no formulário.

## Contexto / porquê
A T-042 cadastrou o grupo da consulta nas 8 OCIs de Infectologia e fechou o
caso que motivou tudo. Mas o mecanismo do grupo diz "tem consulta", nunca
disse "tem dois" — e a crítica do APAC Magnético cobra as duas coisas:

```
000013  PROC.PRINC(...) PMAE EXIGE PELO MENOS 2 PROC.SEC.
        SENDO UM OBRIG.(030101007 OU 030101030)
```

Levantamento em produção (11/09/2026), simulando o menor pacote que o
formulário aceita hoje por OCI: **8 das 31 ainda passam em estado que o SIA
critica**.

| OCI | O que passava | Motivo |
|---|---|---|
| `0901010014`, `0903010011`, `0903010020`, `0903010038`, `0903010046`, `0904010015` | só a consulta (1 secundário) | consulta é `mandatory` e nada mais é obrigatório |
| `0907010016`, `0907010024` | nenhum secundário | Saúde Bucal: sem consulta vinculada e sem grupo |

As outras 23 escapavam por acidente: tinham algum exame obrigatório ou grupo
que, somado à consulta, já dava dois.

Três mecanismos diferentes cobriam a mesma regra — `ProcedureSecondary.
mandatory` em 20 OCIs (que o `sigtap_auditar --aplicar` reverteria, e que
recusa teleconsulta mesmo onde o SIGTAP aceita), `ProcedureRequirementGroup`
em 11, e nada nas 2 de Saúde Bucal. O atributo 053, que o SIGTAP declara e
todas as 46 OCIs da competência 202608a têm, é o que realmente define quem
está sujeito à regra.

## Escopo (o que fazer)
- `ProcedureModel.pmae` (atributo 053) + propagação para a entidade `Procedure`.
- `domain/services/pmae.py`: a regra como função pura — mínimo de 2
  secundários e, **se a OCI aceitar consulta ou teleconsulta**, um dos marcados
  tem que ser uma delas.
- `CreateApacRequestUseCase` passa a recusar o que viola a regra: é a camada
  que faltava, a API aceitava o que o formulário bloqueava.
- Formulário: mesma regra, com alerta proativo no mesmo estilo dos grupos.
- `sigtap_auditar` confere e corrige o 053 contra o `S_PADET`.
- Migration de dados: marca `pmae` nas OCIs cadastradas (prefixo 09) e remove
  os 11 grupos `OCI`, que passam a ser redundantes.

**Por que a exigência da consulta é condicional:** `0907010016` e `0907010024`
têm o atributo 053 mas não têm consulta médica entre os secundários no próprio
SIGTAP. Cobrá-la delas bloquearia a OCI inteira, sem nenhum secundário
disponível capaz de satisfazer. Para elas resta o mínimo de dois.

## Fora de escopo
- Migrar os 20 `ProcedureSecondary.mandatory=True` da consulta (T-044). Eles
  continuam funcionando; ficam redundantes com a regra nova, e a remoção é
  mudança de dado que merece tarefa e conferência próprias.
- Sincronizar o atributo **054** no `sigtap_auditar` (T-045). Ele também está
  fora de sincronia em produção (`0901010057` e `0901010081`), mas mexer nele
  muda a validade exportada — precisa de validação no APAC Magnético.
- Apagar os `ProcedureModel` duplicados (T-046).
- Descobrir o que a regra PMAE cobra das duas OCIs de Saúde Bucal (T-047).

## Arquivos prováveis
- `backend/core/src/apac_core/domain/services/pmae.py` — a regra.
- `backend/core/src/apac_core/domain/entities/procedure.py` — campo `pmae`.
- `.../use_cases/apac_request_cases/create_apac_request_case.py` — cobrança.
- `backend/src/procedure/models.py`, `admin.py`, migrations `0031`/`0032`.
- `backend/src/procedure/management/commands/sigtap_auditar.py` — atributo 053.
- `frontend/.../validates/validateSubProcedures.ts`, `identifySubProceduresForm.tsx`.
- `scripts/sigtap/grupos_exigencia.json` — sai o grupo `OCI`.

## Critério de aceite
- [x] OCI com o atributo recusa envio com menos de 2 secundários.
- [x] OCI que aceita consulta recusa envio sem consulta nem teleconsulta.
- [x] OCI sem consulta no SIGTAP (Saúde Bucal) exige só os 2 secundários.
- [x] A recusa acontece na API, não só no formulário.
- [x] `sigtap_auditar` marca e desmarca o campo conforme o `S_PADET`.
- [x] Migration remove os grupos `OCI` e o `reverse` os recria.
- [ ] Conferido na tela, em dev com banco local.

## Verificação
- Comportamento antes = depois? **Não, e é o ponto**: 8 OCIs deixam de aceitar
  pacote que o SIA critica. Nenhuma APAC existente muda — as 48.411 em
  produção já têm consulta, e a regra não é reavaliada em APAC gravada.
- Gates: `backend/core` 47/47, `backend/src` 83/83, `frontend` 48/48 (7
  suítes), lint sem erros, `tsc --noEmit` limpo.
- Migration testada de ida e volta sobre cópia do banco de dev: aplica (8
  grupos removidos, OCIs marcadas, nenhum não-OCI marcado por engano) e
  reverte (grupos recriados com os membros certos, `0908010044` com só a
  consulta).
- Golden files inalterados — a tarefa não toca no montador do export.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
- Deploy leva o dado junto: a migration roda no boot do container. Backup
  antes, como sempre.
