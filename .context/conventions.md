# Convenções de código

## Nomenclatura (a corrigir — fonte de confusão hoje)

A palavra "controller" significa três coisas erradas no projeto. Alvo:

| Hoje | Alvo | Onde |
|---|---|---|
| `backend/src/*/controller.py` (classes `XController`) | **`XDjangoRepository`** em `repository.py` | são implementações de repositório, não controllers |
| `frontend/src/app/extracao/controllers/*.ts` | **`services/`** ou **`api/`** | são wrappers de `fetch`, não controllers |
| (não existe hoje) "controller" real | camada de **view/serializer** (DRF) | é aqui que fica o HTTP |

> Ao mexer num módulo, prefira já renomear o `controller.py` daquele módulo para `repository.py`. Renome mecânico, sempre com testes verdes antes e depois.

## Camadas — o que pode morar onde

- **Domain (`apac_core/domain`)**: entidades, value objects (`CnsField`, `CpfField`, `CepField`, `CboField`), regras puras, serviços de domínio. **Proibido importar Django.**
- **Application (`apac_core/application`)**: use cases e policies. Recebem repositórios abstratos por injeção de dependência (padrão já usado em `CreateApacRequestUseCase`). **Todo estado de negócio muda aqui.**
- **Infrastructure (`backend/src/<app>`)**: models Django, repositórios (ex-"controller"), integrações externas. Implementa as interfaces de repositório do domínio.
- **Interface**: `views.py` / `serializers.py` (DRF) e o Django Admin. Traduz HTTP↔use case. **Sem regra de negócio.** O mapeamento model→entidade (`to_entity`) é aceitável aqui.

## O que NÃO fazer

- ❌ `queryset.update(status=...)` para transição de negócio (ex.: aprovar). Use o use case.
- ❌ Copiar a regra de visibilidade (`filter(establishment__city=...).exclude(restricted_user=...)`). Use a policy única.
- ❌ Hardcode de `cod_uf`, `cns_paciente`, adaptação por município dentro do fluxo geral do export. Use o perfil por município.
- ❌ Importar Django dentro de `apac_core`.
- ❌ Alterar o conteúdo do arquivo exportado sem tarefa explícita (quebra o golden file).

## Testes

- Domínio/use cases: `backend/core/tests` (pytest, sem banco — usa *fake repositories*).
- Integração dos apps: `backend/src/<app>/tests.py` (Django TestCase).
- Frontend: `frontend/src/**/__tests__` (Jest).
- **Toda tarefa que corrige/adiciona comportamento adiciona teste.** Módulos hoje sem teste (`apac_data`, `apac_batch`, `procedure`, export service) ganham cobertura quando tocados.

## Commits e PRs

- Branch: `refactor/T-XXX-slug-curto`.
- Commits em português, imperativo: `T-003: adiciona autenticação em ExportApacBatch`.
- PR referencia a tarefa (`T-XXX`), lista o que mudou, cola a saída do `/verificar` e confirma que o golden file passou.

## Feature flags

Troca de superfície (admin→React) fica atrás de flag por rota/ambiente. Nunca remova o caminho antigo no mesmo PR que liga o novo — remova só depois de validado em produção (fase 4).
