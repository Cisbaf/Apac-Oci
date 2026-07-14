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
