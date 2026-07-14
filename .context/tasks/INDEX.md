# Quadro de Tarefas — fonte da verdade do progresso

> Cada tarefa tem um arquivo `T-XXX-*.md` neste diretório com escopo, arquivos afetados, critério de aceite e verificação.
> Status: `todo` · `doing` · `blocked` · `done`. Atualize aqui ao iniciar e ao concluir cada tarefa.
> Trabalhe de cima para baixo, respeitando os bloqueios (`dep`).

## Fase 0 — Blindar
| ID | Tarefa | Status | Dep | Branch |
|---|---|---|---|---|
| T-001 | Infra de gates (`scripts/verify.sh`, rodar pytest+jest) | done | — | `refactor/T-001-gates` |
| T-002 | Golden file / teste de caracterização do export | todo | T-001 | `refactor/T-002-golden-export` |
| T-003 | Autenticação em `ExportApacBatch` | todo | T-002 | `refactor/T-003-auth-export` |
| T-004 | Corrigir bug regex em `formatCns` | todo | T-001 | `refactor/T-004-formatcns` |
| T-005 | Limpeza de arquivos temporários + `.gitignore` | todo | — | `refactor/T-005-limpeza-repo` |
| T-006 | Alinhar action de status do admin ao use case | todo | T-002 | `refactor/T-006-admin-status-usecase` |
| T-007 | Corrigir testes quebrados em `backend/core` (fixture `ApacRequestFakeRepository`) | todo | T-001 | `refactor/T-007-fix-core-tests` |
| T-008 | Corrigir teste quebrado em `backend/src` (403 em aprovação com faixa) | todo | T-001 | `refactor/T-008-fix-src-tests` |
| T-009 | Corrigir testes quebrados no frontend (import stale + URL sem barra) | todo | T-001 | `refactor/T-009-fix-frontend-tests` |
| T-010 | Débito de lint do frontend (~81 erros pré-existentes, ESLint recém-configurado) | todo | T-001 | `refactor/T-010-lint-debt` |
| T-011 | Atualizar Next.js (vulnerabilidade de segurança reportada pelo npm) | todo | — | `refactor/T-011-upgrade-nextjs` |

## Fase 1 — Fronteiras
| ID | Tarefa | Status | Dep | Branch |
|---|---|---|---|---|
| T-101 | Renomear `Controller`→`Repository` (backend) | todo | Fase 0 | `refactor/T-101-rename-repository` |
| T-102 | Renomear `controllers/`→`services/` (frontend) | todo | Fase 0 | `refactor/T-102-rename-services` |
| T-103 | `AccessScopePolicy` única (visibilidade) | todo | T-101 | `refactor/T-103-access-scope-policy` |

## Fase 2 — Um caminho por operação
| ID | Tarefa | Status | Dep | Branch |
|---|---|---|---|---|
| T-201 | Transições de estado via use case (admin incluso) | todo | T-006, T-103 | `refactor/T-201-state-usecases` |
| T-202 | `MunicipalityExportProfile` (tirar hardcodes do export) | todo | T-002 | `refactor/T-202-municipality-profile` |

## Fase 3 — Strangler frontend
| ID | Tarefa | Status | Dep | Branch |
|---|---|---|---|---|
| T-301 | Namespace API v2 + infra de feature flag | todo | Fase 2 | `refactor/T-301-api-v2-flags` |
| T-302 | Gestão de status em React | todo | T-301 | `refactor/T-302-status-react` |
| T-303 | Gestão de faixas em React | todo | T-301 | `refactor/T-303-batches-react` |
| T-304 | Dashboard em React | todo | T-301 | `refactor/T-304-dashboard-react` |

## Fase 4 — Remoção do legado
| ID | Tarefa | Status | Dep | Branch |
|---|---|---|---|---|
| T-401 | Remover views/actions legadas e código morto | todo | Fase 3 | `refactor/T-401-remove-legacy` |

---

### Detalhamento das tarefas
Fase 0 e Fase 1 estão detalhadas em arquivos próprios (`T-001-*.md` … `T-103-*.md`).
Fases 2–4 têm stubs (`T-201-*.md` etc.) que devem ser **expandidos com `/tarefa` no momento em que forem iniciadas**, quando o código já refletir as fases anteriores — evita planejar em cima de suposições que vão mudar.

### Log de conclusão
_(preencher ao concluir: `T-XXX — feito em AAAA-MM-DD — PR #NN — resumo de uma linha`)_

- T-001 — feito em 2026-07-14 — `scripts/verify.sh` funcional (ativa venv, usa `manage.py test` em `backend/src`) e ESLint configurado no frontend; gates hoje vermelhos por débito pré-existente, registrado em T-007–T-010.
