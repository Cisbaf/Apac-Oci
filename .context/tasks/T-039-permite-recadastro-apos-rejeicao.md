# T-039 — Checagem de duplicidade deve ignorar solicitação REJEITADA

- **Fase:** 0 · **Status:** done · **Depende de:** —
- **Branch:** `refactor/T-039-permite-recadastro-apos-rejeicao`

## Origem — pedido do usuário

`check_duplicates` (regra que impede registrar duas vezes o mesmo paciente/procedimento/
estabelecimento/competência) comparava **todos** os campos sem olhar o `status` da
solicitação já existente. Isso bloqueava indefinidamente uma nova tentativa de cadastro
mesmo quando a solicitação anterior tinha sido **rejeitada** — o requester ficava sem
caminho para corrigir e reenviar o mesmo paciente na mesma competência.

## Objetivo

Uma solicitação com `status = REJECTED` não conta para a checagem de duplicidade.
Solicitações `PENDING` ou `APPROVED` continuam bloqueando normalmente — só a rejeição
abre exceção.

## Escopo

- [x] `backend/src/apac_request/controller.py` (`ApacRequestController.check_duplicates`):
      `.exclude(status=ApacRequestModel.Status.REJECTED)` na query.
- [x] `backend/core/src/apac_core/application/implementations/apac_request_fake_repository.py`
      (`ApacRequestFakeRepository.check_duplicates`): mesma exclusão, em memória.
- [x] Interface (`domain/repositories/apac_request_repository.py`) não mudou de
      assinatura — a regra é interna à implementação, não um novo parâmetro.
- [x] Testes novos:
  - `backend/core/tests/application/usecases/apac_request/test_create_apac_request.py`:
    duplicidade bloqueada com a primeira `PENDING` (caso que já existia sem cobertura) +
    duplicidade permitida depois de `RejectApacRequestUseCase`.
  - `backend/src/apac_request/tests.py` (`ApacDuplicateCheckTests`): mesmos dois casos,
    via API (Django `TestCase`), confirmando a query real do ORM.

## Fora de escopo

- Mudar a mensagem de erro (`DomainException`) — continua correta para os casos que ainda
  bloqueiam.
- Qualquer alteração no arquivo exportado — a checagem de duplicidade é anterior à criação
  da `ApacData`/export, não toca no layout.

## Verificação

- `cd backend/core && python -m pytest` — 32/32 verde (2 casos novos).
- `cd backend/src && python manage.py test` — 18/18 verde no app `apac_request` (2 casos
  novos), suíte completa sem regressão.
- `bash scripts/verify.sh` — 4/4 verde.
- Golden files inalterados (`git diff` vazio na pasta `golden/`) — mudança não toca export.

## Critério de aceite

- [x] Segunda solicitação para o mesmo paciente/procedimento/estabelecimento/competência
      continua bloqueada enquanto a primeira estiver `PENDING`/`APPROVED`.
- [x] Depois de a primeira ser rejeitada (`RejectApacRequestUseCase`), uma nova solicitação
      idêntica é aceita normalmente (`status` inicial `PENDING`).
- [x] Gates verdes, golden file inalterado.
