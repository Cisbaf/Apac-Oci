# T-005 — Limpeza de arquivos temporários + `.gitignore`

- **Fase:** 0
- **Status:** todo
- **Depende de:** —
- **Branch:** `refactor/T-005-limpeza-repo`

## Objetivo
Tirar do versionamento arquivos operacionais/temporários que poluem o `src` e adicionar as entradas certas no `.gitignore`.

## Contexto / porquê
`ANALISE_ESTADO_ATUAL.md` item 4. Há `db.sqlite3`, `data.json`, `logs/`, `faixas_*.txt`, `fev_to_mar.txt`, `execute_tools.py` e scripts em `tools/` sem documentação dentro de `backend/src/`.

## Escopo
- Adicionar ao `.gitignore`: `db.sqlite3`, `logs/`, `*.pytest_cache`, arquivos `.txt` avulsos de operação, etc.
- Remover do versionamento (mantendo cópia fora do repo se ainda forem úteis) os arquivos operacionais avulsos.
- Para `tools/` e `execute_tools.py`: **não apagar às cegas** — criar `backend/src/tools/README.md` documentando o que cada script faz (`clean_batchs.py`, `duplicados.py`, `audit_street_type.py`), já que mexem em dados de produção. Só remover o que comprovadamente não é mais usado.

## Fora de escopo
- Reescrever os scripts de `tools/`. Só documentar/organizar.

## Arquivos prováveis
- `.gitignore`
- `backend/src/tools/README.md` (novo)
- remoção de arquivos rastreados indevidamente

## Critério de aceite
- [ ] `git status` limpo de artefatos temporários; `.gitignore` cobre-os.
- [ ] `tools/` documentado; nada removido sem confirmação de uso.

## Verificação
- `bash scripts/verify.sh` verde (limpeza não deve afetar testes).
- Conferir que a app ainda sobe em dev.

## Ao concluir
- Marcar done.
