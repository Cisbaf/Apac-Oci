# T-014 — `apa_tipapac` e `apa_motsaida` hardcoded — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-002
- **Branch:** `refactor/T-014-tipo-apac-motivo-saida-hardcoded`

> Stub. Achado ao comparar o export com o documento oficial do layout
> (`~/Downloads/layout_Exportacao_APAC_v20250513.pdf`, ver memória
> `reference_export_layout_spec`), depois da T-002. Expandir com `/tarefa T-014`.

## Objetivo (rascunho)
Verificar se os campos `tipo_apac` (sempre `"3"` — Única) e `motivo_saida`
(sempre `"12"`) deveriam refletir o estado real da APAC, e não um valor fixo.

## Contexto / porquê
O spec define domínios reais para os dois campos:
- `apa_tipapac`: 1=Inicial, 2=Continuidade, 3=Única.
- `apa_motsaida`: código conforme Portaria 719/2007 (múltiplos valores).

O código atual (`controller.py`) sempre envia `"3"` e `"12"`, respectivamente,
independente do histórico/estado real da solicitação.

## Direção
- Verificar se o sistema hoje sequer distingue "inicial" de "continuidade"
  no domínio (`ApacRequest`/`ApacBatch`) — se não distingue, talvez "Única"
  seja de fato o único caso suportado hoje (não seria bug, seria escopo
  atual do produto).
- Mesma lógica para `motivo_saida`: entender se existe informação no sistema
  hoje que mapeia para os códigos da Portaria 719/2007, ou se é um caso não
  coberto ainda.
- Se decidir corrigir, é mudança de conteúdo do export — exige tarefa
  explícita e golden file atualizado de propósito.

## Aceite (rascunho)
- [ ] Decisão documentada: os hardcodes são aceitáveis para o escopo atual
      do produto, ou são bugs a corrigir?
- [ ] Se corrigido: golden atualizado de propósito, com justificativa no PR.
