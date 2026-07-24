# T-023 — Campos novos do export (Fonte Orçamentária, Emendas Parlamentares, Pessoa sem CPF)

- **Fase:** 0 · **Status:** done · **Depende de:** T-002
- **Branch:** `refactor/T-023-campos-export-ausentes`

> Especificação **confirmada pelo layout oficial** (`layout_Exportacao_APAC.pdf`,
> gerado 08/07/2026, comparado com `layout_Exportacao_APAC_v20250513.pdf` em
> `ANALISE_LAYOUT_EXPORTACAO_APAC_DIFF.md`, raiz do repo). Não é mais hipótese — as
> posições/tamanhos abaixo vêm direto do documento técnico do SIA. Pronto para
> implementar.

## Decisão: formato único, não multi-versão
Ficou em aberto se o sistema deveria manter **um export por versão do APAC Magnético**
em vez de um único formato sempre atualizado. Decisão do usuário: **não** — seguir com
um formato único (o mais atual) e validar por teste manual antes de cada mudança
(critério de aceite já definido abaixo). Motivos:
- O padrão histórico do DATASUS é sempre **acrescentar campo no fim do registro**,
  nunca inserir no meio — isso é o que torna razoável esperar que leitores mais antigos
  tolerem os bytes extras (a maioria dos parsers posicionais lê até a posição que
  conhece e ignora o resto). Não há garantia absoluta sem testar (não há como inspecionar
  o parser interno do APAC Magnético a partir daqui), por isso o teste manual continua
  sendo o critério de aceite, não uma opção.
- O próprio DATASUS não trata "ficar numa versão antiga" como estado permanente
  esperado — a obrigatoriedade por competência pressupõe que todo mundo atualiza. Manter
  N formatos em paralelo trata um atraso operacional temporário como se fosse requisito
  arquitetural permanente.
- Se o teste manual (seção abaixo) revelar incompatibilidade real com uma versão ainda
  em uso, o conserto correto é operacional (atualizar o APAC Magnético daquela unidade,
  que é obrigação dela de qualquer forma), não código novo de export paralelo.

## Objetivo
Acrescentar 3 campos novos ao final do registro "14" (`ApacModel`), na ordem e tamanho
exatos do layout oficial, sem alterar nenhum campo existente:

| Campo (nome no domínio) | Nome oficial | Tam | Posição no arquivo | Domínio |
|---|---|---|---|---|
| `fonte_orcamentaria` | `apa_fntorca` | **2** | 534-535 | NUM, zeros à esquerda: `"01"` a `"04"` (ver tabela abaixo) |
| `emendas_parlamentares` | `apa_emenpar` | 1 | 536 | CHAR: `"S"`/`"N"`, ou espaço se sem informação |
| `pessoa_sem_cpf` | `apa_semcpf` | 1 | 537 | CHAR: `"S"`/`"N"` — **obrigatório ter valor definido a partir da competência 07/2026 (mês corrente)** |

Códigos de `fonte_orcamentaria`: `01` = Mod.1 Serviço de Saúde-AES · `02` = Mod.2
Equipe Volante-AES · `03` = Crédito Financ. Parc. Vencidas e Vincendas · `04` = Crédito
Financeiro Transação Tributária.

## Impacto no formato do export
Aditivo, confirmado pela fonte oficial: os 3 campos entram **depois** de `situacao_rua`
(posição 533, hoje o último campo do registro) e **antes** do marcador de fim de linha
do layout oficial (`apa_fim`, que no documento passa de 534-535 para 538-539 — o próprio
DATASUS empurrou o terminador, não os campos existentes). Nenhum campo atual muda de
posição ou tamanho.

## Patch — passo a passo

### 1. `backend/core/src/apac_core/domain/services/apac_extract/apac_model.py`
Adicionar ao `__field_sizes__` (ao final do dict, depois de `"situacao_rua": 1`):
```python
"fonte_orcamentaria": 2,
"emendas_parlamentares": 1,
"pessoa_sem_cpf": 1,
```
Adicionar aos campos da classe (ao final, depois de `situacao_rua`, **nesta ordem** —
tem que bater com a ordem do layout oficial):
```python
fonte_orcamentaria: Optional[str] = ""
emendas_parlamentares: Optional[str] = ""
pessoa_sem_cpf: Optional[str] = Field(default="N")
```

Por que os defaults são diferentes:
- `fonte_orcamentaria` em branco — campo só é preenchido quando a faixa usada tem
  quinto dígito 9 (ver "Parte B" abaixo); hoje o sistema não coleta essa escolha.
- `emendas_parlamentares` em branco — não há hoje nenhuma informação real associada a
  esse campo (o único cenário histórico, quinto dígito 0, está banido desde 12/2025); o
  próprio texto do layout oficial permite espaço em branco quando "não há informação a
  ser registrada" (mesmo padrão de `apa_strua`).
- `pessoa_sem_cpf` sempre `"N"` — diferente dos outros dois, aqui o sistema **sabe**
  algo real: `PatientData.cpf` é obrigatório hoje, então todo paciente cadastrado tem
  CPF, e a resposta correta é sempre "não é isento".

### 2. `backend/core/src/apac_core/domain/services/apac_extract/controller.py`
No `ApacModel(...)` dentro de `body()` (depois de `situacao_rua="N"`, linha 93),
acrescentar, na mesma ordem:
```python
fonte_orcamentaria="",
emendas_parlamentares="",
pessoa_sem_cpf="N",
```

### 3. Golden files (`backend/core/tests/domain/services/export/golden/`)
A linha "14" (registro `apac_model`) termina hoje em `...N` (situação de rua). Depois
do patch, passa a terminar em `...N   N` (a mesma terminação de hoje + 4 caracteres:
2 espaços de `fonte_orcamentaria` em branco + 1 espaço de `emendas_parlamentares` em
branco + `N` de `pessoa_sem_cpf`). Confirmado inspecionando o byte final da linha 2 de
`apac_simples.txt` hoje (`...N$`, onde `$` é fim de linha).

Aplicar essa mesma alteração (`N` → `N   N` no final da linha "14") nos 3 arquivos:
- `apac_simples.txt`
- `apac_com_subprocedimentos.txt`
- `apac_duque_de_caxias.txt`

Mudança de conteúdo **intencional**, documentar no PR (referenciar esta tarefa e
`ANALISE_LAYOUT_EXPORTACAO_APAC_DIFF.md`).

## Parte B — "Fonte Orçamentária" continua fora de escopo aqui
Esse campo exige uma escolha real do operador (1 de 4 códigos), só quando a faixa usada
tem quinto dígito 9 — isso é mudança de UI/fluxo de digitação, não só de export. Fica
reservado em branco nesta tarefa. **Se/quando confirmar que o município já usa quinto
dígito 9**, abrir T-026 só para essa UI (referenciando esta tarefa e a tabela de
códigos acima). Ao implementar, usar `format_with_zeros(codigo, 2)` para o zero à
esquerda — **não** passar o código cru, senão o valor sai errado (ex.: `"1 "` em vez de
`"01"`, porque `fix_length` completa com espaço à direita, não zero à esquerda).

## Fora de escopo
- UI para capturar `fonte_orcamentaria` de verdade — vira T-026 se necessário.
- UI para o cenário real de "paciente sem CPF" (hoje o sistema não permite cadastrar
  sem CPF; tornar `PatientData.cpf` opcional é mudança maior, separada).
- Implementar o campo `apa_fim` (terminador CR+LF explícito) — o código hoje já não
  modela esse campo (usa `"\n".join` entre linhas), débito pré-existente e fora do
  escopo desta tarefa.
- Atualizar `versao_layout` no header (`"Versao 03.15"`) — é só um rótulo textual,
  decisão à parte.

## Como testar direto no APAC Magnético (validação manual)
1. Gerar um export real de uma APAC de teste.
2. Abrir o `.txt` e conferir que a linha "14" agora termina em `...N   N` (4 bytes a
   mais que antes).
3. Importar no APAC Magnético local.
4. Confirmar: importa sem erro, e o campo "Pessoa sem CPF/Registro Civil" aparece na
   tela como "Não". "Fonte Orçamentária"/"Emendas Parlamentares" devem aparecer em
   branco/não preenchidos, sem crítica de campo obrigatório faltando (o layout marca os
   3 como "NÃO obrigatório").

## Critério de aceite
- [x] 3 campos novos implementados, na ordem e tamanho exatos da tabela acima.
- [x] Golden files atualizados de propósito (`N` → `N   N` no fim da linha "14"), PR
      explica o motivo.
- [x] Gates: `bash scripts/verify.sh` verde.
- [x] Validação manual no APAC Magnético local: arquivo aceito, campo "Pessoa sem
      CPF/Registro Civil" exibido corretamente como "Não". Confirmado pelo usuário
      em 2026-07-24.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
- Se o pré-requisito revelar uso de quinto dígito 9: abrir T-026 (UI de Fonte
  Orçamentária) e registrar em `INDEX.md`.
