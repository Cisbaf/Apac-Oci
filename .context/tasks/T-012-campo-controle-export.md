# T-012 — Campo de controle do export hardcoded (`cbc-smt-vrf`) — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-002
- **Branch:** `refactor/T-012-campo-controle-export`

> Stub. Achado ao comparar o export com o documento oficial do layout
> (`~/Downloads/layout_Exportacao_APAC_v20250513.pdf`, ver memória
> `reference_export_layout_spec`), depois da T-002. Expandir com `/tarefa T-012`.

## Objetivo (rascunho)
Verificar se o campo de controle do cabeçalho (`campo_controle`, posições 020-023,
hoje hardcoded como `"1810"` em `HeaderModel`/`controller.py`) precisa ser
calculado dinamicamente, e corrigir se sim.

## Contexto / porquê
O documento oficial do layout (seção final, "OBS - Calculo do campo de
controle") define uma fórmula:
1. Somar o código de todos os procedimentos + quantidade + número da APAC.
2. Obter o resto da divisão do resultado por 1111.
3. Somar 1111 ao resto (domínio final: [1111..2221]).

O código atual sempre envia o literal `"1810"`, independente do conteúdo real
do lote exportado. Se o SIA valida esse campo, isso pode causar rejeição
silenciosa ou aceite por coincidência.

## Direção
- Confirmar com o usuário/documentação do SIA se esse campo é de fato validado
  na importação (ou se é vestigial/não crítico hoje).
- Se for crítico: implementar a fórmula, testar contra o golden file da T-002
  (que hoje fixa `"1810"` — a mudança vai exigir atualizar o golden **de
  propósito**, com justificativa explícita no PR, conforme regra do
  `CLAUDE.md`).
- Cuidado: essa é uma mudança que ALTERA o conteúdo do arquivo exportado —
  regra de ouro do projeto exige tarefa explícita e justificativa clara.

## Aceite (rascunho)
- [ ] Campo de controle calculado conforme a fórmula oficial (ou decisão
      documentada de que não é necessário, com a razão).
- [ ] Golden file atualizado de propósito, com o PR explicando a mudança.
