---
description: Executa uma tarefa do plano (T-XXX) do escopo à branch, respeitando prod-safety
argument-hint: T-XXX
---

Você vai executar a tarefa **$ARGUMENTS**. Se nenhum ID foi passado, use a próxima tarefa desbloqueada do `.context/tasks/INDEX.md`.

Pré-condições (não pule):
1. Se ainda não rodou `/entender` nesta sessão, carregue o contexto primeiro.
2. Leia o arquivo da tarefa em `.context/tasks/$ARGUMENTS-*.md`. Se for um STUB, **expanda-o agora** lendo o código real relevante, e confirme o escopo com o usuário antes de codar.
3. Verifique as dependências (`Dep`) no INDEX — se alguma não estiver `done`, pare e avise.
4. Confirme que `git status` está limpo e que você está partindo da `master` atualizada (`git checkout master && git pull`).

Execução:
5. Crie a branch da tarefa: `git checkout -b refactor/$ARGUMENTS-slug` (use o slug do INDEX).
6. Atualize o status da tarefa para `doing` no `INDEX.md`.
7. Implemente **apenas o escopo descrito**. Nada além. Se descobrir outro problema, registre-o como nova tarefa no INDEX e siga só o escopo.
8. Adicione/atualize os testes que a tarefa pede. Lembre: comportamento antes = depois, salvo se a tarefa disser o contrário.
9. Ao terminar de codar, rode `/verificar`. Não prossiga com gate vermelho.

Regras invioláveis: nunca commite na `master`; não mude estado de negócio fora de use case; não altere o output do export (golden file) sem que a tarefa mande. Ver `CLAUDE.md`.

Ao final, mostre o diff resumido e chame `/finalizar $ARGUMENTS`.
