# Sistema APAC — Visão do Projeto

## O que é

O **Sistema APAC** é uma aplicação web desenvolvida para auxiliar municípios do estado do Rio de Janeiro na digitação e gestão de solicitações de **Autorização de Procedimentos de Alta Complexidade (APAC)** do SUS.

O sistema resolve um problema concreto de operação: os municípios precisavam digitar cada solicitação individualmente no **APAC Magnético** — um sistema legado de terminal de texto — processo que é lento, propenso a erros e exige que o operador conheça todos os campos e códigos de memória.

## Problema que resolve

O APAC Magnético é o sistema oficial do Ministério da Saúde para registro de APACs, mas sua interface de terminal impõe uma série de dificuldades:

- Interface não-intuitiva sem validação em tempo real
- Necessidade de digitação manual de todos os dados do paciente
- Sem banco de dados de procedimentos e CIDs integrado
- Sem verificação de duplicidade
- Sem rastreabilidade do fluxo de aprovação

O sistema APAC substitui essa digitação manual por um formulário web guiado, com integrações externas e validações de negócio, e ao final gera o arquivo no formato esperado pelo APAC Magnético para importação.

## Fluxo principal

O sistema opera com três perfis de usuário e três etapas sequenciais:

**1. Solicitação** — realizada pelo perfil *Solicitante*

O operador abre o formulário de nova APAC e informa o CPF ou CNS do paciente. O sistema consulta o **CADSUS** (Cadastro Nacional de Usuários do SUS) e preenche automaticamente os dados pessoais do paciente (nome, filiação, endereço, data de nascimento, raça/cor, gênero). Em seguida, o operador seleciona o CID principal, o procedimento principal e os subprocedimentos vinculados, informa o médico responsável, o médico autorizador e as datas de procedimento, alta e diagnóstico. Ao finalizar, a solicitação é criada com status **Pendente**.

**2. Autorização** — realizada pelo perfil *Autorizador*

O autorizador visualiza as solicitações pendentes da sua competência e município. Pode aprovar ou rejeitar. Ao aprovar, o sistema automaticamente associa um **número de faixa APAC** (lote pré-cadastrado) disponível para aquela cidade e competência. Ao rejeitar, é obrigatório informar uma justificativa.

**3. Extração** — realizada pelo perfil *Autorizador* ou *Administrador*

Com as APACs aprovadas, o operador acessa a tela de extração, seleciona o estabelecimento, mês e ano de competência, e o sistema gera o arquivo no formato fixo do APAC Magnético, pronto para importação.

## Módulos do sistema

### Backend (Django + Python)

| App Django        | Responsabilidade                                              |
|-------------------|---------------------------------------------------------------|
| `apac_request`    | Gestão do ciclo de vida da solicitação (criação, aprovação, rejeição) |
| `apac_data`       | Dados clínicos e do paciente vinculados a uma solicitação     |
| `apac_batch`      | Controle das faixas numéricas (lotes) de APAC por cidade      |
| `procedure`       | Cadastro de procedimentos (OCI) e CIDs                        |
| `procedure_record`| Subprocedimentos vinculados a um dado de APAC                 |
| `establishment`   | Estabelecimentos de saúde por cidade                          |
| `city`            | Municípios atendidos pelo sistema                             |
| `customuser`      | Usuários com papéis: Admin, Solicitante, Autorizador, Visitante |
| `authjwt`         | Autenticação via JWT                                          |
| `apac_core`       | Pacote Python isolado com domínio, entidades, value objects, use cases e serviços |

### Frontend (Next.js + React)

| Rota          | Função                                         |
|---------------|------------------------------------------------|
| `/solicitar`  | Formulário de nova solicitação APAC            |
| `/responder`  | Painel de autorização/rejeição de APACs        |
| `/visualizar` | Visualização de APACs registradas              |
| `/extracao`   | Exportação do arquivo para o APAC Magnético    |

## Integrações externas

- **CADSUS**: API interna de rede local (`192.168.1.10:8014`) que consulta o Cadastro Nacional de Usuários do SUS pelo CPF ou CNS do paciente e retorna dados pessoais pré-preenchíveis no formulário.

## Stack tecnológica

| Camada      | Tecnologia                                              |
|-------------|--------------------------------------------------------|
| Backend     | Python 3, Django 5.2, Django REST Framework, Pydantic  |
| Frontend    | Next.js 15, React 19, MUI 7, react-hook-form, NextAuth |
| Banco       | MySQL (produção), SQLite (desenvolvimento)              |
| Auth        | JWT (SimpleJWT no backend, next-auth no frontend)       |
| Infra       | Docker, docker-compose, Gunicorn, Whitenoise            |
| Testes      | pytest + Django TestCase (backend), Jest (frontend)     |

## Contexto de negócio

O sistema foi desenvolvido para atender municípios do estado do Rio de Janeiro que precisam entregar arquivos APAC mensalmente para a Secretaria Estadual de Saúde. Cada município possui um conjunto de **faixas numéricas** (lotes) pré-autorizados, e cada APAC aprovada consome uma dessas faixas. O controle e a validade das faixas são gerenciados pelo próprio sistema.

O arquivo gerado na exportação segue o layout fixo da **Versão 03.15 do APAC Magnético**, com campos de tamanho fixo posicionais, e é diretamente importável no sistema legado do Ministério da Saúde.
