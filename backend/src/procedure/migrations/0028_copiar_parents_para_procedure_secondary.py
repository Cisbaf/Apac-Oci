# T-037: copia o M2M "parents" (par principal×secundário) para o modelo
# explícito ProcedureSecondary antes de removê-lo (migration 0029). O valor
# inicial de `mandatory` é herdado do antigo ProcedureModel.mandatory — o
# melhor sinal disponível até o sigtap_auditar corrigir por par; `max_quantity`
# nasce vazio (o cadastro manual nunca guardou essa informação).
from django.db import migrations


def copiar(apps, schema_editor):
    ProcedureModel = apps.get_model("procedure", "ProcedureModel")
    ProcedureSecondary = apps.get_model("procedure", "ProcedureSecondary")

    for filho in ProcedureModel.objects.prefetch_related("parents").all():
        for principal in filho.parents.all():
            ProcedureSecondary.objects.get_or_create(
                parent=principal,
                child=filho,
                defaults={"mandatory": filho.mandatory, "max_quantity": None},
            )


def reverter(apps, schema_editor):
    ProcedureModel = apps.get_model("procedure", "ProcedureModel")
    ProcedureSecondary = apps.get_model("procedure", "ProcedureSecondary")

    for link in ProcedureSecondary.objects.all():
        link.child.parents.add(link.parent)


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0027_proceduresecondary'),
    ]

    operations = [
        migrations.RunPython(copiar, reverter),
    ]
