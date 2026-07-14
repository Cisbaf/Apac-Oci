---
description: Reconstrói o contexto do projeto e do plano de refatoração antes de qualquer trabalho
---

Você vai reconstruir o entendimento completo do projeto APAC OCI. Faça isto **antes de tocar em qualquer código**.

Leia, nesta ordem, e resuma o que entendeu ao final:

1. `.context/index.md` — visão geral e mapa do contexto
2. `.context/architecture.md` — arquitetura-alvo e a regra do banco único
3. `.context/conventions.md` — convenções, nomenclatura, o que pode/não pode
4. `.context/glossary.md` — glossário de domínio (releia se precisar)
5. `.context/workflow.md` — fluxo agêntico, branches, gates, prod-safety
6. `.context/plan/roadmap.md` — fases e critérios de saída
7. `.context/tasks/INDEX.md` — quadro de tarefas e status atual

Depois:
- Rode `git branch --show-current` e `git status --short` para saber onde estamos.
- Identifique a **próxima tarefa desbloqueada** (status `todo`, sem dependências pendentes) no topo do `INDEX.md`.

Ao final, produza um resumo curto:
- Fase corrente e por que ela existe (1–2 frases).
- As **regras invioláveis** (prod-safety) que você vai respeitar.
- A próxima tarefa sugerida (ID + título) e o que ela pede.
- Pergunte se deve seguir com `/tarefa <ID>` ou outra.

Não implemente nada aqui. Este comando só carrega contexto.
