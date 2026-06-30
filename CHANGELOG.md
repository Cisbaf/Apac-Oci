# Changelog

## 2026-06-30

- **feat:** Integração com ViaCEP no formulário de digitação do paciente — campo CEP ganhou botão de busca que preenche logradouro, bairro, município e UF automaticamente.
- **fix:** Erros de API sem campo `message` no JSON (ex: 403 do CADSUS em dev) agora exibem alerta de erro para o usuário em vez de falhar silenciosamente.
