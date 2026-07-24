# T-025 — Bloquear importação de faixa com quinto dígito fora do esperado para OCI (ATE)

- **Fase:** 0 · **Status:** todo · **Depende de:** —
- **Branch:** `refactor/T-025-quinto-digito-sem-validacao`

> Detalhado a partir de `ANALISE_VERSAO_PROGRAMA_SIA_APAC.md` (raiz do repo), seção 2.4,
> e **revisado em 2026-07-24** com base em `CADERNO DE REGISTRO DA PRODUÇÃO - PROGRAMA
> AGORA TEM ESPECIALISTAS (ATE) WEB CONFERENCIA SAO PAULO.pdf` (Nota Técnica CISBAF nº
> 04/2026 v1.3, 23/07/2026 — o documento mais recente e mais específico sobre o assunto).
> **Escopo e local da validação revisados pelo usuário** — ver "Revisão 2026-07-24"
> abaixo. Pronto para implementar.

## Objetivo
Bloquear a **importação** de uma faixa (`ApacBatchModel.batch_number`) cujo quinto
dígito seja **diferente de "7"**. Este sistema opera exclusivamente o componente
**Ambulatorial (OCI)** do programa Agora Tem Especialistas (ATE) — a Nota Técnica
CISBAF nº 04/2026 confirma que o 5º dígito correto da APAC para esse componente é **7**
(habilitação CNES 3801, atributo complementar 053). Uma faixa de outro componente
(cirúrgico, financeiro, ressarcimento etc.) não deve sequer entrar no sistema.

## Revisão 2026-07-24 — o que mudou e por quê

**Quando validar (correção do usuário):** a versão anterior desta tarefa colocava a
checagem no momento da **aprovação** (`ApprovedApacRequestUseCase`), como um alerta de
log, não bloqueio. O usuário apontou que isso é tarde demais — nesse ponto a faixa já
foi importada e está disponível para uso. **A validação certa é na importação/registro
da faixa**, para nunca deixar uma faixa inválida entrar no sistema. Local real
encontrado: `ImportFaixasForm.clean()` (`backend/src/apac_batch/forms.py:67-129`) —
já é onde o sistema valida formato (regex 13 dígitos), quantidade esperada e
duplicatas (banco + input) antes de `salvar()` fazer o `bulk_create`. A validação do
5º dígito entra como mais um passo dessa mesma sequência, e **bloqueia** (levanta
`ValidationError`, mesmo padrão dos outros 4 erros já existentes) — não é só log.

**Qual dígito é o correto (achado do documento novo):** a versão anterior tratava só do
dígito **"0"** (banido pelo DATASUS desde 12/2025, changelog v03.19) e citava "9" como
sendo de "Agora Tem Especialista". A Nota Técnica CISBAF nº 04/2026 (mais recente e
específica ao programa ATE, que sucedeu o PMAE pela Portaria GM/MS nº 7.266/2025) traz a
tabela oficial do 5º dígito por componente e mostra que isso estava impreciso: **7** é o
dígito do componente Ambulatorial/OCI; **9** pertence a Créditos Financeiros,
Ressarcimento ao SUS e Complementar (Modalidades 1 e 2) — componentes que este sistema
**não opera**. O alerta generaliza de "dígito == 0" para "dígito != 7", cobrindo os dois
casos sem precisar manter lista de exceções.

**Verificado com o usuário:** as faixas já cadastradas hoje no sistema (exemplos:
`3326702390979`, `3326702390924`, `3326702390891`) já usam o dígito **7** — a convenção
correta já está em uso na prática. Bloquear na importação não afeta nada que já existe,
só impede que uma faixa errada entre no futuro.

## Por que a validação continua sendo só de formato (não de atributo do procedimento)
A análise original propunha validar o quinto dígito contra o **atributo complementar do
procedimento principal** (ex.: exigir atributo 052/053 no procedimento). Isso não é
possível hoje sem mudança maior: `Procedure` (`domain/entities/procedure.py`) não guarda
atributo complementar do SIGTAP — seria necessário importar/manter essa tabela, escopo
grande e fora do pedido de "mudança mínima". A checagem de formato puro (dígito == "7"
ou não) não depende de nenhuma fonte de dados nova.

## Impacto no formato do export
Nenhum. Não escreve nada novo no arquivo — é uma validação na importação de faixas, uma
etapa totalmente anterior ao export.

## Patch — passo a passo

### `backend/src/apac_batch/forms.py`
Adicionar uma constante e um passo de validação em `ImportFaixasForm.clean()`, no mesmo
padrão dos 4 já existentes (formato, quantidade, duplicatas banco, duplicatas input):

```python
QUINTO_DIGITO_OCI = "7"  # Ambulatorial/OCI — Nota Técnica CISBAF nº 04/2026 v1.3
```

Dentro de `clean()`, após a validação de formato (`invalidos`) e antes/depois das
demais (ordem não importa, todas acumulam em `erros`):

```python
# 5. Validação do quinto dígito (componente Ambulatorial/OCI = "7")
digito_errado = [
    n for n in numeros
    if FORMATO_FAIXA.match(n) and n[4] != QUINTO_DIGITO_OCI
]
if digito_errado:
    lista = ', '.join(digito_errado)
    erros.append(
        f"As seguintes faixas têm o 5º dígito diferente de '{QUINTO_DIGITO_OCI}' "
        f"(esperado para o componente Ambulatorial/OCI, Nota Técnica CISBAF nº "
        f"04/2026): {lista}"
    )
```

Nota: `if FORMATO_FAIXA.match(n)` evita checar o dígito de algo que já falhou na
validação de formato (string maior/menor que 13 dígitos, ou não numérica) — mantém os
erros independentes e evita um `IndexError` se `n` tiver menos de 5 caracteres (não
deveria acontecer após o regex de 13 dígitos, mas a guarda é barata e deixa a lógica
robusta a mudanças futuras no regex).

## Escopo (o que fazer)
- [ ] Aplicar o patch acima em `forms.py`.
- [ ] Teste novo (`backend/src/apac_batch/tests.py`): `ImportFaixasForm` com uma faixa
      de 13 dígitos e 5º dígito `"9"` → `is_valid()` `False`, erro menciona o dígito
      esperado; mesma faixa com `"7"` (padrão real) → válida (dado o resto do input
      correto).
- [ ] Teste cobrindo que a faixa com dígito errado **não é inserida no banco** (não
      chama `salvar()`/`bulk_create` quando o form é inválido — já é o comportamento
      do fluxo existente, só confirmar que continua valendo com a nova validação).

## Fora de escopo
- Validar contra atributo complementar do procedimento via SIGTAP — precisa de fonte de
  dados nova, é tarefa maior, registrar separadamente se for priorizado.
- Qualquer alerta/validação no momento da aprovação (`ApprovedApacRequestUseCase`) — não
  é mais necessário: bloqueando na importação, uma faixa com dígito errado nunca chega
  a existir no banco para ser aprovada.
- Revalidar/corrigir faixas já cadastradas — não é necessário, já confirmado que usam o
  dígito correto ("7") na prática.

## Como testar
- Automatizado: `cd backend/src && python manage.py test apac_batch`.
- Manual: no Django Admin, "Importar Faixas APAC", colar uma faixa de 13 dígitos com 5º
  dígito diferente de "7" e confirmar que o formulário rejeita com a mensagem de erro,
  sem inserir nada no banco.

## Critério de aceite
- [ ] Importação de faixa com 5º dígito diferente de "7" é rejeitada pelo formulário,
      com mensagem clara.
- [ ] Faixas com 5º dígito "7" continuam sendo importadas normalmente.
- [ ] Gates: `bash scripts/verify.sh` verde.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
