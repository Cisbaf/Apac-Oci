# T-401 — Remover views/actions legadas e código morto — STUB

- **Fase:** 4 · **Status:** todo · **Depende de:** Fase 3 validada em produção
- **Branch:** `refactor/T-401-remove-legacy`

> Stub. Expandir com `/tarefa T-401` só depois de as superfícies novas estarem validadas em produção.

## Objetivo (rascunho)
Remover os caminhos antigos (actions de negócio no admin, views substituídas) e o código morto agora que o novo está validado.

## Direção
- Remover flags e fallbacks já desnecessários.
- Código morto conhecido: `frontend/.../utils/dataFakes.ts`, `procedureFakeList.ts`, `establishmentFakeList.ts`, `getCityNameByCode` não implementada.
- Só remover o que estiver comprovadamente sem uso.

## Aceite (rascunho)
- [ ] Um caminho por operação; sem código morto; `.context/` atualizado; testes verdes.
