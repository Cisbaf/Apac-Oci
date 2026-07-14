# T-001 — Infra de gates de verificação

- **Fase:** 0
- **Status:** todo
- **Depende de:** —
- **Branch:** `refactor/T-001-gates`

## Objetivo
Ter um comando único (`scripts/verify.sh`) que roda todos os testes e o lint, falhando se qualquer parte falhar. É a base que todas as tarefas seguintes usam.

## Contexto / porquê
Hoje não há um gate unificado. Sem isso, não dá para garantir "comportamento antes = depois" a cada passo. Ver `../workflow.md` (gates).

## Escopo
- Confirmar como os testes rodam hoje: `cd backend/core && python -m pytest`, `cd backend/src && python -m pytest`, `cd frontend && npm test`, `cd frontend && npm run lint`. Ajustar caminhos conforme a realidade do repo.
- Criar `scripts/verify.sh` que executa os quatro e retorna código de saída ≠ 0 se algum falhar. Imprimir um resumo no final (o que passou/falhou).
- Garantir que roda a partir da raiz do projeto e documenta pré-requisitos (venv do backend ativa, `npm ci` no frontend).
- (Opcional, se houver GitHub Actions) esboçar workflow de CI que chama o mesmo script em PRs para `master`.

## Fora de escopo
- Corrigir testes que já estejam quebrados (registrar como tarefa nova se algum estiver vermelho).
- Adicionar novos testes (isso é T-002 em diante).

## Arquivos prováveis
- `scripts/verify.sh` (novo)
- `.github/workflows/ci.yml` (novo, opcional)

## Critério de aceite
- [ ] `bash scripts/verify.sh` roda os 4 gates e reflete corretamente sucesso/falha no exit code.
- [ ] Documentado no `CLAUDE.md` (já referenciado) e funciona conforme descrito.

## Verificação
- Rodar `bash scripts/verify.sh` com a suíte atual e confirmar que o estado atual é reportado com fidelidade.

## Ao concluir
- Marcar T-001 como done no `INDEX.md`.
