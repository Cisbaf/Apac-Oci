# T-003 — Autenticação em `ExportApacBatch`

- **Fase:** 0
- **Status:** todo
- **Depende de:** T-002
- **Branch:** `refactor/T-003-auth-export`

## Objetivo
Proteger o endpoint de exportação, que hoje não tem autenticação nem permissão — qualquer um com a URL pode gerar arquivos com dados sensíveis de pacientes.

## Contexto / porquê
`ANALISE_ESTADO_ATUAL.md` item 12 (crítico). Em `backend/src/apac_batch/views.py`, `ExportApacBatch(APIView)` não define `authentication_classes` nem `permission_classes`, ao contrário das outras views.

## Escopo
- Adicionar em `ExportApacBatch` os mesmos `authentication_classes = [SessionAuthentication, JWTAuthentication]` e `permission_classes = [IsAuthenticated]` já usados em `ApacBatchsAvailable` e nas views de `apac_request`.
- Confirmar que o frontend (`/extracao` → `GetExtractFile`) envia a credencial pelo proxy autenticado; ajustar se necessário.

## Fora de escopo
- Regras de autorização por perfil (só autorizador/admin pode exportar) — se desejável, vira tarefa nova. Aqui é só exigir usuário autenticado.

## Arquivos prováveis
- `backend/src/apac_batch/views.py`

## Critério de aceite
- [ ] Requisição sem autenticação ao endpoint de export retorna 401/403.
- [ ] Fluxo de exportação pelo frontend continua funcionando para usuário logado.
- [ ] Golden file (T-002) inalterado — o conteúdo do arquivo não muda.

## Verificação
- Teste que chama o endpoint sem credencial e espera 401/403.
- `bash scripts/verify.sh` verde. Teste manual da tela `/extracao` logado.

## Ao concluir
- Marcar done; nota no PR de que é correção de segurança crítica.
