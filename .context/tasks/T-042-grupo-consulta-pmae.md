# T-042 — Grupo da consulta PMAE nas 8 OCIs de Infectologia

- **Fase:** 0
- **Status:** doing
- **Depende de:** T-040
- **Branch:** `refactor/T-042-grupo-consulta-pmae`

## Objetivo
Fazer o formulário exigir consulta ou teleconsulta nas 8 OCIs de Infectologia,
como já acontece nas demais OCIs — hoje elas aceitam solicitação que o APAC
Magnético critica.

## Contexto / porquê
Achado em 11/09/2026 respondendo à dúvida de um município ("posso faturar a
OCI inicial de síndrome respiratória só com a tomografia?"). A resposta pelas
tabelas do SIGTAP era "sim" — a tomografia de tórax é o único secundário
obrigatório da `0908010010`. O validador real disse o contrário:

```
000013  PROC.PRINC(0908010010) PMAE EXIGE PELO MENOS 2 PROC.SEC.
        SENDO UM OBRIG.(030101007 OU 030101030)
```

É a regra PMAE (atributo complementar SIGTAP **053**, Portaria SAES/MS Nº
2.331/2024), já conhecida no projeto: foi ela que motivou o grupo
`attribute_code="OCI"` criado para GIN3 (`0906010055`), nasofaringe/orofaringe
(`0904010031`) e câncer gástrico (`0901010073`). As 8 OCIs de Infectologia
ficaram de fora — nelas a consulta é só `ProcedureSecondary` compatível, e
nada impede o envio sem ela.

**A regra não está em tabela nenhuma do SIGTAP.** Em `S_PAPA` a consulta é
`PAPA_TRAT=01` (compatível); `S_PADET` só diz que o procedimento é PMAE (053),
sem a quantidade nem os códigos. Por isso ela precisa ser cadastrada, e por
isso quem lê só as tabelas conclui, errado, que a OCI fecha sem consulta.

Comprovado no validador (ambiente `202608a`, arquivos montados pelo domínio de
export do `apac-platform`):

| Secundários da `0908010010` | Resultado |
|---|---|
| TC de tórax + consulta (`0301010072`) | SEM ERROS |
| TC de tórax + teleconsulta (`0301010307`) | SEM ERROS |
| TC de tórax + baciloscopia (sem consulta) | crítica `000013` PMAE |
| consulta + baciloscopia (sem a TC) | crítica `000013` secundário obrigatório |

As 8 OCIs passaram `SEM ERROS` com "obrigatórios + 1 membro do grupo de
exigência + consulta".

**Estado de produção conferido antes de mexer:** nenhuma das 48.291 APACs de
OCI está sem consulta/teleconsulta, e as 13 de Infectologia (todas `pending`,
competência 08/2026) estão conformes. Não há dado a corrigir — o risco é de
digitação futura.

## Escopo (o que fazer)
- 8 entradas novas no `scripts/sigtap/grupos_exigencia.json`, uma por OCI de
  Infectologia, `attribute_code="OCI"`, `minimum=1`, membros `0301010072` e
  `0301010307` — só `0301010072` na `0908010044`, a única em que o SIGTAP não
  lista teleconsulta como secundário.
- `sigtap_semear_grupos_exigencia`: só aceitar como membro quem é secundário
  **daquele** principal. Com `code__in` cru, procedimento duplicado em dois ids
  (`0301010307` em 243/269, `0203020030` em 239/326) entra duas vezes e sobra
  membro pendurado, que foi o que aconteceu no GIN3 e no atributo 068 da
  `0908010052`.

## Fora de escopo
- Migrar as 20 OCIs que usam `ProcedureSecondary.mandatory=True` na consulta
  para o modelo de grupo (T-043).
- Trocar o cadastro caso a caso por uma regra derivada do atributo 053
  (T-044) — é a correção estrutural, e a decisão de fazê-la é do usuário.
- Apagar os `ProcedureModel` duplicados (T-045). Esta tarefa só deixa de
  criar membro pendurado novo; não remove os que já existem.
- As 2 OCIs de Saúde Bucal (`0907010016`, `0907010024`), que têm o atributo
  053 mas não têm consulta médica entre os secundários no próprio SIGTAP —
  precisa descobrir no validador o que a regra cobra delas antes de cadastrar.

## Arquivos prováveis
- `scripts/sigtap/grupos_exigencia.json` — as 8 entradas + procedência da regra.
- `backend/src/procedure/management/commands/sigtap_semear_grupos_exigencia.py`
  — `_resolver_membros` restrito aos secundários do principal.
- `backend/src/procedure/tests.py` — testes do comando.

## Critério de aceite
- [x] Rodar o semeador cria os 8 grupos com os membros certos.
- [x] Membro com código duplicado que não é secundário da OCI fica de fora.
- [x] Sem `--aplicar` nada é gravado.
- [ ] No formulário, OCI de Infectologia sem consulta nem teleconsulta não
      passa da etapa de procedimentos secundários.

## Verificação
- Comportamento antes = depois? **Não, e é o ponto**: solicitação de OCI de
  Infectologia sem consulta deixa de ser aceita. Nenhuma APAC existente muda —
  todas já têm consulta.
- Gates: `bash scripts/verify.sh` verde (frontend rodado com o `node_modules`
  do checkout principal; esta branch não toca em `frontend/`).
- Teste da duplicata provado vermelho sem o fix (`3 != 2`).
- Export inalterado: a tarefa não toca no montador nem nos golden files.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
- Aplicar em produção com `--aplicar` (é dado, não deploy) — exige backup
  prévio e autorização explícita do usuário.
