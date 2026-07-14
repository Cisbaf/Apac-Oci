# Quadro de Tarefas — fonte da verdade do progresso

> Cada tarefa tem um arquivo `T-XXX-*.md` neste diretório com escopo, arquivos afetados, critério de aceite e verificação.
> Status: `todo` · `doing` · `blocked` · `done`. Atualize aqui ao iniciar e ao concluir cada tarefa.
> Trabalhe de cima para baixo, respeitando os bloqueios (`dep`).

## Fase 0 — Blindar
| ID | Tarefa | Status | Dep | Branch |
|---|---|---|---|---|
| T-001 | Infra de gates (`scripts/verify.sh`, rodar pytest+jest) | done | — | `refactor/T-001-gates` |
| T-002 | Golden file / teste de caracterização do export | done | T-001 | `refactor/T-002-golden-export` |
| T-003 | Autenticação em `ExportApacBatch` | done | T-002 | `refactor/T-003-auth-export` |
| T-004 | Corrigir bug regex em `formatCns` | done | T-001 | `refactor/T-004-formatcns` |
| T-005 | Limpeza de arquivos temporários + `.gitignore` | done | — | `refactor/T-005-limpeza-repo` |
| T-006 | Alinhar action de status do admin ao use case | done | T-002 | `refactor/T-006-admin-status-usecase` |
| T-007 | Corrigir testes quebrados em `backend/core` (fixture `ApacRequestFakeRepository`) | todo | T-001 | `refactor/T-007-fix-core-tests` |
| T-008 | Corrigir teste quebrado em `backend/src` (403 em aprovação com faixa) | todo | T-001 | `refactor/T-008-fix-src-tests` |
| T-009 | Corrigir testes quebrados no frontend (import stale + URL sem barra) | todo | T-001 | `refactor/T-009-fix-frontend-tests` |
| T-010 | Débito de lint do frontend (~81 erros pré-existentes, ESLint recém-configurado) | todo | T-001 | `refactor/T-010-lint-debt` |
| T-011 | Atualizar Next.js (vulnerabilidade de segurança reportada pelo npm) | todo | — | `refactor/T-011-upgrade-nextjs` |
| T-012 | Campo de controle do export hardcoded (`cbc-smt-vrf` = "1810" fixo) | todo | T-002 | `refactor/T-012-campo-controle-export` |
| T-013 | `apa_munpcnte` usa cidade do estabelecimento, não do paciente | todo | T-002 | `refactor/T-013-municipio-paciente-export` |
| T-014 | `apa_tipapac`/`apa_motsaida` hardcoded (sempre "Única"/"12") | todo | T-002 | `refactor/T-014-tipo-apac-motivo-saida-hardcoded` |

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
- fix/ci-editable-install-paths — feito em 2026-07-14 — CI (T-001) quebrava 100% das PRs: `backend/requirements.txt` e `backend/core/requirements.txt` tinham `-e` com caminho absoluto específico de máquina/container (`/app/core`, `/home/daniel/...`). Trocado para caminhos relativos (`-e ./core`, `-e .`) + ajuste de `cd` no workflow e no `scripts/verify.sh`; validado com venv nova do zero e com `docker build` do backend.
- T-002 — feito em 2026-07-14 — golden file do export (3 cenários: simples, com subprocedimentos, Duque de Caxias) em `backend/core/tests/domain/services/export/`, byte a byte, com data mockada e determinismo confirmado.
- T-003 — feito em 2026-07-14 — `ExportApacBatch` agora exige `IsAuthenticated` (`SessionAuthentication`/`JWTAuthentication`, mesmo padrão de `ApacBatchsAvailable`); antes qualquer um com a URL exportava dados sensíveis de pacientes sem login. Frontend já enviava `Authorization: Bearer` via proxy (`/api/proxy`), não precisou de ajuste. Teste novo cobre POST sem credencial → 401/403. Golden file (T-002) inalterado. Gates hoje vermelhos só por débito pré-existente (T-007–T-010).
- T-004 — feito em 2026-07-14 — `formatCns` (`PatientInfoService.ts`) usava `cns.replace('/\D/g', '')` (string literal, não regex) e não limpava CNS com espaços/traços/pontos; corrigido para `/\D/g`. `formatCpf`/`formatCep` já usavam regex correta, nenhuma outra ocorrência do bug no frontend. Teste Jest novo (`PatientInfoService.test.tsx`, 9 casos) cobre os três formatadores. Gates hoje vermelhos só por débito pré-existente (T-007–T-010).
- T-005 — feito em 2026-07-14 — escopo original (gitignore + remoção de `data.json`/`faixas_*.txt`/scripts soltos) já estava resolvido manualmente antes de eu começar (arquivos movidos para a branch local `tools`; `db.sqlite3`/`logs/`/`.pytest_cache` já cobertos pelo `.gitignore` genérico). Único item real restante: `backend/src/tools/README.md` (novo) documentando `audit_street_type.py`, o único script que sobrou rastreado em `tools/`. `manage.py check` ok. Gates vermelhos por débito pré-existente (T-007–T-010), inalterados por esta mudança.
- T-006 — feito em 2026-07-14 — escopo mudou ao investigar: a action `alterar_status` descrita na tarefa era código morto (nunca registrada em `actions`, template `change_status.html` inexistente) — removida junto com `StatusForm`. O vetor real e ativo era outro: `get_readonly_fields` liberava `status`/`authorizer`/`review_date` para edição direta por superuser no form padrão do admin, pulando o use case e não associando faixa. Corrigido: esses 3 campos agora são sempre readonly, para todo mundo — aprovar/rejeitar passa a existir só pelo caminho React/use case. `architecture.md` atualizado (tabela de superfícies). Testes novos (`ApacRequestAdminStatusLockTests`, 2 casos) cobrem superuser e admin comum. Golden file inalterado. Gates vermelhos por débito pré-existente (T-007–T-010).
