# T-037 — Papel e quantidade máxima do secundário são do par, não do procedimento

- **Fase:** 0
- **Status:** todo
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
- [ ] `020208003` consta obrigatório em `090801002` e compatível nas outras 5
- [ ] `030704011` consta com quantidade 2 em `090701001` e 1 em `090701002`
- [ ] `sigtap_auditar` acusa divergência de papel e de quantidade
- [ ] Golden file do export inalterado

## Verificação
- Gates: `bash scripts/verify.sh` verde.
- Migration preserva todos os vínculos atuais (contar antes/depois).
