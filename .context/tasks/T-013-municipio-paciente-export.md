# T-013 — `apa_munpcnte` usa cidade do estabelecimento, não do paciente — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-002
- **Branch:** `refactor/T-013-municipio-paciente-export`

> Stub. Achado ao comparar o export com o documento oficial do layout
> (`~/Downloads/layout_Exportacao_APAC_v20250513.pdf`, ver memória
> `reference_export_layout_spec`), depois da T-002. Expandir com `/tarefa T-013`.

## Objetivo (rascunho)
Verificar se o campo `apa_munpcnte` (código IBGE do município do **paciente**,
posições 171-177) deveria vir do endereço real do paciente, e não da cidade da
faixa/estabelecimento como hoje.

## Contexto / porquê
O documento oficial descreve o campo como "Código do Município (Cód. IBGE) do
logradouro de residência do paciente". O código atual (`controller.py`) usa
`apac_batch.city.ibge_code` — a cidade da faixa/estabelecimento, não a do
paciente. `PatientData` hoje só guarda `address_city`/`address_state` como
texto livre, sem código IBGE.

## Direção
- Confirmar se pacientes atendidos fora da cidade do estabelecimento são um
  cenário real do sistema (provavelmente sim, dado que APAC é regional).
- Se for necessário corrigir: precisa adicionar um jeito de capturar o
  código IBGE do município de residência do paciente (não existe hoje em
  `PatientData`) — mudança de modelo, não só de export.
- Mudança de conteúdo do export exige tarefa explícita e atualização
  proposital do golden file (T-002), com justificativa no PR.

## Aceite (rascunho)
- [ ] Decisão documentada: é bug real ou comportamento aceitável hoje?
- [ ] Se corrigido: `apa_munpcnte` reflete o município do paciente; golden
      atualizado de propósito.

## Investigação (2026-07-15) — escopo real, decisão: pular por ora

Expandida ao rodar `/tarefa T-013`. Achados:

- O campo pydantic correspondente a `apa_munpcnte` não se chama isso — é
  `cod_municipio` (`apac_model.py`, tamanho fixo 7, posições 171-177).
  Montado em `controller.py:61`: `cod_municipio=apac_batch.city.ibge_code`
  (cidade da faixa/estabelecimento, não do paciente).
- `PatientData` (`domain/dto/patientData.py:9-25`) não tem nenhum campo de
  código IBGE — só `address_city`/`address_state` como texto livre. Corrigir
  de verdade exige mudança de **modelo de dados** (+ migração Django), não só
  de export.
- **Pista relevante para quando isso for retomado**: os dados de origem já
  passam pelo sistema em dois pontos, só são descartados:
  - CADSUS (`frontend/src/app/api/cadsus/route.ts`) devolve `city_code` no
    endereço (`schemas/patientInfo.ts:1-10`, tipo `Address`), mas o
    mapeamento está **comentado** em
    `PatientInfoService.ts:77` (`getCityNameByCode` — função que nem existe).
  - ViaCEP (`components/field/cepInput.tsx:24-34`) devolve um campo `ibge`
    na resposta, também não usado — só `localidade` (nome) e `uf`.
  - Frontend (`identifyPatientForm.tsx:184-196`) captura "Município" como
    `TextField` de texto livre, sem dropdown de municípios/IBGE.
- Não existe tabela/lookup de IBGE por nome de cidade no sistema — só
  `City`/`CityModel` (cidades do consórcio, preenchidas manualmente via
  Django Admin), não uma lista geral de municípios do Brasil.
- Nenhum teste/fixture cobre paciente residente em cidade diferente da
  faixa/estabelecimento hoje.

**Decisão do usuário:** pular esta tarefa por ora — não é prioridade no
momento. Fica documentada para retomar quando decidido, sem precisar refazer
o levantamento acima. Nenhum código alterado nesta investigação.
