# T-101 — Renomear `Controller` → `Repository` (backend)

- **Fase:** 1
- **Status:** todo
- **Depende de:** Fase 0 concluída
- **Branch:** `refactor/T-101-rename-repository`

## Objetivo
Eliminar a maior fonte de confusão de nomenclatura: as classes `*Controller` do backend são, na verdade, repositórios Django (implementam as interfaces abstratas de `apac_core.domain.repositories`).

## Contexto / porquê
`ANALISE_ESTADO_ATUAL.md` item 1 (alto). Ver `../conventions.md` (tabela de nomenclatura).

## Escopo
- Renomear em cada app: `controller.py` → `repository.py`; classe `XController` → `XDjangoRepository` (ex.: `ApacRequestController` → `ApacRequestDjangoRepository`).
- Atualizar todos os imports (views, use cases, testes). Buscar por `Controller` em todo o backend.
- Renome puramente mecânico: **sem mudança de comportamento**. Testes verdes antes e depois.
- Fazer app por app (commits separados) para revisão fácil, mas pode ser um PR só.

## Fora de escopo
- Mudar a lógica dos repositórios.
- Renomear o frontend (isso é T-102).

## Arquivos prováveis
- `backend/src/*/controller.py` → `repository.py` (todos os apps)
- `backend/src/*/views.py`, use cases e testes que importam essas classes

## Critério de aceite
- [ ] Nenhuma classe "Controller" que seja repositório permanece.
- [ ] `grep -r "Controller" backend/src` só retorna ocorrências legítimas (se houver).
- [ ] Testes verdes; comportamento idêntico.

## Verificação
- `bash scripts/verify.sh` verde.

## Ao concluir
- Atualizar `conventions.md` marcando o renome como feito.
