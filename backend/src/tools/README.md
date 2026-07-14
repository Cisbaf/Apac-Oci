# `backend/src/tools/`

Scripts avulsos de operação/auditoria em produção, fora do ciclo normal de
`manage.py` (views/management commands). Rodados manualmente, sob demanda.

## `audit_street_type.py`

Script **read-only** de auditoria. Lista os valores distintos gravados em
`dados_apac.patient_address_street_type` e aponta quais não existem em
`STREET_TYPE_CHOICES`, para decisão manual (corrigir via data migration
pontual ou deixar cair no fallback de `ApacDataInlineForm`).

Criado para rodar antes do deploy da migration que adiciona `choices` a
`ApacDataModel.patient_address_street_type` — mantido aqui para reuso caso
surjam novas divergências.

**Uso** (de dentro de `backend/src`):
```bash
python manage.py shell < tools/audit_street_type.py
```
