# T-007 — Corrigir testes quebrados em backend/core — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** T-001
- **Branch:** `refactor/T-007-fix-core-tests`

> Stub. Descoberto ao rodar `bash scripts/verify.sh` pela primeira vez (T-001). Expandir com `/tarefa T-007`.

## Objetivo (rascunho)
Destravar o gate `backend/core (pytest)`, hoje vermelho antes de qualquer mudança de comportamento intencional.

## Direção
- `ApacRequestFakeRepository` (fixture em `tests/application/conftest.py`) não implementa o método abstrato `check_duplicates`, o que quebra a instanciação e derruba 16 testes com `TypeError`.
- Implementar o método fake ausente (compatível com a interface de repositório real) ou revisar se a interface pediu esse método recentemente sem atualizar o fake.
- **Achado na T-002:** `tests/application/usecases/apac_export/test_export_case.py::test_generate` é um dos 16 quebrados pela fixture, mas além disso tem uma string esperada **desatualizada** — não reflete a versão atual de `adaptar_oci`/`data_autorizacao` em `controller.py` (o próprio código tem o comentário `# por enquanto fixo` documentando a mudança). A T-002 criou `tests/domain/services/export/test_golden_export.py`, que já cobre (e de forma correta/atual) o que esse teste tentava caracterizar. Ao chegar aqui, considerar **remover** `test_export_case.py` em vez de consertá-lo, já que ficou redundante — mas ainda assim implementar `check_duplicates`, pois os outros 15 testes quebrados dependem dele.

## Aceite (rascunho)
- [ ] `cd backend/core && python -m pytest` verde.
- [ ] Nenhuma mudança de comportamento de negócio — só a fixture de teste.
