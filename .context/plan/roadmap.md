# Roadmap por fases

Baseado em `../../ANALISE_COMPLEMENTAR_E_PLANO_REFATORACAO.md` (seção 4). Cada fase entrega valor sozinha e tem um **critério de saída**. As tarefas concretas estão em `../tasks/INDEX.md`.

## Fase 0 — Blindar o que está em produção
**Objetivo:** poder refatorar sem medo. Rede de segurança + fechar buracos críticos.
**Tarefas:** T-001 (infra de gates), T-002 (golden file do export), T-003 (auth no export), T-004 (bug formatCns), T-005 (limpeza do repo), T-006 (alinhar action de status do admin ao use case).
**Critério de saída:** `scripts/verify.sh` roda e passa; golden file protege o export; nenhum caminho de escrita diverge do use case; bugs críticos corrigidos.

## Fase 1 — Fronteiras e regra transversal centralizada
**Objetivo:** clareza estrutural e uma fonte única para a regra de visibilidade.
**Tarefas:** T-101 (renomear Controller→Repository no backend), T-102 (renomear controllers→services no frontend), T-103 (AccessScopePolicy única, aplicada nos 5 lugares).
**Critério de saída:** nenhuma classe chamada "Controller" que seja repositório; regra de visibilidade em um só lugar; testes verdes.

## Fase 2 — Um caminho por operação de negócio
**Objetivo:** toda transição de estado passa por use case; regras por município isoladas.
**Tarefas:** T-201 (transições de estado via use case, admin incluso), T-202 (`MunicipalityExportProfile` — tirar hardcodes `adaptar_oci`/`cod_uf`/etc. do fluxo geral).
**Critério de saída:** admin e React usam os mesmos use cases; export parametrizado por município sem `if municipio == X`; golden file ainda verde.

## Fase 3 — Strangler no frontend (admin → React)
**Objetivo:** consolidar a operação em um só sistema (React), aposentando ferramentas do admin.
**Tarefas:** T-301 (namespace API v2 + infra de feature flag), T-302 (gestão de status em React), T-303 (gestão de faixas em React), T-304 (dashboard em React).
**Critério de saída:** cada ferramenta migrada roda em React atrás de flag, com o admin como fallback; dados idênticos (mesmos models).

## Fase 4 — Remoção do legado
**Objetivo:** remover caminhos antigos e código morto após validação em produção.
**Tarefas:** T-401 (remover views/actions legadas e código morto: `dataFakes.ts`, `getCityNameByCode`, etc.).
**Critério de saída:** um caminho só por operação; sem código morto; contexto (`.context/`) atualizado.

## Futuro (pós-refatoração) — Módulo de Exportação como diagnóstico SIA/APAC
Ver seção 5 da análise complementar. Três blocos: validação pré-exportação (erros clássicos do SIA), parser de retorno de crítica (erro→explicação→link para a APAC), perfis por município. Reconciliação futura com TabNet/DATASUS. Estas serão desdobradas em tarefas T-5xx quando a base estiver consolidada.

## Como as fases se relacionam com o risco

```
risco ▲
      │ ██ (mexer no export sem rede)
      │ ██
      │ ██──┐ Fase 0 derruba o risco cedo
      │     └──▄▄  Fases 1-2 (estrutura, sem mudar comportamento)
      │           ▄▄▄  Fase 3 (troca de superfície, com flag)
      │                ▁  Fase 4 (remoção, já validado)
      └───────────────────────────────────────▶ tempo
```
