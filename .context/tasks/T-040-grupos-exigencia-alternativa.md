# T-040 — Grupos de exigência alternativa ("exige ao menos N destes M")

- **Fase:** 0
- **Status:** done
- **Depende de:** T-037
- **Branch:** `refactor/T-040-grupos-exigencia-alternativa`

## Objetivo
Modelar e cadastrar a regra "este procedimento exige ao menos N de um grupo de
secundários alternativos" (atributos SIGTAP complementares 057, 067, 068, 069,
070), e mostrar isso ao usuário antes de ele tentar enviar a solicitação.

## Contexto / porquê
Achado ao testar de ponta a ponta (usuário simulado: solicitar → aprovar →
exportar pela plataforma real → validar no APAC Magnético real) as 10 OCIs já
com T-035/T-036/T-037 aplicadas: 5 das 8 OCIs de Infectologia tomaram
`EXIGE AO MENOS 1 PROC.SEC. (...)` ou `EXIGE PELO MENOS 1 PROC. SECUNDARIO
SUBGRUPO ...` — uma regra diferente da T-037 (que resolve "1 secundário
específico obrigatório"). Aqui é "1 dentre vários alternativos", que o modelo
`ProcedureSecondary.mandatory` não consegue expressar.

**Fonte de verdade não está no SIGTAP.** Confirmado nesta tarefa: nem
`S_PAPA.PAPA_TRAT` (98/99 é exclusão mútua, assunto diferente — não há
nenhuma linha 98/99 para as 5 OCIs afetadas), nem `S_PAREGR` (regras
genéricas, as mesmas 5 em todas as 8 OCIs, não distinguem a regra específica)
carregam essa lista — só `S_PADET` diz "existe uma regra" (o código do
atributo). A lista dos membros do grupo veio do texto oficial:
- Atributos **067, 068, 069, 070**: Portaria SAES/MS Nº 4.306/2026, Art. 3º
  §§1º-4º (PDF oficial do Diário Oficial, extraído com `pdftotext`).
- Atributo **057**: pré-existente do SIGTAP, não criado por esta portaria —
  "Exige procedimento de ressonância magnética" (subgrupo 02.07), confirmado
  via wiki.saude.gov.br/sigtap. Achado por eliminação: era o único atributo
  presente em `0908010044` e ausente nas outras 7 OCIs, batendo exatamente
  com a única OCI que tomou a crítica de "SUBGRUPO 02.07".

Confirmado contra `S_PAPA`: todo código exigido por cada grupo **já existia**
como secundário compatível da respectiva OCI antes desta tarefa — a portaria
só amarra "escolha pelo menos 1 destes que você já podia escolher", não
introduz procedimento novo. Por isso o cadastro não precisou de nenhum
`ProcedureModel` novo, só a regra de grupo em cima do que já estava linkado.

## Escopo (o que fazer)
- `ProcedureRequirementGroup` (principal, attribute_code, description,
  minimum, `members` M2M para `ProcedureModel`) — modelo novo, aditivo.
- `scripts/sigtap/grupos_exigencia.json` — as 5 regras, com `members` (lista
  fixa) para 067/068/070 ou `subgroup_prefixes` (resolvido contra os
  secundários já compatíveis da OCI) para 057/069.
- `manage.py sigtap_semear_grupos_exigencia` — mesmo padrão de
  `sigtap_auditar`/`sigtap_semear_cid_secundario`: sem `--aplicar` só relata.
- `ProcedureSerializer.requirement_groups` — `[{description, minimum,
  member_ids}]`, member_ids referenciando os `id` que já aparecem em `children`.
- Frontend (`identifySubProceduresForm.tsx`): alerta visual por grupo
  (satisfeito/não) + `validateSubProcedures.ts` **bloqueia** o avanço se
  faltar — mesmo padrão de enforcement do secundário obrigatório da T-037,
  não apenas informativo (decisão implícita: o usuário pediu explicitamente
  para não induzir erro, e o padrão irmão já bloqueia).

## Fora de escopo
- Qualquer atributo de grupo além de 057/067/068/069/070 (071 é "exige
  procedimento reabilitador", carga única, cabe no `ProcedureSecondary`
  simples — não entrou aqui).
- Reconciliar a numeração de tarefas colidente com outras branches locais
  (`docs/T-035-...`, `refactor/T-036-authorizer-id-...`,
  `refactor/T-037-fix-cid-admin-filter`, etc.) — pré-existente, fora do
  escopo desta sessão.

## Arquivos prováveis
- `backend/src/procedure/models.py` — `ProcedureRequirementGroup`
- `backend/src/procedure/migrations/0030_procedurerequirementgroup.py`
- `backend/src/procedure/management/commands/sigtap_semear_grupos_exigencia.py`
- `backend/src/procedure/serializers.py`
- `frontend/src/shared/schemas/procedure.ts`
- `frontend/src/app/solicitar/apacRequest/components/forms/identifySubProceduresForm.tsx`
- `frontend/src/app/solicitar/apacRequest/components/forms/validates/validateSubProcedures.ts`
- `scripts/sigtap/grupos_exigencia.json`

## Critério de aceite
- [x] As 5 OCIs afetadas (`0908010036`, `0908010044`, `0908010052`,
  `0908010060`, `0908010079`) têm grupo cadastrado com os membros corretos
- [x] Nenhum procedimento novo foi criado — todos os membros já existiam
- [x] Formulário mostra o aviso e bloqueia "Próximo" sem satisfazer o mínimo
- [x] Golden file do export inalterado (regra não toca export)

## Verificação
- Gates: `bash scripts/verify.sh` verde (backend/core, backend/src, frontend
  jest, lint sem erro novo).
- `sigtap_semear_grupos_exigencia`: 5 mudanças → 0, idempotente.
- Teste real ponta a ponta (solicitar via API real → aprovar → exportar):
  os 5 IDs de secundário exigidos por grupo confirmados persistidos em
  `ApacDataModel.records` para as 5 OCIs.
- Validação no APAC Magnético real: pendente de confirmação do usuário (o
  mesmo fluxo de download manual que já confirmou a T-036/T-037 — a geração
  de arquivo por `docker exec`/`docker cp` deste ambiente de teste não é
  reconhecida pelo emulador por motivo não relacionado ao cadastro, já
  investigado e descartado como bug real na conversa).
