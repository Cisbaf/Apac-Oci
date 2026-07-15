# T-017 — CI falha em `backend/src (manage.py test)` por diretório `logs/` ausente — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** —
- **Branch:** `refactor/T-017-ci-logs-dir`

> Stub. Achado ao investigar por que o CI da T-011 falhava no gate `backend/src`
> mesmo com `scripts/verify.sh` verde localmente. Expandir com `/tarefa T-017`.

## Objetivo (rascunho)
Fazer o gate `backend/src (manage.py test)` passar de fato numa checkout limpa
(CI), não só localmente.

## Contexto / porquê
`backend/src/app/settings.py:218-227` configura `LOGGING` com um `FileHandler`
apontando para `logs/django.log` (relativo a `BASE_DIR`). `logging.FileHandler`
cria o arquivo, mas não o diretório pai. `logs/` está no `.gitignore` (adicionado
na T-005), então numa checkout 100% limpa (como o runner do GitHub Actions) essa
pasta não existe — `django.setup()` explode com `FileNotFoundError` antes de
qualquer teste rodar.

Localmente o bug fica mascarado porque a pasta `backend/src/logs/` já existe em
disco (criada por execuções anteriores fora do Git).

**Gravidade:** confirmado via API do GitHub que **todo PR desde a T-001** (gates)
terminou com `conclusion: failure` neste check. O critério de saída da Fase 0
("`scripts/verify.sh` roda e passa") nunca foi de fato validado em CI — só
localmente, onde o bug está mascarado.

## Direção
- Correção provável e mínima: garantir o diretório antes do dict `LOGGING`,
  ex. `os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)` em
  `backend/src/app/settings.py`.
- Testar em ambiente limpo de verdade (ex.: `git clone` novo ou removendo a
  pasta `logs/` local) antes de considerar concluído — não confiar só na
  execução local normal, que é justamente o que mascarou o bug até agora.
- Depois de corrigir, abrir o PR e conferir que o check do GitHub Actions
  realmente fica verde (não só `scripts/verify.sh` local).

## Aceite (rascunho)
- [ ] `backend/src (manage.py test)` passa em checkout limpa (CI).
- [ ] Confirmado no Actions do GitHub (não só localmente) que o check fica verde.
- [ ] Nenhuma mudança de comportamento de negócio — só infra de logging/testes.
