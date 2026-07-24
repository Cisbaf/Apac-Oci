# T-029 — Atualiza rótulo `versao_layout` do header do export

- **Fase:** 0
- **Status:** done
- **Depende de:** T-002
- **Branch:** `refactor/T-029-versao-layout-header`

## Objetivo
Atualizar o rótulo textual `versao_layout` do header do arquivo exportado, de
`"Versao 03.15"` para `"Versao 04.00"`, refletindo a versão real que o sistema já
implementa depois da T-023 (campos da v03.17) e T-024 (regra de validade da v04.00,
Portaria SAES/MS Nº 3.958/2026).

## Contexto / porquê
Identificado ao validar a T-023/T-024 com o usuário. `HeaderModel.versao_layout`
(`header_model.py:34`, campo de 15 posições) é hoje fixo em `"Versao 03.15"`
(`controller.py:34`) — a versão de abril/2025. Isso já estava desatualizado *antes*
desta tarefa (o sistema não implementava nem v03.16), mas ficou mais evidente agora:
depois da T-023/T-024 o sistema passa a gerar campos e regras de versões posteriores
(v03.17, v04.00) enquanto o próprio arquivo se declara na v03.15. É só um rótulo
textual — não há evidência de que o SIA valide esse valor contra o conteúdo do arquivo
(ver `ANALISE_VERSAO_PROGRAMA_SIA_APAC.md`, raiz do repo, seção 2) — mas é uma
inconsistência de conteúdo que vale corrigir, já que o rótulo é lido por quem inspeciona
o arquivo manualmente (incluindo o próprio APAC Magnético na importação).

## Escopo (o que fazer)
- `backend/core/src/apac_core/domain/services/apac_extract/controller.py:34`:
  `versao_layout="Versao 03.15"` → `versao_layout="Versao 04.00"`.
- Golden files (`backend/core/tests/domain/services/export/golden/`): a linha 1
  (header) tem `Versao 03.15` seguido de 3 espaços (preenchimento até 15 posições);
  trocar para `Versao 04.00` (mesmo tamanho, mesmo preenchimento) nos 3 arquivos:
  - `apac_simples.txt`
  - `apac_com_subprocedimentos.txt`
  - `apac_duque_de_caxias.txt`

## Fora de escopo
- Qualquer lógica de versão dinâmica/multi-formato — decisão já tomada na T-023
  (formato único, sempre o mais atual).
- Reavaliar se o sistema de fato implementa **tudo** que a v04.00 exige (fora os
  itens já cobertos por T-023/T-024/T-025) — isso seria um levantamento novo, não
  parte desta tarefa pontual de rótulo.

## Critério de aceite
- [x] `versao_layout` gera `"Versao 04.00"` no arquivo exportado.
- [x] Golden files atualizados de propósito, PR explica o motivo.
- [x] Gates: `bash scripts/verify.sh` verde (4/4).

## Verificação
- Comportamento antes = depois? Não — mudança de conteúdo intencional do export
  (só o rótulo de versão, nenhum campo de dado muda). Golden file atualizado de
  propósito.
- Gates: `bash scripts/verify.sh` verde.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
