# Análise complementar — Portaria SAES/MS Nº 4.304, de 23/06/2026

**Fonte:** Diário Oficial da União, publicado em 26/06/2026, Edição 118, Seção 1, Página 97
**Sistema avaliado:** CISBAF — APAC OCI
**Data da análise:** 16/07/2026

---

## 1. É agregável? Sim — é o achado mais diretamente ligado ao domínio do sistema até agora

Diferente do changelog do APAC Magnético (que fala de regras gerais de digitação/export)
e dos PDFs de layout (que falam do formato do arquivo), esta Portaria cria **conteúdo
novo dentro do Grupo 09** — exatamente o grupo que dá nome ao seu sistema (OCI =
Oferta de Cuidados Integrados, Grupo 09 da Tabela SUS). Não mexe no formato do arquivo
exportado (T-023/T-024/T-025 continuam válidas como estão); mexe no **catálogo de
procedimentos** que o sistema precisa reconhecer.

## 2. O que a Portaria cria

Novo Subgrupo dentro do Grupo 09: **09.07 — Atenção em Saúde Bucal**, Forma de
Organização 01 — Oferta de Cuidado Integral em Saúde Bucal, destinado a **mulheres em
situação de violência doméstica e familiar** com perdas dentárias ou danos bucais
decorrentes da violência.

Dois procedimentos principais novos:

| Código | Nome | Valor | Ciclo assistencial mínimo |
|---|---|---|---|
| `09.07.01.001-6` | OCI - Atenção em Saúde Bucal na Atenção Especializada para Mulheres em Situação de Violência | R$ 400,00 | Consulta inicial (nível superior) → diagnóstico → clínico-restaurador → consulta final (nível superior), até 4 unidades dentárias |
| `09.07.01.002-4` | OCI - Reabilitação Protética em Saúde Bucal na Atenção Especializada para Mulheres em Situação de Violência | R$ 650,00 | Tudo do anterior + procedimento(s) reabilitador(es), até 4 unidades dentárias ou 2 arcadas |

Ambos: CBO 2232 (Cirurgiões-dentistas), sexo ambos, 6 meses a 130 anos, quantidade
máxima 1, financiamento FAEC/PMAE (subtipo 0086 - Agora Tem Especialistas -
Componente Ambulatorial), CID-10 associado a violência (T74, T74.2, Y04, Y08.0, Y09,
F43.0, F43.1).

Cada um tem uma lista extensa de **procedimentos secundários compatíveis** (Anexo IV —
~30 radiografias, tratamentos restauradores/endodônticos e prótese dentária), cada um
com sua própria quantidade máxima por APAC.

Dois atributos complementares novos, específicos dessas OCIs:
- **064** — Exige procedimento diagnóstico e procedimento clínico-restaurador (aplica-se a `09.07.01.001-6`).
- **065** — Exige procedimento reabilitador (aplica-se a `09.07.01.002-4`).

Além disso, ~40 procedimentos odontológicos já existentes na Tabela SUS (radiografias,
restaurações, próteses etc.) ganham os atributos 053 (PMAE) e 058 (CPF obrigatório)
para poderem ser usados como secundários dessas duas OCIs (Anexo II).

**Vigência:** a Portaria entra em vigor na publicação, mas os efeitos operacionais nos
sistemas do SUS (SIGTAP/SIA) valem "na competência seguinte à data de publicação" —
publicação 26/06/2026 → competência **07/2026, o mês corrente**.

## 3. O que muda no sistema CISBAF — e o que não muda

**Não muda:** nada no layout do arquivo exportado. Essas duas OCIs seguem o mesmo
registro "14"/"13" de qualquer outra APAC — T-023/T-024/T-025 não são afetadas por
esta Portaria.

**Muda (cadastro, não código):** o sistema guarda procedimentos e CIDs numa tabela
própria (`ProcedureModel`/`CidModel`, gerenciada pelo Django Admin — não há
sincronização automática com o SIGTAP oficial, é cadastro manual). Para que um
operador consiga abrir uma APAC dessas duas novas OCIs no sistema, alguém precisa
cadastrar manualmente:

1. Os 2 procedimentos principais (`09.07.01.001-6` e `09.07.01.002-4`).
2. Os CIDs do Anexo I (T74, T74.2, Y04, Y08.0, Y09, F43.0, F43.1) vinculados a eles.
3. Os procedimentos secundários compatíveis do Anexo IV, como filhos (`parents`) de
   cada um dos 2 principais — a lista é longa (~30 códigos), reaproveitável entre os
   dois principais com pequenas diferenças de quantidade máxima.

**Observação:** o sistema hoje não valida quantidade máxima por procedimento
secundário nem a regra dos atributos 064/065 (ciclo assistencial mínimo) — isso é
consistente com o padrão já identificado: essas críticas de conteúdo ficam por conta do
APAC Magnético/SIA na importação, não do formulário de digitação guiada.

## 4. Tarefa registrada
Registrei `T-026` em `.context/tasks/` — é uma tarefa de **cadastro**, não de código;
funciona como checklist para quem for habilitar essa OCI no sistema.

## 5. Pergunta em aberto
Essa OCI de Saúde Bucal para mulheres em situação de violência já está no escopo de
atendimento do(s) município(s) que usam o sistema? Se não, T-026 pode ficar em espera
sem risco — nada quebra, é só uma funcionalidade nova disponível quando for priorizada.
