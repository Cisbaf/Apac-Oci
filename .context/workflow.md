# Fluxo agêntico e prod-safety

## Modelo de branches (master sempre em produção)

```
master  ●────────────●────────────●────────────●───────▶  (sempre deployável)
         \           / \          / \          /
          ● T-002 ──●   ● T-003 ─●   ● T-101 ─●
          branch por tarefa, curta, com PR e gate verde
```

- `master` = produção. **Nunca** recebe commit direto.
- Cada tarefa nasce de uma branch curta a partir da `master` atualizada: `refactor/T-XXX-slug`.
- Merge só via **Pull Request** com todos os gates verdes.
- Branch de tarefa vive **horas a poucos dias**, não semanas — evita divergência e conflito.
- Rebase na `master` antes de abrir o PR se a master andou.

## Ciclo padrão de trabalho (uma sessão / uma tarefa)

1. `/entender` — reconstrói o contexto (lê `.context/` inteiro + estado das tarefas).
2. Escolher a próxima tarefa **desbloqueada** no topo de `tasks/INDEX.md`.
3. `/tarefa T-XXX` — lê o arquivo da tarefa, cria a branch, confere pré-condições, implementa **apenas o escopo descrito**.
4. `/verificar` — roda `scripts/verify.sh` (todos os gates) e mostra o resultado.
5. `/finalizar T-XXX` — atualiza `INDEX.md`, atualiza `.context/` se algo mudou, escreve o corpo do PR (o que mudou + saída do verificar), deixa pronto para você revisar e abrir o PR.
6. Você revisa, testa manualmente o que quiser, e faz o merge.

## Gates de verificação (todos precisam passar para mergear)

| Gate | Comando | Falha significa |
|---|---|---|
| Testes de domínio/use cases | `cd backend/core && python -m pytest` | regra de negócio quebrou |
| Testes de integração | `cd backend/src && python -m pytest` | fluxo Django quebrou |
| Testes frontend | `cd frontend && npm test` | UI/serviço quebrou |
| **Golden file do export** | incluído nos testes (T-002) | **o arquivo do APAC Magnético mudou — risco de glosa** |
| Lint | `cd frontend && npm run lint` | estilo/erros estáticos |

Atalho: `bash scripts/verify.sh` roda todos e falha se qualquer um falhar.

## Princípios de segurança para não quebrar produção

1. **Comportamento antes = comportamento depois**, salvo quando a tarefa diz o contrário. Refatoração muda estrutura, não comportamento observável.
2. **Caracterização primeiro** (T-002): antes de mexer no export, ter o golden file. Antes de refatorar um fluxo sem teste, escrever um teste que fixa o comportamento atual.
3. **Passos pequenos e reversíveis.** Se um PR fica grande, quebre em tarefas menores.
4. **Nunca ligar o novo e apagar o velho no mesmo PR.** Feature flag liga o novo; a remoção do velho é tarefa separada, depois de validado (fase 4).
5. **Escopo fechado.** Achou outro problema no caminho? Registra como nova tarefa no `INDEX.md`, não conserta agora.

## Trabalho ao longo de vários dias

Como cada sessão começa por `/entender` e o estado vive em `tasks/INDEX.md` (não na memória do agente), qualquer sessão nova — sua ou de outro agente — retoma exatamente de onde parou. O `INDEX.md` é a fonte da verdade do progresso.
