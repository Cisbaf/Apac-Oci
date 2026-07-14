# T-011 — Atualizar Next.js (vulnerabilidade de segurança) — STUB

- **Fase:** 0 · **Status:** todo · **Depende de:** —
- **Branch:** `refactor/T-011-upgrade-nextjs`

> Stub. `npm install` (T-001) reportou: "next@15.3.6: This version has a security vulnerability. Please upgrade to a patched version." Expandir com `/tarefa T-011`.

## Objetivo (rascunho)
Atualizar `next` (`frontend/package.json`, hoje `15.3.6`) para uma versão corrigida, sem quebrar build/testes.

## Direção
- Conferir o boletim oficial do Next.js referenciado pelo aviso do npm para saber o alcance da vulnerabilidade e a versão mínima segura.
- Atualizar `next` (e dependências relacionadas, se exigido) e rodar `bash scripts/verify.sh` + build (`npm run build`) antes de considerar concluído.
- Ficar atento a breaking changes entre minor/major.

## Aceite (rascunho)
- [ ] `next` em versão sem a vulnerabilidade reportada.
- [ ] `npm run build`, testes e lint verdes (ou sem regressão em relação ao estado pré-tarefa).
