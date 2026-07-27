# T-017 — CI falha em `backend/src (manage.py test)` por diretório `logs/` ausente

- **Fase:** 0 · **Status:** done · **Depende de:** —
- **Branch:** `refactor/T-017-ci-logs-dir`

## Objetivo
Fazer o gate `backend/src (manage.py test)` passar de fato numa checkout limpa
(CI), não só localmente.

## Contexto / porquê
`backend/src/app/settings.py` configurava `LOGGING` com um `FileHandler`
apontando para `logs/django.log` (relativo a `BASE_DIR`). `logging.FileHandler`
cria o arquivo, mas não o diretório pai. `logs/` está no `.gitignore` (adicionado
na T-005), então numa checkout 100% limpa (como o runner do GitHub Actions) essa
pasta não existe — `django.setup()` explode com `FileNotFoundError` antes de
qualquer teste rodar.

**Gravidade:** confirmado via API do GitHub que **todo PR desde a T-001** (gates)
terminou com `conclusion: failure` neste check. O critério de saída da Fase 0
("`scripts/verify.sh` roda e passa") nunca foi de fato validado em CI — só
localmente, onde o bug estava mascarado.

### Por que ficou tanto tempo invisível
Todos os ambientes de uso real mascaravam a falha, cada um por um motivo:

| Ambiente | Por que não quebrava |
|---|---|
| Máquina do dev | `backend/src/logs/` já existia em disco de execuções antigas (fora do Git) |
| `docker-compose` (dev e prod) | `docker-compose.yml:7` / `docker-compose.dev.yml:7` montam `./logs:/app/src/logs`; o Docker cria o diretório do host se faltar |
| **GitHub Actions** | ❌ checkout limpa, sem compose — **único lugar que expunha o bug** |

## O que foi feito
`backend/src/app/settings.py`: extraído `LOG_DIR` e garantido o diretório com
`os.makedirs(LOG_DIR, exist_ok=True)` **antes** do dict `LOGGING`; o handler
passou a usar `os.path.join(LOG_DIR, 'django.log')`. Comentário no código
explica por que o `makedirs` existe, para ninguém removê-lo achando que é sobra.

Correção deliberadamente em `settings.py`, não no `.gitignore` nem no workflow do
CI: resolve de uma vez para CI, clone novo, container sem volume e máquina de dev
nova, sem depender de um `.gitkeep` rastreado que contradiria o `.gitignore`.

`backend/src/app/tests.py` (novo): `LogDirectorySetupTests`, 2 casos travando a
invariante — o diretório existe após carregar as settings, e o `filename` do
handler aponta para dentro dele. Estes testes **não reproduzem o crash**: quando
ele acontece, o processo morre em `django.setup()` antes do test runner subir, e
o sintoma é o gate inteiro vermelho, não um teste falhando. Eles existem para
documentar a invariante e pegar o handler sendo reapontado para fora do
diretório garantido. Decisão de escopo tomada com o usuário.

## Verificação
Bug reproduzido antes do fix, removendo `backend/src/logs/` para simular a
checkout limpa:

```
FileNotFoundError: [Errno 2] No such file or directory: '.../backend/src/logs/django.log'
ValueError: Unable to configure handler 'file'   ← dentro de django.setup(), 0 testes executados
```

Depois do fix, na mesma condição (`rm -rf backend/src/logs`): `Ran 54 tests — OK`,
diretório recriado automaticamente.

Gate completo (`bash scripts/verify.sh`), rodado 2x com resultado consistente:

| Gate | Resultado |
|---|---|
| `backend/core (pytest)` | ✅ 25 passed |
| `backend/src (manage.py test)` | ✅ Ran 54 tests — OK (52 anteriores + 2 novos) |
| Golden file do export | ✅ inalterado (nenhum arquivo de export tocado) |
| `frontend (jest)` | ✅ 5/5 suítes, 31/31 testes |
| `frontend (lint)` | ✅ 0 erros (10 warnings `exhaustive-deps` pré-existentes, T-010) |

## Aceite
- [x] `backend/src (manage.py test)` passa em checkout limpa (validado removendo
      `backend/src/logs/` e rodando o gate).
- [x] Confirmado no Actions do GitHub que o check fica verde — **PR #27**,
      check `CI / verify (pull_request)` successful em 1m
      ([run 30296433542](https://github.com/Cisbaf/Apac-Oci/actions/runs/30296433542/job/90078538961?pr=27)).
      Primeira vez que os 4 gates passam em CI desde que o gate existe (T-001).
      Mergeado em 2026-07-27 (merge commit `b587efc`).
- [x] Nenhuma mudança de comportamento de negócio — só infra de logging/testes.
- [x] Golden file do export inalterado.
