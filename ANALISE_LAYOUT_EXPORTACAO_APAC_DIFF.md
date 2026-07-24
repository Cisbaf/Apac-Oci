# Análise — Diff entre versões do Layout Oficial de Exportação APAC/SIA

**Documentos comparados:**
- `layout_Exportacao_APAC_v20250513.pdf` — gerado 13/05/2025 (o mesmo já referenciado em `T-013`)
- `layout_Exportacao_APAC.pdf` — gerado **08/07/2026** (2 dias depois da versão 04.00 do APAC Magnético, changelog analisado anteriormente)

**Data da análise:** 16/07/2026

---

## 1. Resultado direto: só existe UMA diferença entre os dois documentos

Os dois PDFs têm 20/21 páginas e são idênticos campo a campo em **todas** as seções — cabeçalho, corpo, e as 14 partes variáveis (Oncologia/Quimioterapia, Oncologia/Radioterapia, Nefrologia, Medicamentos, Cirurgia Bariátrica pré/pós, Geral, Prótese de Mama, Tratamento Dialítico, Acompanhamento Multiprofissional em DRC, Confecção de Fístula Arteriovenosa) — **exceto** pela tabela "CORPO" (registro identificador `14`), onde o documento novo acrescenta **3 campos** entre o campo `apa_strua` (posição 533) e o marcador de fim de linha `apa_fim`.

Isso confirma, com fonte oficial, exatamente a hipótese registrada em `T-023`: os campos novos entram **no fim do registro**, sem deslocar nenhum campo existente.

## 2. Os 3 campos novos — especificação oficial completa

| Seq | Nome | Tam | Ini | Fim | Obrigatório | Domínio/valores | Observação do documento |
|---|---|---|---|---|---|---|---|
| 49 | `apa_fntorca` | **2** | 534 | 535 | NÃO | NUM, zeros à esquerda: `01`=Mod.1 Serviço de Saúde-AES, `02`=Mod.2 Equipe Volante-AES, `03`=Crédito Financ. Parc. Vencidas e Vincendas, `04`=Crédito Financeiro Transação Tributária | — |
| 50 | `apa_emenpar` | 1 | 536 | 536 | NÃO | CHAR: `S`/`N` | — |
| 51 | `apa_semcpf` | 1 | 537 | 537 | NÃO | CHAR: `S`/`N` | **"Válido a partir da competência 07/2026"** — bate exatamente com a v04.00 do changelog |
| 52 | `apa_fim` | 2 | 538 | 539 | SIM | CR+LF | Antes ficava em 534-535; agora em 538-539 (registro cresceu 4 bytes) |

**Correção em relação à minha estimativa anterior em T-023:** eu tinha assumido 1 caractere para `fonte_orcamentaria` — o documento oficial confirma **2 caracteres**, numérico, com zero à esquerda (`"01"`–`"04"`), não texto livre. Os outros dois campos (`emendas_parlamentares`, `pessoa_sem_cpf`) batem com o que eu já tinha assumido (1 char, S/N).

## 3. O que isso muda para T-023

- **A hipótese de posição não precisa mais ser testada empiricamente** — a especificação oficial confirma que os campos vão no fim do registro "14", antes do `apa_fim`. O teste manual no APAC Magnético continua recomendado (é sempre bom confirmar), mas deixa de ser a única fonte de verdade.
- **O tamanho de `fonte_orcamentaria` muda de 1 para 2 posições** no patch.
- Reescrevi `T-023` (`.context/tasks/T-023-campos-export-ausentes.md`) com a especificação oficial — ver arquivo para o patch atualizado.

## 4. Nota sobre o padrão de preenchimento "em branco"

O texto de `apa_semcpf` no documento novo é uma cópia quase literal do texto de `apa_strua` (situação de rua) no documento antigo: *"Quando preenchido, deverão ser utilizadas apenas as opções 'N' [...] ou 'S' [...]. Caso não tenha informação a ser registrada, deixar espaço em branco."* Isso sugere que **espaço em branco é um valor válido** para os 3 campos novos quando não há informação a registrar — não é obrigatório forçar "N" em tudo. Ajustei a recomendação em T-023: para `pessoa_sem_cpf`, mantenho `"N"` porque o sistema **sabe** afirmativamente que o paciente tem CPF (é campo obrigatório hoje); para `emendas_parlamentares`, mudei a recomendação para espaço em branco, já que não há hoje nenhuma informação real associada a esse campo.

## 5. Confirmação cronológica
A data de geração do PDF novo (08/07/2026) é 2 dias depois da versão 04.00 do APAC Magnético (06/07/2026) — bate exatamente com o changelog analisado antes: a v04.00 introduziu `apa_semcpf`, obrigatória a partir da competência 07/2026 (mês corrente). Os campos `apa_fntorca`/`apa_emenpar` já existiam desde a v03.17 (25/09/2025) mas não estavam na versão do documento de 13/05/2025 porque esse PDF antecede a própria v03.17 — ou seja, o documento de maio/2025 já estava desatualizado em relação ao changelog mesmo antes da v04.00.
