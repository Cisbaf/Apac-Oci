# Glossário de domínio

Termos que o agente precisa entender para não errar regra. Fontes na seção final de `../ANALISE_COMPLEMENTAR_E_PLANO_REFATORACAO.md`.

- **APAC** — Autorização de Procedimentos Ambulatoriais de Alta Complexidade. Instrumento do SUS para autorizar e registrar produção ambulatorial de alta complexidade/custo.
- **APAC Magnético** — Sistema legado (terminal) do Ministério da Saúde onde a APAC é digitada/importada. O sistema gera o arquivo posicional que ele consome. **Layout fixo v03.15.**
- **OCI** — Oferta de Cuidados Integrados. Pacotes de procedimentos do **Grupo 09** da Tabela SUS, dentro do **PMAE** (Programa Mais Acesso a Especialistas). Registrados via APAC no SIA, com um **procedimento principal** e **procedimentos secundários (subprocedimentos)**.
- **SIA / SIASUS** — Sistema de Informações Ambulatoriais do SUS. Recebe, consolida e **valida** a produção (APAC/BPA), e valida o pagamento antes de aprovar. É quem rejeita arquivos malformados.
- **Glosa** — Rejeição do pagamento de uma produção pelo SIA/gestor. O maior risco de negócio: arquivo errado = município não é pago. Por isso o export é o ativo mais crítico.
- **Faixa (batch / `ApacBatchModel`)** — Intervalo/numeração de APAC pré-autorizada por cidade e competência. Cada APAC aprovada **consome uma faixa**. Controlada pelo próprio sistema (`apac_batch`).
- **Competência** — Mês/ano de referência da produção (ex.: "2025-06"). Filtro e agrupador onipresente. Erro clássico de importação no SIA: mais de uma competência no mesmo arquivo.
- **CADSUS** — Cadastro Nacional de Usuários do SUS. API interna (rede local `192.168.1.10:8014`) consultada por CPF/CNS para pré-preencher dados do paciente.
- **CNES** — Cadastro Nacional de Estabelecimentos de Saúde. Erro clássico do SIA: mais de um CNES no arquivo, ou CNES divergente.
- **CNS** — Cartão Nacional de Saúde (paciente/profissional). Value object `CnsField`. No export atual o CNS do paciente está fixado em zeros (ver débito na análise).
- **CBO** — Classificação Brasileira de Ocupações (do profissional). Value object `CboField`. Precisa ser compatível com o procedimento, senão o SIA critica.
- **CID** — Classificação Internacional de Doenças. APAC tem CID principal (e possível secundário).
- **BPA** — Boletim de Produção Ambulatorial. Outro documento de produção do SIA (não é o foco deste sistema, mas compartilha o pipeline de importação/validação).
- **TabNet / DATASUS** — Ferramenta pública de tabulação da produção ambulatorial já processada pelo SIA. Uso futuro: reconciliar o que foi exportado × o que foi processado/pago.
- **Solicitante / Autorizador** — Perfis. Solicitante cadastra e envia; Autorizador aprova/rejeita (rejeição exige justificativa) e, ao aprovar, o sistema associa a faixa.
- **`restricted_user`** — Usuário restrito de um estabelecimento: é **excluído** da visibilidade daquele estabelecimento na regra de escopo. Parte central da política de visibilidade a ser centralizada.
- **`adaptar_oci`** — Adaptação hardcoded no export para o caso de Duque de Caxias. A isolar como regra por município (`MunicipalityExportProfile`).
