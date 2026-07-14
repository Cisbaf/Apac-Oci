# T-202 — `MunicipalityExportProfile` (tirar hardcodes do export) — STUB

- **Fase:** 2 · **Status:** todo · **Depende de:** T-002
- **Branch:** `refactor/T-202-municipality-profile`

> Stub. Expandir com `/tarefa T-202` quando iniciar. O golden file (T-002) deve cobrir o caso `adaptar_oci` antes desta tarefa.

## Objetivo (rascunho)
Isolar as regras específicas por município hoje hardcoded no fluxo geral do export (`adaptar_oci` para Duque de Caxias, `cod_uf="33"`, códigos fixos) em um perfil de exportação por município.

## Direção
- Criar `MunicipalityExportProfile` (por cidade/UF) com os parâmetros hoje fixos.
- Substituir `adaptar_oci` inline e `cod_uf` fixo pelo perfil correspondente.
- Preparar para novos municípios/estados sem `if municipio == X`.

## Aceite (rascunho)
- [ ] Sem hardcode de município/UF no fluxo geral do export.
- [ ] Golden file: mudança **intencional e explícita** só se o output realmente mudar; idealmente permanece idêntico para os municípios atuais.
