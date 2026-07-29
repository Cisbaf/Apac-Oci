# T-032 — Validade fixa de 2 competências por procedimento (regressão da T-024)

- **Fase:** 0 · **Status:** done · **Depende de:** T-002, T-024
- **Branch:** `refactor/T-032-validade-fixa-por-procedimento`

## Origem — erro real em produção

Arquivo exportado na competência 06/2026 (lote `3326701975003`, Policlínica Municipal
São José / Mesquita) rejeitado pelo APAC Magnético:

```
202606 3326701975003 ERR CORPO 010087 PROCEDIMENTO EXIGE VALIDADE FIXA DE 2 COMPETENCIAS
```

APAC 34393, procedimento principal **OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE CÂNCER
DE PRÓSTATA**, procedimento em 30/06/2026.

Diagnóstico (sessão de 2026-07-29): **não é erro de preenchimento.** Nenhum campo da tela
do admin alimenta a validade — ela é calculada no export a partir da competência. Para
06/2026 o arquivo saiu com:

| campo | gerado | exigido |
|---|---|---|
| `data_inicio_validade` | `20260601` | `20260601` |
| `data_fim_validade` | `20260831` (3 competências) | `20260731` (2 competências) |

## Causa raiz

A **T-024** trocou a validade de 2 → 3 competências **incondicionalmente**
(`get_end_of_month_offset(d, 2)` em `controller.py:42` e `adapter.py:14`), apoiada no
changelog v03.22 do APAC Magnético, que diz que a Portaria SAES/MS Nº 3.958/2026 excluiu
o atributo complementar "054 — APAC com validade fixa de 2 competências".

A produção mostra que essa premissa era ampla demais: **esta OCI ainda exige 2
competências**. A exclusão do atributo não foi geral — é por procedimento.

A própria T-024 previu o cenário e o deixou fora de escopo ("se aparecer, é tarefa
nova"). Também explica por que a validação manual da T-024 passou em 2026-07-24: foi
feita com um procedimento sem o atributo 054.

## Objetivo

Tornar a validade **condicional por procedimento**, em vez de global: procedimento
marcado com o atributo 054 exporta 2 competências; o resto continua com 3 (regra vigente
da Portaria 3.958/2026). Não reverter a T-024 — ela está certa para o caso geral.

## Escopo

- [x] `ProcedureModel`: campo booleano `fixed_validity_two_competences` (default `False`)
      + migration (`0025_proceduremodel_fixed_validity_two_competences`). Rótulo em
      português no admin, deixando claro que é o atributo SIGTAP 054.
- [x] `Procedure` (entidade pydantic): mesmo campo, default `False` — mantém
      compatibilidade com todos os testes e fixtures existentes.
- [x] `ProcedureModel.to_entity`: propagar o campo.
- [x] `controller.py`: derivar `months_ahead` de
      `apac_data.main_procedure.fixed_validity_two_competences` (1 quando marcado, 2
      caso contrário) em vez do `2` fixo.
- [x] `adapter.py` (`adaptar_oci`): receber `months_ahead` do controller em vez de fixar
      `2` — hoje ele recalcula as duas datas por cima do controller.
- [x] Admin de procedimentos: expor a flag em `list_display`/`list_editable`/`list_filter`
      para o campo poder ser marcado sem migration de dados (só o CISBAF sabe quais
      procedimentos carregam o atributo 054 no SIGTAP).
- [x] Testes: 5 casos novos em `test_validade_por_procedimento.py` (flag ligada → 2
      competências, flag desligada → 3, + virada de ano) e 2 em `procedure/tests.py`
      (propagação da flag no `to_entity`).

## Impacto no formato do export

**Nenhum.** `data_inicio_validade`/`data_fim_validade` continuam com 8 posições
(`AAAAMMDD`) nas mesmas posições. Só muda o *valor*, e só para procedimentos marcados.

**Golden files não podem mudar** — os procedimentos das fixtures não têm a flag, então
caem no default `False` → offset 2 → `20250731`, exatamente como a T-024 deixou. Se o
golden mudar, a implementação está errada (regra 4 do `CLAUDE.md`).

## Fora de escopo

- Marcar quais procedimentos carregam o atributo 054 — é dado, não código; feito no
  admin depois do merge (ver "Após o merge").
- Importar atributos do SIGTAP automaticamente.
- Outros atributos complementares (067-070, citados no changelog v04.00 e ligados às OCIs
  de Infectologia da T-027).

## Verificação

- `cd backend/core && python -m pytest` — inclui os 3 golden files **inalterados**.
- `cd backend/src && python manage.py test`
- `bash scripts/verify.sh` (4 gates).
- `git diff` nos 3 arquivos de `golden/` precisa vir **vazio**.

## Critério de aceite

- [x] Procedimento com a flag ligada exporta `data_fim_validade` = fim do mês seguinte
      (2 competências).
- [x] Procedimento sem a flag continua exportando fim do 3º mês (3 competências).
- [x] Golden files byte a byte idênticos aos da `master` (`git diff` vazio nos 3).
- [x] Gates verdes — `bash scripts/verify.sh` 4/4 (`backend/core` 30/30, `backend/src`
      59/59, jest 5 suítes, lint sem novos avisos).
- [x] Teste do caso 054 **provado vermelho sem o fix** (com `controller.py`/`adapter.py`
      revertidos via stash: `assert '20250731' == '20250630'`).

## Validação com o caso real

Confirmado pelo usuário em 2026-07-29: marcando a OCI de progressão da avaliação
diagnóstica de câncer de próstata com a flag e reexportando, o erro `010087` deixou de
ocorrer. A hipótese do diagnóstico (atributo 054 ainda vigente **por procedimento**, não
excluído em geral) está confirmada na prática, não só no changelog.

## Após o merge (ação do usuário, não do código)

1. No Django Admin → Procedimentos, marcar "Validade fixa de 2 competências" em qualquer
   **outra** OCI que tenha o atributo 054 no SIGTAP — a flag nasce `False` para todas, e
   só a de câncer de próstata foi marcada até agora. Cada procedimento não marcado que
   na verdade tenha o 054 vai reproduzir o mesmo `010087` na próxima exportação.
2. Vale revisar isso junto ao cadastro das OCIs novas da T-026 (Saúde Bucal) e T-027
   (Infectologia), que ainda vão entrar.
