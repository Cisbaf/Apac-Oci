# Análise complementar — Portaria SAES/MS Nº 4.306, de 24/06/2026

**Fonte:** Diário Oficial da União, publicado em 26/06/2026, Edição 118, Seção 1, Página 101
**Sistema avaliado:** CISBAF — APAC OCI
**Data da análise:** 17/07/2026

---

## 1. Mesma categoria da Portaria 4.304: conteúdo novo no Grupo 09, sem mudança de formato

Publicada 1 dia depois da 4.304 (mulheres em situação de violência), no mesmo Diário
Oficial. Cria o **Subgrupo 08 — Atenção em Infectologia**, Forma de Organização 01 —
Ofertas de Cuidados Integrados em Infectologia, para investigação clínica e definição
diagnóstica de pessoas vivendo com HIV/aids em situação de imunossupressão. Mesma
conclusão da análise anterior: **não altera o layout do arquivo exportado** (T-023/
T-024/T-025 continuam válidas como estão) — é cadastro de procedimentos novos, não
código.

## 2. Achado que fecha um ponto em aberto da primeira análise
No relatório inicial (`ANALISE_VERSAO_PROGRAMA_SIA_APAC.md`, seção sobre a versão
04.00 do APAC Magnético) eu já tinha listado os atributos complementares **067, 068,
069 e 070** como parte da v04.00, sem saber qual portaria os originava. **Esta é essa
portaria** — o Art. 3º define os quatro atributos com o texto quase idêntico ao do
changelog:

| Atributo | Regra | OCI que o usa |
|---|---|---|
| 067 | Exige Punção Lombar e/ou Tomografia de Crânio | `09.08.01.003-6` (Avaliação inicial — Síndrome Neurológica) |
| 068 | Exige procedimento dos subgrupos 02.02 e/ou 02.03 | `09.08.01.005-2` (Avaliação inicial — Síndrome Mucocutânea) |
| 069 | Exige procedimento dos subgrupos 02.06 e/ou 02.09 | `09.08.01.002-8` (Progressão — Síndrome Respiratória) |
| 070 | Exige tomografia e/ou biópsia | `09.08.01.007-9` (Avaliação inicial — Síndrome Consumptiva) |

## 3. O que a Portaria cria — 8 procedimentos principais novos
Quatro síndromes clínicas associadas a HIV/aids, cada uma com um par "Avaliação
Diagnóstica Inicial" / "Progressão da Avaliação Diagnóstica":

| Síndrome | Avaliação inicial | Valor | Progressão | Valor |
|---|---|---|---|---|
| Respiratória | `09.08.01.001-0` | R$ 574,72 | `09.08.01.002-8` | R$ 387,87 |
| Neurológica | `09.08.01.003-6` | R$ 566,84 | `09.08.01.004-4` | R$ 1.500,00 |
| Mucocutânea | `09.08.01.005-2` | R$ 283,34 | `09.08.01.006-0` | R$ 1.479,38 |
| Consumptiva | `09.08.01.007-9` | R$ 827,36 | `09.08.01.008-7` | R$ 1.228,61 |

Todos: APAC (Proc. Principal), Ambulatorial, Média Complexidade, FAEC/PMAE (subtipo
040086), sexo ambos, 0 meses a 130 anos, quantidade máxima 1, CBO 2251/2252/2253
(médicos clínicos/cirúrgicos/diagnóstico), atributos 053 (PMAE), 058 (Obrigatório
CPF), 059 (Componente Complementar Modalidade 2), 043 (Exige CID de causas
associadas) + o atributo específico da síndrome (tabela acima).

**Regra de registro clínico (Art. 2º, §2º):** além do CID principal (um dos códigos
HIV/aids: B20–B24 ou Z21), é preciso registrar também o **CID secundário** da condição
relacionada ao HIV/aids que motivou o atendimento — cada par de OCI tem uma lista longa
de CIDs secundários compatíveis (pneumonias, neurotoxoplasmose, sarcoma de Kaposi,
linfomas etc.), listada na própria Portaria por síndrome. Não é uma mudança de sistema,
mas é uma orientação clínica de preenchimento relevante para quem for digitar essas
APACs.

Cada procedimento principal tem sua lista de secundários obrigatórios (Anexo III) e
compatíveis (Anexo IV) — exames de imagem, culturas, testes moleculares e biópsias já
existentes na Tabela SUS, que ganham (Anexo II) os atributos 053/058 para poder ser
usados como secundários dessas 8 OCIs.

**Vigência:** publicação 26/06/2026 → efeitos operacionais no SIA a partir da
competência seguinte → **07/2026, o mês corrente** (mesma janela da Portaria 4.304).

## 4. Impacto no sistema CISBAF
Igual ao da Portaria 4.304: nenhuma mudança de código ou de formato de export. Se o(s)
município(s) atendidos forem oferecer essa OCI de Infectologia, alguém precisa
cadastrar manualmente (Django Admin, `ProcedureModel`/`CidModel`) os 8 procedimentos
principais, os CIDs (principal e secundários) e os procedimentos secundários
compatíveis — mesmo processo de T-026, sem necessidade de tocar em código de export
nem em regra de negócio.

## 5. Tarefa registrada
Registrei `T-027` em `.context/tasks/`, no mesmo formato de checklist de cadastro que
`T-026`.

## 6. Pergunta em aberto
Assim como a OCI de Saúde Bucal, esta é uma funcionalidade nova — vale confirmar se o
atendimento a pessoas vivendo com HIV/aids em investigação diagnóstica já está no
escopo do(s) município(s), ou se T-027 fica em espera até ser priorizada.
