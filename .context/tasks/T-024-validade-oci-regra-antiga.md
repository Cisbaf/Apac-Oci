# T-024 — Validade da APAC OCI usa regra extinta (2 competências → 3 meses)

- **Fase:** 0 · **Status:** todo · **Depende de:** T-002
- **Branch:** `refactor/T-024-validade-oci-regra-antiga`

> Detalhado a partir de `ANALISE_VERSAO_PROGRAMA_SIA_APAC.md` (raiz do repo), seção 2.3
> e 4.1. Pronto para implementar — patch concreto abaixo. **Prioridade alta:** o
> comportamento atual já está incorreto desde a competência 04/2026 (Portaria SAES/MS
> Nº 3.958/2026).
>
> **Nota de reconciliação (2026-07-23):** esta tarefa nasceu como "T-019" numa branch
> de documentação (`docs/registra-T-018-a-T-022`) que colidiu com o T-019 já em uso
> pela linha de correção da faixa (`refactor/T-019-admin-lock-vinculo-faixa`).
> Renumerada para T-024. Já existe uma implementação candidata deste patch no branch
> local `t019-patch-ready` (commit `ff6f43b`) — precisa rebase em cima da `master`
> atual e renomeação para `refactor/T-024-validade-oci-regra-antiga` antes de virar PR.

## Objetivo
Trocar o cálculo de `data_fim_validade` de "fim do mês seguinte" (2 competências, regra
extinta do atributo complementar 054) para "fim do 3º mês" (3 competências, validade
normal vigente desde 04/2026). **Zero mudança de forma do arquivo** — só o valor de dois
campos que já existem.

## Impacto no formato do export
Nenhum. `data_inicio_validade`/`data_fim_validade` continuam com 8 posições
(`AAAAMMDD`), na mesma posição no registro. Compatível com qualquer versão do APAC
Magnético instalada localmente (não depende de campo novo).

## Patch — passo a passo

### 1. `backend/core/src/apac_core/domain/services/apac_extract/utils.py`
Adicionar uma versão generalizada de `get_end_of_next_month`, mantendo a função antiga
intacta (não é usada em mais nenhum lugar depois do passo 2, mas não precisa remover):

```python
def get_end_of_month_offset(d: date, months_ahead: int) -> date:
    """
    Retorna o último dia do mês que fica `months_ahead` meses à frente do mês de `d`.

    months_ahead=1 replica o comportamento antigo de `get_end_of_next_month`
    (regra extinta do atributo complementar 054 — 2 competências).
    months_ahead=2 dá o último dia do 3º mês, ou seja, a validade normal de uma
    APAC (3 meses/competências) vigente desde a Portaria SAES/MS Nº 3.958/2026
    (competência 04/2026 em diante).
    """
    year = d.year
    month = d.month + months_ahead
    while month > 12:
        month -= 12
        year += 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)
```

### 2. `backend/core/src/apac_core/domain/services/apac_extract/controller.py`
- Linha 12-14 (import): trocar `get_end_of_next_month` por `get_end_of_month_offset`.
- Linha 42: `data_fim = get_end_of_next_month(self.date_production)` →
  `data_fim = get_end_of_month_offset(self.date_production, 2)`

### 3. `backend/core/src/apac_core/domain/services/apac_extract/adapter.py`
- Linha 5 (import): trocar `get_end_of_next_month` por `get_end_of_month_offset`.
- Linha 14: `apac_model.data_fim_validade = get_end_of_next_month(procedure_date).strftime("%Y%m%d")`
  → `apac_model.data_fim_validade = get_end_of_month_offset(procedure_date, 2).strftime("%Y%m%d")`

### 4. Golden files (`backend/core/tests/domain/services/export/golden/`)
`PRODUCTION = date(2025, 5, 1)` nos testes → `data_fim_validade` muda de `20250630`
(fim de junho/2025, 2 competências) para `20250731` (fim de julho/2025, 3
competências). Ocorre **1 vez em cada um dos 3 arquivos** (confirmado por grep):

- `apac_simples.txt` — trocar `20250630` → `20250731`
- `apac_com_subprocedimentos.txt` — trocar `20250630` → `20250731`
- `apac_duque_de_caxias.txt` — trocar `20250630` → `20250731`

Essa é uma mudança de conteúdo **intencional** do golden — documentar no PR (referenciar
esta tarefa e a Portaria SAES/MS Nº 3.958/2026).

## Escopo (o que fazer)
- [ ] Aplicar o patch acima (utils.py, controller.py, adapter.py).
- [ ] Atualizar os 3 golden files.
- [ ] Rodar `cd backend/core && python -m pytest` — os 3 testes de golden file e o de
      determinismo devem passar com os novos valores.
- [ ] Testar manualmente (ver seção abaixo).

## Fora de escopo
- Tornar a validade condicional por atributo do procedimento (ex.: algum procedimento
  específico que ainda exija 2 competências) — não há evidência disso no changelog para
  as versões atuais; se aparecer, é tarefa nova.
- `adaptar_oci`/generalização por município (`MunicipalityExportProfile`) — isso é T-202.

## Como testar direto no APAC Magnético (validação manual)
1. Gerar um export real do sistema (ambiente de homologação/local) para uma APAC de
   teste, competência atual.
2. Abrir o `.txt` gerado e conferir visualmente que `data_fim_validade` (posições 47-54
   da linha "14") corresponde a **3 meses** a partir da data de produção, não 2.
3. Importar esse arquivo no APAC Magnético instalado localmente.
4. Na tela da APAC importada, conferir o período de vigência exibido — deve mostrar 3
   meses de validade, sem crítica/erro de data.
5. Se o APAC Magnético aceitar sem erro e mostrar a vigência correta: mudança validada,
   pode seguir para PR. Se der erro ou mostrar vigência diferente da esperada: parar e
   revisar a hipótese antes de prosseguir (pode indicar que a Portaria define a janela
   de um jeito diferente do assumido aqui — nesse caso, valeria pegar o texto integral
   da Portaria SAES/MS Nº 3.958/2026 para confirmar).

## Critério de aceite
- [ ] `data_fim_validade` reflete 3 meses (fim do mês `produção + 2`) em vez de 2.
- [ ] Golden files atualizados de propósito, PR explica o motivo.
- [ ] Gates: `bash scripts/verify.sh` verde.
- [ ] Validação manual no APAC Magnético local feita e documentada no PR (aceitou o
      arquivo, vigência exibida bate com o esperado).

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
