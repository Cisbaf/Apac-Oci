# T-025 — Alertar quinto dígito de faixa fora do esperado para OCI (ATE)

- **Fase:** 0 · **Status:** todo · **Depende de:** —
- **Branch:** `refactor/T-025-quinto-digito-sem-validacao`

> Detalhado a partir de `ANALISE_VERSAO_PROGRAMA_SIA_APAC.md` (raiz do repo), seção 2.4,
> e **revisado em 2026-07-24** com base em `CADERNO DE REGISTRO DA PRODUÇÃO - PROGRAMA
> AGORA TEM ESPECIALISTAS (ATE) WEB CONFERENCIA SAO PAULO.pdf` (Nota Técnica CISBAF nº
> 04/2026 v1.3, 23/07/2026 — o documento mais recente e mais específico sobre o assunto).
> **Escopo revisado em relação à versão original** — ver "Revisão 2026-07-24" abaixo.
> Pronto para implementar.

## Objetivo
Emitir um alerta (log, não bloqueio) quando uma faixa (`ApacBatch.batch_number`) tiver
o quinto dígito **diferente de "7"** ao ser associada a uma solicitação. Este sistema
opera exclusivamente o componente **Ambulatorial (OCI)** do programa Agora Tem
Especialistas (ATE) — a Nota Técnica CISBAF nº 04/2026 confirma que o 5º dígito correto
da APAC para esse componente é **7** (habilitação CNES 3801, atributo complementar 053).
Qualquer faixa com outro dígito é, no mínimo, suspeita.

## Revisão 2026-07-24 — por que o escopo mudou
A versão original desta tarefa (baseada só no changelog do APAC Magnético) tratava
apenas do dígito **"0"**, banido pelo DATASUS desde 12/2025 (changelog v03.19), e citava
o dígito "9" como sendo o de "Agora Tem Especialista". A Nota Técnica CISBAF nº 04/2026
(mais recente e específica ao programa ATE, que sucedeu o PMAE pela Portaria GM/MS nº
7.266/2025) traz a tabela oficial do 5º dígito por componente e mostra que isso estava
impreciso: **7** é o dígito do componente Ambulatorial/OCI; **9** pertence a Créditos
Financeiros, Ressarcimento ao SUS e Complementar (Modalidades 1 e 2) — componentes que
este sistema **não opera**. Ou seja, "9" não é um dígito válido esperado aqui, e "0"
continua banido — mas o alerta fica mais útil generalizando para "diferente de 7", que
cobre os dois casos e qualquer outro dígito fora do esperado, sem precisar manter uma
lista de exceções.

**Verificado com o usuário:** as faixas já cadastradas hoje no sistema (exemplos:
`3326702390979`, `3326702390924`, `3326702390891`) já usam o dígito **7** — a
convenção correta já está em uso na prática, isso não é uma correção de dado urgente.
O alerta serve para pegar desvios futuros, não um problema existente.

## Por que a validação continua sendo só de formato (não de atributo do procedimento)
A análise original propunha validar o quinto dígito contra o **atributo complementar
do procedimento principal** (ex.: exigir atributo 052/053 no procedimento). Isso não é
possível hoje sem mudança maior: `Procedure` (`domain/entities/procedure.py`) não guarda
atributo complementar do SIGTAP — seria necessário importar/manter essa tabela, o que é
escopo grande e fora do pedido de "mudança mínima". A checagem de formato puro (dígito
== "7" ou não) não depende de nenhuma fonte de dados nova.

## Impacto no formato do export
Nenhum. Não escreve nada novo no arquivo, é um log/alerta no fluxo de aprovação.

## Patch — passo a passo

### 1. `backend/core/src/apac_core/domain/entities/apac_batch.py`
Adicionar um método/propriedade pura ao `ApacBatch`:

```python
def has_unexpected_fifth_digit(self) -> bool:
    """
    Este sistema opera exclusivamente o componente Ambulatorial (OCI) do programa
    Agora Tem Especialistas (ATE), cujo 5º dígito correto na APAC é "7" (Nota
    Técnica CISBAF nº 04/2026 v1.3, 23/07/2026 — habilitação CNES 3801, atributo
    complementar 053). "0" foi banido pelo DATASUS desde 12/2025 (changelog
    v03.19); outros dígitos (6, 8, 9) pertencem a componentes diferentes
    (cirúrgico, créditos financeiros, ressarcimento, complementar) que este
    sistema não opera. Qualquer faixa fora do "7" é, no mínimo, suspeita.
    """
    return len(self.batch_number) >= 5 and self.batch_number[4] != "7"
```

### 2. `backend/core/src/apac_core/application/use_cases/apac_request_cases/authorize_apac_request_case.py`
Em `ApprovedApacRequestUseCase.execute`, depois de `apac_batch.set_apac_request(apac_request)`
(linha 39) e antes do `save` (linha 41), adicionar:

```python
import logging

logger = logging.getLogger(__name__)

# ... dentro de execute(), após apac_batch.set_apac_request(apac_request):
if apac_batch.has_unexpected_fifth_digit():
    logger.warning(
        "Faixa %s associada à APAC %s usa o quinto dígito '%s', diferente do "
        "esperado ('7') para o componente Ambulatorial/OCI (Nota Técnica CISBAF "
        "nº 04/2026). Confirmar se a faixa está correta antes de exportar.",
        apac_batch.batch_number, apac_request.id, apac_batch.batch_number[4],
    )
```
Não bloqueia a aprovação — só registra o alerta, para não mudar comportamento existente.

## Escopo (o que fazer)
- [ ] Aplicar o patch acima.
- [ ] Teste novo: `ApacBatch(batch_number="33267023**0**0979", ...).has_unexpected_fifth_digit()`
      → `True` (dígito banido); mesma faixa com "9" no lugar → `True` (componente
      errado); com "7" (padrão real de faixas já cadastradas) → `False`.
- [ ] Teste novo (ou ajuste de teste existente) cobrindo que `ApprovedApacRequestUseCase`
      continua aprovando normalmente mesmo com o alerta (não passa a lançar exceção).

## Fora de escopo
- Validar contra atributo complementar do procedimento via SIGTAP — precisa de fonte de
  dados nova, é tarefa maior, registrar separadamente se for priorizado.
- Bloquear a aprovação quando o dígito for inesperado — o pedido foi manter o sistema
  funcional com mudança mínima; alertar é reversível e não quebra nenhum fluxo hoje.
- Revalidar/corrigir faixas já cadastradas — não é necessário, já confirmado que usam o
  dígito correto ("7") na prática.

## Como testar
- Automatizado: `cd backend/core && python -m pytest -k has_unexpected_fifth_digit`.
- Manual: aprovar uma solicitação de teste com uma faixa cujo batch_number tenha dígito
  diferente de "7" na 5ª posição e conferir que o log de warning aparece, sem impedir a
  aprovação.

## Critério de aceite
- [ ] `has_unexpected_fifth_digit()` implementado e testado.
- [ ] Alerta emitido no log ao aprovar com faixa de dígito inesperado, sem bloquear o
      fluxo.
- [ ] Gates: `bash scripts/verify.sh` verde.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
