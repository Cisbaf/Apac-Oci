# T-035 — Ferramenta de cadastro a partir do SIGTAP + correção do cadastro das 10 OCIs novas

- **Fase:** 0
- **Status:** doing
- **Depende de:** —
- **Branch:** `refactor/T-035-ferramenta-sigtap`

## Objetivo
Substituir a transcrição manual de portaria por extração das tabelas oficiais do
SIGTAP, e corrigir com ela o cadastro das 10 OCIs novas (T-026 e T-027).

## Contexto / porquê
T-026 e T-027 descreviam o cadastro como transcrição manual do Anexo da portaria
para o Django Admin. O teste de 02/09/2026 no APAC Magnético
(`criticas-202608-20260902-164632.csv`) mostrou o custo disso: das 10 OCIs
cadastradas à mão, 171 divergências contra o SIGTAP.

O achado que destrava tudo: o `apac-magnetico-validador` já monta, por
competência, as tabelas DBF do SIGTAP em `ambientes/<competencia>/`. São as
mesmas tabelas que o APAC Magnético consulta para criticar. Não é preciso
transcrever portaria — dá para ler a fonte.

## Escopo (o que fazer)
- `scripts/sigtap/` — leitor DBF sem dependências + extrator CLI que produz o
  cadastro oficial (principal, secundários com papel e quantidade, CIDs, CBOs,
  atributos) em JSON ou relatório legível.
- Management command `sigtap_auditar` — compara o cadastro do sistema com o JSON
  e, com `--aplicar`, corrige.
- Rodar a correção nas 10 OCIs novas.
- Preservar os CIDs de causas associadas em `scripts/sigtap/cids_causas_associadas.json`
  antes de desvinculá-los (viram entrada da T-036).

## Fora de escopo
- Campo de CID de causas associadas — **T-036**.
- Papel/quantidade máxima por par principal×secundário — **T-037**.
- Qualquer mudança no arquivo exportado.

## Arquivos prováveis
- `scripts/sigtap/{dbf.py,extrair.py,README.md,cids_causas_associadas.json}` — novos
- `backend/src/procedure/management/commands/sigtap_auditar.py` — novo

## Critério de aceite
- [x] `extrair.py` reproduz o cadastro oficial das 10 OCIs a partir de `202608a`
- [x] `sigtap_auditar` sem `--aplicar` não escreve nada (transação com rollback)
- [x] Após `--aplicar`, nova auditoria acusa zero divergências
- [x] Nenhum procedimento ou CID é apagado — só desvinculado
- [x] Golden file do export inalterado

## Verificação
- Comportamento antes = depois? Sim no código de export (nada tocado ali).
  O cadastro muda de propósito — é o objetivo da tarefa.
- Gates: `bash scripts/verify.sh` verde.
- Auditoria idempotente: 171 divergências → 0 → 0.

## Reteste no APAC Magnetico (03/09/2026, tabela 202608a)

Arquivo de teste regerado a partir do extrato do SIGTAP (CID principal aceito,
todos os secundarios obrigatorios, CBO valido por procedimento) e submetido ao
programa oficial.

| Critica | Antes (02/09) | Depois (03/09) |
|---|---|---|
| `PROC.(...) INCOMPATIVEL COM CID (...)` | 8 | **0** |
| `PMAE EXIGE PELO MENOS 2 PROC.SEC.` | 8 | **0** |
| `EXIGE PELO MENOS (00N) PROC. SECUNDARIO OBRIGATORIO` | 2 | **0** |
| `EXIGE AO MENOS 1 PROC.SEC. (... OU ...)` | 2 | **0** |
| `PROC.(...) CBO (...) INCOMPATIVEIS` | 5 | **0** |
| `EXIGE CID CAUSAS ASSOC.` (T-036) | 8 | 8 |
| `DIGITO VERIFICADOR INVALIDO` (numero fabricado) | 9 | 9 |
| `CNS INVALIDO` (dado de teste) | 17 | 6 |
| **Total** | **58** | **23** |

Toda critica de **conteudo de cadastro** zerou. O que sobra nao e cadastro:

- As 2 OCIs de **Saude Bucal** (`0907010016`, `0907010024`) ficaram **sem nenhuma
  critica de conteudo** — so o digito verificador do numero fabricado. Estao
  prontas para o municipio preencher e faturar.
- As 8 OCIs de **Infectologia** ficaram so com `EXIGE CID CAUSAS ASSOC`, que e
  exatamente a **T-036**. Confirma que aquele erro nao era dado de teste: e
  lacuna de sistema, e e o unico bloqueio restante.
- `DIGITO VERIFICADOR` e os 6 `CNS` restantes sao do gerador de teste (numeros
  fabricados e o campo `cns_medico_executante`, que o gerador nao trocou), nao do
  cadastro.

## Ao concluir
- Marcar T-026 e T-027 como cobertas por esta ferramenta.
