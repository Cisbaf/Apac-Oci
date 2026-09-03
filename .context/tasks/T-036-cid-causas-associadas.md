# T-036 — CID de causas associadas (atributo SIGTAP 043) não tem onde ser guardado

- **Fase:** 0
- **Status:** todo
- **Depende de:** T-035
- **Branch:** `refactor/T-036-cid-causas-associadas`

## Objetivo
Permitir registrar o segundo CID que as 8 OCIs de Infectologia exigem, para que
essas APACs deixem de ser rejeitadas pelo SIA.

## Contexto / porquê
**Esta tarefa bloqueia o faturamento das 8 OCIs de Infectologia.** Sem ela, o
cadastro pode estar perfeito e a APAC ainda assim é rejeitada.

Os 8 procedimentos `09.08.01.001-0` a `09.08.01.008-7` carregam o atributo
complementar **043 — Exige CID de causas associadas** (confirmado em `S_PADET`
da competência 202608). A Portaria SAES/MS Nº 4.306/2026, Art. 2º §2º, manda
registrar dois CIDs: o principal (HIV/aids: B20–B24, B23.0, B23.1, Z21 — os 8 que
o `S_PACID` aceita com `PACID_PRIN='S'`) **e** o CID secundário da síndrome que
motivou o atendimento.

O APAC Magnético cobra os dois. No teste de 02/09/2026, todas as 8 OCIs de
Infectologia tomaram `EXIGE CID CAUSAS ASSOC.CONF.PT/GM 584 DE 15/5/15`.

Hoje `ApacDataModel` tem **um** campo `cid` (`apac_data/models.py:65`), que
alimenta o `apa_cidpri`. Não há onde guardar o segundo.

**O layout do arquivo já tem o campo — ele é escrito vazio.** Três lugares em
`domain/services/apac_extract/` reservam a posição e recebem `""` fixo:
- `controller.py:76` → `cid_causas_associadas=""`
- `controller.py:108` → `apa_cidsec=""`
- `apac_procedure.py:29` → `cid_secundario` com default `""`

Ou seja: **não é mudança de layout, é preencher um campo que já existe.** O
golden file só muda para APACs que de fato tenham o segundo CID preenchido.

## Escopo (o que fazer)
- `ApacDataModel.secondary_cid` — FK nullable para `CidModel` (nullable porque só
  as OCIs com atributo 043 exigem).
- Distinguir, no vínculo CID×procedimento, quais CIDs são principais e quais são
  de causas associadas — hoje `CidModel.procedure` é um M2M plano e foi
  exatamente essa indistinção que fez o teste escolher `A16.2` como principal.
- Propagar até o export (`apa_cidsec` e `cid_causas_associadas`).
- Frontend: segundo campo de CID no formulário, exibido quando o procedimento
  principal exigir.
- Semear os CIDs de causas associadas de `scripts/sigtap/cids_causas_associadas.json`
  (128 CIDs das 8 OCIs, preservados na T-035).

## Fora de escopo
- Papel/quantidade por par principal×secundário — T-037.
- Validar clinicamente a lista de CIDs secundários: ela vem da portaria e já está
  no JSON preservado.

## Arquivos prováveis
- `backend/src/apac_data/models.py` — campo novo + migration
- `backend/src/procedure/models.py` — distinguir papel do CID
- `backend/core/src/apac_core/domain/entities/apac_data.py` — entidade
- `backend/core/src/apac_core/domain/services/apac_extract/controller.py` — preencher
- `frontend/` — campo no formulário
- `backend/core/tests/domain/services/export/golden/` — golden novo para o caso com 2 CIDs

## Critério de aceite
- [ ] APAC de OCI de Infectologia com os dois CIDs exporta `apa_cidsec` preenchido
- [ ] APAC sem o segundo CID exporta exatamente como hoje (golden atual intacto)
- [ ] O formulário só cobra o segundo CID nos procedimentos com atributo 043
- [ ] Validador não acusa mais `EXIGE CID CAUSAS ASSOC` nas 8 OCIs

## Verificação
- Gates: `bash scripts/verify.sh` verde.
- Golden file atual **inalterado** (o campo novo entra vazio quando não usado).
- Reteste no `apac-magnetico-validador` com a competência 202608a.
