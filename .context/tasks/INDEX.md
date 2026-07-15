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
| T-007 | Corrigir testes quebrados em `backend/core` (fixture `ApacRequestFakeRepository`) | done | T-001 | `refactor/T-007-fix-core-tests` |
| T-008 | Corrigir teste quebrado em `backend/src` (403 em aprovação com faixa) | done | T-001 | `refactor/T-008-fix-src-tests` |
| T-009 | Corrigir testes quebrados no frontend (import stale + URL sem barra) | done | T-001 | `refactor/T-009-fix-frontend-tests` |
| T-010 | Débito de lint do frontend (~81 erros pré-existentes, ESLint recém-configurado) | done | T-001 | `refactor/T-010-lint-debt` |
| T-011 | Atualizar Next.js (vulnerabilidade de segurança reportada pelo npm) | done | — | `refactor/T-011-upgrade-nextjs` |
| T-012 | Campo de controle do export hardcoded (`cbc-smt-vrf` = "1810" fixo) | done | T-002 | `refactor/T-012-campo-controle-export` |
| T-013 | `apa_munpcnte` usa cidade do estabelecimento, não do paciente | todo | T-002 | `refactor/T-013-municipio-paciente-export` |
| T-014 | `apa_tipapac`/`apa_motsaida` hardcoded (sempre "Única"/"12") | todo | T-002 | `refactor/T-014-tipo-apac-motivo-saida-hardcoded` |
| T-015 | Teste de integração para o fluxo de solicitação de APAC (`ApacRequestFormProvider` + `ApacRequestFillingData` + `ApacRequestFinishForm`) | todo | T-009 | `refactor/T-015-integration-test-apac-request` |
| T-016 | Vulnerabilidades restantes do `npm audit` no frontend (14 avisos: `form-data` crítico, `next-auth` moderado, `babel/core`, `lodash`, `ws`, `js-yaml`, `minimatch`, `picomatch`, `postcss`, `yaml`, etc. — transitivas de devDependencies/`next-auth`, não relacionadas ao Next.js em si) | todo | — | `refactor/T-016-npm-audit-debt` |
| T-017 | **Urgente** — CI (`scripts/verify.sh` no GitHub Actions) falha em `backend/src (manage.py test)` em toda checkout limpa: `LOGGING` (`backend/src/app/settings.py:218`) aponta `FileHandler` para `logs/django.log`, mas `logs/` está no `.gitignore` (T-005) e `FileHandler` não cria o diretório pai — `django.setup()` explode com `FileNotFoundError` antes de rodar qualquer teste. Mascarado localmente porque a pasta já existe em disco (fora do Git). Confirmado via API do GitHub: **todo PR desde a T-001 já terminou com `conclusion: failure`** neste check — o critério de saída da Fase 0 ("`scripts/verify.sh` roda e passa") nunca foi de fato validado em CI. Correção provável: `os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)` antes do dict `LOGGING` em `settings.py`. | todo | — | `refactor/T-017-ci-logs-dir` |

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
- T-007 — feito em 2026-07-14 — `backend/core (pytest)` foi de 16 erros + 4 falhas para 19/19 verde. Causa raiz: `ApacRequestFakeRepository` não implementava `check_duplicates` (abstrato na interface) — implementado espelhando a lógica do `ApacRequestController` real. Ao corrigir isso, apareceu um segundo caso do mesmo tipo: `ApacBatchFakeRepository.search_for_available_batch` só aceitava `city_id`, mas a interface já exige `(city_id, competence)` — adicionado o parâmetro (opcional, sem filtro por competência, já que nenhum teste depende disso e replicar a regra real de código de faixa por ano seria comportamento novo). Removido `tests/application/usecases/apac_export/test_export_case.py`: redundante com o golden file da T-002 e com string esperada desatualizada (confirmado com o usuário antes de apagar). Nenhuma mudança de comportamento de negócio, só fixtures de teste. Golden file inalterado.
- T-008 — feito em 2026-07-14 — `backend/src (manage.py test)` foi de 2 falhas (403 em vez de 200 na aprovação) para 49/49 verde e estável (5 execuções seguidas). Causa raiz: o commit `997c279` ("search batch for year competence") passou a exigir que `batch_number` codifique o ano de competência (2 dígitos) nas posições 3-4 (`Substr('batch_number', 3, 2)` em `ApacBatchController.search_for_available_batch`), mas o helper `create_batch` dos testes (`apac_request/tests.py`) gerava um número totalmente aleatório — nunca batia, então a faixa nunca era encontrada. Não era regressão de produção nem flakiness real, era teste desatualizado em relação a uma regra de negócio já intencional. Corrigido: `create_batch` agora embute o ano de competência correto (derivado do `request_date` do APAC). Nenhuma mudança de código de produção. Golden file inalterado.
- T-009 — feito em 2026-07-14 — `frontend (jest)` foi de 2 suítes falhando (1 erro de config + 1 assert) para 5/5 suítes, 31/31 testes verdes. `VerificationService.test.tsx` esperava `/api/proxy/procedure/apac/check-age-alert/` (com barra final); o código usa sem barra, batendo com a rota Django (`path('apac/check-age-alert', ...)`, sem barra) e com a convenção de todo o resto do frontend (~10 outras chamadas `/api/proxy/*` conferidas, nenhuma com barra final) — corrigida a expectativa do teste, código intocado. `ApacRequestService.test.tsx` importava um componente (`components/ApacRequestService`) que nunca existiu no histórico do git (não foi renomeado) e assumia um contrato incompatível com a arquitetura atual do fluxo de solicitação (`ApacRequestFormProvider`/`ApacRequestFillingData`/`ApacRequestFinishForm`, que faz fetch direto) — era teste morto, removido (confirmado com o usuário antes). Registrada T-015 para escrever teste de integração real do fluxo atual, fora do escopo desta tarefa. Nenhuma mudança de código de produção. Golden file inalterado.
- T-010 — feito em 2026-07-14 — `frontend (lint)` foi de 80 erros para 0 (10 warnings de `react-hooks/exhaustive-deps` deixados de fora, conforme aceite). Corrigidos por categoria: imports/variáveis não usados removidos; `var`→`let`; `@ts-ignore`→`@ts-expect-error` com descrição; `display-name` ausente em componentes `forwardRef` anônimos (`.displayName` adicionado); `any` explícito tipado corretamente (`auth.ts`: `JWT`/`JwtPayload` do next-auth/jwt-decode; `GlobalAlert.tsx`: tipos derivados de `SnackbarProps` em vez de recriar à mão; `validate.ts`/`ExportContext.tsx`: tipos reais das libs). Duas exceções pontuais e justificadas com `eslint-disable-next-line` (não elegíveis para tipagem sem refactor maior): `GlobalUIContext.showResponseApi` (repassa JSON de formatos heterogêneos de vários endpoints) e `sensitiveFields.removeSensitiveFields` (destructuring para excluir `password`, padrão idiomático). Após tipar `auth.ts`/`next-auth.d.ts`, `npx tsc --noEmit` acusou 2 erros reais introduzidos pela tipagem mais estrita (JWT.user.name/email não aceitavam `null` como `DefaultUser`; TransitionProps do Snackbar não batia com GrowProps) — corrigidos, e `tsc --noEmit` + `npm run build` (build de produção completo) confirmados limpos, não só o lint. Nenhuma mudança de comportamento do app. Golden file inalterado (sem mudanças em backend). **Primeira vez que os 4 gates do `scripts/verify.sh` passam juntos.**
- T-011 — feito em 2026-07-15 — `next` 15.3.6 → 15.5.20 (`frontend/package.json` + `eslint-config-next` junto). Advisory oficial (GHSA-mg66-mrh9-m8jx e outros) mostrou que a linha 15.x tem backport corrigido a partir de `15.5.16` — não foi preciso pular para o major 16. `npm audit` não lista mais `next` como vulnerável. `npm run build` e os 4 gates de `scripts/verify.sh` verdes (build só com os warnings pré-existentes de `react-hooks/exhaustive-deps`, fora de escopo desde T-010). As ~14 vulnerabilidades restantes do `npm audit` (transitivas de devDependencies/`next-auth`, não do Next.js) ficaram fora do escopo por decisão do usuário — registradas em T-016. Nenhuma mudança em backend; golden file inalterado.
- T-012 — feito em 2026-07-15 — escopo ajustado pelo usuário ao confirmar: `campo_controle` (`"1810"` fixo) é recalculado automaticamente pelo próprio APAC Magnético após a importação, então nunca causou problema — não é crítico corrigir agora. Implementada só a fórmula oficial (soma código de procedimentos + quantidade + número da APAC, resto mod 1111, +1111) como função pura e isolada: `calculate_control_field` em `domain/services/apac_extract/control_field.py`, 6 testes novos em `tests/domain/services/apac_extract/test_control_field.py` (limites do domínio [1111..2221], soma composta, cenário com dados reais dos fixtures do golden). **Não ligada ao fluxo real** — `controller.py`/`header()` continua com `"1810"` fixo, golden file (T-002) inalterado (confirmado por `git diff` vazio). Fica disponível para ativação futura, documentada no próprio arquivo da tarefa. Gates verdes.
