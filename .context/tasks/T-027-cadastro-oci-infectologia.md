# T-027 — Cadastrar novas OCIs de Infectologia (investigação diagnóstica HIV/aids)

- **Fase:** 0 · **Status:** todo · **Depende de:** —
- **Branch:** não se aplica diretamente (cadastro via Django Admin) — se algum ajuste de
  código for necessário durante a execução, `refactor/T-027-cadastro-oci-infectologia`

> Detalhado a partir de `ANALISE_PORTARIA_4306_2026_OCI_INFECTOLOGIA.md` (raiz do
> repo). Mesma natureza de T-026: **tarefa de cadastro de dados**, não de código — não
> mexe no formato do arquivo exportado.

## Objetivo
Cadastrar em `ProcedureModel`/`CidModel` (Django Admin) os 8 novos procedimentos
principais de OCI de Infectologia (Portaria SAES/MS Nº 4.306/2026), seus CIDs e seus
procedimentos secundários obrigatórios/compatíveis, para que o sistema permita abrir
uma APAC desse tipo.

## Pré-requisito antes de executar
- [ ] Confirmar que o(s) município(s) atendidos pelo sistema vão oferecer essa OCI
      (investigação diagnóstica de pessoas vivendo com HIV/aids em situação de
      imunossupressão). Se não, deixar em espera.

## Contexto / porquê
A Portaria (vigente na competência 07/2026) cria, no Grupo 09 - OCI, o Subgrupo 08 -
Atenção em Infectologia, com 8 procedimentos principais (4 síndromes clínicas × 2
estágios: avaliação inicial e progressão). Assim como em T-026, o sistema não
sincroniza com o SIGTAP automaticamente — sem esse cadastro, o operador não consegue
selecionar esses procedimentos na tela de digitação.

## Escopo (o que fazer)

### 1. Cadastrar os 8 procedimentos principais
| Código | Nome | Valor |
|---|---|---|
| `09.08.01.001-0` | OCI - Avaliação Diagnóstica Inicial de Síndrome Respiratória | R$ 574,72 |
| `09.08.01.002-8` | OCI - Progressão da Avaliação Diagnóstica de Síndrome Respiratória | R$ 387,87 |
| `09.08.01.003-6` | OCI - Avaliação Diagnóstica Inicial de Síndrome Neurológica | R$ 566,84 |
| `09.08.01.004-4` | OCI - Progressão da Avaliação Diagnóstica de Síndrome Neurológica | R$ 1.500,00 |
| `09.08.01.005-2` | OCI - Avaliação Diagnóstica Inicial de Síndrome Mucocutânea | R$ 283,34 |
| `09.08.01.006-0` | OCI - Progressão da Avaliação Diagnóstica de Síndrome Mucocutânea | R$ 1.479,38 |
| `09.08.01.007-9` | OCI - Avaliação Diagnóstica Inicial de Síndrome Consumptiva | R$ 827,36 |
| `09.08.01.008-7` | OCI - Progressão da Avaliação Diagnóstica de Síndrome Consumptiva | R$ 1.228,61 |

Todos: CBO 2251/2252/2253, quantidade máxima 1, FAEC/PMAE subtipo 040086.

### 2. CID principal (igual para os 8) e CID secundário (varia por síndrome)
CID principal: `B20`, `B21`, `B22`, `B23` (inclui B23.0/B23.1), `B24`, `Z21`.

CID secundário — cadastrar por síndrome conforme Anexo I da Portaria (listas longas,
específicas por procedimento: pneumonias/histoplasmose/criptococose para
Respiratória; toxoplasmose/criptococose cerebral/tuberculoma para Neurológica;
herpes/candidíase/sarcoma de Kaposi para Mucocutânea; caquexia/neoplasias para
Consumptiva). **Não transcrevi a lista completa aqui** — consultar a Portaria
diretamente (Anexo I) no momento do cadastro, são ~10-15 CIDs secundários por par de
procedimento.

**Atenção ao registrar a produção:** a Portaria (Art. 2º, §2º) exige registrar tanto o
CID principal quanto o CID secundário da condição relacionada ao HIV/aids — reforçar
isso na orientação de digitação, não é um campo novo, é uma exigência de preenchimento
correto do campo que já existe.

### 3. Cadastrar os procedimentos secundários (Anexo III = obrigatório, Anexo IV = compatível), como filhos de cada principal
Exames de imagem (tomografias, ressonâncias), laboratoriais (culturas para
micobactérias, testes moleculares, contagem de células no líquor, dosagens), consultas/
teleconsultas em atenção especializada, biópsias e punção lombar — cada par de OCI tem
sua própria lista com quantidade máxima por item (ver Anexo III e IV da Portaria,
página a página, um bloco por procedimento principal). Como são ~10 a 20 itens por
procedimento e a maioria se repete entre síndromes com pequenas variações de
quantidade, cadastrar consultando a Portaria diretamente item a item no momento da
execução, em vez de reproduzir aqui (risco de erro de transcrição numa lista tão
longa).

### 4. Conferir os ~15 procedimentos do Anexo II
Tomografias, baciloscopias, testes moleculares/culturas para micobactérias,
broncoscopia, biópsias etc. — ganham atributo 053/058 e viram compatíveis como
secundários. Muitos já devem existir no cadastro (são exames comuns); conferir se
faltam e se têm o atributo/instrumento de registro corretos.

## Fora de escopo
- Validar automaticamente os atributos 067/068/069/070 (ciclo assistencial por
  síndrome) ou as quantidades máximas dos Anexos III/IV — mesmo padrão já
  identificado, fica para o APAC Magnético/SIA.
- Qualquer mudança no export — esta Portaria não altera o layout do arquivo.

## Critério de aceite
- [ ] Pré-requisito respondido (município vai oferecer essa OCI?).
- [ ] Se sim: 8 procedimentos principais, CIDs e secundários obrigatórios/compatíveis
      cadastrados no Django Admin.
- [ ] Teste manual: operador consegue abrir uma APAC de teste com um dos 8 códigos como
      principal e selecionar os secundários esperados.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
