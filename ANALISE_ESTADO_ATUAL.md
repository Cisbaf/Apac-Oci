# Análise do Estado Atual — Sistema APAC

> Documento de diagnóstico arquitetural. Objetivo: registrar honestamente o estado do código hoje, identificar débitos técnicos e servir de base para decisões de refatoração futura.

---

## O que foi bem executado

Antes do diagnóstico dos problemas, é importante reconhecer as decisões certas que foram tomadas:

**Separação do `apac_core`**: A decisão de isolar o domínio em um pacote Python separado (`backend/core`) foi correta e é o maior ativo arquitetural do projeto. Entidades Pydantic, repositórios abstratos, value objects e use cases estão desacoplados do Django. Isso permite testar a lógica de negócio sem banco de dados.

**Value Objects implementados**: `CnsField`, `CpfField`, `CepField`, `CboField` existem como tipos próprios no domínio. É o padrão correto e encapsula validação.

**Use Cases com injeção de dependência**: Os use cases recebem repositórios abstratos via construtor. O `CreateApacRequestUseCase` é um exemplo funcional e bem estruturado, com validações de negócio claras.

**Testes de integração em `apac_request`**: O arquivo `apac_request/tests.py` tem uma suíte de testes de integração bem organizada, com classe base, helpers e cobertura dos fluxos principais (criação, aprovação, rejeição, edge cases).

**Frontend bem organizado no módulo `solicitar`**: A pasta `solicitar/apacRequest` segue uma estrutura clara com separação de `components`, `contexts`, `schemas`, `services`, `utils` e `hooks`.

---

## Problemas arquiteturais

### 1. Nomenclatura inconsistente: "Controller" usado como "Repository"

**Impacto: Alto**

As classes em `apac_request/controller.py`, `apac_data/controller.py`, `apac_batch/controller.py` etc. são implementações de repositórios Django — elas estendem as classes abstratas do `apac_core.domain.repositories`. Não são controllers no sentido de MVC nem de DDD.

O nome correto seria `ApacRequestRepository` (implementação), não `ApacRequestController`. Essa nomenclatura confunde qualquer desenvolvedor que entre no projeto, pois "controller" sugere que é onde fica a lógica de requisição HTTP (que está nas `views.py`).

```python
# Hoje (nome errado)
class ApacRequestController(ApacRequestRepository): ...

# Correto
class ApacRequestDjangoRepository(ApacRequestRepository): ...
```

### 2. `apac_data` não tem views nem URLs

**Impacto: Médio**

O app `apac_data` tem `views.py` vazio e nenhum `urls.py`. Os dados de APAC são criados indiretamente através do use case chamado pela view de `apac_request`. Isso faz com que o app `apac_data` seja um módulo com model e controller (repositório), mas sem endpoint próprio — a fronteira do módulo é opaca.

### 3. `procedure_record` não tem URLs

**Impacto: Médio**

Similar ao caso acima: o app `procedure_record` tem model, controller e view, mas não possui `urls.py`. O frontend nunca acessa subprocedimentos diretamente — eles são passados como parte do payload de criação da APAC.

### 4. Arquivos operacionais/temporários dentro do `src`

**Impacto: Médio (organização)**

Há vários arquivos que não deveriam estar no repositório dentro de `backend/src/`:

- `db.sqlite3` — banco de dados de desenvolvimento (deveria estar no `.gitignore`)
- `data.json` — fixture de dados sem documentação de propósito
- `faixas_novas.txt`, `faixas_removidas.txt`, `faixas_novas_bel.txt`, `faixas_removidas_mage.txt`, `fev_to_mar.txt` — arquivos de operações avulsas
- `execute_tools.py` — script avulso sem contexto claro
- `logs/` — diretório de logs que deveria estar no `.gitignore`

A pasta `tools/` tem scripts de limpeza e deduplicação (`clean_batchs.py`, `duplicados.py`) que foram criados para resolver problemas pontuais e permanecem sem documentação ou testes.

### 5. Cobertura de testes extremamente desigual

**Impacto: Alto**

A cobertura de testes está concentrada em um único lugar:

| Local | Estado |
|---|---|
| `apac_request/tests.py` | Bem coberto — fluxo principal, aprovação, rejeição, edge cases |
| `apac_core/tests/` | 3 arquivos de teste para use cases |
| `apac_data/tests.py` | Vazio |
| `apac_batch/tests.py` | Vazio |
| `city/tests.py` | Vazio |
| `establishment/tests.py` | Vazio |
| `procedure/tests.py` | Vazio |
| `procedure_record/tests.py` | Vazio |
| `customuser/tests.py` | Vazio |
| `authjwt/tests.py` | Vazio |
| Frontend (`__tests__/`) | 1 arquivo, provavelmente mínimo |

Módulos críticos como o serviço de exportação do arquivo APAC (`apac_core/domain/services/apac_extract/`) não têm testes de unidade documentados aqui.

---

## Bugs e inconsistências no código

### 6. Bug: `formatCns` com regex inválida no frontend

**Impacto: Alto (funcional)**

Em `PatientInfoService.ts`, a função `formatCns` tem um bug:

```typescript
// Errado — a string '/\D/g' não é uma regex, é texto literal
const digits = cns.replace('/\D/g', '');

// Correto
const digits = cns.replace(/\D/g, '');
```

Isso faz com que CNS com espaços ou traços não seja limpo corretamente antes de verificar o tamanho.

### 7. Bug potencial: `patient_race_color` com valores inconsistentes

**Impacto: Médio**

O model `ApacDataModel` define os choices de raça/cor como `("01", "Branca")`, `("02", "Preta")` etc. (códigos numéricos). No entanto, os dados de teste em `tests.py` usam `"parda"` (texto) para o campo `patient_race_color`. Isso indica que em algum ponto do fluxo o campo pode estar recebendo valores em formato diferente do esperado pelo banco.

### 8. `updated_at` com `auto_now_add` em vez de `auto_now`

**Impacto: Baixo-Médio**

Em `ApacRequestModel`:

```python
updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de atualização")
```

`auto_now_add=True` define o valor apenas na criação. Para um campo chamado "Data de atualização", o correto seria `auto_now=True`, que atualiza a cada `save()`.

### 9. `cns_paciente` hardcoded como zeros na exportação

**Impacto: Médio**

Em `apac_core/domain/services/apac_extract/controller.py`, o CNS do paciente no arquivo de saída é fixado em `"000000000000000"`:

```python
cns_paciente="000000000000000",
```

Apesar do CNS do paciente existir no banco (`apac_data.patient_data.cns`), ele não é usado no arquivo exportado. Isso pode ser intencional por uma regra do layout, mas não está documentado.

### 10. UF hardcoded para Rio de Janeiro

**Impacto: Médio (escalabilidade)**

No export controller:

```python
cod_uf="33",  # código do RJ
```

O código de UF está fixo. Se o sistema for usado em outros estados, isso precisará ser parametrizado.

### 11. `adaptar_oci` — gambiarra documentada

**Impacto: Médio (manutenibilidade)**

No export controller existe:

```python
apac_model=adaptar_oci(  # essa nova linha está adaptando o apac model para o caso de duque de caxias
    apac_model=ApacModel(...)
)
```

Uma adaptação específica para Duque de Caxias foi adicionada diretamente no fluxo geral de exportação. Não se sabe o que `adaptar_oci` faz sem abrir o arquivo, e não está claro se isso afeta outros municípios. É o tipo de código que tende a crescer com mais `if municipio == X` ao longo do tempo.

### 12. `ExportApacBatch` sem autenticação

**Impacto: Alto (segurança)**

A view de exportação não tem `authentication_classes` nem `permission_classes`:

```python
class ExportApacBatch(APIView):
    # sem authentication_classes
    # sem permission_classes
    def post(self, request): ...
```

Qualquer um com acesso à URL pode gerar arquivos de exportação contendo dados sensíveis de pacientes.

### 13. `getCityNameByCode` não implementada

**Impacto: Baixo (funcionalidade incompleta)**

Em `PatientInfoService.ts`:

```typescript
function getCityNameByCode(cityCode?: string | null): string {
  // Implementação real precisaria de um dicionário ou API de consulta
  return cityCode ? 'Nome da Cidade' : '';
}
```

A função está comentada no uso mas existe no código. O campo de cidade do endereço do paciente retornado pelo CADSUS (código IBGE) não está sendo convertido para nome de cidade.

### 14. Busca de faixa por substring do número do lote

**Impacto: Médio (fragilidade)**

Em `ApacBatchController.search_for_available_batch`:

```python
.annotate(year_part=Substr('batch_number', 3, 2))  # começa em 1, então 3 = 3º caractere
.filter(..., year_part=year_str)
```

A lógica de encontrar um lote disponível para o ano correto depende de extrair 2 dígitos de uma posição fixa do número do lote. Se o formato do número de lote mudar, a busca quebra silenciosamente (retorna 0 resultados em vez de erro).

---

## Débitos técnicos no frontend

### 15. Estrutura inconsistente entre rotas

A rota `/solicitar` tem estrutura sofisticada com contexts, hooks, schemas, services e utils. Já `/responder` tem apenas `context/authorizationContext.tsx` e `page.tsx`. A mesma disciplina não foi aplicada a todas as rotas.

### 16. `dataFakes.ts` e `establishmentFakeList.ts` em produção

Existem arquivos de dados falsos (`utils/dataFakes.ts`, `utils/procedureFakeList.ts`, `utils/establishmentFakeList.ts`) que provavelmente foram usados durante o desenvolvimento. Não está claro se ainda são usados em produção ou podem ser removidos.

### 17. API CADSUS com IP local no `.env`

```
API_CADSUS=http://192.168.1.10:8014/consult
```

O endereço é um IP de rede local. Isso significa que o sistema só funciona quando conectado à rede interna do município. Não há fallback nem mensagem de erro amigável se o CADSUS estiver indisponível.

---

## Resumo dos débitos por prioridade

| Prioridade | Item |
|---|---|
| 🔴 Crítico | Autenticação ausente em `ExportApacBatch` |
| 🔴 Crítico | Bug na `formatCns` (regex inválida) |
| 🟠 Alto | Nomenclatura "Controller" para repositórios — confunde toda a base de código |
| 🟠 Alto | Cobertura de testes em `apac_data`, `apac_batch`, `procedure`, export service |
| 🟠 Alto | `patient_race_color` com valores inconsistentes entre model e testes |
| 🟡 Médio | `adaptar_oci` acoplado ao fluxo geral sem documentação |
| 🟡 Médio | `cod_uf` e `cns_paciente` hardcoded no export |
| 🟡 Médio | Busca de faixa por substring frágil |
| 🟡 Médio | `updated_at` com `auto_now_add` em vez de `auto_now` |
| 🟢 Baixo | Arquivos temporários e operacionais no `src` |
| 🟢 Baixo | `getCityNameByCode` não implementada |
| 🟢 Baixo | Dados fake possivelmente não removidos |

---

## Direção recomendada

A arquitetura central do `apac_core` está no caminho certo. O esforço deve ser de **consolidação**, não reescrita:

1. Renomear as classes "Controller" para "Repository" + adicionar testes nos módulos sem cobertura.
2. Corrigir os dois bugs críticos (autenticação no export, regex no formatCns).
3. Documentar e isolar o `adaptar_oci` como uma regra de negócio específica por município, não como um hack inline.
4. Mover arquivos temporários para fora do `src` e adicionar ao `.gitignore`.
5. Parametrizar os valores hardcoded (`cod_uf`, `cns_paciente`) para preparar o sistema para novos municípios/estados.
