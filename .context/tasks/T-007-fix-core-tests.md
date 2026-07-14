# T-007 — Corrigir testes quebrados em backend/core — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-001
- **Branch:** `refactor/T-007-fix-core-tests`

> Stub. Descoberto ao rodar `bash scripts/verify.sh` pela primeira vez (T-001). Expandir com `/tarefa T-007`.

## Objetivo (rascunho)
Destravar o gate `backend/core (pytest)`, hoje vermelho antes de qualquer mudança de comportamento intencional.

## Direção
- `ApacRequestFakeRepository` (fixture em `tests/application/conftest.py`) não implementa o método abstrato `check_duplicates`, o que quebra a instanciação e derruba 16 testes com `TypeError`.
- Implementar o método fake ausente (compatível com a interface de repositório real) ou revisar se a interface pediu esse método recentemente sem atualizar o fake.

## Aceite (rascunho)
- [ ] `cd backend/core && python -m pytest` verde.
- [ ] Nenhuma mudança de comportamento de negócio — só a fixture de teste.
