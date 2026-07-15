# T-011 — Atualizar Next.js (vulnerabilidade de segurança)

- **Fase:** 0 · **Status:** doing · **Depende de:** —
- **Branch:** `refactor/T-011-upgrade-nextjs`

## Contexto
`npm install` (T-001) reportou: "next@15.3.6: This version has a security vulnerability. Please upgrade to a patched version."
`npm audit` lista múltiplos GHSA para `next` no range `15.3.6`, o mais relevante sendo **GHSA-mg66-mrh9-m8jx** (DoS via exaustão de conexão em Cache Components).

## Investigação
- Advisory oficial: afetados `>=15.0.0, <15.5.16` (linha 15.x) e `>=16.0.0, <16.2.5` (linha 16.x).
- **Não é preciso pular para o major 16** — a linha 15.x tem backport corrigido a partir de `15.5.16`.
- `npm audit fix --force` sugeriu `next@15.5.20` (dist-tag `backport`, última patch estável da linha 15.5.x, > mínimo corrigido).
- `eslint-config-next` segue a mesma versão do `next` por convenção do próprio pacote — bump junto para `15.5.20`.

## Escopo (confirmado com o usuário)
- Atualizar **apenas** `next` (15.3.6 → 15.5.20) e `eslint-config-next` (15.3.6 → 15.5.20) em `frontend/package.json`.
- **Fora de escopo:** as outras ~14 vulnerabilidades do `npm audit` (`form-data` crítico, `next-auth` moderado, `babel/core`, `lodash`, `ws`, `js-yaml`, `minimatch`, `picomatch`, `postcss`, `yaml` etc.) — são transitivas de devDependencies/`next-auth`, não do Next.js em si. Registradas como **T-016**.

## Aceite
- [x] `next` em `15.5.20` (fora do range afetado pelo GHSA-mg66-mrh9-m8jx e demais advisories da linha 15.x).
- [x] `npm audit` não lista mais `next` entre os pacotes vulneráveis.
- [x] `npm run build` (build de produção) limpo — só os warnings pré-existentes de `react-hooks/exhaustive-deps` (fora do escopo desde T-010).
- [x] `bash scripts/verify.sh` — todos os 4 gates verdes (backend/core, backend/src, frontend jest, frontend lint).
- [x] Nenhuma mudança em código de backend — golden file do export inalterado.
