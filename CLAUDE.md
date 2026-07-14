# CLAUDE.md — Guia de Operação do Agente (Sistema APAC OCI · CISBAF)

> Este arquivo é lido automaticamente a cada sessão. Ele diz **como trabalhar neste repositório**.
> O que fazer (o conteúdo/plano) mora em `.context/`. Aqui está o **como** e as **regras invioláveis**.

## Antes de qualquer coisa

Toda sessão de trabalho começa pelo comando `/entender`. Ele carrega, nesta ordem:
`.context/index.md` → `architecture.md` → `conventions.md` → `glossary.md` → `plan/roadmap.md` → `tasks/INDEX.md`.

Nunca comece a editar código sem ter lido o `.context/`. Se o contexto e o código divergirem, **pare e avise** — o `.context/` pode estar desatualizado.

## Regras invioláveis (prod-safety)

1. **`master` está SEMPRE em produção.** Nunca faça commit direto na `master`. Todo trabalho acontece em branch de tarefa (`refactor/T-XXX-slug`) e volta via Pull Request.
2. **Uma tarefa = uma branch = um PR.** Não misture tarefas. PRs pequenos e revisáveis.
3. **Nenhum merge com gate vermelho.** Os gates (`.context/tasks/` → seção "Verificação" de cada tarefa) precisam passar: testes backend, testes frontend, golden file do export e lint.
4. **O arquivo exportado é sagrado.** Nenhuma tarefa pode alterar o conteúdo do arquivo gerado para o APAC Magnético **a menos que a tarefa diga explicitamente**. O golden file (`T-002`) é a rede de segurança — se ele mudar sem intenção, a mudança está errada.
5. **Não crie segundo banco.** Uma persistência só; as "duas versões" convivem sobre os mesmos models. Ver `architecture.md`.
6. **Não altere estado de negócio fora da camada Application** (use cases). Ver `conventions.md`.
7. Se uma tarefa crescer além do escopo descrito, **pare, registre o excedente como nova tarefa** em `tasks/INDEX.md` e siga só o escopo original.

## Ciclo de uma tarefa

```
/entender              → reconstrói o contexto do projeto e do plano
/tarefa T-XXX          → lê a tarefa, cria a branch, implementa o escopo
/verificar             → roda todos os gates e mostra resultado
/finalizar T-XXX       → atualiza status, escreve resumo, prepara o PR
```

Cada comando está documentado em `.claude/commands/`.

## Como rodar e verificar (comandos reais)

- Backend (testes de domínio, sem banco): `cd backend/core && python -m pytest`.
- Backend (testes de integração Django, com banco): `cd backend/src && python manage.py test` (não há `pytest-django` configurado — `python -m pytest` aqui não encontra os testes).
- Frontend (testes): `cd frontend && npm test`
- Lint frontend: `cd frontend && npm run lint`
- Gate completo: `bash scripts/verify.sh` (roda tudo e falha se qualquer parte falhar).

## Ao terminar uma tarefa, atualize o contexto

Se a tarefa mudou arquitetura, convenção ou nomenclatura, **atualize o arquivo correspondente em `.context/`** no mesmo PR. O contexto desatualizado é a maior causa de agente perdido. Marque a tarefa como concluída em `.context/tasks/INDEX.md`.

## Idioma

Documentação, comentários de PR e mensagens de commit em **português**. Código em inglês (segue o padrão atual do repo).
