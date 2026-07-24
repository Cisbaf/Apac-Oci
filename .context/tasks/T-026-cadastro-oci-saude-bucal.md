# T-026 — Cadastrar novas OCIs de Saúde Bucal (mulheres em situação de violência)

- **Fase:** 0 · **Status:** todo · **Depende de:** —
- **Branch:** não se aplica diretamente (tarefa de cadastro via Django Admin, não de
  código — mas se algum ajuste de código for necessário durante a execução, abrir
  branch normal `refactor/T-026-cadastro-oci-saude-bucal`)

> Detalhado a partir de `ANALISE_PORTARIA_4304_2026_OCI_SAUDE_BUCAL.md` (raiz do
> repo). **Diferente de T-023/T-024/T-025, esta não é uma tarefa de código** — é um
> checklist de cadastro de dados (Django Admin) para habilitar uma OCI nova no
> catálogo de procedimentos do sistema. Não mexe no formato do arquivo exportado.

## Objetivo
Cadastrar em `ProcedureModel`/`CidModel` (Django Admin) os 2 novos procedimentos
principais de OCI de Saúde Bucal criados pela Portaria SAES/MS Nº 4.304/2026, seus CIDs
e seus procedimentos secundários compatíveis, para que o sistema permita abrir uma APAC
desse tipo.

## Pré-requisito antes de executar
- [ ] Confirmar que o(s) município(s) atendidos pelo sistema vão oferecer essa OCI
      (Atenção em Saúde Bucal para Mulheres em Situação de Violência). Se não, deixar
      em espera — não há risco em adiar, é funcionalidade nova, não correção.

## Contexto / porquê
A Portaria (vigente na competência 07/2026) cria, no Grupo 09 - OCI, o Subgrupo 07 -
Atenção em Saúde Bucal, com 2 procedimentos principais novos e ~40 procedimentos já
existentes na Tabela SUS ganhando atributo para servir de secundário a essas OCIs. O
sistema não sincroniza com o SIGTAP automaticamente (`ProcedureModel`/`CidModel` são
cadastro manual via Django Admin) — sem esse cadastro, o operador não consegue
selecionar esses procedimentos na tela de digitação.

## Escopo (o que fazer)

### 1. Cadastrar os 2 procedimentos principais
| Código | Nome | CID-10 a vincular |
|---|---|---|
| `09.07.01.001-6` | OCI - Atenção em Saúde Bucal na Atenção Especializada para Mulheres em Situação de Violência | T74, T74.2, Y04, Y08.0, Y09, F43.0, F43.1 |
| `09.07.01.002-4` | OCI - Reabilitação Protética em Saúde Bucal na Atenção Especializada para Mulheres em Situação de Violência | T74, T74.2, Y04, Y08.0, Y09, F43.0, F43.1 |

### 2. Cadastrar os procedimentos secundários compatíveis (Anexo IV da Portaria), como filhos (`parents`) de cada principal

**Secundários de `09.07.01.001-6`** (qtd. máxima por APAC entre parênteses):
`03.01.01.004-8` Consulta de profissionais de nível superior (exceto médico) (2) ·
`02.06.01.004-4` Tomografia de face/seios/ATM (1) · `02.04.01.017-9` Radiografia
Panorâmica (1) · `02.04.01.022-5` Radiografia periapical (4) · `02.04.01.003-9`
Radiografia bilateral de órbitas (1) · `02.04.01.004-7` Radiografia de arcada
zigomático-malar (1) · `02.04.01.005-5` Radiografia de ATM bilateral (1) ·
`02.04.01.007-1` Radiografia de crânio (PA+lateral+obliqua) (1) · `02.04.01.008-0`
Radiografia de crânio (PA+lateral) (1) · `02.04.01.011-0` Radiografia de maxilar (1) ·
`02.04.01.012-8` Radiografia de ossos da face (1) · `02.04.01.014-4` Radiografia de
seios da face (1) · `02.04.01.016-0` Radiografia oclusal (2) · `02.04.01.020-9`
Teleradiografia (1) · `02.04.01.021-7` Radiografia interproximal/bite wing (2) ·
`02.06.01.007-9` Tomografia de crânio (1) · `03.07.01.006-6` Tratamento inicial do
dente traumatizado (4) · `03.07.02.003-7` Tratamento endodôntico de dente decíduo (4) ·
`03.07.01.003-1` Restauração de dente permanente anterior (4) · `03.07.01.012-0`
Restauração de dente permanente posterior (4) · `03.07.02.004-5` Endodontia
birradicular (4) · `03.07.02.005-3` Endodontia 3+ raízes (4) · `03.07.02.006-1`
Endodontia unirradicular (4) · `03.07.02.007-0` Pulpotomia dentária (4) ·
`03.07.03.007-5` Tratamento de lesões da mucosa oral (4) · `04.14.02.008-1` Enxerto
gengival (4) · `04.14.02.016-2` Gengivoplastia (1) · `04.14.02.013-8` Exodontia de
dente permanente (4) · `04.14.02.014-6` Exodontia múltipla c/ alveoloplastia (1) ·
`04.14.02.024-3` Reimplante/transplante dental (4) · `04.04.02.044-5` Contenção de
dentes por splintagem (2) · `04.01.01.010-4` Incisão e drenagem de abscesso (1) ·
`04.04.02.005-4` Drenagem de abscesso da boca (1) · `04.01.01.005-8` Excisão de lesão
de pele/mucosa (2) · `04.04.02.009-7` Excisão e sutura de lesão na boca (2) ·
`03.07.04.011-9` Instalação de aparelho ortodôntico fixo (2) · `03.07.04.012-7`
Manutenção de aparelho ortodôntico (2) · `03.07.04.017-8` Moldagem dento-gengival
ortodôntica (2).

**Secundários de `09.07.01.002-4`** (inclui os mesmos diagnósticos/radiografias acima
com quantidades ajustadas — conferir Anexo IV — mais os itens de prótese abaixo):
`02.07.01.002-1` Ressonância de ATM bilateral (1) · `07.01.07.012-9` Prótese Total
Mandibular (1) · `07.01.07.013-7` Prótese Total Maxilar (1) · `07.01.07.009-9` Prótese
Parcial Mandibular Removível (1) · `07.01.07.010-2` Prótese Parcial Maxilar Removível
(1) · `07.01.07.014-5` Prótese Coronária/Intrarradicular Fixa/Adesiva (4) ·
`07.01.07.015-3` Prótese dentária sobre implante (4) · `04.14.02.042-1` Implante
dentário osteointegrado (4) · `03.07.04.006-2` Manutenção periódica de prótese
buco-maxilo-facial (1) · `03.07.04.007-0` Moldagem dento-gengival p/ prótese (4) ·
`03.07.04.008-9` Reembasamento/conserto de prótese (4) · `03.07.04.013-5` Cimentação de
prótese (4) · `03.07.04.014-3` Adaptação de prótese (4) · `03.07.04.015-1` Ajuste
oclusal (4) · `03.07.04.016-0` Instalação de prótese dentária (4) ·
`03.07.04.018-6` Escaneamento Intraoral (1) · `03.07.04.019-4` Planejamento de prótese
em fluxo digital (4) · `07.01.07.018-8` a `07.01.07.025-0` — próteses em fluxo digital
(1, exceto `07.01.07.023-4` que é 4).

> O sistema hoje **não** tem campo para registrar quantidade máxima por
> procedimento-secundário — isso fica a cargo da crítica do APAC Magnético/SIA na
> importação (mesmo padrão já identificado para os demais atributos complementares).
> As quantidades acima são só para referência de quem for conferir a digitação
> manualmente, não precisam virar campo novo no sistema.

### 3. Conferir que os CIDs do Anexo I existem em `CidModel`
`T74` · `T74.2` · `Y04` · `Y08.0` · `Y09` · `F43.0` · `F43.1` — cadastrar os que
faltarem, vinculados aos 2 procedimentos principais.

## Fora de escopo
- Validar automaticamente os atributos complementares 064/065 (ciclo assistencial
  mínimo) ou as quantidades máximas do Anexo IV — consistente com o resto do sistema,
  essa crítica fica para o APAC Magnético/SIA.
- Qualquer mudança no export (`ApacModel`/`ApacVariavel`/`ApacProcedure`) — esta
  Portaria não altera o layout do arquivo.

## Critério de aceite
- [ ] Pré-requisito respondido (município vai oferecer essa OCI?).
- [ ] Se sim: 2 procedimentos principais, CIDs do Anexo I e os secundários
      compatíveis cadastrados no Django Admin.
- [ ] Teste manual: operador consegue abrir uma APAC de teste com `09.07.01.001-6` ou
      `09.07.01.002-4` como procedimento principal e selecionar os secundários
      esperados.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
