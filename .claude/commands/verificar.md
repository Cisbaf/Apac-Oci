---
description: Roda todos os gates de verificação e mostra o resultado
---

Rode os gates de verificação e reporte com honestidade. Não declare sucesso se algo falhou.

1. Execute `bash scripts/verify.sh` a partir da raiz do projeto.
2. Se o script não existir ainda (antes da T-001), rode manualmente:
   - `cd backend/core && python -m pytest`
   - `cd backend/src && python -m pytest`
   - `cd frontend && npm test`
   - `cd frontend && npm run lint`
3. Preste atenção especial ao **golden file do export**: se ele falhou e a tarefa atual NÃO era de mudar o export, o problema está na sua alteração — reverta/corrija. Nunca atualize o golden para "passar" sem que a tarefa mande.

Reporte:
- Tabela com cada gate: ✅/❌ e a mensagem-chave em caso de falha.
- Se tudo verde: confirme que está pronto para `/finalizar`.
- Se algo vermelho: aponte a causa provável e o que corrigir. Não avance.
