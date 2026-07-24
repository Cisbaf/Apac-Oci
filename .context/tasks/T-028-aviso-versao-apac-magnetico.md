# T-028 — Aviso na tela de exportação sobre versão do APAC Magnético

- **Fase:** 0
- **Status:** todo
- **Depende de:** —
- **Branch:** `refactor/T-028-aviso-versao-apac-magnetico`

## Objetivo
Exibir um aviso informativo na página `/extracao` (React) explicando que o arquivo
gerado agora inclui campos exigidos pelas versões mais recentes do APAC Magnético
(v03.17 e v04.00), e que o usuário precisa confirmar que o APAC Magnético instalado
localmente está atualizado antes de importar.

## Contexto / porquê
Nasceu de uma dúvida do usuário ao validar manualmente a T-023/T-024: os campos novos
do export (`fonte_orcamentaria`/`emendas_parlamentares`, da v03.17; `pessoa_sem_cpf`,
da v04.00) só são compreendidos corretamente por um APAC Magnético já atualizado.
Isso é uma exigência do próprio DATASUS, amarrada à competência — não depende do
nosso sistema — mas quem opera a exportação no dia a dia pode não saber disso. Um
aviso na tela evita que alguém rode uma importação com um APAC Magnético desatualizado
sem entender por que falhou ou por que os campos vêm em branco. Ver
`ANALISE_VERSAO_PROGRAMA_SIA_APAC.md` (raiz do repo, seção 4) para o levantamento
completo das versões/competências.

## Escopo (o que fazer)
- Componente novo `frontend/src/app/extracao/components/ExportVersionNotice.tsx`:
  `Alert` do MUI (severity `warning`, dispensável via `onClose`), explicando:
  - Desde a competência 07/2026 o arquivo inclui os campos da v04.00 ("Pessoa sem
    CPF/Registro Civil") e da v03.17 ("Fonte Orçamentária"/"Recurso de Emendas
    Parlamentares").
  - O APAC Magnético instalado localmente precisa estar atualizado para a versão mais
    recente para importar o arquivo corretamente.
  - Link para `sia.datasus.gov.br` (fonte oficial de atualização, já citada em
    `ANALISE_VERSAO_PROGRAMA_SIA_APAC.md`).
- Inserir `<ExportVersionNotice />` no topo de `frontend/src/app/extracao/page.tsx`.

## Fora de escopo
- Qualquer lógica de detectar automaticamente a versão do APAC Magnético do usuário
  (não há como o frontend saber isso) — é só um aviso textual.
- Mudar o campo `versao_layout` do header do export (rótulo interno do arquivo,
  registrado como decisão em aberto na T-023).

## Arquivos prováveis
- `frontend/src/app/extracao/components/ExportVersionNotice.tsx` — novo
- `frontend/src/app/extracao/page.tsx` — inclui o componente

## Critério de aceite
- [ ] Aviso visível ao entrar em `/extracao`, com o texto explicando os campos novos e
      a necessidade de atualizar o APAC Magnético local.
- [ ] Dispensável (fecha com o `x`, não bloqueia o uso da tela).
- [ ] Gates: `bash scripts/verify.sh` verde (frontend jest + lint, sem impacto em
      backend).

## Verificação
- Comportamento antes = depois? Não se aplica no sentido de regra de negócio — é só
  UI informativa, não muda nenhum caminho de dado ou export. Golden file inalterado
  (não toca backend).
- Gates: `bash scripts/verify.sh` verde.
- Verificação manual: abrir `/extracao` no navegador e conferir o aviso.

## Ao concluir
- Atualizar status em `INDEX.md` e no log de conclusão.
