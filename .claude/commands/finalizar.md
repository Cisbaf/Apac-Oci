---
description: Fecha uma tarefa — atualiza contexto, status e prepara o corpo do PR
argument-hint: T-XXX
---

Finalize a tarefa **$ARGUMENTS**. Só rode isto com os gates verdes (`/verificar`).

1. Confirme que `/verificar` passou. Se não passou, pare.
2. Se a tarefa mudou arquitetura, convenção ou nomenclatura, **atualize o arquivo correspondente em `.context/`** (architecture/conventions/glossary) nesta mesma branch.
3. Atualize `.context/tasks/INDEX.md`: status da tarefa → `done` e adicione uma linha no "Log de conclusão" (`$ARGUMENTS — feito em <data> — resumo de uma linha`).
4. Faça o commit em português, imperativo: `git add -A && git commit -m "$ARGUMENTS: <resumo>"`.
5. Prepare o corpo do Pull Request (mostre ao usuário, não abra sozinho a menos que ele peça):
   - O que mudou e por quê (referencie a tarefa e a análise).
   - Confirmação: "golden file inalterado" (ou, se mudou, justificativa explícita).
   - Cole o resultado do `/verificar`.
   - Checklist de aceite da tarefa, marcado.
6. Lembre o usuário: revisar, testar manualmente o que quiser, e fazer o **merge para `master` via PR**. Master está sempre em produção.

Ao final, sugira a próxima tarefa desbloqueada do INDEX.
