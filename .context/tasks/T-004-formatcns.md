# T-004 — Corrigir bug de regex em `formatCns`

- **Fase:** 0
- **Status:** todo
- **Depende de:** T-001
- **Branch:** `refactor/T-004-formatcns`

## Objetivo
Corrigir a limpeza de CNS no frontend, hoje quebrada por uma regex escrita como string literal.

## Contexto / porquê
`ANALISE_ESTADO_ATUAL.md` item 6 (crítico funcional). Em `PatientInfoService.ts`, `cns.replace('/\D/g', '')` usa uma string, não uma regex — CNS com espaços/traços não é limpo corretamente.

## Escopo
- Trocar `cns.replace('/\D/g', '')` por `cns.replace(/\D/g, '')`.
- Procurar o mesmo padrão de bug em outros formatadores do frontend (CPF, CEP) e corrigir se existir.
- Adicionar teste unitário (Jest) cobrindo CNS com espaços/traços/pontos.

## Fora de escopo
- Refatorar o serviço inteiro. Só o bug + teste.

## Arquivos prováveis
- `frontend/src/app/solicitar/apacRequest/services/PatientInfoService.ts`
- `frontend/src/**/__tests__/` (teste novo)

## Critério de aceite
- [ ] `formatCns` limpa corretamente entradas com caracteres não numéricos.
- [ ] Teste Jest cobre o caso e passa.

## Verificação
- `bash scripts/verify.sh` verde.

## Ao concluir
- Marcar done.
