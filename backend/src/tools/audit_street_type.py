"""
Script avulso de auditoria (read-only) — roda manualmente antes do deploy
da migration que adiciona `choices` a ApacDataModel.patient_address_street_type.

Lista os valores distintos gravados hoje em `dados_apac.patient_address_street_type`
e aponta quais não existem em STREET_TYPE_CHOICES, para decisão manual
(corrigir via data migration pontual ou deixar cair no fallback de
ApacDataInlineForm).

Uso (de dentro de backend/src): python manage.py shell < tools/audit_street_type.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.db.models import Count

from apac_data.models import ApacDataModel
from apac_data.choices import STREET_TYPE_CHOICES

codigos_validos = {code for code, _ in STREET_TYPE_CHOICES}

valores = (
    ApacDataModel.objects
    .values('patient_address_street_type')
    .annotate(total=Count('id'))
    .order_by('-total')
)

total_registros = 0
divergentes = []

for v in valores:
    valor = v['patient_address_street_type']
    total = v['total']
    total_registros += total
    if valor not in codigos_validos:
        divergentes.append((valor, total))

print(f"Total de registros analisados: {total_registros}")
print(f"Valores distintos encontrados: {len(valores)}")
print(f"Valores fora de STREET_TYPE_CHOICES: {len(divergentes)}")
print()

if divergentes:
    print("Valor divergente | Quantidade de registros")
    for valor, total in sorted(divergentes, key=lambda x: -x[1]):
        print(f"{valor!r} | {total}")
else:
    print("Nenhuma divergência encontrada — todos os valores já são códigos válidos.")
