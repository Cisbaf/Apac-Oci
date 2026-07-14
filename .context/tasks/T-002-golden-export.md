# T-002 — Golden file / teste de caracterização do export

- **Fase:** 0
- **Status:** todo
- **Depende de:** T-001
- **Branch:** `refactor/T-002-golden-export`
- **Prioridade:** máxima — é a rede de segurança de tudo.

## Objetivo
Congelar o comportamento atual do serviço de exportação: dado um conjunto fixo de APACs de exemplo, gerar o arquivo posicional e salvá-lo como referência ("golden file"). Um teste compara a saída atual com o golden **byte a byte**.

## Contexto / porquê
O arquivo exportado é o produto mais crítico (bate no SIA; erro = glosa). Nenhuma refatoração pode alterá-lo sem intenção. Sem esse teste, qualquer mexida no export é risco cego. Ver `../glossary.md` (glosa) e análise complementar seção 4/Fase 0.

## Escopo
- Montar um cenário determinístico (fixtures) cobrindo: 1 APAC simples, 1 com subprocedimentos, e o caso `adaptar_oci` (Duque de Caxias), para o golden capturar também a regra específica antes de ela ser refatorada em T-202.
- Gerar o arquivo com o código atual (`ExportApacBatchController` / `ApacExportCase`) e salvá-lo em `backend/core/tests/.../export/golden/`.
- Escrever teste que reexecuta e compara com o golden (falha se diferente). Datas dinâmicas (`date.today()` no header) precisam ser fixadas/mockadas para o teste ser estável.
- Incluir esse teste no `scripts/verify.sh` (já roda via pytest do core).

## Fora de escopo
- Corrigir os débitos do export (`cns_paciente` zerado, `cod_uf` fixo). O golden fixa o comportamento **como está hoje**, inclusive com os defeitos. Correções vêm depois, como tarefas explícitas que atualizam o golden de propósito.

## Arquivos prováveis
- `backend/core/tests/domain/services/export/test_golden_export.py` (novo)
- `backend/core/tests/.../export/golden/*.txt` (novos, arquivos de referência)
- `backend/core/tests/.../export/fixtures.py` (novo, cenários determinísticos)

## Critério de aceite
- [ ] Teste gera a saída e compara com o golden, passando no estado atual.
- [ ] Datas mockadas; teste é determinístico (roda 2x = mesmo resultado).
- [ ] Cobre APAC simples, com subprocedimentos e caso `adaptar_oci`.

## Verificação
- `bash scripts/verify.sh` verde. Rodar 2x para confirmar determinismo.

## Ao concluir
- A partir daqui, **qualquer mudança no golden exige tarefa explícita**. Anotar isso no PR.
