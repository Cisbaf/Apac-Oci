# Análise — Histórico de Versões do Programa APAC Magnético / SIA

**Fonte analisada:** `SUPORTE TÉCNICO AO SISTEMA DE INFORMAÇÃO AMBULATORIAL (SIA).txt` (changelog oficial DATASUS, versões 01.00 a 04.00, 2007–2026)
**Sistema próprio avaliado:** CISBAF — APAC OCI (repositório `apac`)
**Data da análise:** 16/07/2026

---

## 1. Resumo do documento-fonte

O arquivo é o changelog oficial de suporte técnico do **APAC Magnético**, o sistema legado do Ministério da Saúde que recebe a digitação/importação de APACs e gera o arquivo que alimenta o SIA/SUS. Cobre 90+ versões, de 01.00 (jan/2008) até **04.00 (06/07/2026)**.

### 1.1 Versão atual e mais recentes (as que importam agora)

| Versão | Data | Obrigatória? | Competência | Resumo |
|---|---|---|---|---|
| **04.00** | 06/07/2026 | **Sim** | **07/2026 (mês corrente)** | Novo campo "Pessoa sem CPF/Registro Civil" (SIM/NÃO); regras de subprocedimento obrigatório para atributos complementares 067–070 (punção lombar/tomografia, exames micológicos, subgrupos 02.06/02.09, tomografia/biópsia); ajuste na cobrança do "Agora Tem Especialistas" (códigos 38.02–38.06). |
| 03.26 | 22/05/2026 | Sim | 05/2026 | CPF obrigatório x CNS obrigatório passam a ser exigidos conforme atributo do procedimento (antes eram tratados de forma genérica). |
| 03.25 | 12/05/2026 | Não | 04/2026 | Ajuste de mensagem de erro (procedimento secundário obrigatório). |
| 03.24 | 24/04/2026 | Não | 04/2026 | Ajuste de crítica "procedimento não permitido para num. autorização". |
| 03.23 | 17/04/2026 | Sim | 04/2026 | Atributos complementares 061 e 062 (Portaria SAES/MS Nº 3.949/2026): exigem procedimento secundário compatível específico. |
| **03.22** | 16/04/2026 | **Sim** | **04/2026** | **Portaria SAES/MS Nº 3.958/2026 exclui o atributo complementar "054 — APAC com validade fixa de 2 competências". A partir de 04/2026 a validade normal de uma APAC volta a ser 3 meses.** |
| 03.21 | 25/02/2026 | Não | 10-11/2025 | Fonte orçamentária passa a ser **obrigatória** para APAC quinto dígito 9; desativa marcação de emendas parlamentares. |
| 03.20 | 23/01/2026 | Sim | 01/2026 | Inclui "I" (Indeterminado) como opção válida de sexo, padrão CNS. |
| 03.19 | 14/01/2026 | Sim | 12/2025 | Proíbe quinto dígito "0"; desativa emendas parlamentares no quinto dígito 9. |
| 03.18 | 24/10/2025 | Sim | 10/2025 | Libera quinto dígito **8** exclusivo para São Paulo (esgotamento de numeração). |
| **03.17** | 25/09/2025 | Sim | 10/2025 | **Programa Agora Tem Especialista**: quinto dígito **9**, atributos complementares 052/053, identificação só por CPF (exceto indígena), **novos campos obrigatórios "Fonte Orçamentária"** (4 opções) e **"Recurso de Emendas Parlamentares"** (S/N). |
| 03.16 | 03/07/2025 | Sim | 07/2025 | Numeração especial quinto dígito "0" para parcela única de custeio (atenção especializada). |
| 03.13 | 07/04/2025 | Sim | 04/2025 | Regras de atributos 056/057/058 (tomografia, ressonância, CPF obrigatório); regras específicas de datas para **APAC de OCI (Grupo 09)**. |
| 03.12 | 11/03/2025 | Sim | 03/2025 | Campo opcional "CNES Terceiro" — habilitado só para **APAC com procedimento principal do Grupo 09 (OCI)**. |
| 03.09 | 13/01/2025 | Sim | 01/2025 | Compatibilidade obrigatória principal×secundário (Anexo V, Portaria SAES/MS Nº 2.331/2024). |
| 03.03 | 18/07/2024 | Sim | 07/2024 | Nasce o **PMAE** (Programa Mais Acesso a Especialistas): quinto dígito 7, atributo 053, regras do subgrupo 0901, layout ganha o campo `apa_dtiden`. |
| 03.00 | 09/04/2023 | Sim | 04/2024 | Campo **CPF do paciente** entra no sistema (digitação, consistência, export e import: `apa_cpfpcnte`). |

### 1.2 Leitura geral
O programa evoluiu de um sistema genérico de digitação de APAC (até ~v03.02) para um sistema fortemente orientado a **OCI/PMAE** a partir de 2024–2025: quase toda versão de 03.03 em diante mexe em regras específicas do Grupo 09, do quinto dígito da numeração, ou de campos exigidos por programas federais (PMAE, Agora Tem Especialista). É exatamente o domínio do seu sistema.

---

## 2. Impacto técnico no sistema CISBAF (APAC OCI)

O sistema de vocês **não reimplementa** as críticas do APAC Magnético/SIA (não há, no código, nenhuma validação de "atributo complementar", CID compatível ou compatibilidade principal×secundário — isso é esperado, porque o papel do sistema é gerar o arquivo posicional para importação, deixando as críticas de conteúdo para o APAC Magnético/SIA). O que importa para vocês é: **o layout e os campos do arquivo exportado batem com o que essas versões passaram a exigir?**

O export declara explicitamente `versao_layout="Versao 03.15"` (`controller.py:34`) — ou seja, o sistema hoje **mira a versão 03.15 (abr/2025)**, e já existem **9 versões obrigatórias posteriores** (03.16 → 04.00). Comparando o código com o changelog, encontrei três pontos concretos:

### 2.1 🔴 Campo novo obrigatório ausente: "Pessoa sem CPF/Registro Civil" (v04.00 — vigente **agora**, competência 07/2026)
Busquei em todo o repositório (`sem_cpf`, `registro_civil`, etc.) e não há nenhum campo correspondente em `PatientData`, `ApacModel` ou nos formulários. A v04.00 (obrigatória a partir da competência corrente) cria esse campo justamente para tratar exceção de pacientes sem CPF quando o procedimento tem o atributo "058 — Obrigatório CPF" — que é exatamente o cenário de várias OCIs. Hoje `PatientData.cpf` é campo obrigatório sem exceção (`patientData.py`), então não há como o sistema sequer representar esse caso.

### 2.2 🟠 Campos obrigatórios da v03.17 ausentes: "Fonte Orçamentária" e "Recurso de Emendas Parlamentares"
Vigentes desde a competência 10/2025 (há **9 meses**) para toda APAC com quinto dígito 9 (Agora Tem Especialistas — sucessor direto do PMAE que este sistema atende). Nenhum dos dois campos existe em `ApacModel` (`apac_model.py`) nem em `PatientData`/telas do frontend. Se as faixas usadas pelo seu sistema incluem numeração com quinto dígito 9, o arquivo gerado está incompleto para esse cenário desde outubro/2025.

### 2.3 🔴 Validade da APAC OCI usando regra que foi **oficialmente extinta** (vigente desde abril/2026)
Este é o achado mais sério, porque já é comportamento ativo e incorreto, não só uma lacuna.

Em `controller.py` (linhas 42, 51-52) e em `adapter.py` (`adaptar_oci`, aplicada a **toda** exportação, não só à do Duque de Caxias — ver `.context/glossary.md`), a validade de toda APAC gerada é calculada como:
- início = data de produção/autorização
- fim = **último dia do mês seguinte** (`get_end_of_next_month`)

Isso é, na prática, o padrão do antigo **atributo complementar "054 — APAC com validade fixa de 2 competências"**. A Portaria SAES/MS Nº 3.958, de 20/03/2026 (changelog v03.22, obrigatória desde a competência 04/2026), **excluiu esse atributo** e determinou: *"A partir de 04/2026, validade normal de uma APAC (3 meses)."*

Ou seja: desde abril/2026 (há mais de 3 competências), o padrão oficial para APAC de OCI deixou de ser 2 meses e passou a ser 3 meses — mas o código continua gerando a validade antiga de 2 meses, incondicionalmente, para toda APAC exportada. Isso é risco direto de glosa/rejeição pelo SIA (data de fim de validade divergente do que a Portaria vigente exige).

### 2.4 🟡 Numeração (quinto dígito) sem nenhuma validação no sistema
Não há, em todo o repositório, qualquer lógica ligada a "quinto dígito" da numeração da APAC (0, 6, 7, 8, 9 — cada um com um significado normativo diferente desde 2016). O `apac_batch.batch_number` é uma string pré-atribuída externamente (faixa), então o sistema hoje **confia cegamente** que a faixa carregada já tem o quinto dígito certo para o procedimento/programa da APAC. Não é um bug de código, mas é um risco operacional que vale registrar: nada impede, hoje, que uma faixa com quinto dígito errado (ex.: "9" sem o procedimento ter atributo 052/053) seja usada.

### 2.5 O que **não** parece ser um problema novo
- `cns_paciente` fixo em zeros + CPF sempre enviado: isso já é um débito conhecido (ver golden test), mas coincide, por acaso, com a regra da v03.17 de que APAC quinto dígito 9 deve identificar o paciente **só por CPF**. Não tratar como bug novo.
- `caracter_atendimento="01"` (eletivo) fixo: correto, é exigência de praticamente todas as versões de PMAE/OCI/Agora Tem Especialista.
- Nenhuma das regras de "atributo complementar" (056–070) precisa ser implementada como validação no seu sistema — isso é papel do APAC Magnético/SIA na importação, não do seu formulário de digitação guiada.

---

## 3. Tarefas registradas no projeto

Conforme combinado, os achados das seções 2.1–2.4 foram registrados como tarefas em `.context/tasks/` (formato stub, para expandir com `/tarefa` quando forem priorizadas):

- **T-023** — Campos novos ausentes no export (Fonte Orçamentária + Pessoa sem CPF/Registro Civil).
- **T-024** — Validade da APAC OCI usa regra extinta (2 competências) em vez da regra vigente (3 meses).
- **T-025** — Numeração (quinto dígito) sem validação no sistema.

Nenhum código foi alterado — só a documentação/registro das tarefas, seguindo o fluxo do `CLAUDE.md` do projeto (`/entender` → `/tarefa T-XXX` → `/verificar` → `/finalizar`).

---

## 4. Análise complementar — dá para resolver sem mudar a forma/campos atuais do export?

Pergunta do usuário: os três achados (T-023/T-024/T-025) podem ser resolvidos de forma **aditiva**, mantendo o sistema funcional como está hoje, sem uma reestruturação grande do que já é exportado?

**Resposta curta: sim para T-024 e T-025 (impacto zero na forma do arquivo); sim em princípio para T-023, mas com uma dependência externa antes de codar.**

| Tarefa | Muda a "forma" do arquivo (posições/tamanho dos campos já existentes)? | Classificação |
|---|---|---|
| T-024 (validade) | **Não.** Só troca o *valor* calculado de dois campos que já existem (`data_inicio_validade`/`data_fim_validade`), mesmo tamanho, mesma posição. | Mudança mínima, segura |
| T-025 (quinto dígito) | **Não.** É uma validação nova, não escreve nada novo no arquivo. Pode nem bloquear nada — só alertar. | Mudança mínima, segura |
| T-023 (campos novos) | **Não precisa.** O próprio DATASUS historicamente estende o layout **acrescentando campos no fim do registro**, sem tocar nas posições já existentes (é literalmente o que a versão 700/711 do changelog fez em 2006/2007 ao ampliar a parte variável de 60 para 85 posições: "o arquivo do APAC permanece com as 60 primeiras posições em sua posição original"). Então dá para seguir o mesmo padrão aqui. | Aditivo, mas falta um dado externo (ver 4.3) |

### 4.1 T-024 — pode ser feito hoje, sem tocar no formato
O `data_fim_validade` já é um campo existente (8 posições, `AAAAMMDD`). A única mudança é a fórmula que calcula o valor:

- Hoje: `get_end_of_next_month(data)` → fim do **mês seguinte** (padrão antigo de 2 competências).
- Proposto: uma função equivalente para "fim do 3º mês" (ex.: `get_end_of_month_plus_n(data, 2)`, mantendo a mesma assinatura), usada nos dois pontos onde `get_end_of_next_month` aparece hoje (`controller.py:42` e dentro de `adaptar_oci`, `adapter.py`).

Não adiciona campo, não remove campo, não muda tamanho de nada — é troca de fórmula em ~2 linhas. O único efeito colateral esperado é que o golden file (T-002) muda de valor nessas duas datas, o que é esperado e deve ser atualizado deliberadamente (é exatamente o caso que o `CLAUDE.md`/golden test preveem: mudança de conteúdo intencional, documentada no PR).

### 4.2 T-025 — pode ser feito sem tocar no export
Isso nem precisa alterar o que é escrito no arquivo. Pode ser implementado como um alerta na hora de associar a faixa à solicitação (ex.: "faixa com quinto dígito 9 associada a procedimento sem atributo 052/053 — confirmar antes de aprovar"), sem bloquear o fluxo atual. Zero risco de regressão no export.

### 4.3 T-023 — aditivo, mas falta um insumo antes de implementar
Tecnicamente dá para adicionar `fonte_orcamentaria`, `emendas_parlamentares` e `pessoa_sem_cpf` como campos novos no fim do registro `ApacModel`/`ApacVariavel` (mesmo padrão de `apa_dtiden`, que já foi adicionado dessa forma na v03.03) — isso não exige tocar nos campos já existentes.

O que falta é a **posição e o tamanho exatos** desses campos no layout oficial vigente. O changelog que analisei descreve *o que* cada campo significa, mas não *onde* ele fica no arquivo posicional — isso só está no documento técnico de layout (o `T-013` já referencia um `layout_Exportacao_APAC_v20250513.pdf`, que não está neste repositório nem acessível daqui). Duas alternativas:

1. Você me envia o layout oficial mais recente (idealmente já na versão 04.00) e eu extraio a posição/tamanho certos.
2. Antes de investir nisso, vale confirmar uma coisa mais barata: **as faixas que o seu município usa hoje têm quinto dígito 9** (Agora Tem Especialista)? Se ainda não usam, esse campo não é necessário agora e T-023 pode ficar em espera sem risco — só "Pessoa sem CPF" (v04.00) é urgente independente do quinto dígito, porque vale para qualquer OCI com atributo 058.

### 4.4 Ordem recomendada
1. **T-024** — implementar já (2 linhas, zero mudança de forma, resolve o item mais urgente/já incorreto).
2. **T-025** — implementar como alerta simples, sem bloqueio (zero risco).
3. **T-023** — separar em duas partes: "Pessoa sem CPF" pode avançar assim que eu tiver a posição/tamanho oficiais; "Fonte Orçamentária"/"Emendas Parlamentares" só depois de confirmar se o município já usa quinto dígito 9.

### 4.5 As três tarefas foram reescritas para aplicação direta
A pedido do usuário, `T-023`, `T-024` e `T-025` em `.context/tasks/` deixaram de ser stubs e passaram a ter patch completo (arquivo, linha, código) e um roteiro de teste manual no APAC Magnético local:

- **T-024** — patch pronto (nova função `get_end_of_month_offset`, 2 pontos de chamada, 3 golden files com o valor exato a trocar). Sem dependência externa.
- **T-025** — escopo reduzido de propósito: validar contra o atributo do procedimento exigiria uma fonte de dados nova (SIGTAP), fora do pedido de mudança mínima. Ficou só o alerta para o quinto dígito "0", que o DATASUS já proibiu categoricamente desde 12/2025 — checagem sem nenhuma dependência nova.
- **T-023** — como ainda falta a posição oficial dos campos novos, virou uma **hipótese testável**: acrescenta os 3 campos no fim do registro (mesmo padrão que o DATASUS já usou historicamente) e usa a importação real no APAC Magnético local como critério de aceite — se o programa aceitar o arquivo e mostrar os campos certos, a hipótese está confirmada; se der erro, para antes de ir para produção. "Fonte Orçamentária" fica reservada em branco (não exige UI nova agora); "Pessoa sem CPF" vai sempre "N" (o sistema já exige CPF sempre, então isso é sempre verdade hoje).

---

## 5. Compatibilidade — quem está numa versão anterior do APAC Magnético precisa atualizar?

**Sim, separadamente do seu sistema.** São duas coisas diferentes que precisam estar alinhadas:

1. **O APAC Magnético instalado localmente em cada unidade/município** (o programa legado de mesa, baixado do site do SIA) — é ele quem importa o arquivo que o seu sistema gera. O DATASUS amarra a obrigatoriedade à **competência**: cada versão "Obrigatória" do changelog diz a partir de qual competência ela passa a valer (ex.: v04.00 é obrigatória desde 07/2026 — agora). Quem está processando a competência 07/2026 com uma versão do APAC Magnético anterior a essa **precisa atualizar o programa local**; isso é o DATASUS quem exige, é uma atualização direta no site do SIA (`sia.datasus.gov.br`), independe do seu sistema. Vale confirmar com quem opera cada unidade se o APAC Magnético local já está na v04.00.
2. **O seu sistema (CISBAF)** gera o arquivo que alimenta esse APAC Magnético local. Aqui o efeito da desatualização é diferente por tarefa:
   - **T-024 (validade):** nenhum risco de compatibilidade — não adiciona campo novo, só troca o valor de datas que já existem. Funciona igual em qualquer versão do APAC Magnético instalado.
   - **T-023 (campos novos):** aqui pode haver dependência real. Se uma unidade ainda estiver rodando um APAC Magnético **anterior** à versão que introduziu esses campos (03.17/04.00), o comportamento ao importar um arquivo com os bytes extras no fim da linha é incerto — pode ignorar (tolerante) ou pode dar erro de tamanho de linha (estrito). É por isso que o teste manual de importação faz parte do critério de aceite dessa tarefa: testar na versão do APAC Magnético que as unidades realmente usam hoje, não numa instalação nova/já atualizada.

Resumindo: **atualizar o seu sistema não substitui a necessidade de cada unidade manter o APAC Magnético local atualizado** — são duas atualizações independentes que precisam andar juntas para a competência corrente não ser glosada.

---

## 6. Próximos documentos

Você mencionou que vai trazer mais documentos (portarias, versões do sistema). Sugestão para os próximos: ao me passar uma portaria específica (ex.: SAES/MS Nº 3.949/2026 ou Nº 3.958/2026), consigo aprofundar a leitura do texto legal e cruzar artigo por artigo com o código — o changelog só me deu o resumo executivo de cada uma.
