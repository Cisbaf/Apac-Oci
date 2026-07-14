# Análise Complementar e Plano de Refatoração — Sistema APAC OCI (CISBAF)

> Complementa o `ANALISE_ESTADO_ATUAL.md`. Aquele documento diagnosticou bugs e débitos pontuais. Este foca no **problema estrutural de fundo** — por que a regra de negócio se espalhou — e propõe uma **estratégia de refatoração incremental** que mantém o sistema em produção e sobre os mesmos dados.

---

## 1. Entendimento do propósito do sistema

O sistema existe para **substituir a digitação manual no APAC Magnético** (sistema legado de terminal do Ministério da Saúde) por um fluxo web guiado, validado e rastreável, gerando ao final o arquivo posicional (layout fixo, versão 03.15) que é importado no APAC Magnético e processado pelo **SIA/SUS**.

O ponto de negócio que a documentação atual descreve de forma genérica, mas que é o **coração do sistema**, é o seguinte: cada APAC aprovada consome uma **faixa numérica** (lote) pré-autorizada por cidade/competência, e o arquivo exportado precisa bater exatamente com o que o SIA espera — senão a produção do município é **glosada** (rejeitada no faturamento). Ou seja, o valor do sistema não é "cadastrar APAC", é **garantir que o arquivo passe no SIA sem erro**. Isso tem implicação direta na refatoração: o serviço de exportação é o ativo mais crítico e o que menos pode quebrar silenciosamente.

Contexto de domínio relevante (pesquisa complementar): as **OCI (Ofertas de Cuidados Integrados)** são pacotes de procedimentos do **Grupo 09** da Tabela SUS, dentro do **Programa Mais Acesso a Especialistas (PMAE)**. O registro é feito via **APAC no SIA/SUS**, informando o procedimento principal e os secundários. Isso confirma o modelo de dados atual (procedimento principal + subprocedimentos), e indica que o sistema tende a crescer em complexidade de regras por linha de cuidado (oncologia, cardiologia, ortopedia), o que reforça a necessidade de centralizar regras antes de escalar.

---

## 2. O diagnóstico de fundo que faltava: regra espalhada tem uma causa raiz

A análise anterior listou 17 débitos como se fossem independentes. Na prática, quase todos são **sintomas de duas causas estruturais**:

### Causa raiz A — Existem dois "cérebros" concorrentes: o Django Admin e o React/API

O sistema tem, hoje, **dois caminhos de escrita que aplicam regras diferentes para a mesma operação de negócio**. Isso é o que faz "front e backend se perderem nas responsabilidades".

Exemplo concreto e grave — **aprovar/mudar status de uma APAC**:

- **Caminho React → API** (`ApacRequestApprovedAPIView` → `ApprovedApacRequestUseCase`): aplica a regra de negócio completa, incluindo **associar uma faixa APAC disponível** ao aprovar.
- **Caminho Admin** (`admin.py`, action `alterar_status`): faz `queryset.update(status=..., review_date=..., authorizer=...)` **direto no ORM**, sem passar pelo use case, e portanto **sem associar faixa**. 

O mesmo dado ("status aprovado") pode significar coisas diferentes dependendo de por onde passou. Uma APAC "aprovada" pelo admin pode entrar na exportação sem faixa, ou com estado inconsistente. Este é o tipo de divergência que gera glosa e é praticamente invisível até o arquivo ser rejeitado no SIA.

A sua intuição de que "algumas ferramentas do admin poderiam ir para o React e padronizar em um lugar só" está **arquiteturalmente correta**. O admin, hoje, não é só uma tela administrativa — ele reimplementa fluxo de negócio (mudança de status, edição de faixa, dashboard, filtros de visibilidade) por fora da camada de aplicação.

### Causa raiz B — A regra transversal de "quem vê o quê" está copiada em todo lugar

A regra "um usuário só enxerga registros da sua cidade, exceto estabelecimentos onde é `restricted_user`; superusuário vê tudo" está **duplicada, com pequenas variações, em pelo menos cinco lugares**:

| Local | Trecho |
|---|---|
| `apac_request/admin.py` → `get_queryset` | `filter(establishment__city=request.user.city).exclude(establishment__restricted_user=request.user)` |
| `apac_request/admin.py` → `EstablishmentCityFilter` | mesma lógica, reescrita |
| `apac_request/admin.py` → `formfield_for_foreignkey` | mesma lógica, reescrita |
| `apac_request/views.py` → `ApacRequestListCreate.get` | mesma lógica, reescrita |
| `apac_batch/views.py` → `ApacBatchsAvailable.get` | variação com `city=request.user.city` |

São cinco implementações da **mesma política de autorização**. Mudar a regra (ex.: novo perfil, nova exceção) exige editar cinco lugares e torcer para não esquecer nenhum. É exatamente o sintoma de "regra de negócio misturada" que você descreveu.

### Outros pontos que reforçam o diagnóstico

- **Colisão de nomenclatura "controller" em dois níveis**: no backend, `controller.py` é na verdade um **repositório** (já apontado). No frontend, `extracao/controllers/` são **wrappers de `fetch`**. A palavra "controller" significa três coisas diferentes no projeto e nenhuma delas é um controller. Isso sozinho desorienta qualquer pessoa nova.
- **Validação de negócio está bem no lugar certo em um caso e no lugar errado em outro**: o `CreateApacRequestUseCase` é um bom exemplo — regras de data, duplicidade e cidade estão no domínio. Mas a mudança de status no admin não respeita nada disso. A arquitetura correta existe; ela só não é o **único** caminho.
- **Regras específicas de município embutidas no fluxo geral**: `adaptar_oci(...)` (caso Duque de Caxias), `cod_uf="33"`, `cns_paciente="000000000000000"` estão hardcoded dentro do export. São regras de configuração/estratégia por município, não constantes globais.

---

## 3. Como pensar a refatoração: o modelo mental correto

Você descreveu a ideia como um "subsistema de refatoração que funciona como o atual, corrigido, sobre os mesmos dados, antes da migração completa". Isso é exatamente o padrão **Strangler Fig** (figueira estranguladora): você constrói o novo por dentro, rota a rota, envolvendo o legado, até que o legado possa ser removido — sem um "big bang".

O ponto mais importante para a sua dúvida de "manter os mesmos dados funcionando entre as duas versões":

> **Não crie um segundo banco nem um segundo conjunto de dados para sincronizar. Isso seria a maior armadilha do projeto.** Mantenha **um único banco e um único conjunto de models Django** (a camada de persistência). As "duas versões" não são dois bancos — são **duas superfícies (APIs/telas) sobre a mesma persistência**. Assim os dados são sempre os mesmos por construção, e não há nada para sincronizar.

O que muda entre "versão antiga" e "versão nova" não é o dado — é **onde a regra roda**. A versão nova roda toda regra na camada de aplicação (use cases); a antiga (admin + views atuais) continua funcionando até ser substituída rota a rota.

### Arquitetura-alvo (4 camadas, uma direção de dependência)

```
┌─────────────────────────────────────────────────────────┐
│ Interface        views/serializers (API v2)  |  React     │  ← HTTP, JSON, sessão
├─────────────────────────────────────────────────────────┤
│ Application      use_cases / policies                     │  ← ORQUESTRA regra, 1 caminho só
├─────────────────────────────────────────────────────────┤
│ Domain (apac_core)  entities, value objects, services     │  ← REGRA pura, sem Django
├─────────────────────────────────────────────────────────┤
│ Infrastructure   repositories Django (hoje "controller")  │  ← ORM, único ponto que fala com o banco
└─────────────────────────────────────────────────────────┘
```

Regra de ouro: **nenhuma tela (nem React, nem Admin) muda estado de negócio sem passar pela camada Application.** O Admin passa a ser só leitura/consulta ou, quando precisar agir, chama o mesmo use case que o React chama.

---

## 4. Plano incremental (fases)

Ordenado para reduzir risco primeiro e destravar a evolução depois. Cada fase entrega valor sozinha.

### Fase 0 — Blindar o que está em produção (dias, não semanas)

Antes de refatorar qualquer coisa, congelar o comportamento atual para poder mexer sem medo:

1. **Corrigir os dois bugs críticos** já apontados: autenticação em `ExportApacBatch` e a regex de `formatCns`.
2. **Criar um "teste de caracterização" (golden file) do export**: para um conjunto fixo de APACs de exemplo, gerar o arquivo hoje e salvá-lo como referência. Qualquer refatoração futura deve produzir **byte a byte** o mesmo arquivo (exceto mudanças intencionais). Sem isso, qualquer mexida no export é um risco de glosa. **Este é o item mais importante da Fase 0.**
3. **Limpar o repositório**: mover `db.sqlite3`, `data.json`, `logs/`, `.txt` avulsos e `tools/` para fora do `src`/para `.gitignore`, documentando o que cada script fez.
4. **Neutralizar o caminho divergente do admin**: no mínimo, fazer a action `alterar_status` do admin chamar o mesmo use case de aprovação/rejeição (ou desativá-la temporariamente), para eliminar a divergência de faixa. Este é um bug de dados esperando para acontecer.

### Fase 1 — Estabelecer as fronteiras e centralizar a regra transversal

1. **Renomear `Controller` → `Repository`** em todos os apps (`ApacRequestController` → `ApacRequestDjangoRepository`, etc.). Renomear os `controllers/` do frontend para `services/` ou `api/`. Puro renome, sem mudar comportamento — mas elimina a maior fonte de confusão mental.
2. **Criar uma única política de visibilidade/escopo** (ex.: `AccessScopePolicy` no domínio, ou um método de repositório `for_user(user)`) e fazer **os cinco lugares** citados na seção 2.B usarem essa única fonte. A partir daí, mudar a regra de "quem vê o quê" é editar **um** arquivo.
3. **Documentar a arquitetura-alvo** em um `ARQUITETURA.md` curto, com a regra de ouro (ninguém muda estado fora do use case) e o mapa de camadas. Serve de contrato para o time.

### Fase 2 — Um só caminho para cada operação de negócio

1. Levar **toda transição de estado** (aprovar, rejeitar, mudar status, atribuir/trocar faixa) para use cases, se ainda não estiver. O Admin e o React passam a chamar os mesmos use cases.
2. **Isolar as regras por município** (`adaptar_oci`, `cod_uf`, `agency_name`, códigos fixos) em uma **configuração/estratégia por cidade** (ex.: um objeto `MunicipalityExportProfile`), removendo os `if municipio == X` e hardcodes do fluxo geral do export. Prepara o sistema para novos municípios/estados sem tocar no núcleo.

### Fase 3 — Strangler no frontend: migrar as ferramentas do Admin para o React

Aqui entra a sua ideia de "padronizar num lugar só". Criar um **namespace de API v2** e módulos React novos que substituem, uma a uma, as ferramentas hoje presas no Admin:

- Gestão de status/aprovação em lote → tela React (consumindo os use cases da Fase 2).
- Gestão de faixas (batch) → tela React.
- Dashboard (hoje `apac_dashboard` renderizado no Django) → página React com os mesmos dados via API.
- Filtros de competência/estabelecimento → componentes React reutilizáveis.

Cada ferramenta migrada usa **feature flag por rota**: liga a versão nova, mantém a antiga como fallback até validar em produção. Como ambas leem os mesmos models, não há divergência de dados. Ao final da fase, o Admin volta a ser o que deveria ser: uma ferramenta de suporte/emergência, não a interface de operação.

### Fase 4 — Remoção do legado

Quando todas as rotas estiverem no caminho novo e validadas, remover as views antigas, as actions de negócio do admin e o código morto (`dataFakes.ts`, `establishmentFakeList.ts`, `getCityNameByCode` não implementada, etc.).

### Sequência visual

```
Fase 0  ──▶  Fase 1  ──▶  Fase 2  ──▶  Fase 3  ──▶  Fase 4
blindar     fronteiras   1 caminho    strangler     remover
+ golden    + política   por regra    p/ React      legado
  file        única
   │            │            │            │            │
   └── produção nunca para; mesmos models o tempo todo ──┘
```

---

## 5. Visão futura: módulo de Exportação como ferramenta de diagnóstico SIA/APAC

Sua ideia de transformar a exportação num módulo que **detecta e ajuda a corrigir erros** do APAC Magnético/SIA é a evolução natural — e o modelo de camadas acima é o que a viabiliza. Sugestão de arquitetura em três blocos:

**1. Validação pré-exportação (evita o erro antes de gerar o arquivo).** Uma camada de validadores que roda antes de montar o arquivo e bloqueia/avisa sobre os erros clássicos que o SIA rejeita na importação — muitos deles conhecidos e determinísticos: mais de um CNES no arquivo, competência divergente, campo de controle diferente do calculado, UF do arquivo diferente da esperada, arquivo vazio, CNS/CBO/procedimento inconsistentes com a Tabela SUS. Cada validador aponta **qual APAC** causou o problema, com link direto para corrigir.

**2. Parser de retorno de erros (diagnóstico pós-importação).** Quando o SIA/APAC Magnético devolve um relatório de crítica/rejeição, o módulo lê esse retorno, mapeia cada código de erro para uma **explicação em linguagem clara** e um **link para a APAC correspondente**, sugerindo a correção. Transforma "erro 137 na linha 42" em "a APAC do paciente X está com CBO incompatível com o procedimento — clique para corrigir".

**3. Perfis de exportação por município/competência.** Consolidando o que foi isolado na Fase 2, cada município tem seu perfil (UF, códigos, adaptações). Facilita expandir para novos municípios e valida configuração antes de exportar.

Complemento de dados: como o SIA alimenta o **TabNet/DATASUS** (produção ambulatorial pública), o módulo poderia, mais adiante, oferecer **reconciliação** — comparar o que o município exportou com o que aparece processado, ajudando a identificar produção perdida/glosada. Isso fecha o ciclo de "não é só exportar, é garantir que a produção seja paga".

---

## 6. Por onde começar (resumo acionável)

Se for para escolher os primeiros passos concretos desta semana:

1. **Golden file do export + correção dos 2 bugs críticos** (Fase 0). Rede de segurança antes de tudo.
2. **Alinhar a action de status do admin com o use case** (Fase 0/2). Fecha o buraco de divergência de dados que hoje é invisível.
3. **Renomear `Controller` → `Repository`** e centralizar a **política de visibilidade** num único lugar (Fase 1). Maior ganho de clareza por menor esforço.
4. Só então abrir o **namespace v2 + primeira tela React** substituindo uma ferramenta do admin (Fase 3), com feature flag.

A boa notícia, reforçando o que a análise anterior já dizia: **o núcleo (`apac_core`) está no caminho certo.** Isto é consolidação e disciplina de fronteiras, não reescrita. O maior risco do projeto não é o código — é criar um segundo banco para "a versão nova". Não faça isso: um banco, uma persistência, duas superfícies convergindo para uma.

---

## Fontes (pesquisa de domínio)

- [OCI: Ofertas de Cuidados Integrados e o novo modelo de atenção — A4PM](https://www.a4pm.com.br/post/oci-ofertas-de-cuidados-integrados-e-o-novo-modelo-de-aten%C3%A7%C3%A3o-na-sa%C3%BAde-p%C3%BAblica)
- [Manual PMAE — Registro da Produção (Ministério da Saúde)](https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/guias-e-manuais/2024/manual-pmae-registro-da-producao-controle-e-avaliacao.pdf)
- [Procedimentos OCI — Grupo 09 (audhosp.com.br)](https://audhosp.com.br/wp-content/uploads/2024/09/Procedimentos-Oferta-de-Cuidados-Integrados_Andressa-Gorla.pdf)
- [SIA/SUS — Sistema de Informações Ambulatoriais (BVSMS/Ministério da Saúde)](https://bvsms.saude.gov.br/bvs/publicacoes/07_0194_M.pdf)
- [Manual Técnico Operacional SIA/SUS](http://www1.saude.rs.gov.br/dados/1273242960988Manual_Operacional_SIA2010.pdf)
- [Produção Ambulatorial (SIA/SUS) — DATASUS/TabNet](https://datasus.saude.gov.br/acesso-a-informacao/producao-ambulatorial-sia-sus/)
- [Tutorial TABNET 2020 — DATASUS](https://datasus.saude.gov.br/wp-content/uploads/2020/02/Tutorial-TABNET-2020.pdf)
