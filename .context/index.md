# .context — Contexto do Projeto APAC OCI (CISBAF)

> Ponto de entrada do contexto durável do projeto, no estilo *dotcontext / Codebase Context Specification*.
> Objetivo: qualquer agente (ou pessoa) reconstruir o entendimento do projeto e do plano de refatoração **do zero**, sem depender de memória de sessões anteriores.

## O que é este projeto (resumo de 30 segundos)

Plataforma web que substitui a digitação manual no **APAC Magnético** (sistema legado do Ministério da Saúde) por um fluxo guiado e validado, gerando ao final um **arquivo posicional** (layout fixo v03.15) importável no APAC Magnético e processado pelo **SIA/SUS**. Cada APAC aprovada consome uma **faixa** numérica pré-autorizada. Se o arquivo não bater com o que o SIA espera, a produção do município é **glosada** (não paga). Contexto de negócio detalhado: `../PROJETO.md` e `../Apac OCI Cisbaf.md`.

Stack: Django 5 + DRF + Pydantic (backend), Next.js 15 + React 19 + MUI (frontend), MySQL (prod). Domínio isolado em `backend/core` (`apac_core`).

## Por que estamos refatorando

Ver diagnóstico completo em `../ANALISE_ESTADO_ATUAL.md` e `../ANALISE_COMPLEMENTAR_E_PLANO_REFATORACAO.md`.
Em uma frase: **a regra de negócio se espalhou** porque existem dois "cérebros" concorrentes (Django Admin e React/API) que aplicam regras diferentes para a mesma operação, e a regra transversal de visibilidade está duplicada em vários lugares. A refatoração consolida tudo em uma arquitetura de 4 camadas, de forma incremental (padrão *Strangler Fig*), sem parar a produção.

## Mapa do contexto (leia nesta ordem)

| Arquivo | Para quê |
|---|---|
| `architecture.md` | Arquitetura-alvo (4 camadas) e a regra do banco único / duas superfícies |
| `conventions.md` | Convenções de código, nomenclatura, camadas, o que pode/não pode |
| `glossary.md` | Glossário de domínio (APAC, OCI, SIA, faixa, competência, glosa, CADSUS...) |
| `workflow.md` | Fluxo agêntico, modelo de branches, gates e prod-safety |
| `plan/roadmap.md` | Plano por fases (0 a 4) com objetivos e critérios de saída |
| `tasks/INDEX.md` | Quadro de tarefas com status — a fonte da verdade do "o que fazer agora" |

## Estado atual da refatoração

- **Fase corrente:** 0 — Blindar o que está em produção.
- **Próxima tarefa sugerida:** ver o topo de `tasks/INDEX.md`.
- Nada foi alterado no código de produção ainda; este scaffold é só contexto/planejamento.

## Regra de manutenção deste diretório

Toda tarefa que muda arquitetura, convenção ou nomenclatura **deve atualizar o arquivo correspondente aqui, no mesmo PR**. Contexto desatualizado é bug.
