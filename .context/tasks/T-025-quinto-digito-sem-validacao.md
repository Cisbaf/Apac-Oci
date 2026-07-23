# T-025 — Alertar quinto dígito de faixa já proibido pelo DATASUS

- **Fase:** 0 · **Status:** todo · **Depende de:** —
- **Branch:** `refactor/T-025-quinto-digito-sem-validacao`

> Detalhado a partir de `ANALISE_VERSAO_PROGRAMA_SIA_APAC.md` (raiz do repo), seção 2.4.
> **Escopo reduzido deliberadamente** em relação à análise original — ver "Por que o
> escopo foi reduzido" abaixo. Pronto para implementar.

## Objetivo
Emitir um alerta (log, não bloqueio) quando uma faixa (`ApacBatch.batch_number`) com
quinto dígito **"0"** for associada a uma solicitação — essa numeração foi **proibida**
pelo DATASUS a partir da competência 12/2025 (changelog v03.19, "Não permitir quinto
dígito 0 nas APAC's"). Uma faixa "0" ainda em uso hoje é, com alta confiança, um erro
de numeração ou faixa residual que não deveria mais circular.

## Por que o escopo foi reduzido
A análise original propunha validar o quinto dígito contra o **atributo complementar
do procedimento principal** (ex.: dígito "9" exige atributo 052/053 no procedimento).
Isso não é possível hoje sem mudança maior: `Procedure`
(`domain/entities/procedure.py`) não guarda atributo complementar do SIGTAP — seria
necessário importar/manter essa tabela, o que é escopo grande e fora do pedido de
"mudança mínima".

O que dá para fazer **sem nenhuma dependência nova**: o único dígito que o changelog diz
categoricamente que **não deve mais existir**, independente do procedimento, é o "0"
(proibido desde 12/2025). Isso não depende de saber o atributo do procedimento — é uma
checagem de formato pura.

## Impacto no formato do export
Nenhum. Não escreve nada novo no arquivo, é um log/alerta no fluxo de aprovação.

## Patch — passo a passo

### 1. `backend/core/src/apac_core/domain/entities/apac_batch.py`
Adicionar um método/propriedade pura ao `ApacBatch`:

```python
def has_deprecated_fifth_digit(self) -> bool:
    """
    O quinto dígito "0" do número da APAC foi proibido pelo DATASUS a partir da
    competência 12/2025 (era usado para "parcela única de custeio", changelog
    versão 03.16→03.19). Uma faixa com esse dígito hoje é, com alta confiança,
    numeração residual/errada.
    """
    return len(self.batch_number) >= 5 and self.batch_number[4] == "0"
```

### 2. `backend/core/src/apac_core/application/use_cases/apac_request_cases/authorize_apac_request_case.py`
Em `ApprovedApacRequestUseCase.execute`, depois de `apac_batch.set_apac_request(apac_request)`
(linha 39) e antes do `save` (linha 41), adicionar:

```python
import logging

logger = logging.getLogger(__name__)

# ... dentro de execute(), após apac_batch.set_apac_request(apac_request):
if apac_batch.has_deprecated_fifth_digit():
    logger.warning(
        "Faixa %s associada à APAC %s usa o quinto dígito '0', proibido pelo "
        "DATASUS desde a competência 12/2025 (ver changelog APAC Magnético v03.19). "
        "Confirmar se a faixa está correta antes de exportar.",
        apac_batch.batch_number, apac_request.id,
    )
```
Não bloqueia a aprovação — só registra o alerta, para não mudar comportamento existente.

## Escopo (o que fazer)
- [ ] Aplicar o patch acima.
- [ ] Teste novo: `ApacBatch(batch_number="332570027**0**201", ...).has_deprecated_fifth_digit()`
      → `True`; com dígito "7" no lugar → `False`.
- [ ] Teste novo (ou ajuste de teste existente) cobrindo que `ApprovedApacRequestUseCase`
      continua aprovando normalmente mesmo com o alerta (não passa a lançar exceção).

## Fora de escopo
- Validar contra atributo complementar do procedimento (052/053/061/062 etc.) — precisa
  de fonte de dados nova, é tarefa maior, registrar separadamente se for priorizado.
- Bloquear a aprovação quando o dígito for "0" — o pedido foi manter o sistema
  funcional com mudança mínima; alertar é reversível e não quebra nenhum fluxo hoje.

## Como testar
- Automatizado: `cd backend/core && python -m pytest -k has_deprecated_fifth_digit`.
- Manual: aprovar uma solicitação de teste com uma faixa cujo batch_number tenha "0"
  na 5ª posição e conferir que o log de warning aparece, sem impedir a aprovação.

## Critério de aceite
- [ ] `has_deprecated_fifth_digit()` implementado e testado.
- [ ] Alerta emitido no log ao aprovar com faixa "0", sem bloquear o fluxo.
- [ ] Gates: `bash scripts/verify.sh` verde.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
