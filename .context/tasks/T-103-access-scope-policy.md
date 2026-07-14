# T-103 — `AccessScopePolicy` única (política de visibilidade)

- **Fase:** 1
- **Status:** todo
- **Depende de:** T-101
- **Branch:** `refactor/T-103-access-scope-policy`

## Objetivo
Centralizar em um só lugar a regra "usuário vê só a sua cidade, exceto estabelecimentos onde é `restricted_user`; superuser vê tudo", hoje duplicada em 5 lugares com variações.

## Contexto / porquê
Análise complementar seção 2, Causa raiz B. Duplicada em: `apac_request/admin.py` (`get_queryset`, `EstablishmentCityFilter`, `formfield_for_foreignkey`), `apac_request/views.py` (`ApacRequestListCreate.get`), `apac_batch/views.py` (`ApacBatchsAvailable.get`).

## Escopo
- Criar uma fonte única da regra. Duas opções (decidir na tarefa e documentar):
  - método de repositório `for_user(user)` / `scoped_to_user(qs, user)` na infraestrutura, ou
  - um objeto de política reutilizável que recebe `user` e devolve o filtro.
- Substituir **as 5 implementações** por chamadas à fonte única. Cuidado: hoje há pequenas variações (o batch usa `city=user.city`) — verificar se são intencionais ou bugs; unificar e anotar decisão.
- Adicionar testes cobrindo: superuser vê tudo; usuário comum vê só a sua cidade; `restricted_user` é excluído.

## Fora de escopo
- Novos perfis/permissões. Só consolidar a regra existente.

## Arquivos prováveis
- Novo: `backend/src/<comum>/access_scope.py` ou método nos repositórios relevantes
- `apac_request/admin.py`, `apac_request/views.py`, `apac_batch/views.py`

## Critério de aceite
- [ ] A regra de visibilidade existe em **um** lugar; os 5 pontos a consomem.
- [ ] Testes dos três cenários passam.
- [ ] Comportamento observável preservado (ou divergência de batch corrigida e documentada como intencional).

## Verificação
- `bash scripts/verify.sh` verde. Teste manual: logar como usuário comum e superuser e conferir listas.

## Ao concluir
- Atualizar `architecture.md` (regra transversal com dono único: feito).
