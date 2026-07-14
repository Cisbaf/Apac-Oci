# T-006 — Alinhar a action de status do admin ao use case

- **Fase:** 0
- **Status:** todo
- **Depende de:** T-002
- **Branch:** `refactor/T-006-admin-status-usecase`

## Objetivo
Eliminar a divergência mais perigosa do sistema: aprovar/mudar status pelo Django Admin hoje **não** passa pelo use case e **não** associa faixa, ao contrário do caminho React.

## Contexto / porquê
Análise complementar seção 2, Causa raiz A (a mais grave). Em `apac_request/admin.py`, a action `alterar_status` faz `queryset.update(status=..., review_date=..., authorizer=...)` direto no ORM. O `ApprovedApacRequestUseCase` (caminho React) associa uma faixa ao aprovar. Resultado: uma APAC "aprovada" pelo admin pode ir para a exportação sem faixa/estado inconsistente — bug de dados invisível até virar glosa.

## Escopo
- Fazer a action do admin chamar os use cases existentes (`ApprovedApacRequestUseCase` / `RejectApacRequestUseCase`) em vez de `queryset.update`, para cada registro selecionado, dentro de transação.
- Tratar erros por registro (ex.: sem faixa disponível) e reportar ao usuário do admin via `message_user`.
- Se aprovar em lote for inviável agora, no mínimo **desabilitar** a transição para "approved" via ORM cru e permitir só pending↔rejected, deixando a aprovação para o caminho correto. Decidir na tarefa e documentar.
- Adicionar teste garantindo que aprovar pelo caminho admin resulta no mesmo estado que aprovar pelo use case (inclui faixa associada).

## Fora de escopo
- Migrar a tela para React (isso é T-302, fase 3). Aqui só se corrige a regra por trás da action atual.

## Arquivos prováveis
- `backend/src/apac_request/admin.py` (action `alterar_status`, `StatusForm`)
- teste em `backend/src/apac_request/tests.py`

## Critério de aceite
- [ ] Aprovar pelo admin produz estado idêntico a aprovar pelo use case (faixa associada, `review_date`, `authorizer`).
- [ ] Erros (ex.: faixa indisponível) não deixam estado parcial; usuário é avisado.
- [ ] Golden file inalterado.

## Verificação
- Teste comparando os dois caminhos de aprovação.
- `bash scripts/verify.sh` verde.

## Ao concluir
- Atualizar `architecture.md` (tabela de superfícies: Aprovar/Rejeitar deixa de divergir).
