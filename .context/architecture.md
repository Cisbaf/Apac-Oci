# Arquitetura-alvo

## Princípio central: um banco, duas superfícies

A refatoração **não** cria um segundo banco nem um segundo conjunto de dados. Existe **uma única persistência** (os models Django atuais). As "duas versões" (legada e nova) são apenas **duas superfícies — API/telas — sobre os mesmos models**. Assim os dados são idênticos por construção e não há nada para sincronizar.

O que migra da versão antiga para a nova não é o dado, é **onde a regra roda**: a versão nova executa toda regra na camada de aplicação (use cases); a antiga (admin + views atuais) segue funcionando até ser substituída, rota a rota (*Strangler Fig*).

## As 4 camadas

```
┌──────────────────────────────────────────────────────────────┐
│ INTERFACE     views/serializers (API), React, Django Admin    │  HTTP, JSON, sessão, telas
│               → só traduz entrada/saída. NÃO contém regra.     │
├──────────────────────────────────────────────────────────────┤
│ APPLICATION   use_cases, policies                             │  ORQUESTRA a regra. Caminho ÚNICO
│               → único lugar que muda estado de negócio.       │  para cada operação.
├──────────────────────────────────────────────────────────────┤
│ DOMAIN        entities, value objects, domain services        │  REGRA pura. Zero Django.
│  (apac_core)  → testável sem banco.                           │  Já existe e está no caminho certo.
├──────────────────────────────────────────────────────────────┤
│ INFRASTRUCTURE  repositories Django (hoje chamados            │  ORM. Único ponto que fala com o banco.
│                 "controller.py"), integrações (CADSUS)        │
└──────────────────────────────────────────────────────────────┘
```

**Direção de dependência:** de cima para baixo. Interface depende de Application; Application depende de Domain e de interfaces de repositório; Infrastructure implementa essas interfaces. Domain não depende de ninguém.

## Regra de ouro

> **Nenhuma tela — nem React, nem Django Admin — muda estado de negócio sem passar pela camada Application (use case).**

O Admin passa a ser leitura/consulta. Quando precisar agir (aprovar, mudar status, mexer em faixa), chama **o mesmo use case** que o React chama. Isso elimina a divergência descrita em `../ANALISE_COMPLEMENTAR_E_PLANO_REFATORACAO.md` (seção 2, Causa raiz A).

## Regras transversais têm um dono único

Políticas que hoje estão copiadas em vários lugares passam a ter uma implementação só:

- **Visibilidade/escopo por usuário** ("vê só a sua cidade, exceto `restricted_user`; superuser vê tudo"): uma única `AccessScopePolicy` / método `for_user(user)` no repositório, consumida por todos (admin, views, batch). Hoje está duplicada em 5 lugares.
- **Regras específicas por município** (`adaptar_oci`, `cod_uf`, códigos fixos do export): isoladas em um perfil de exportação por município (`MunicipalityExportProfile`), fora do fluxo geral.

## Estado da migração das superfícies (Strangler)

| Ferramenta | Hoje | Alvo |
|---|---|---|
| Solicitar APAC | React `/solicitar` → use case ✅ | mantém |
| Aprovar/Rejeitar | React `/responder` → use case ✅ (único caminho). Admin: `status`/`authorizer`/`review_date` são sempre readonly (mesmo para superuser) — T-006 fechou a edição direta que pulava o use case e não associava faixa. | Admin ganhar action própria que chame o mesmo use case, se necessário no futuro |
| Gestão de faixas | Admin inline | React (API v2) |
| Mudança de status em lote | Não existe hoje (a action antiga era código morto — nunca registrada em `actions`, template inexistente; removida na T-006) | React (use case), se vier a ser necessário |
| Dashboard | Django template | React (API) |
| Exportação | React `/extracao` → use case | mantém + evolui (validação/diagnóstico) |

Legenda: ✅ correto · ❌ caminho que viola a regra de ouro.

## Namespace de convivência

Enquanto legado e novo coexistem, a API nova vive sob `/api/v2/` (ou flag por rota). O frontend aponta para v2 rota a rota, com **feature flag**, mantendo o caminho antigo como fallback até validar em produção.
